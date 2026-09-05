"""Map raw journal/booktitle strings to the venue keys in data/venues.yml."""
from __future__ import annotations

import re

import yaml

from . import config
from .model import Pub, fold


class VenueTable:
    def __init__(self, path=config.VENUES_YML):
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        self.table: dict[str, dict] = {}
        for key, v in raw.items():
            v = dict(v)
            v["key"] = key
            v["match"] = [m.lower() for m in v.get("match", [])] + [key.lower()]
            self.table[key] = v

    def lookup(self, raw: str) -> str | None:
        s = fold(raw)
        if not s:
            return None
        # exact / regex-ish anchors first
        for key, v in self.table.items():
            for m in v["match"]:
                if m.startswith("^") and m.endswith("$"):
                    if s == m[1:-1]:
                        return key
        # long patterns before short ones to avoid "ase" matching "database"
        cands = []
        for key, v in self.table.items():
            for m in v["match"]:
                if m.startswith("^"):
                    continue
                if len(m) <= 5:
                    # short acronyms must appear as a standalone token
                    if re.search(rf"(?<![a-z0-9]){re.escape(m)}(?![a-z0-9])", s):
                        cands.append((len(m), key))
                elif m in s:
                    cands.append((len(m) + 100, key))
        if cands:
            cands.sort(reverse=True)
            return cands[0][1]
        return None

    def info(self, key: str | None) -> dict | None:
        return self.table.get(key) if key else None

    def assign(self, pub: Pub) -> None:
        key = pub.venue if pub.venue in self.table else self.lookup(pub.venue_raw)
        if not key:
            return
        pub.venue = key
        vt = self.table[key]["type"]
        # The venue's kind refines the record kind: a DBLP "journal article" in
        # IEEE Computer is a magazine piece; a paper in a workshop proceedings is a
        # workshop paper. Preprint venues never downgrade a reviewed record.
        if vt in ("magazine", "workshop") or (vt in ("journal", "conference") and pub.type in ("other", "conference", "journal")):
            pub.type = vt

    def guess_short(self, raw: str) -> str:
        """Best-effort acronym for an unmapped venue, e.g. 'International Conference on Foo Bar' → 'ICFB'."""
        words = [w for w in re.findall(r"[A-Za-z]+", raw) if w.lower() not in {"on", "of", "the", "and", "for", "in", "acm", "ieee", "proceedings", "international", "conference", "symposium", "workshop", "joint", "annual"}]
        acro = "".join(w[0] for w in words).upper()
        return acro[:8] or raw[:12]
