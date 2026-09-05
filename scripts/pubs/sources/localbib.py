"""Local BibTeX (data/publications.local.bib) — manual entries and abstracts.

A deliberately small, tolerant BibTeX reader (no dependency): handles
`field = {..{nested}..}`, `field = "..."`, `field = 2024`, and `month = apr`.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path

from ..model import Author, Pub, norm_arxiv, norm_doi

log = logging.getLogger("pubs.local")

MONTHS = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}
BIB_TYPES = {
    "article": "journal",
    "inproceedings": "conference",
    "incollection": "book",
    "book": "book",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "misc": "other",
    "unpublished": "preprint",
    "techreport": "other",
}


def parse_bibtex(text: str) -> list[tuple[str, str, dict[str, str]]]:
    entries = []
    i = 0
    n = len(text)
    while True:
        at = text.find("@", i)
        if at < 0:
            break
        m = re.match(r"@(\w+)\s*\{", text[at:])
        if not m:
            i = at + 1
            continue
        etype = m.group(1).lower()
        j = at + m.end()
        # find matching close brace
        depth, k = 1, j
        while k < n and depth:
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        body = text[j : k - 1]
        i = k
        if etype in ("comment", "preamble", "string"):
            continue
        key, _, rest = body.partition(",")
        fields = _parse_fields(rest)
        entries.append((etype, key.strip(), fields))
    return entries


def _parse_fields(s: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    i, n = 0, len(s)
    while i < n:
        m = re.match(r"\s*([\w\-]+)\s*=\s*", s[i:])
        if not m:
            break
        name = m.group(1).lower()
        i += m.end()
        if i >= n:
            break
        if s[i] == "{":
            depth, j = 1, i + 1
            while j < n and depth:
                if s[j] == "{":
                    depth += 1
                elif s[j] == "}":
                    depth -= 1
                j += 1
            val = s[i + 1 : j - 1]
            i = j
        elif s[i] == '"':
            j = i + 1
            while j < n and s[j] != '"':
                j += 1
            val = s[i + 1 : j]
            i = j + 1
        else:
            m2 = re.match(r"[^,\n]+", s[i:])
            val = m2.group(0).strip() if m2 else ""
            i += m2.end() if m2 else 0
        # skip to next comma
        m3 = re.match(r"\s*,?", s[i:])
        i += m3.end() if m3 else 0
        fields[name] = _clean(val)
    return fields


def _clean(v: str) -> str:
    v = re.sub(r"\s+", " ", v).strip()
    v = v.replace("\\&", "&").replace("\\%", "%").replace("--", "–")
    v = re.sub(r"\\['`^\"~=.uvHtcdb]\{(\w)\}", r"\1", v)  # \'{a} → a (accent dropped; DBLP wins anyway)
    v = re.sub(r"\\['`^\"~=.]([a-zA-Z])", r"\1", v)
    v = v.replace("{", "").replace("}", "")
    return v


def load(path: Path) -> list[Pub]:
    if not path.exists():
        return []
    out: list[Pub] = []
    for etype, key, f in parse_bibtex(path.read_text(encoding="utf-8")):
        title = f.get("title")
        if not title:
            continue
        authors = [Author(name=a.strip()) for a in re.split(r"\s+and\s+", f.get("author", "")) if a.strip()]
        year = int(f["year"]) if f.get("year", "").isdigit() else None
        mon = f.get("month", "").lower()[:3]
        month = MONTHS.get(mon) if mon in MONTHS else (int(f["month"]) if f.get("month", "").isdigit() else None)
        venue_raw = f.get("journal") or f.get("booktitle") or ""
        ptype = BIB_TYPES.get(etype, "other")
        arxiv = norm_arxiv(f.get("eprint") or f.get("arxiv") or f.get("website", "") or f.get("url", "") or venue_raw)
        if "arxiv" in venue_raw.lower():
            ptype = "preprint"
        url = f.get("url") or f.get("website")
        pub = Pub(
            title=title,
            authors=authors,
            year=year,
            month=month,
            type=ptype,
            status="preprint" if ptype == "preprint" else "published",
            venue_raw=venue_raw,
            volume=f.get("volume"),
            number=f.get("number"),
            pages=f.get("pages"),
            publisher=f.get("publisher"),
            doi=norm_doi(f.get("doi") or (url if url and "doi.org" in url else None)),
            arxiv=arxiv if "arxiv" in (f.get("website", "") + f.get("url", "") + venue_raw).lower() else norm_arxiv(f.get("eprint")),
            url=url,
            pdf=f.get("pdf"),
            code=f.get("code"),
            abstract=f.get("abstract"),
            keywords=[k.strip() for k in f.get("keywords", "").split(",") if k.strip()],
            note=f.get("note"),
            award=f.get("award"),
            key=key or None,
            sources={"local": key},
        )
        if f.get("selected", "").lower() == "true":
            pub.selected = True
        out.append(pub)
    log.info("local bib → %d entries", len(out))
    return out
