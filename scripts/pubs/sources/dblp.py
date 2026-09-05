"""DBLP — authoritative CS bibliography. Fetched per author pid.

Primary: the pid XML export (full records). Fallbacks: the two official
mirrors, then the publication *search* API (JSON, slightly less detail),
because dblp.org occasionally answers 503 for record exports while the
search index stays up.

Each DBLP record becomes one Pub. arXiv/CoRR entries are typed `preprint` and
later merged with their peer-reviewed twin by title.
"""
from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET

from .. import web
from ..model import Author, Pub, norm_arxiv, norm_doi

log = logging.getLogger("pubs.dblp")

HOSTS = ["https://dblp.org", "https://dblp.uni-trier.de", "https://dblp.dagstuhl.de"]

DBLP_TYPES = {
    "article": "journal",
    "inproceedings": "conference",
    "incollection": "book",
    "book": "book",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
}
SEARCH_TYPES = {
    "Journal Articles": "journal",
    "Conference and Workshop Papers": "conference",
    "Informal and Other Publications": "preprint",
    "Parts in Books or Collections": "book",
    "Books and Theses": "thesis",
    "Editorship": "other",
}
SKIP_SEARCH_TYPES = {"Data and Artifacts", "Reference Works", "Withdrawn Items"}

# name → pid pairs seen in author lists; sync.py turns these into ID suggestions
SEEN_PIDS: dict[str, str] = {}


def search_author(name: str) -> list[dict]:
    """Return candidate DBLP authors for a name (used by --discover)."""
    data = web.get_json(
        "https://dblp.org/search/author/api", params={"q": name, "format": "json", "h": 10}
    )
    hits = (data or {}).get("result", {}).get("hits", {}).get("hit", []) or []
    return [
        {
            "name": h["info"]["author"],
            "pid": h["info"]["url"].split("/pid/")[-1],
            "url": h["info"]["url"],
            "notes": h["info"].get("notes", {}),
        }
        for h in hits
    ]


def fetch_author(pid: str, name_hint: str | None = None) -> list[Pub]:
    last: Exception | None = None
    for host in HOSTS:
        try:
            xml = web.get_text(f"{host}/pid/{pid}.xml", min_interval=1.0, retries=2)
            if xml:
                pubs = _parse_xml(xml)
                log.info("DBLP %s (%s) → %d records", pid, host, len(pubs))
                return pubs
        except web.SourceUnavailable as e:
            last = e
            log.warning("DBLP %s unavailable: %s", host, e)
    # Fallback: publication search API (needs the author's DBLP display name)
    if name_hint:
        try:
            pubs = _search_publications(name_hint)
            if pubs:
                log.info("DBLP search fallback for %s → %d records", name_hint, len(pubs))
                return pubs
        except web.SourceUnavailable as e:
            last = e
    raise web.SourceUnavailable(f"DBLP pid {pid}: {last}")


def _parse_xml(xml: str) -> list[Pub]:
    root = ET.fromstring(xml)
    pubs: list[Pub] = []
    for r in root.findall("r"):
        rec = list(r)[0]
        kind = rec.tag
        if kind not in DBLP_TYPES:
            continue
        get = lambda tag: (rec.findtext(tag) or "").strip()  # noqa: E731
        title = re.sub(r"\.$", "", get("title"))
        if not title:
            continue
        authors = []
        for a in rec.findall("author"):
            nm = (a.text or "").strip()
            authors.append(Author(name=nm))
            if a.get("pid"):
                SEEN_PIDS.setdefault(nm, a.get("pid"))
        year = int(get("year")) if get("year").isdigit() else None
        journal = get("journal")
        booktitle = get("booktitle")
        venue_raw = journal or booktitle
        ptype = DBLP_TYPES[kind]
        ees = [e.text.strip() for e in rec.findall("ee") if e.text]
        doi = next((d for d in (norm_doi(e) for e in ees if "doi.org" in e) if d), None)
        arxiv = next((a for a in (norm_arxiv(e) for e in ees if "arxiv" in e.lower()) if a), None)
        url = next((e for e in ees if "doi.org" not in e and "arxiv.org" not in e), None)
        volume = get("volume") or None
        if journal == "CoRR" or rec.get("publtype") == "informal":
            ptype = "preprint"
            if not arxiv:
                arxiv = norm_arxiv(get("volume"))  # "abs/2507.09665"
            volume = None
        pub = Pub(
            title=title,
            authors=authors,
            year=year,
            type=ptype,
            venue_raw=venue_raw,
            volume=volume,
            number=get("number") or None,
            pages=get("pages") or None,
            publisher=get("publisher") or None,
            doi=doi,
            arxiv=arxiv,
            url=url,
            sources={"dblp": rec.get("key")},
        )
        if ptype == "preprint":
            pub.status = "preprint"
        pubs.append(pub)
    return pubs


def _search_publications(name: str) -> list[Pub]:
    q = "author:" + name.replace(" ", "_") + ":"
    pubs: list[Pub] = []
    first = 0
    while True:
        data = web.get_json(
            "https://dblp.org/search/publ/api",
            params={"q": q, "h": 1000, "f": first, "format": "json"},
            min_interval=1.0,
            retries=2,
        )
        hits = (data or {}).get("result", {}).get("hits", {})
        items = hits.get("hit", []) or []
        for h in items:
            info = h["info"]
            if info.get("type") in SKIP_SEARCH_TYPES:
                continue
            title = re.sub(r"\.$", "", info.get("title", "")).replace("&quot;", '"').replace("&amp;", "&")
            if not title:
                continue
            auths = info.get("authors", {}).get("author", [])
            if isinstance(auths, dict):
                auths = [auths]
            authors = []
            for a in auths:
                nm = re.sub(r"\s\d{4}$", "", a.get("text", ""))
                authors.append(Author(name=nm))
                if a.get("@pid"):
                    SEEN_PIDS.setdefault(nm, a["@pid"])
            year = int(info["year"]) if str(info.get("year", "")).isdigit() else None
            ptype = SEARCH_TYPES.get(info.get("type", ""), "other")
            ee = info.get("ee", "")
            doi = norm_doi(info.get("doi")) or norm_doi(ee)
            arxiv = norm_arxiv(info.get("doi", "")) if "arxiv" in info.get("doi", "").lower() else (norm_arxiv(ee) if "arxiv" in ee.lower() else None)
            venue = info.get("venue", "")
            if isinstance(venue, list):
                venue = " / ".join(venue)
            volume = info.get("volume")
            if venue == "CoRR":
                ptype = "preprint"
                arxiv = arxiv or norm_arxiv(info.get("volume", ""))
                volume = None
            pub = Pub(
                title=title,
                authors=authors,
                year=year,
                type=ptype,
                status="preprint" if ptype == "preprint" else "published",
                venue_raw=venue,
                volume=volume,
                number=info.get("number"),
                pages=info.get("pages"),
                doi=doi,
                arxiv=arxiv,
                url=None if ("doi.org" in ee or "arxiv.org" in ee) else (ee or None),
                sources={"dblp": info.get("key")},
            )
            pubs.append(pub)
        total = int(hits.get("@total", 0))
        first += len(items)
        if not items or first >= total:
            break
    return pubs
