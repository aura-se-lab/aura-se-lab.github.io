"""Draft news posts for newly discovered publications (written as draft: true)."""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

from . import config
from .model import Pub

TEMPLATES = {
    "published": "Our paper *{title}* has been {verb} at **{venue}**{year}. {congrats}",
    "accepted": "Our paper *{title}* has been accepted at **{venue}**{year}. {congrats}",
    "preprint": "New preprint on arXiv: *{title}*. {congrats}",
}


def _slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:60]


def draft_for(pub: Pub, venue_name: str, member_names: dict[str, str], today: dt.date | None = None) -> tuple[Path, str] | None:
    today = today or dt.date.today()
    if pub.type in ("thesis", "other", "book") or pub.hidden:
        return None
    members = [a.member for a in pub.authors if a.member and a.member != "antonio-mastropaolo"]
    links = ", ".join(f"[{member_names.get(m, m)}](/people/{m}/)" for m in members)
    congrats = f"Congratulations to {links}!" if links else ""
    year = f" {pub.year}" if pub.year and pub.type != "journal" else ""
    verb = "published" if pub.status == "published" else "accepted"
    kind = "preprint" if pub.status == "preprint" else ("accepted" if pub.status == "accepted" else "published")
    body = TEMPLATES[kind].format(title=pub.title, venue=venue_name or pub.venue_raw, year=year, congrats=congrats, verb=verb).strip()
    if pub.doi:
        body += f"\n\nRead it: [doi.org/{pub.doi}](https://doi.org/{pub.doi})"
    elif pub.arxiv:
        body += f"\n\nRead it: [arXiv:{pub.arxiv}](https://arxiv.org/abs/{pub.arxiv})"
    if pub.status == "preprint":
        title = f'"{_short(pub.title)}" now on arXiv'
    else:
        title = f'"{_short(pub.title)}" accepted at {pub.venue or venue_name}'
    fm = [
        "---",
        f"title: {_yaml(title)}",
        f"date: {today.isoformat()}",
        "kind: paper",
        f"publication: {pub.key}",
        f"people: [{', '.join(members)}]",
        "draft: true          # ← flip to false (or delete the line) to publish",
        "social: true         # ← posted to Bluesky/X by the social workflow once published",
        "---",
        "",
        "<!-- Drafted automatically by scripts/pubs/sync.py — edit freely. -->",
        body,
        "",
    ]
    path = config.NEWS_DIR / f"{today.isoformat()}-{_slug(pub.key or pub.title)}.md"
    return path, "\n".join(fm)


def _short(t: str, n: int = 70) -> str:
    return t if len(t) <= n else t[: n - 1].rsplit(" ", 1)[0] + "…"


def _yaml(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
