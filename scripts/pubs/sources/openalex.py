"""OpenAlex — citation counts + open-access locations, matched by DOI.

OpenAlex now meters API usage; set OPENALEX_API_KEY for a daily budget.
Without a key the source is skipped quietly.
"""
from __future__ import annotations

import logging

from .. import config, web
from ..model import Author, Pub, norm_doi

log = logging.getLogger("pubs.openalex")


def _params(extra: dict | None = None) -> dict:
    p = {"mailto": config.MAILTO}
    if config.OPENALEX_API_KEY:
        p["api_key"] = config.OPENALEX_API_KEY
    p.update(extra or {})
    return p


def _to_pub(w: dict) -> Pub | None:
    if not w.get("title"):
        return None
    pub = Pub(
        title=w["title"],
        authors=[Author(name=(a.get("author") or {}).get("display_name", "")) for a in w.get("authorships", [])],
        year=w.get("publication_year"),
        date=w.get("publication_date"),
        doi=norm_doi(w.get("doi")),
        venue_raw=((w.get("primary_location") or {}).get("source") or {}).get("display_name", "") or "",
        sources={"openalex": w.get("id")},
    )
    if w.get("cited_by_count") is not None:
        pub.citations["openalex"] = w["cited_by_count"]
    oa = w.get("open_access") or {}
    if oa.get("oa_url"):
        pub.pdf = oa["oa_url"]
    return pub


def enrich(pubs: list[Pub]) -> list[Pub]:
    if not config.OPENALEX_API_KEY:
        log.info("OpenAlex skipped (no OPENALEX_API_KEY)")
        return []
    dois = [p.doi for p in pubs if p.doi]
    out: list[Pub] = []
    for i in range(0, len(dois), 50):
        chunk = dois[i : i + 50]
        data = web.get_json(
            "https://api.openalex.org/works",
            params=_params({"filter": "doi:" + "|".join(chunk), "per-page": 50}),
            min_interval=0.3,
            retries=2,
        )
        for w in (data or {}).get("results", []):
            pub = _to_pub(w)
            if pub:
                out.append(pub)
    log.info("OpenAlex enrich → %d/%d found", len(out), len(dois))
    return out


def fetch_author(author_id: str) -> list[Pub]:
    if not config.OPENALEX_API_KEY:
        return []
    out: list[Pub] = []
    cursor = "*"
    while cursor:
        data = web.get_json(
            "https://api.openalex.org/works",
            params=_params({"filter": f"author.id:{author_id}", "per-page": 200, "cursor": cursor}),
            min_interval=0.3,
            retries=2,
        )
        if not data:
            break
        for w in data.get("results", []):
            pub = _to_pub(w)
            if pub:
                out.append(pub)
        cursor = (data.get("meta") or {}).get("next_cursor")
    return out
