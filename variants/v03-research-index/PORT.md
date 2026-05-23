# PORT — v03 Research Index

Drop-in for the AURA Lab Jekyll (al-folio) site.

## 1. Copy files

- `jekyll/_layouts/about.liquid` -> `_layouts/about.liquid` (overwrite)
- `jekyll/_sass/_variant.scss`   -> `_sass/_variant.scss`

## 2. Wire up SCSS

In `assets/css/main.scss` (after al-folio's base partials), add:

```scss
@import "variant";
```

Selectors are namespaced (`.v03-*`, `body:has(.v03-shell)`) so other
pages are unaffected.

## 3. Fonts

Add to `_includes/head.liquid`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

## 4. `_pages/about.md` front matter

```yaml
layout: about
title: About
permalink: /
news: true
selected_papers: false
social: true
```

The old `subtitle:` and `profile:` blocks are ignored — the masthead is
built into the new layout.

## 5. Optional: data-driven publications

Create `_data/v03_publications.yml` with entries like:

```yaml
- venue: TOSEM
  year: 2024
  title: "From Triumph to Uncertainty: ..."
  authors: "Mastropaolo, A.; Escobar-Velásquez, C.; ..."
  chips:
    - { label: Survey, accent: true }
    - { label: "AI for SE" }
```

If absent, six canonical entries render inline.

## 6. Verify

`bundle exec jekyll serve` and check `/` at 1440 / 1024 / 375.
