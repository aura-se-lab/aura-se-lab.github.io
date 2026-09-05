"""arXiv — preprints by author name (Atom API). Provides abstracts + arXiv ids."""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ET

from .. import web
from ..model import Author, Pub, norm_arxiv, norm_doi, split_name

log = logging.getLogger("pubs.arxiv")
NS = {"a": "http://www.w3.org/2005/Atom", "ar": "http://arxiv.org/schemas/atom"}


def _query_for(name: str) -> str:
    giv, fam = split_name(name)
    fam = fam.replace(" ", "_")
    first = giv.split(" ")[0] if giv else ""
    # arXiv wants au:Family_Given (full first name); au:Family_G (initial) returns nothing
    return f"au:{fam}_{first}" if first else f"au:{fam}"


def fetch_author(name: str, max_results: int = 200) -> list[Pub]:
    xml = web.get_text(
        "https://export.arxiv.org/api/query",
        params={"search_query": _query_for(name), "max_results": max_results, "sortBy": "submittedDate"},
        min_interval=3.0,
    )
    if not xml:
        return []
    root = ET.fromstring(xml)
    out: list[Pub] = []
    for e in root.findall("a:entry", NS):
        title = " ".join((e.findtext("a:title", "", NS) or "").split())
        if not title:
            continue
        aid = norm_arxiv(e.findtext("a:id", "", NS))
        published = (e.findtext("a:published", "", NS) or "")[:10]
        doi_el = e.find("ar:doi", NS)
        pub = Pub(
            title=title,
            authors=[Author(name=(a.findtext("a:name", "", NS) or "").strip()) for a in e.findall("a:author", NS)],
            year=int(published[:4]) if published[:4].isdigit() else None,
            month=int(published[5:7]) if len(published) >= 7 else None,
            date=published or None,
            type="preprint",
            status="preprint",
            venue_raw="arXiv",
            arxiv=aid,
            doi=(lambda d: None if not d or d.startswith("10.48550/arxiv") else d)(norm_doi(doi_el.text) if doi_el is not None else None),
            url=f"https://arxiv.org/abs/{aid}" if aid else None,
            pdf=f"https://arxiv.org/pdf/{aid}" if aid else None,
            abstract=" ".join((e.findtext("a:summary", "", NS) or "").split()) or None,
            sources={"arxiv": aid},
        )
        out.append(pub)
    log.info("arXiv %s → %d records", name, len(out))
    return out
