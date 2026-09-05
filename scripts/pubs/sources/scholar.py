"""Google Scholar — OPTIONAL enrichment via the `scholarly` package.

Scholar has no API; scraping is rate-limited, CAPTCHA-prone and against the
letter of its ToS. We therefore only *read citation counts and spot
missing titles* here, never treat it as the backbone, and never fail the
pipeline because of it. Enable with `--scholar` (and `pip install scholarly`).
"""
from __future__ import annotations

import logging

from ..model import Pub

log = logging.getLogger("pubs.scholar")


def fetch_author(scholar_id: str) -> tuple[list[Pub], dict]:
    try:
        from scholarly import scholarly  # type: ignore
    except ImportError:
        log.warning("scholarly not installed — skipping Google Scholar")
        return [], {}
    try:
        author = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(author, sections=["basics", "indices", "publications"])
    except Exception as e:  # pragma: no cover - network / captcha
        log.warning("Google Scholar unavailable (%s) — skipping", e)
        return [], {}
    profile = {
        "name": author.get("name"),
        "citedby": author.get("citedby"),
        "hindex": author.get("hindex"),
        "i10index": author.get("i10index"),
        "citedby5y": author.get("citedby5y"),
    }
    pubs: list[Pub] = []
    for p in author.get("publications", []):
        bib = p.get("bib", {})
        title = bib.get("title")
        if not title:
            continue
        year = bib.get("pub_year")
        pub = Pub(
            title=title,
            year=int(year) if str(year).isdigit() else None,
            venue_raw=bib.get("citation", ""),
            sources={"scholar": p.get("author_pub_id")},
        )
        if p.get("num_citations") is not None:
            pub.citations["scholar"] = p["num_citations"]
        pubs.append(pub)
    log.info("Scholar %s → %d records", scholar_id, len(pubs))
    return pubs, profile
