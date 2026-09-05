"""Semantic Scholar — citation counts, TL;DRs, open-access PDFs, arXiv ids.

Two modes:
  * enrich(pubs): batch lookup by DOI / arXiv id (needs no author ids)
  * fetch_author(author_id): every paper of an S2 author id (discovery)
Both degrade gracefully: on 429 / no key the source is simply skipped.
"""
from __future__ import annotations

import logging

from .. import config, web
from ..model import Author, Pub, norm_arxiv, norm_doi

log = logging.getLogger("pubs.s2")

FIELDS = (
    "externalIds,title,year,venue,publicationVenue,citationCount,openAccessPdf,"
    "publicationTypes,publicationDate,journal,authors,abstract"
)
BATCH_FIELDS = FIELDS + ",tldr"  # tldr is only available on the paper endpoints


def _headers() -> dict:
    return {"x-api-key": config.S2_API_KEY} if config.S2_API_KEY else {}


def _to_pub(p: dict) -> Pub | None:
    if not p or not p.get("title"):
        return None
    ext = p.get("externalIds") or {}
    pdate = p.get("publicationDate")
    month = int(pdate[5:7]) if pdate and len(pdate) >= 7 else None
    ptypes = p.get("publicationTypes") or []
    # S2 tags most conference papers as JournalArticle *and* Conference — check Conference first
    ptype = "conference" if "Conference" in ptypes else "journal" if "JournalArticle" in ptypes else "other"
    doi = norm_doi(ext.get("DOI"))
    venue_l = (p.get("venue") or "").lower()
    # arXiv-only records (S2 often labels them JournalArticle) → preprint
    if ext.get("ArXiv") and (not doi or doi.startswith("10.48550/arxiv")):
        ptype = "preprint"
        if doi and doi.startswith("10.48550/arxiv"):
            doi = None
    elif venue_l in ("arxiv.org", "arxiv") and not doi:
        ptype = "preprint"
    pv = p.get("publicationVenue") or {}
    pub = Pub(
        title=p["title"],
        authors=[Author(name=a.get("name", "")) for a in p.get("authors") or []],
        year=p.get("year"),
        month=month,
        date=pdate,
        type=ptype,
        venue_raw=pv.get("name") or p.get("venue") or "",
        doi=doi,
        arxiv=norm_arxiv(ext.get("ArXiv")),
        pdf=(p.get("openAccessPdf") or {}).get("url"),
        abstract=p.get("abstract"),
        sources={"s2": p.get("paperId")},
    )
    if ptype == "preprint":
        pub.status = "preprint"
    if p.get("citationCount") is not None:
        pub.citations["s2"] = p["citationCount"]
    if p.get("tldr") and p["tldr"].get("text"):
        pub.sources["tldr"] = p["tldr"]["text"]
    return pub


def fetch_author(author_id: str) -> list[Pub]:
    out: list[Pub] = []
    offset = 0
    while True:
        data = web.get_json(
            f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers",
            params={"fields": FIELDS, "limit": 500, "offset": offset},
            headers=_headers(),
            min_interval=1.1,
        )
        if not data:
            break
        for p in data.get("data", []):
            pub = _to_pub(p)
            if pub:
                out.append(pub)
        if data.get("next") is None:
            break
        offset = data["next"]
    log.info("S2 author %s → %d records", author_id, len(out))
    return out


def enrich(pubs: list[Pub]) -> list[Pub]:
    """Look up each pub by DOI or arXiv id in one batch call (≤500 ids)."""
    ids, index = [], []
    for p in pubs:
        if p.doi:
            ids.append(f"DOI:{p.doi}")
            index.append(p)
        elif p.arxiv:
            ids.append(f"ARXIV:{p.arxiv}")
            index.append(p)
    out: list[Pub] = []
    for i in range(0, len(ids), 400):
        chunk = ids[i : i + 400]
        data = web.post_json(
            "https://api.semanticscholar.org/graph/v1/paper/batch",
            {"ids": chunk},
            params={"fields": BATCH_FIELDS},
            headers=_headers(),
            min_interval=1.1,
        )
        for p in data or []:
            pub = _to_pub(p) if p else None
            if pub:
                out.append(pub)
    log.info("S2 batch enrich → %d/%d found", len(out), len(ids))
    return out
