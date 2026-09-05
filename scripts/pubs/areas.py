"""Assign research threads to publications from keyword rules in src/content/research/*.md."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from . import config
from .model import Pub, fold


def load_threads(research_dir: Path = config.RESEARCH_DIR) -> dict[str, dict]:
    out = {}
    for p in sorted(research_dir.glob("*.md")):
        m = re.match(r"^---\s*\n(.*?)\n---", p.read_text(encoding="utf-8"), flags=re.S)
        fm = yaml.safe_load(m.group(1)) if m else {}
        out[p.stem] = {
            "keywords": [k.lower() for k in fm.get("keywords", [])],
            "featured": fm.get("featured", []),
            "order": fm.get("order", 99),
        }
    return out


def classify(pub: Pub, threads: dict[str, dict], min_score: int = 1) -> list[str]:
    text = fold(" ".join([pub.title, pub.title, pub.abstract or "", " ".join(pub.keywords)]))
    scores = []
    for slug, t in threads.items():
        s = 0
        for kw in t["keywords"]:
            if kw in text:
                s += 3 if kw in fold(pub.title) else 1
        if s >= min_score:
            scores.append((s, -t["order"], slug))
    scores.sort(reverse=True)
    if not scores:
        return []
    top = scores[0][0]
    # keep every thread within 60% of the best score (papers legitimately span threads), max 2
    return [slug for s, _, slug in scores if s >= max(1, top * 0.6)][:2]
