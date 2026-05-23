# Variant v09 — Port instructions

Drop-in for `/Users/amastro/Academia/W&M/aura-se-lab.github.io`.

## 1. Copy files

- `jekyll/_layouts/about.liquid`  →  `_layouts/about.liquid` (replace existing).
- `jekyll/_sass/_variant.scss`    →  `_sass/_variant.scss` (new file).

## 2. Wire up the SCSS partial

In `_sass/_base.scss` (or `assets/css/main.scss`, wherever al-folio aggregates
sass), add at the bottom:

```scss
@import "variant";
```

## 3. Load fonts

In the site's `_includes/head.liquid` (or wherever `<head>` is built), add:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,400;1,8..60,500;1,8..60,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
```

## 4. Frontmatter

`_pages/about.md` keeps `layout: about` and `permalink: /`. All content is now
rendered by the new layout itself; the markdown body of `about.md` is
ignored — feel free to leave it empty or as a comment.

## 5. News integration

If `site.news` collection exists, the layout will pull from it automatically
(date + truncated content). If not, the layout falls back to the four hand-
curated items from `_content.md`.

## 6. Notes

- All variant CSS is scoped under `.v09-root`, so other al-folio pages
  (publications, CV, etc.) are unaffected.
- Reading-progress bar and scroll-reveal degrade gracefully without JS and
  respect `prefers-reduced-motion`.
- The al-folio navbar/footer remain (via `layout: default` parent).
