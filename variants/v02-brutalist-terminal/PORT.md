# Port — v02 Brutalist Terminal

Drop the variant into the live al-folio Jekyll site.

## 1. Copy files

From this folder into the repo root:

```
jekyll/_layouts/about.liquid   ->   _layouts/about.liquid
jekyll/_sass/_variant.scss     ->   _sass/_variant.scss
```

Back up the originals first (e.g. `mv _layouts/about.liquid _layouts/about.liquid.bak`).

## 2. Import the sass partial

In `_sass/_base.scss` (or `assets/css/main.scss` — wherever al-folio
collects partials), add at the very end so the variant overrides:

```scss
@import "variant";
```

## 3. Load IBM Plex Mono

In `_includes/head.liquid`, add inside `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

## 4. Tweak `_pages/about.md`

- Keep `permalink: /`, `layout: about`, `news: true`.
- Keep the `subtitle:` HTML — the variant restyles inline green spans
  via `.v02-tagline span[style*="green"]`.
- The `profile:` block can stay; the variant ignores `prof_pic.png`
  (no avatar in brutalist mode). Remove it if you want a cleaner front-matter.
- Set `selected_papers: true` to render the bibtex block.

## 5. Publications partial (optional, for true bibtex look)

The variant styles `.v02-bib pre` and the `.bib__*` spans. If you want
the canonical bibtex appearance shown in `preview.html`, override
`_includes/selected_papers.liquid` to emit `<pre class="bib__entry">…</pre>`
blocks. If you keep the default al-folio rendering, entries still inherit
the monospace + dim-rule treatment from `.v02-bib`.

## 6. News partial

The variant wraps `{% include news.liquid %}` in `.v02-gitlog-wrap` and
restyles the al-folio news table as a `git log`-style list. No changes
needed to the partial itself.

## 7. Smoke test

`bundle exec jekyll serve` and visit `/`. Check at 1440 / 1024 / 375px.
Box-drawing rule should span the full width without wrapping; if it
clips on very wide displays, lengthen the `content:` string in
`.v02-rule::before`.
