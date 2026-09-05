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
CACHE = os.path.join(ROOT, ".cache", "pdfs")
OUT = os.path.join(ROOT, "src", "assets", "papers")
AR = 17 / 22
W = 520                                                    # 2x of the 260px card
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def source_for(p):
    """Local accepted manuscript first, then arXiv. None means no open full text."""
    local = os.path.join(LOCAL, p["key"] + ".pdf")
    if os.path.exists(local):
        return ("local", local)
    if p.get("arxiv"):
        return ("arxiv", f"https://arxiv.org/pdf/{p['arxiv']}")
    return (None, None)


def fetch(url, dest):
    subprocess.run(["curl", "-sSL", "--max-time", "60", "-A", UA, "-o", dest, url], check=True)
    ok = os.path.getsize(dest) > 20000 and open(dest, "rb").read(5) == b"%PDF-"
    if not ok and os.path.exists(dest):
        os.remove(dest)
    return ok


def render(pdf, key):
    stem = os.path.join(CACHE, key)
    subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", "150", "-jpeg",
                    "-jpegopt", "quality=92", pdf, stem], check=True, capture_output=True)
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

    for d in (CACHE, OUT, LOCAL):
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
        pdf = src if kind == "local" else os.path.join(CACHE, key + ".pdf")
        if kind == "arxiv" and not os.path.exists(pdf):
            if not fetch(src, pdf):
                print(f"  ! {key}: could not fetch {src}", file=sys.stderr)
                continue
            time.sleep(0.6)                                 # be polite to arXiv
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
        print("Post the accepted manuscript to public/papers/<key>.pdf to cover the rest.")


if __name__ == "__main__":
    main()
