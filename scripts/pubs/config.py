"""Paths and constants shared by the publications pipeline."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"
PEOPLE_DIR = ROOT / "src" / "content" / "people"
RESEARCH_DIR = ROOT / "src" / "content" / "research"
NEWS_DIR = ROOT / "src" / "content" / "news"

LAB_YML = DATA_DIR / "lab.yml"
VENUES_YML = DATA_DIR / "venues.yml"
OVERRIDES_YML = DATA_DIR / "publications.overrides.yml"
LOCAL_BIB = DATA_DIR / "publications.local.bib"

OUT_JSON = ROOT / "src" / "data" / "publications.json"
OUT_BIB = ROOT / "public" / "aura.bib"
OUT_METRICS = ROOT / "src" / "data" / "metrics.json"
REPORT_MD = DATA_DIR / "sync-report.md"

USER_AGENT = os.environ.get(
    "PUBS_USER_AGENT",
    "auralab-pubs-sync/1.0 (https://auralab.sh; mailto:aura.se.lab@gmail.com)",
)
MAILTO = os.environ.get("PUBS_MAILTO", "aura.se.lab@gmail.com")

S2_API_KEY = os.environ.get("S2_API_KEY", "")
OPENALEX_API_KEY = os.environ.get("OPENALEX_API_KEY", "")

# Seconds a cached HTTP response stays fresh (CI passes --max-age to shorten).
DEFAULT_CACHE_TTL = 6 * 3600
