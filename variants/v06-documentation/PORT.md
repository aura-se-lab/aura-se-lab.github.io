# v06 Documentation — Port Instructions

Drop-in for the al-folio AURA Lab site. The variant scopes its CSS under
`.v06-doc`, so it will not collide with al-folio chrome.

## 1. Copy files

```
variants/v06-documentation/jekyll/_layouts/about.liquid  ->  _layouts/about.liquid
variants/v06-documentation/jekyll/_sass/_variant.scss     ->  _sass/_variant.scss
```

Back up the existing `_layouts/about.liquid` first.

## 2. Hook the Sass partial

Add to the top-level sass entry point (al-folio uses `assets/css/main.scss`
which imports from `_sass/`). Append:

```scss
@import "variant";
```

so the partial loads after the al-folio base.

## 3. Load fonts

The layout already injects the Google Fonts `<link>` tag for Inter and
JetBrains Mono at the top of the rendered page. No changes needed in
`_includes/head.liquid`. If the site CSP or self-hosting policy forbids
Google Fonts, swap the `<link>` for self-hosted equivalents and update the
`--sans` / `--mono` custom properties at the top of `_variant.scss`.

## 4. Front-matter for `_pages/about.md`

The layout renders the canonical content itself; `_pages/about.md` only
needs minimal front-matter:

```yaml
---
layout: about
title: home
permalink: /
---
```

Anything you place in the page body still renders (it appears between the
lead paragraph and the "Lab identity" section via `{{ content }}`).

## 5. News integration (optional)

If `site.news` is populated (al-folio's `_news` collection), the News
section pulls from there automatically (sorted reverse-chrono, capped at 6).
Otherwise it falls back to the four canonical items hard-coded in the
layout. No further config needed.

## 6. Verify

- Open `/` at 1440 / 1024 / 375 px. Sidebar collapses to hamburger below
  768 px; the right "on this page" rail hides below 1100 px.
- The scrollspy highlights the rail item matching the section currently
  in view.
- The accent color is `#1d4ed8`; the AURA green (`#1f6b3a`) is used only
  as a typographic highlight on the acronym initials.
