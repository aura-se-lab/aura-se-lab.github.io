"""Load lab members (and their author IDs) from src/content/people/*.md."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import config
from .model import name_keys, norm_title, split_name


@dataclass
class Member:
    slug: str
    name: str
    role: str
    status: str
    joined: str | None
    left: str | None
    ids: dict
    aliases: list[str] = field(default_factory=list)

    @property
    def since_year(self) -> int | None:
        if self.joined:
            m = re.match(r"(\d{4})", str(self.joined))
            return int(m.group(1)) if m else None
        return None

    def keys(self) -> set[str]:
        ks = set()
        for n in [self.name, *self.aliases]:
            ks |= name_keys(n)
        # also plain "family|first-initial" from the display name without nicknames "(Ben)"
        clean = re.sub(r"\([^)]*\)", "", self.name)
        ks |= name_keys(clean)
        return ks


def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def load_members(people_dir: Path = config.PEOPLE_DIR) -> list[Member]:
    out: list[Member] = []
    for p in sorted(people_dir.glob("*.md")):
        fm = _frontmatter(p.read_text(encoding="utf-8"))
        if not fm:
            continue
        ids = fm.get("ids") or {}
        out.append(
            Member(
                slug=p.stem,
                name=fm["name"],
                role=fm.get("role", "phd"),
                status=fm.get("status", "current"),
                joined=fm.get("joined"),
                left=fm.get("left"),
                ids={k: v for k, v in ids.items() if k != "aliases" and v},
                aliases=list(ids.get("aliases") or []),
            )
        )
    return out


class MemberIndex:
    """Fast author-string → member-slug lookup."""

    def __init__(self, members: list[Member]):
        self.members = members
        self._exact: dict[str, str] = {}  # "family|given" → slug
        self._initial: dict[str, set[str]] = {}  # "family|g" → {slug}
        for m in members:
            for k in m.keys():
                if "|" in k:
                    fam, giv = k.split("|", 1)
                    if len(giv) == 1:
                        self._initial.setdefault(k, set()).add(m.slug)
                    else:
                        self._exact[k] = m.slug

    def match(self, author_name: str) -> str | None:
        giv, fam = split_name(author_name)
        fam_k, giv_k = norm_title(fam), norm_title(giv)
        if giv_k and f"{fam_k}|{giv_k}" in self._exact:
            return self._exact[f"{fam_k}|{giv_k}"]
        # given-name prefix match ("Md Zahidul" vs "Md Zahidul Haque")
        for k, slug in self._exact.items():
            f, g = k.split("|", 1)
            if f == fam_k and giv_k and (g.startswith(giv_k) or giv_k.startswith(g)):
                return slug
        if giv_k:
            cands = self._initial.get(f"{fam_k}|{giv_k[0]}", set())
            if len(cands) == 1:
                return next(iter(cands))
        return None
