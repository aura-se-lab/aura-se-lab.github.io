"""Tiny cached HTTP client with polite retries.

Every source goes through `get_json` / `get_text`, so rate limits and
transient failures are handled in one place. Responses are cached on disk
(data/cache/, git-ignored; restored by actions/cache in CI) so a re-run
within the TTL is free and offline runs (--offline) still work.
"""
from __future__ import annotations

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any

import requests

from . import config

log = logging.getLogger("pubs.web")

_session = requests.Session()
_session.headers.update({"User-Agent": config.USER_AGENT})

OFFLINE = False
CACHE_TTL = config.DEFAULT_CACHE_TTL


class SourceUnavailable(RuntimeError):
    """Raised when a source cannot be used right now (rate-limited, down, no key)."""


def _cache_path(url: str, params: dict | None, method: str, body: Any) -> Path:
    key = json.dumps([method, url, params or {}, body], sort_keys=True, default=str)
    h = hashlib.sha1(key.encode()).hexdigest()
    host = requests.utils.urlparse(url).netloc.replace(":", "_")
    d = config.CACHE_DIR / host
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{h}.json"


def _read_cache(p: Path, max_age: float | None):
    if not p.exists():
        return None
    try:
        raw = json.loads(p.read_text())
    except Exception:
        return None
    age = time.time() - raw.get("t", 0)
    if max_age is not None and age > max_age and not OFFLINE:
        return None
    return raw


def request(
    method: str,
    url: str,
    *,
    params: dict | None = None,
    json_body: Any = None,
    headers: dict | None = None,
    max_age: float | None = None,
    retries: int = 4,
    backoff: float = 2.0,
    min_interval: float = 0.0,
) -> tuple[int, str]:
    """Return (status, text). Uses cache when fresh; retries on 429/5xx."""
    ttl = CACHE_TTL if max_age is None else max_age
    cp = _cache_path(url, params, method, json_body)
    cached = _read_cache(cp, ttl)
    if cached is not None:
        return cached["status"], cached["text"]
    if OFFLINE:
        raise SourceUnavailable(f"offline and not cached: {url}")

    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            if min_interval:
                time.sleep(min_interval)
            r = _session.request(
                method, url, params=params, json=json_body, headers=headers, timeout=45
            )
        except requests.RequestException as e:  # network hiccup
            last_exc = e
            log.warning("%s %s failed (%s); retry %d", method, url, e, attempt + 1)
            time.sleep(backoff * (attempt + 1))
            continue
        if r.status_code in (429, 500, 502, 503, 504):
            wait = float(r.headers.get("Retry-After", backoff * (2**attempt)))
            log.warning("%s %s → %s; waiting %.0fs", method, url, r.status_code, min(wait, 60))
            time.sleep(min(wait, 60))
            continue
        cp.write_text(json.dumps({"t": time.time(), "status": r.status_code, "text": r.text}))
        return r.status_code, r.text
    if last_exc:
        raise SourceUnavailable(f"{url}: {last_exc}")
    raise SourceUnavailable(f"{url}: still rate-limited after {retries} attempts")


def get_json(url: str, **kw) -> Any:
    status, text = request("GET", url, **kw)
    if status == 404:
        return None
    if status >= 400:
        raise SourceUnavailable(f"GET {url} → {status}: {text[:200]}")
    return json.loads(text)


def get_text(url: str, **kw) -> str | None:
    status, text = request("GET", url, **kw)
    if status == 404:
        return None
    if status >= 400:
        raise SourceUnavailable(f"GET {url} → {status}: {text[:200]}")
    return text


def post_json(url: str, body: Any, **kw) -> Any:
    status, text = request("POST", url, json_body=body, **kw)
    if status >= 400:
        raise SourceUnavailable(f"POST {url} → {status}: {text[:200]}")
    return json.loads(text)
