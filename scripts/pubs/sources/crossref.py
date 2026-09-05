"""Crossref — per-DOI metadata (dates, pages, container title, abstract when deposited)."""
from __future__ import annotations

import logging
import re

from .. import config, web
from ..model import Author, Pub

log = logging.getLogger("pubs.crossref")

CR_TYPES = {
    "journal-article": "journal",
    "proceedings-article": "conference",
    "book-chapter": "book",
    "posted-content": "preprint",
    "dissertation": "thesis",
}


def _date(parts: dict | None) -> tuple[int | None, int | None, str | None]:
    if not parts or not parts.get("date-parts") or not parts["date-parts"][0]:
        return None, None, None
    dp = parts["date-parts"][0]
    y = dp[0] if len(dp) > 0 else None
    m = dp[1] if len(dp) > 1 else None
    d = dp[2] if len(dp) > 2 else None
    iso = None
    if y and m and d:
        iso = f"{y:04d}-{m:02d}-{d:02d}"
    elif y and m:
        iso = f"{y:04d}-{m:02d}"
    return y, m, iso


def fetch_doi(doi: str) -> Pub | None:
    if doi.startswith("10.48550/arxiv"):
        return None
    data = web.get_json(
        f"https://api.crossref.org/works/{doi}",
        params={"mailto": config.MAILTO},
        min_interval=0.2,
        retries=2,
    )
    if not data:
        return None
    w = data["message"]
    title = (w.get("title") or [""])[0]
    if not title:
        return None
    authors = []
    for a in w.get("author", []) or []:
        if a.get("given") or a.get("family"):
            authors.append(Author(name=f"{a.get('given','')} {a.get('family','')}".strip()))
        elif a.get("name"):
            authors.append(Author(name=a["name"]))
    # Prefer print/online publication date, then issued
    y, m, iso = _date(w.get("published-print") or w.get("published-online") or w.get("issued"))
    container = (w.get("container-title") or [""])[0]
    event = (w.get("event") or {}).get("name")
    abstract = w.get("abstract")
    if abstract:
        abstract = re.sub(r"<[^>]+>", "", abstract).strip()
        abstract = re.sub(r"^\s*Abstract\s*", "", abstract)
    return Pub(
        title=title,
        authors=authors,
        year=y,
        month=m,
        date=iso,
        type=CR_TYPES.get(w.get("type", ""), "other"),
        venue_raw=container or event or "",
        volume=w.get("volume"),
        number=w.get("issue"),
        pages=w.get("page"),
        publisher=w.get("publisher"),
        doi=doi,
        url=w.get("URL"),
        abstract=abstract or None,
        sources={"crossref": doi},
    )
