# v05 Swiss Minimal — Port Instructions

## 1. Copy files

```
jekyll/_layouts/about.liquid  ->  _layouts/about.liquid   (overwrite)
jekyll/_sass/_variant.scss    ->  _sass/_v05-variant.scss
```

## 2. Wire the SCSS

In `_sass/_base.scss` (or whichever partial `assets/css/main.scss` imports
last) append:

```scss
@import "v05-variant";
```

Rules are scoped under `.v05-shell` and won't collide with al-folio.

## 3. Load Inter

In `_includes/head.liquid` add inside `<head>` (skip if already present):

```liquid
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## 4. Disable default about chrome

In `_pages/about.md` front matter, set:

```yaml
profile: false
news: false
selected_papers: false
social: false
```

The new layout renders statement, pubs, people, news itself; `{{ content }}`
still receives any free-form Markdown body.

## 5. Verify

- `bundle exec jekyll serve`, open `/`.
- Check 1440 / 1024 / 375 px — no horizontal scroll; lab name fits one
  line above 1024 px and wraps cleanly below.
- Red accent appears only on A/R/A in the lab name, the active nav state,
  and the `→` arrow on publications.

## Revert

Restore the original `_layouts/about.liquid`, delete
`_sass/_v05-variant.scss`, remove the `@import "v05-variant";` line.
