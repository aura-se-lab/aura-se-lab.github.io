# PORT — v07 Editorial Magazine ("AURA Quarterly")

Drop-in for the al-folio Jekyll site. ~10 minute port.

## 1. Files to copy

```
v07-editorial-magazine/jekyll/_layouts/about.liquid  →  _layouts/about.liquid
v07-editorial-magazine/jekyll/_sass/_variant.scss    →  _sass/_variant.scss
```

Back up the original `_layouts/about.liquid` first.

## 2. Wire in the sass

In `_sass/_base.scss` (or whichever stylesheet your site imports), add at the
very end so it can override base styles:

```scss
@import "variant";
```

If your site uses `assets/css/main.scss` instead, add `@import "variant";`
there.

## 3. Load the web fonts

In `_includes/head.liquid` add inside `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

## 4. Content notes

- The layout reads canonical content from `_content.md`. All papers, people,
  and news are inlined in `about.liquid` as static markup (al-folio's
  `news` collection is consumed when present; otherwise the four canonical
  dispatches render as fallback).
- `_pages/about.md` only needs front-matter `layout: about`. Page body is
  ignored — content lives in the layout.

## 5. Color / accent

The accent (deep editorial red `#b8332a`) is set via `--accent`. To revert
to the existing AURA green, edit `_sass/_variant.scss`:

```scss
--accent: #1f6b3a;
```

The masthead bar, pull-quote band, drop caps, and lead-story tag all
re-color from that single token.

## 6. Verify

Visit `/`. Expect: black masthead bar with red underline, giant Fraunces
headline breaking across five lines, asymmetric agenda + publications
sections, dark pull-quote spread, and a four-column dispatches strip. No
horizontal scroll at 1440 / 1024 / 375.
