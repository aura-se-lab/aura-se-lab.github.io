#!/usr/bin/env python3
"""First-page previews for the Publications grid — see docs/SPEC.html § 04.3.

For every publication with an open full text, fetch the PDF, render page 1, and
normalise it to a 17:22 frame so every card in the grid matches. Runs alongside
the weekly sync, so a new paper arrives with its preview already made.

Only papers with an arXiv id are fetched: arXiv sends no X-Frame-Options, so its
PDFs can also be embedded in the reader. Publisher PDFs (ACM DL, IEEE Xplore) are
paywalled and frame-blocked. The durable fix is to post the author's accepted
manuscript to public/papers/<key>.pdf — both ACM and IEEE author agreements allow
it — which this script picks up automatically in preference to arXiv.

    python3 scripts/pubs/previews.py [--force]

Requires: pdftoppm (poppler-utils), pillow.
"""
import argparse, json, os, subprocess, sys, time
from PIL import Image, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PUBS = os.path.join(ROOT, "src", "data", "publications.json")
LOCAL = os.path.join(ROOT, "public", "papers")            # green-OA copies, preferred
# A first page supplied as an image, for a paper whose full text we cannot post.
# Kept out of public/ because it is a cover, not a copy of the paper.
PAGES = os.path.join(ROOT, "data", "first-pages")
CACHE = os.path.join(ROOT, ".cache", "pdfs")
OUT = os.path.join(ROOT, "src", "assets", "papers")
AR = 17 / 22
W = 1040                                                   # 4x the 260px card: the
                                                           # record page shows it at
                                                           # 320 and the news lead
                                                           # larger still, so 520 was
                                                           # soft on any modern screen
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")


# Repositories that serve the PDF straight off the URL, with no bot wall in the
# way. Publisher domains (link.springer.com, dl.acm.org, sciencedirect, ieee) are
# deliberately absent: they answer a PDF request with an HTML challenge page even
# when Unpaywall calls the record open access.
OPEN_HOSTS = (
    "ceur-ws.org",
    "aclanthology.org",
    "openreview.net",
    "proceedings.mlr.press",
    "proceedings.neurips.cc",
    "www.usenix.org",
    "usenix.org",
    "arxiv.org",
    "hal.science",
    "zenodo.org",
)


def _open_pdf_url(p):
    """A direct PDF link on a host that actually serves it."""
    for cand in (p.get("pdf"), p.get("url")):
        if not cand or not cand.lower().endswith(".pdf"):
            continue
        host = cand.split("/")[2].lower() if "//" in cand else ""
        if host in OPEN_HOSTS:
            return cand
    return None


def source_for(p):
    """Local accepted manuscript first, then arXiv, then an open repository.

    None means no open full text — the site draws a typographic cover instead.
    The durable fix for a paywalled paper is to drop the accepted manuscript at
    public/papers/<key>.pdf, which both ACM and IEEE author agreements allow;
    this picks it up on the next run in preference to anything else.
    """
    local = os.path.join(LOCAL, p["key"] + ".pdf")
    if os.path.exists(local):
        return ("local", local)
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        page = os.path.join(PAGES, p["key"] + ext)
        if os.path.exists(page):
            return ("first-page", page)
    if p.get("arxiv"):
        return ("arxiv", f"https://arxiv.org/pdf/{p['arxiv']}")
    repo = _open_pdf_url(p)
    if repo:
        return ("repository", repo)
    return (None, None)


def fetch(url, dest):
    subprocess.run(["curl", "-sSL", "--max-time", "60", "-A", UA, "-o", dest, url], check=True)
    ok = os.path.getsize(dest) > 20000 and open(dest, "rb").read(5) == b"%PDF-"
    if not ok and os.path.exists(dest):
        os.remove(dest)
    return ok


def frame(im):
    """Normalise to the 17:22 card frame — pad, never crop the title block."""
    im = im.convert("RGB")
    ar = im.width / im.height
    if abs(ar - AR) > 0.01:
        if ar > AR:
            canvas = Image.new("RGB", (im.width, round(im.width / AR)), "white")
        else:
            canvas = Image.new("RGB", (round(im.height * AR), im.height), "white")
        canvas.paste(im, ((canvas.width - im.width) // 2, 0))
        im = canvas
    im = im.resize((W, round(W / AR)), Image.LANCZOS)
    return ImageEnhance.Contrast(im).enhance(1.03)


def render(pdf, key):
    stem = os.path.join(CACHE, key)
    subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", "300", "-jpeg",
                    "-jpegopt", "quality=95", pdf, stem], check=True, capture_output=True)
    page = next((f for f in sorted(os.listdir(CACHE)) if f.startswith(key + "-")), None)
    if not page:
        return None
    im = Image.open(os.path.join(CACHE, page)).convert("RGB")
    ar = im.width / im.height
    if abs(ar - AR) > 0.01:                                # pad, never crop the title block
        if ar > AR:
            canvas = Image.new("RGB", (im.width, round(im.width / AR)), "white")
        else:
            canvas = Image.new("RGB", (round(im.height * AR), im.height), "white")
        canvas.paste(im, ((canvas.width - im.width) // 2, 0))
        im = canvas
    im = im.resize((W, round(W / AR)), Image.LANCZOS)
    return ImageEnhance.Contrast(im).enhance(1.03)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-render even if a preview exists")
    args = ap.parse_args()

    for d in (CACHE, OUT, LOCAL, PAGES):
        os.makedirs(d, exist_ok=True)
    pubs = json.load(open(PUBS))

    made = skipped = none = 0
    for p in pubs:
        key = p["key"]
        dest = os.path.join(OUT, key + ".jpg")
        if os.path.exists(dest) and not args.force:
            skipped += 1
            continue
        kind, src = source_for(p)
        if not kind:
            none += 1
            continue
        if kind == "first-page":
            im = frame(Image.open(src))
            im.save(dest, quality=82, optimize=True, progressive=True)
            print(f"  + {key}  ({kind})")
            made += 1
            continue
        pdf = src if kind == "local" else os.path.join(CACHE, key + ".pdf")
        if kind != "local" and not os.path.exists(pdf):
            if not fetch(src, pdf):
                print(f"  ! {key}: could not fetch {src}", file=sys.stderr)
                continue
            time.sleep(0.6)                                 # be polite to the host
        im = render(pdf, key)
        if im is None:
            print(f"  ! {key}: no page rendered", file=sys.stderr)
            continue
        im.save(dest, quality=82, optimize=True, progressive=True)
        print(f"  + {key}  ({kind})")
        made += 1

    print(f"\n{made} rendered · {skipped} already present · {none} without an open full text "
          f"({len(pubs)} publications)")
    if none:
        print("Post the accepted manuscript to public/papers/<key>.pdf, or drop a\n"
              "first-page image at data/first-pages/<key>.png, to cover the rest.")


if __name__ == "__main__":
    main()
