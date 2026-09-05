"""Publication record + normalisation helpers."""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field, asdict
from typing import Any

TYPES = ("journal", "conference", "workshop", "magazine", "preprint", "thesis", "book", "other")


def fold(s: str) -> str:
    """ASCII-fold + lowercase (é→e, ł→l...)."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def norm_title(t: str) -> str:
    t = fold(t)
    t = re.sub(r"\\[a-z]+\{([^}]*)\}", r"\1", t)  # \emph{x} → x
    t = t.replace("{", "").replace("}", "")
    t = re.sub(r"[^a-z0-9]+", "", t)
    return t


def norm_doi(d: str | None) -> str | None:
    """Lower-cased bare DOI, or None. arXiv's own DOIs (10.48550/arXiv.*) are
    dropped here — use `norm_arxiv` on the same string to get the arXiv id."""
    if not d:
        return None
    d = d.strip()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d, flags=re.I)
    d = re.sub(r"^doi:\s*", "", d, flags=re.I)
    d = d.lower()
    if d.startswith("10.48550/arxiv") or not d.startswith("10."):
        return None
    return d or None


def norm_arxiv(a: str | None) -> str | None:
    if not a:
        return None
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", a)
    if m:
        return m.group(1)
    m = re.search(r"([a-z\-]+(?:\.[A-Z]{2})?/\d{7})", a)
    return m.group(1) if m else None


def split_name(name: str) -> tuple[str, str]:
    """Return (given, family) for 'Given Family' or 'Family, Given'."""
    name = re.sub(r"\s+", " ", name.strip())
    name = re.sub(r"\s\d{4}$", "", name)  # DBLP disambiguation suffix "0001"
    if "," in name:
        fam, giv = [x.strip() for x in name.split(",", 1)]
        return giv, fam
    parts = name.split(" ")
    if len(parts) == 1:
        return "", parts[0]
    # keep multi-word surnames with particles together (di penta, van der, nader palacio handled by aliases)
    particles = {"di", "de", "del", "della", "van", "von", "der", "da", "dos", "la", "le"}
    i = len(parts) - 1
    while i - 1 > 0 and parts[i - 1].lower() in particles:
        i -= 1
    return " ".join(parts[:i]), " ".join(parts[i:])


def short_name(name: str) -> str:
    giv, fam = split_name(name)
    initials = " ".join(
        "-".join(p[0] + "." for p in g.split("-") if p) for g in giv.split(" ") if g
    )
    return f"{initials} {fam}".strip()


def name_keys(name: str) -> set[str]:
    """Keys used to match an author string against a member: 'family|g' and 'family|given'."""
    giv, fam = split_name(name)
    fam_k = norm_title(fam)
    keys = {fam_k}
    if giv:
        keys.add(f"{fam_k}|{norm_title(giv)[0]}")
        keys.add(f"{fam_k}|{norm_title(giv)}")
    return keys


@dataclass
class Author:
    name: str
    member: str | None = None  # people slug

    def to_json(self) -> dict:
        d = {"name": self.name}
        if self.member:
            d["member"] = self.member
        return d


@dataclass
class Pub:
    title: str
    authors: list[Author] = field(default_factory=list)
    year: int | None = None
    month: int | None = None
    date: str | None = None  # ISO, best known publication date
    type: str = "other"
    status: str = "published"  # published | accepted | preprint
    venue_raw: str = ""
    venue: str | None = None  # key into venues.yml
    volume: str | None = None
    number: str | None = None
    pages: str | None = None
    publisher: str | None = None
    doi: str | None = None
    arxiv: str | None = None
    url: str | None = None
    pdf: str | None = None
    code: str | None = None
    data: str | None = None
    slides: str | None = None
    video: str | None = None
    abstract: str | None = None
    keywords: list[str] = field(default_factory=list)
    threads: list[str] = field(default_factory=list)
    selected: bool = False
    award: str | None = None
    note: str | None = None
    citations: dict[str, Any] = field(default_factory=dict)  # {source: count}
    sources: dict[str, Any] = field(default_factory=dict)  # provenance ids
    key: str | None = None
    hidden: bool = False

    # ── identity ────────────────────────────────────────────────────────────
    @property
    def tkey(self) -> str:
        return norm_title(self.title)

    def match_keys(self) -> set[str]:
        ks = {"t:" + self.tkey}
        if self.doi:
            ks.add("doi:" + self.doi)
        if self.arxiv:
            ks.add("arxiv:" + self.arxiv)
        return ks

    def to_json(self) -> dict:
        d = asdict(self)
        d["authors"] = [a.to_json() for a in self.authors]
        # drop empty values for a compact file
        return {k: v for k, v in d.items() if v not in (None, "", [], {}) or k in ("selected",)}


# Field precedence when merging records from several sources (first wins).
PRIORITY = ["override", "local", "crossref", "dblp", "s2", "openalex", "arxiv", "scholar", "existing"]
# Who we trust about the *kind* of publication (journal vs conference vs preprint).
TYPE_PRIORITY = ["override", "dblp", "crossref", "s2", "openalex", "local", "existing", "scholar", "arxiv"]
