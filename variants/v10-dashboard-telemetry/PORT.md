# v10 — Dashboard / Telemetry — Port Instructions

Drop-in steps to ship this variant on the live al-folio Jekyll site.

## 1. Copy files

From this folder into the repo root:

```
jekyll/_layouts/about.liquid    →  _layouts/about.liquid     (overwrite)
jekyll/_sass/_variant.scss      →  _sass/_variant.scss       (new file)
```

Back up the existing `_layouts/about.liquid` first if you want a rollback path.

## 2. Wire up the sass partial

In `_sass/_base.scss` (or `assets/css/main.scss`, wherever al-folio's bottom-most
import lives), add at the end:

```scss
@import "variant";
```

The partial namespaces everything under `.aura-v10`, so it will not bleed into
publications, blog, or CV pages.

## 3. Load fonts

Add to `_includes/head.liquid` inside `<head>` (or to the al-folio fonts include):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

## 4. Front-matter for `_pages/about.md`

Strip out al-folio's `profile:` / `news:` / `selected_papers:` toggles — this
layout renders its own panels. Keep just:

```yaml
---
layout: about
title: about
permalink: /
---
```

Optional: pass an override paragraph via `lab_statement:` in the front-matter
to replace the default lede.

## 5. Optional: live news from `_news/`

The layout already checks `site.news` and will render up to 6 sorted items
into the "Recent Dispatches" panel. If `site.news` is empty it falls back to
the four hard-coded items from `_content.md`. No further action needed.

## 6. Verify

- `bundle exec jekyll serve` and confirm the homepage at `/` renders the
  panel grid.
- Resize to 1440 / 1024 / 375 — panels should reflow 12-col → 6-col → 1-col
  with no horizontal scrollbar.
- Other pages (publications, blog, cv) should be untouched.
