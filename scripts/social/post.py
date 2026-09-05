#!/usr/bin/env python3
"""
Post published news items to Bluesky and/or X.

  python3 scripts/social/post.py            # post anything new, append to data/social-log.json
  python3 scripts/social/post.py --dry-run  # show the composed posts, change nothing

A news item is eligible when its frontmatter has `social: true` and `draft: false`
(the default) and it is not yet in the log. Each network is used only if its
credentials are present in the environment:

  Bluesky : BLUESKY_HANDLE, BLUESKY_APP_PASSWORD   (app password, not the account password)
  X       : X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET  (free tier can post)

Posts are short: title · one line · link to the news page (and the DOI when the
item is about a paper). Nothing is ever posted twice, even across networks that
were added later — the log is per (item, network).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
NEWS = ROOT / "src" / "content" / "news"
LOG = ROOT / "data" / "social-log.json"
PUBS = ROOT / "src" / "data" / "publications.json"
SITE = os.environ.get("SITE_URL", "https://auralab.sh").rstrip("/")


def frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, flags=re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def first_sentence(md: str, limit: int = 140) -> str:
    txt = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    txt = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", txt)
    txt = re.sub(r"[*_`>#]", "", txt)
    txt = " ".join(txt.split())
    s = re.split(r"(?<=[.!?])\s", txt, 1)[0]
    return s if len(s) <= limit else s[: limit - 1].rsplit(" ", 1)[0] + "…"


def compose(slug: str, fm: dict, body: str, pubs: dict) -> tuple[str, list[tuple[str, str]]]:
    """Return (text, [(url, label), ...]) — links are appended and also returned for rich facets."""
    url = f"{SITE}/news/{slug}/"
    title = fm["title"]
    lead = first_sentence(body)
    links = [(url, "auralab.sh")]
    pub = pubs.get(fm.get("publication") or "")
    if pub and pub.get("doi"):
        links.append((f"https://doi.org/{pub['doi']}", "doi"))
    elif pub and pub.get("arxiv"):
        links.append((f"https://arxiv.org/abs/{pub['arxiv']}", "arXiv"))
    tail = " ".join(u for u, _ in links)
    budget = 280 - len(tail) - 3
    text = title
    if lead and lead.lower() not in title.lower() and len(title) + len(lead) + 2 <= budget:
        text = f"{title}\n\n{lead}"
    if len(text) > budget:
        text = text[: budget - 1].rsplit(" ", 1)[0] + "…"
    return f"{text}\n\n{tail}", links


def post_bluesky(text: str, links: list[tuple[str, str]]) -> str | None:
    handle, pw = os.environ.get("BLUESKY_HANDLE"), os.environ.get("BLUESKY_APP_PASSWORD")
    if not (handle and pw):
        return None
    from atproto import Client, client_utils  # type: ignore

    client = Client()
    client.login(handle, pw)
    # Build rich text: everything before the links as plain text, links as facets.
    body, _, _ = text.rpartition("\n\n")
    tb = client_utils.TextBuilder().text(body + "\n\n")
    for i, (u, label) in enumerate(links):
        tb.link(u, u)
        if i < len(links) - 1:
            tb.text(" ")
    res = client.send_post(tb)
    return res.uri


def post_x(text: str) -> str | None:
    keys = [os.environ.get(k) for k in ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET")]
    if not all(keys):
        return None
    import tweepy  # type: ignore

    client = tweepy.Client(consumer_key=keys[0], consumer_secret=keys[1], access_token=keys[2], access_token_secret=keys[3])
    res = client.create_tweet(text=text)
    return str(res.data.get("id"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="post only this news slug")
    args = ap.parse_args(argv)

    log: dict[str, dict] = json.loads(LOG.read_text()) if LOG.exists() else {}
    pubs = {p["key"]: p for p in json.loads(PUBS.read_text())} if PUBS.exists() else {}
    networks = {
        "bluesky": bool(os.environ.get("BLUESKY_HANDLE") and os.environ.get("BLUESKY_APP_PASSWORD")),
        "x": all(os.environ.get(k) for k in ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET")),
    }
    print("networks configured:", ", ".join(k for k, v in networks.items() if v) or "none")

    posted_any = False
    for path in sorted(NEWS.glob("*.md")):
        slug = path.stem
        if args.only and slug != args.only:
            continue
        fm, body = frontmatter(path.read_text(encoding="utf-8"))
        if not fm or fm.get("draft") or not fm.get("social"):
            continue
        entry = log.setdefault(slug, {})
        todo = [n for n, ok in networks.items() if ok and n not in entry]
        if not todo and not args.dry_run:
            continue
        text, links = compose(slug, fm, body, pubs)
        print(f"\n─── {slug} → {', '.join(todo) or '(nothing new)'}\n{text}\n")
        if args.dry_run:
            continue
        for n in todo:
            try:
                ref = post_bluesky(text, links) if n == "bluesky" else post_x(text)
                if ref:
                    entry[n] = ref
                    posted_any = True
                    print(f"  ✓ {n}: {ref}")
            except Exception as e:  # keep going with other networks / items
                print(f"  ✗ {n}: {e}", file=sys.stderr)
    if posted_any or (not LOG.exists() and not args.dry_run):
        LOG.write_text(json.dumps(log, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
