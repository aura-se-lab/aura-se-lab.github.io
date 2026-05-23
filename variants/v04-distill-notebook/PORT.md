# Port: v04 — Distill Notebook

Drop-in port for the AURA Lab al-folio site.

## 1. Copy files

From this folder into the site root:

```
jekyll/_layouts/about.liquid   ->  _layouts/about.liquid     (overwrite)
jekyll/_sass/_variant.scss     ->  _sass/_variant.scss        (new)
```

## 2. Wire the SCSS

In `_sass/_base.scss` (or `assets/css/main.scss`, wherever the al-folio
partials are imported), add at the bottom:

```scss
@import "variant";
```

The partial is scoped under `.aura-notebook`, so it will not affect any
other page.

## 3. Load the fonts

Add to `_includes/head.liquid` (inside `<head>`):

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
```

## 4. About-page front matter

`_pages/about.md` can keep its existing front matter; the new layout
ignores `profile:` and `subtitle:` (the headline / byline is rendered
inside the layout itself). The layout still honors
`{% include news.liquid %}` if `page.news: true` and
`site.announcements.enabled: true`, and `{% include selected_papers.liquid %}`
if `page.selected_papers: true` — when those are off it falls back to the
hard-coded canonical list.

## 5. Verify

- `bundle exec jekyll serve`
- Open `http://localhost:4000/`
- Check at 1440 / 1024 / 375px; sticky TOC tracks scroll; margin notes
  collapse to inline boxes below 1024px.

## Notes / caveats

- The `body.layout-about` rule hides al-folio's default `.post-header` /
  `.profile`. If your build doesn't auto-add that body class, either add
  it via `_includes/head.liquid` or remove that selector at the bottom of
  `_variant.scss`.
- If you want the live news feed instead of the canonical fallback,
  ensure `page.news: true` and `site.announcements.enabled: true`.
