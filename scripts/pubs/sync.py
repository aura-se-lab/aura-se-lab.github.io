#!/usr/bin/env python3
"""
AURA Lab publications sync
==========================

Collects the lab's publications from several bibliographic sources, merges
them into one deduplicated list, enriches with citation counts and links,
classifies them into research threads, and writes:

  src/data/publications.json   ← consumed by the Astro site
  src/data/metrics.json        ← lab-level counts for the homepage
  public/aura.bib              ← downloadable BibTeX of everything
  data/sync-report.md          ← human summary used as the PR body
  src/content/news/*.md        ← DRAFT news posts for new papers (opt-out: --no-news)

Sources (all optional except DBLP): DBLP · Crossref · Semantic Scholar ·
OpenAlex · arXiv · local BibTeX · Google Scholar (--scholar).

Usage:
  python3 scripts/pubs/sync.py                      # full run
  python3 scripts/pubs/sync.py --offline            # rebuild from cache only
  python3 scripts/pubs/sync.py --sources dblp,crossref,arxiv,local
  python3 scripts/pubs/sync.py --discover           # print candidate IDs for members lacking them
  python3 scripts/pubs/sync.py --dry-run            # compute, print report, write nothing
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import re
import sys
from pathlib import Path

# allow `python3 scripts/pubs/sync.py`
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml  # noqa: E402

from pubs import config, web  # noqa: E402
from pubs.areas import classify, load_threads  # noqa: E402
from pubs.bibtex import to_bibtex  # noqa: E402
from pubs.members import MemberIndex, load_members  # noqa: E402
from pubs.merge import cluster, make_key, merge_cluster  # noqa: E402
from pubs.model import Pub, norm_arxiv, norm_doi, norm_title  # noqa: E402
from pubs.news import draft_for  # noqa: E402
from pubs.sources import arxiv as src_arxiv  # noqa: E402
from pubs.sources import crossref as src_crossref  # noqa: E402
from pubs.sources import dblp as src_dblp  # noqa: E402
from pubs.sources import localbib as src_local  # noqa: E402
from pubs.sources import openalex as src_openalex  # noqa: E402
from pubs.sources import s2 as src_s2  # noqa: E402
from pubs.sources import scholar as src_scholar  # noqa: E402
from pubs.venues import VenueTable  # noqa: E402

log = logging.getLogger("pubs")
ALL_SOURCES = ["dblp", "crossref", "s2", "openalex", "arxiv", "local"]


# ── overrides ────────────────────────────────────────────────────────────────
def load_overrides() -> dict:
    if not config.OVERRIDES_YML.exists():
        return {}
    return yaml.safe_load(config.OVERRIDES_YML.read_text(encoding="utf-8")) or {}


def _ref_matches(ref: dict, pub: Pub) -> bool:
    if "key" in ref and pub.key == ref["key"]:
        return True
    if "doi" in ref and pub.doi and norm_doi(ref["doi"]) == pub.doi:
        return True
    if "arxiv" in ref and pub.arxiv and norm_arxiv(ref["arxiv"]) == pub.arxiv:
        return True
    if "title" in ref and norm_title(ref["title"]) == pub.tkey:
        return True
    return False


def apply_overrides(pubs: list[Pub], ov: dict, warnings: list[str]) -> None:
    entries = ov.get("entries") or {}
    for key, patch in entries.items():
        ref = {"key": key}
        if isinstance(patch, dict):
            for k in ("doi", "arxiv", "title"):
                if k in patch:
                    ref[k] = patch[k]
        target = next((p for p in pubs if _ref_matches(ref, p)), None)
        if not target:
            warnings.append(f"override `{key}` matched no publication")
            continue
        for k, v in (patch or {}).items():
            if k in ("doi", "arxiv") and v:
                v = norm_doi(v) if k == "doi" else norm_arxiv(v)
            if k == "threads" and isinstance(v, list):
                target.threads = v
            elif k == "authors" and isinstance(v, list):
                from pubs.model import Author

                target.authors = [Author(name=a) for a in v]
            elif hasattr(target, k):
                setattr(target, k, v)
            else:
                warnings.append(f"override `{key}`: unknown field `{k}`")
    for ref in ov.get("exclude") or []:
        for p in pubs:
            if _ref_matches(ref, p):
                p.hidden = True


# ── main ─────────────────────────────────────────────────────────────────────
def run(args) -> int:
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    web.OFFLINE = args.offline
    if args.max_age is not None:
        web.CACHE_TTL = args.max_age
    sources = set(args.sources.split(",")) if args.sources else set(ALL_SOURCES)
    warnings: list[str] = []
    skipped: list[str] = []

    lab = yaml.safe_load(config.LAB_YML.read_text(encoding="utf-8"))
    founded_year = int(str(lab.get("founded", "2024"))[:4])
    members = load_members()
    midx = MemberIndex(members)
    venues = VenueTable()
    threads = load_threads()
    ov = load_overrides()
    since_raw = str((ov.get("defaults") or {}).get("since", lab.get("founded", founded_year)))
    since_default = int(since_raw[:4])
    since_month = int(since_raw[5:7]) if len(since_raw) >= 7 and since_raw[5:7].isdigit() else 1

    if args.discover:
        return discover(members)

    existing: dict[str, dict] = {}
    if config.OUT_JSON.exists():
        for e in json.loads(config.OUT_JSON.read_text()):
            existing[e["key"]] = e

    records: list[tuple[str, Pub]] = []

    # 1) DBLP per member pid (the backbone)
    if "dblp" in sources:
        for m in members:
            pid = m.ids.get("dblp")
            if not pid:
                continue
            try:
                records += [("dblp", p) for p in src_dblp.fetch_author(pid, name_hint=m.name)]
            except web.SourceUnavailable as e:
                skipped.append(f"DBLP {m.name}: {e}")

    # 2) Semantic Scholar / OpenAlex author pages for members who list those ids
    if "s2" in sources:
        for m in members:
            sids = m.ids.get("semanticscholar")
            sids = sids if isinstance(sids, list) else [x.strip() for x in str(sids).split(",") if x.strip()] if sids else []
            for sid in sids:
                try:
                    records += [("s2", p) for p in src_s2.fetch_author(str(sid))]
                except web.SourceUnavailable as e:
                    skipped.append(f"S2 author {m.name} ({sid}): {e}")
    if "openalex" in sources:
        for m in members:
            oid = m.ids.get("openalex")
            if oid:
                try:
                    records += [("openalex", p) for p in src_openalex.fetch_author(oid)]
                except web.SourceUnavailable as e:
                    skipped.append(f"OpenAlex author {m.name}: {e}")

    # 3) arXiv by name for the director (+ any member flagged with ids.arxiv: true)
    if "arxiv" in sources:
        for m in members:
            if m.role == "director" or m.ids.get("arxiv"):
                try:
                    records += [("arxiv", p) for p in src_arxiv.fetch_author(m.name)]
                except web.SourceUnavailable as e:
                    skipped.append(f"arXiv {m.name}: {e}")

    # 4) local BibTeX (manual entries / abstracts)
    if "local" in sources:
        records += [("local", p) for p in src_local.load(config.LOCAL_BIB)]

    # 5) previous output keeps keys stable and survives a source outage
    for e in existing.values():
        p = _from_json(e)
        records.append(("existing", p))

    # ── keep only lab-relevant records before spending enrichment calls ──────
    for _, p in records:
        for a in p.authors:
            a.member = midx.match(a.name)

    def _after_since(p: Pub, year: int, month: int) -> bool:
        if p.year is None:
            return False
        if p.year > year:
            return True
        if p.year < year:
            return False
        # same year: use the month when we know it; unknown month → be inclusive
        return p.month is None or p.month >= month

    def relevant(p: Pub) -> bool:
        if p.year is None:
            return False
        for a in p.authors:
            if not a.member:
                continue
            m = next(mm for mm in members if mm.slug == a.member)
            my, mm_ = since_default, since_month
            if m.since_year and m.since_year > my:
                my, mm_ = m.since_year, int(str(m.joined)[5:7]) if len(str(m.joined)) >= 7 else 1
            if _after_since(p, my, mm_):
                return True
        return False

    include_refs = ov.get("include") or []
    records = [
        (s, p)
        for s, p in records
        if relevant(p) or any(_ref_matches(r, p) for r in include_refs) or s == "existing"
    ]

    # ── enrichment by identifier (needs the DOIs discovered above) ───────────
    seed = [merge_cluster(c) for c in cluster(records)]
    if "crossref" in sources:
        for p in seed:
            if p.doi and not p.doi.startswith("10.48550/arxiv"):
                try:
                    cr = src_crossref.fetch_doi(p.doi)
                    if cr:
                        records.append(("crossref", cr))
                except web.SourceUnavailable as e:
                    skipped.append(f"Crossref {p.doi}: {e}")
    if "s2" in sources:
        try:
            records += [("s2", p) for p in src_s2.enrich(seed)]
        except web.SourceUnavailable as e:
            skipped.append(f"Semantic Scholar enrich: {e}")
    if "openalex" in sources:
        try:
            records += [("openalex", p) for p in src_openalex.enrich(seed)]
        except web.SourceUnavailable as e:
            skipped.append(f"OpenAlex enrich: {e}")
    scholar_profile: dict = {}
    if args.scholar:
        pi = next((m for m in members if m.role == "director"), None)
        if pi and pi.ids.get("scholar"):
            sp, scholar_profile = src_scholar.fetch_author(pi.ids["scholar"])
            records += [("scholar", p) for p in sp]

    # ── final merge ──────────────────────────────────────────────────────────
    for _, p in records:
        for a in p.authors:
            a.member = midx.match(a.name)
    pubs = [merge_cluster(c) for c in cluster(records)]
    for p in pubs:
        for a in p.authors:
            a.member = a.member or midx.match(a.name)
    pubs = [p for p in pubs if relevant(p) or any(_ref_matches(r, p) for r in include_refs)]

    # keys: (1) reuse the key a paper already had, (2) accept valid keys supplied by
    # the local bib, (3) generate the rest. Keys must be URL-safe slugs.
    taken: set[str] = set()
    assigned: set[int] = set()
    ex_by_key: dict[str, str] = {}
    for e in existing.values():
        ex_by_key.update({k: e["key"] for k in _from_json(e).match_keys()})
    for p in pubs:
        k = next((ex_by_key[mk] for mk in p.match_keys() if mk in ex_by_key), None)
        if k and k not in taken:
            p.key, _ = k, taken.add(k)
            assigned.add(id(p))
    for p in pubs:
        if id(p) in assigned:
            continue
        if p.key and re.fullmatch(r"[a-z0-9][a-z0-9_-]*", p.key) and p.key not in taken:
            taken.add(p.key)
            assigned.add(id(p))
        else:
            p.key = None
    for p in pubs:
        if id(p) not in assigned:
            p.key = make_key(p, taken)

    # venue mapping, status, threads, overrides
    unmapped: dict[str, int] = {}
    this_year = dt.date.today().year
    for p in pubs:
        venues.assign(p)
        if not p.venue and p.type != "preprint" and p.venue_raw:
            unmapped[p.venue_raw] = unmapped.get(p.venue_raw, 0) + 1
        if p.type == "preprint":
            p.status = "preprint"
        elif p.doi:
            p.status = "published"
        elif p.year and p.year >= this_year:
            p.status = "accepted"
        if not p.threads:
            p.threads = classify(p, threads)
        # featured lists in research pages imply the thread
        for slug, t in threads.items():
            if p.key in t["featured"] and slug not in p.threads:
                p.threads.insert(0, slug)
        if p.date and len(p.date) >= 7 and p.date[5:7].isdigit():
            p.month = int(p.date[5:7])  # the best-known publication date wins over bib months
        if not p.date and p.year:
            p.date = f"{p.year}-{p.month:02d}" if p.month else str(p.year)
        if p.note and p.status == "published" and re.search(r"to appear|just accepted|accepted", p.note, re.I):
            p.note = None  # stale "To Appear" notes from the local bib
    apply_overrides(pubs, ov, warnings)
    pubs = [p for p in pubs if not p.hidden]

    # sort newest first
    pubs.sort(key=lambda p: (p.year or 0, p.month or 0, p.date or "", p.title), reverse=True)

    # ── diff vs previous run ─────────────────────────────────────────────────
    new = [p for p in pubs if p.key not in existing]
    removed = [k for k in existing if k not in {p.key for p in pubs}]
    changed = []
    for p in pubs:
        if p.key in existing:
            old = existing[p.key]
            diffs = []
            for f in ("status", "venue", "doi", "arxiv", "year", "type"):
                if (old.get(f) or None) != (getattr(p, f) or None):
                    diffs.append(f"{f}: {old.get(f)} → {getattr(p, f)}")
            oc = (old.get("citations") or {}).get("count")
            nc = _best_citation(p)
            if oc != nc:
                diffs.append(f"citations: {oc} → {nc}")
            if diffs:
                changed.append((p, diffs))

    # ── outputs ──────────────────────────────────────────────────────────────
    out_json = []
    bib_parts = []
    for p in pubs:
        vinfo = venues.info(p.venue)
        d = p.to_json()
        d["citations"] = {"count": _best_citation(p), "by_source": p.citations} if p.citations else {}
        d["venue_info"] = (
            {"key": vinfo["key"], "name": vinfo["name"], "type": vinfo["type"], "url": vinfo.get("url"), "rank": vinfo.get("rank")}
            if vinfo
            else {"key": venues.guess_short(p.venue_raw) if p.venue_raw else "", "name": p.venue_raw, "type": p.type}
        )
        d["bibtex"] = to_bibtex(p, vinfo)
        d.pop("hidden", None)
        out_json.append(d)
        bib_parts.append(d["bibtex"])

    metrics = _metrics(pubs, members, midx, scholar_profile)
    report = _report(pubs, new, changed, removed, unmapped, warnings, skipped, metrics, sources, members)

    if args.dry_run:
        print(report)
        return 0

    config.OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    config.OUT_JSON.write_text(json.dumps(out_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    config.OUT_METRICS.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    config.OUT_BIB.parent.mkdir(parents=True, exist_ok=True)
    header = f"% AURA Lab publications — generated {dt.date.today().isoformat()} by scripts/pubs/sync.py\n% https://auralab.sh/publications/\n\n"
    config.OUT_BIB.write_text(header + "\n\n".join(bib_parts) + "\n", encoding="utf-8")
    config.REPORT_MD.write_text(report, encoding="utf-8")

    drafted = []
    if not args.no_news and existing:  # never spam drafts on the very first run
        names = {m.slug: m.name for m in members}
        for p in new:
            vinfo = venues.info(p.venue) or {}
            d = draft_for(p, vinfo.get("name", ""), names)
            if d:
                path, text = d
                if not path.exists():
                    path.write_text(text, encoding="utf-8")
                    drafted.append(path.name)
    if drafted:
        with config.REPORT_MD.open("a", encoding="utf-8") as fh:
            fh.write("\n## Drafted news posts (review, then set `draft: false`)\n\n")
            fh.writelines(f"- `src/content/news/{n}`\n" for n in drafted)
    print(report)
    log.info("wrote %s (%d publications)", config.OUT_JSON, len(out_json))
    return 0


def discover(members) -> int:
    print("Candidate DBLP profiles for members without ids.dblp:\n")
    for m in members:
        if m.ids.get("dblp"):
            continue
        try:
            hits = src_dblp.search_author(m.name)
        except web.SourceUnavailable as e:
            print(f"- {m.name}: DBLP unavailable ({e})")
            continue
        print(f"- {m.name} ({m.slug}):")
        for h in hits[:5]:
            notes = h.get("notes", {}).get("note")
            aff = ""
            if isinstance(notes, dict):
                aff = notes.get("text", "")
            elif isinstance(notes, list):
                aff = "; ".join(n.get("text", "") for n in notes if isinstance(n, dict))
            print(f"    dblp: \"{h['pid']}\"   # {h['name']} {('— ' + aff) if aff else ''}")
        if not hits:
            print("    (no DBLP hits yet)")
    print("\nPaste the right `dblp:` line under `ids:` in src/content/people/<slug>.md")
    return 0


def _best_citation(p: Pub) -> int | None:
    vals = [v for v in p.citations.values() if isinstance(v, int)]
    return max(vals) if vals else None


def _from_json(e: dict) -> Pub:
    from pubs.model import Author

    p = Pub(title=e["title"])
    for k, v in e.items():
        if k == "authors":
            p.authors = [Author(name=a["name"], member=a.get("member")) for a in v]
        elif k == "citations":
            p.citations = dict((v or {}).get("by_source") or {})
        elif k in ("venue_info", "bibtex"):
            continue
        elif hasattr(p, k):
            setattr(p, k, v)
    return p


def _metrics(pubs, members, midx, scholar_profile) -> dict:
    by_year: dict[str, int] = {}
    by_type: dict[str, int] = {}
    cites = 0
    for p in pubs:
        by_year[str(p.year)] = by_year.get(str(p.year), 0) + 1
        by_type[p.type] = by_type.get(p.type, 0) + 1
        cites += _best_citation(p) or 0
    reviewed = [p for p in pubs if p.type in ("journal", "conference", "workshop")]
    return {
        "updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
        "total": len(pubs),
        "reviewed": len(reviewed),
        "by_year": dict(sorted(by_year.items())),
        "by_type": by_type,
        "citations": cites,
        "venues": sorted({p.venue for p in reviewed if p.venue}),
        "members_current": len([m for m in members if m.status == "current"]),
        "phd_current": len([m for m in members if m.status == "current" and m.role == "phd"]),
        "scholar": scholar_profile or None,
    }


def _report(pubs, new, changed, removed, unmapped, warnings, skipped, metrics, sources, members) -> str:
    L = []
    L.append(f"# Publications sync — {dt.date.today().isoformat()}")
    L.append("")
    L.append(f"**{len(pubs)} publications** ({metrics['reviewed']} peer-reviewed) · {metrics['citations']} citations tracked · sources: {', '.join(sorted(sources))}")
    L.append("")
    if new:
        L.append(f"## ✨ New ({len(new)})")
        L.append("")
        L.append("| Key | Title | Venue | Year | Status |")
        L.append("|---|---|---|---|---|")
        for p in new:
            L.append(f"| `{p.key}` | {p.title} | {p.venue or p.venue_raw or '—'} | {p.year} | {p.status} |")
        L.append("")
    if changed:
        L.append(f"## ✏️ Changed ({len(changed)})")
        L.append("")
        for p, diffs in changed:
            L.append(f"- `{p.key}` — {'; '.join(diffs)}")
        L.append("")
    if removed:
        L.append(f"## ⚠️ No longer found ({len(removed)}) — kept out; add to `data/publications.local.bib` if they are real")
        L.append("")
        L.extend(f"- `{k}`" for k in removed)
        L.append("")
    if unmapped:
        L.append("## 🏷️ Venues without a row in `data/venues.yml`")
        L.append("")
        L.extend(f"- {v} ({n})" for v, n in sorted(unmapped.items(), key=lambda x: -x[1]))
        L.append("")
    no_ids = [m for m in members if m.status == "current" and not (m.ids.get("dblp") or m.ids.get("semanticscholar") or m.ids.get("openalex"))]
    if no_ids:
        L.append("## 🪪 Members without author IDs (their solo papers can't be discovered)")
        L.append("")
        from pubs.members import MemberIndex as _MI

        for m in no_ids:
            hint = ""
            for nm, pid in src_dblp.SEEN_PIDS.items():
                if _MI([m]).match(nm):
                    hint = f" — seen on DBLP as **{nm}**, add `dblp: \"{pid}\"` under `ids:` in `src/content/people/{m.slug}.md`"
                    break
            L.append(f"- {m.name}{hint}")
        L.append("")
    if skipped:
        L.append("## ⏭️ Sources skipped this run")
        L.append("")
        L.extend(f"- {s}" for s in skipped)
        L.append("")
    if warnings:
        L.append("## ⚠️ Warnings")
        L.append("")
        L.extend(f"- {w}" for w in warnings)
        L.append("")
    if not (new or changed or removed):
        L.append("_No changes to the publication list._")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", help=f"comma list of {','.join(ALL_SOURCES)} (default: all)")
    ap.add_argument("--scholar", action="store_true", help="also query Google Scholar (needs `scholarly`)")
    ap.add_argument("--offline", action="store_true", help="only use cached responses")
    ap.add_argument("--max-age", type=float, help="cache TTL in seconds (default 6h; 0 forces refresh)")
    ap.add_argument("--dry-run", action="store_true", help="print the report; write nothing")
    ap.add_argument("--no-news", action="store_true", help="do not draft news posts")
    ap.add_argument("--discover", action="store_true", help="suggest DBLP ids for members lacking them")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
