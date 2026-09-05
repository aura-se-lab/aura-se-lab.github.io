"""Cluster records from all sources that describe the same paper and merge them."""
from __future__ import annotations

import logging
import re
from collections import defaultdict

from .model import PRIORITY, TYPE_PRIORITY, Author, Pub, fold, norm_title

log = logging.getLogger("pubs.merge")

# fields merged by priority (first non-empty wins, in PRIORITY order)
SCALAR_FIELDS = [
    "title", "year", "month", "date", "venue_raw", "volume", "number", "pages", "publisher",
    "doi", "arxiv", "url", "pdf", "code", "data", "slides", "video", "abstract", "note", "award", "key",
]


class Cluster:
    def __init__(self):
        self.records: list[tuple[str, Pub]] = []  # (source, pub)

    def add(self, src: str, pub: Pub):
        self.records.append((src, pub))

    def keys(self) -> set[str]:
        ks = set()
        for _, p in self.records:
            ks |= p.match_keys()
        return ks


def cluster(records: list[tuple[str, Pub]]) -> list[Cluster]:
    """Union-find over DOI / arXiv / normalised-title keys."""
    parent: dict[str, str] = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for _, p in records:
        ks = list(p.match_keys())
        for k in ks[1:]:
            union(ks[0], k)
    groups: dict[str, Cluster] = defaultdict(Cluster)
    for src, p in records:
        root = find(next(iter(p.match_keys())))
        groups[root].add(src, p)
    return list(groups.values())


def _rank(src: str) -> int:
    return PRIORITY.index(src) if src in PRIORITY else len(PRIORITY)


def _type_rank(src: str) -> int:
    return TYPE_PRIORITY.index(src) if src in TYPE_PRIORITY else len(TYPE_PRIORITY)


def _best_type(recs: list[tuple[str, Pub]]) -> tuple[str, str]:
    """Any peer-reviewed/other record beats a preprint; among those, the most
    authoritative source (DBLP, Crossref…) decides journal vs conference."""
    reviewed = [sp for sp in recs if sp[1].type not in ("preprint", "other")]
    preprints = [sp for sp in recs if sp[1].type == "preprint"]
    pool = reviewed or preprints or recs
    pool = sorted(pool, key=lambda sp: _type_rank(sp[0]))
    return pool[0][1].type, pool[0][1].status


def merge_cluster(c: Cluster) -> Pub:
    recs = sorted(c.records, key=lambda sp: _rank(sp[0]))
    # The previous run's output only matters when every live source missed the
    # paper (outage); otherwise stale values must not carry forward.
    if any(src != "existing" for src, _ in recs):
        recs = [sp for sp in recs if sp[0] != "existing"]
    ptype, status = _best_type(recs)
    out = Pub(title="", type=ptype, status=status)
    # For scalar fields: the highest-priority *non-preprint* record wins where a
    # reviewed version exists (so the venue/pages come from the conference, not CoRR),
    # except arxiv/abstract/pdf which preprints are best at.
    reviewed = [sp for sp in recs if sp[1].type != "preprint"] or recs
    has_reviewed = any(sp[1].type != "preprint" for sp in recs)
    for f in SCALAR_FIELDS:
        pool = recs if f in ("arxiv", "abstract", "pdf", "code", "data", "key", "note", "award") else reviewed
        for _, p in pool:
            v = getattr(p, f)
            if v not in (None, "", []):
                setattr(out, f, v)
                break
        # bibliographic details (volume/pages/venue) must never leak from a CoRR record
        # into a paper that also has a reviewed version
        if getattr(out, f) in (None, "") and pool is not recs and not (has_reviewed and f in ("volume", "number", "pages", "publisher", "venue_raw")):
            for _, p in recs:
                v = getattr(p, f)
                if v not in (None, ""):
                    setattr(out, f, v)
                    break
    # Authors: prefer the longest authoritative list (DBLP/Crossref) — they keep full names
    for _, p in recs:
        if p.authors and (not out.authors or len(p.authors) > len(out.authors)):
            if not out.authors or _rank(recs[0][0]) >= 2:
                out.authors = [Author(name=a.name, member=a.member) for a in p.authors]
    if not out.authors:
        for _, p in recs:
            if p.authors:
                out.authors = [Author(name=a.name, member=a.member) for a in p.authors]
                break
    # drop exact duplicates some publishers deposit (same person listed twice)
    seen_auth: set[str] = set()
    deduped = []
    for a in out.authors:
        k = norm_title(a.name)
        if k in seen_auth:
            continue
        seen_auth.add(k)
        deduped.append(a)
    out.authors = deduped
    # union of keywords / citations / sources / threads / flags
    kw: list[str] = []
    for _, p in recs:
        for k in p.keywords:
            if k.lower() not in [x.lower() for x in kw]:
                kw.append(k)
        out.citations.update({k: v for k, v in p.citations.items() if v is not None})
        out.sources.update(p.sources)
        for t in p.threads:
            if t not in out.threads:
                out.threads.append(t)
        out.selected = out.selected or p.selected
        out.hidden = out.hidden or p.hidden
        if p.venue and not out.venue:
            out.venue = p.venue
    out.keywords = kw
    # arXiv-only → preprint status; DOI on a reviewed venue → published
    if out.type == "preprint":
        out.status = "preprint"
    return out


def make_key(pub: Pub, taken: set[str]) -> str:
    fam = "anon"
    if pub.authors:
        from .model import split_name

        _, fam = split_name(pub.authors[0].name)
    fam = re.sub(r"[^a-z]", "", fold(fam)) or "anon"
    stop = {"a", "an", "the", "on", "of", "in", "for", "to", "and", "is", "are", "toward", "towards", "from", "how", "when", "what", "why", "with", "via"}
    words = [w for w in re.findall(r"[a-z0-9]+", fold(pub.title)) if w not in stop]
    first = words[0] if words else "paper"
    base = f"{fam}{pub.year or ''}{first}"
    key, n = base, 2
    while key in taken:
        key = f"{base}{n}"
        n += 1
    taken.add(key)
    return key
