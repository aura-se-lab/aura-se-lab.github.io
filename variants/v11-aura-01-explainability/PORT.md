# Port — v11 aura-01-explainability into al-folio

Variant device: **Annotated Margins**. Every claim has a sticky rationale rail
pinned beside it; on narrow screens the rail collapses inline. The page is the
argument for the Explainability research avenue.

## Files to drop into the al-folio repo

1. `jekyll/_layouts/about.liquid` -> `_layouts/about.liquid`
   (replaces the about layout; keeps `{{ content }}` so existing news/projects
   includes still render below the chrome).

2. `jekyll/_sass/_variant.scss` -> `_sass/_variant.scss`
   Add `@import "variant";` near the end of `assets/css/main.scss` (after
   al-folio's own imports so cascade wins). The partial declares `:root`
   tokens so it overrides al-folio's theme variables on the home page.

3. Add Google Fonts in `_includes/head.html` (or rely on the layout's
   `<link>` tags — both work):

       <link rel="preconnect" href="https://fonts.googleapis.com">
       <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">

## Content wiring

The hero (logo, h1, tagline, facts) lives in the layout. Author the page body
(`pages/about.md`) with the five sections in this order, each wrapped in
`<div class="track"> ... <aside class="track__rail"> ... </aside></div>`:

- `#about`     (Mission)        — pillars map to avenues `[02]`, `[05]`, `[01]`
- `#research`  (Avenues)        — mark avenue [01] with class `avenue--01`
- `#pubs`      (Publications)   — each `<pre class="bib__entry">` paired with
                                  `<details class="explain">`
- `#people`    (Members)        — `ls -la` table + collab list
- `#news`      (Activity Log)   — `git log` style ordered list

See `preview.html` for the canonical markup of every block. Copy verbatim;
content is real and must not be paraphrased.

## Constraints

- Do not change the palette tokens.
- Do not swap IBM Plex Mono.
- Do not remove the ASCII AURA plate or window chrome.
- Rationales must be grounded in `variants/_content.md` — no invented stats.

## Responsive

- 1440px : main 72ch + 280px rail, gap 28px.
- 1024px : same; rail still fits.
- <=960px : rail collapses inline below each section.
- 375px  : single column, no horizontal scroll.

No JS required. The explain drawers use native `<details>`.
