"""Emit clean BibTeX for a publication (used for public/aura.bib and the per-paper copy button)."""
from __future__ import annotations

from .model import Pub, split_name

MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split()


def _esc(s: str) -> str:
    return s.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_") if s else s


def _protect_title(t: str) -> str:
    # keep capitalisation of acronyms: wrap all-caps tokens in braces
    out = []
    for w in t.split(" "):
        core = w.strip(":,;.?!()")
        if len(core) > 1 and core.isupper() or any(c.isupper() for c in core[1:]):
            out.append("{" + w + "}")
        else:
            out.append(w)
    return " ".join(out)


def to_bibtex(pub: Pub, venue_info: dict | None) -> str:
    vtype = (venue_info or {}).get("type")
    t = pub.type
    if t == "journal" or t == "magazine":
        etype = "article"
    elif t in ("conference", "workshop"):
        etype = "inproceedings"
    elif t == "preprint":
        etype = "misc"
    elif t == "thesis":
        etype = "phdthesis"
    elif t == "book":
        etype = "incollection"
    else:
        etype = "misc"
    authors = " and ".join(f"{split_name(a.name)[1]}, {split_name(a.name)[0]}".strip(", ") for a in pub.authors)
    venue_name = (venue_info or {}).get("name") or pub.venue_raw
    f: list[tuple[str, str]] = [("title", "{" + _protect_title(_esc(pub.title)) + "}"), ("author", "{" + _esc(authors) + "}")]
    if etype == "article":
        f.append(("journal", "{" + _esc(venue_name) + "}"))
    elif etype == "inproceedings":
        f.append(("booktitle", "{" + _esc(pub.venue_raw or venue_name) + "}"))
    elif pub.type == "preprint" and pub.arxiv:
        f += [("howpublished", "{arXiv preprint arXiv:" + pub.arxiv + "}"), ("eprint", "{" + pub.arxiv + "}"), ("archivePrefix", "{arXiv}")]
    if pub.year:
        f.append(("year", "{" + str(pub.year) + "}"))
    if pub.month:
        f.append(("month", MONTHS[pub.month - 1]))
    for k in ("volume", "number", "pages", "publisher"):
        v = getattr(pub, k)
        if v:
            f.append((k, "{" + _esc(str(v)).replace("–", "--") + "}"))
    if pub.doi:
        f.append(("doi", "{" + pub.doi + "}"))
    url = (f"https://doi.org/{pub.doi}" if pub.doi else None) or (f"https://arxiv.org/abs/{pub.arxiv}" if pub.arxiv else None) or pub.url
    if url:
        f.append(("url", "{" + url + "}"))
    if pub.note:
        f.append(("note", "{" + _esc(pub.note) + "}"))
    width = max(len(k) for k, _ in f)
    body = ",\n".join(f"  {k.ljust(width)} = {v}" for k, v in f)
    return f"@{etype}{{{pub.key},\n{body}\n}}"
