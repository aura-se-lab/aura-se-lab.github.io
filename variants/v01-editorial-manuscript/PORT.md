# Port v01 "Editorial Manuscript" into Jekyll

This variant renders the AURA Lab homepage as a typeset academic manuscript.

## 1. Copy files

From the repo root:

```
cp variants/v01-editorial-manuscript/jekyll/_layouts/about.liquid _layouts/about.liquid
cp variants/v01-editorial-manuscript/jekyll/_sass/_variant.scss   _sass/_variant.scss
```

Back up the originals first (`_layouts/about.liquid` will be overwritten).

## 2. Wire the SCSS partial

Add one line near the bottom of `_sass/_base.scss` (after the theme variables and
layout imports, so the variant can reference them and override the page chrome):

```scss
@import "variant";
```

The partial is namespaced under `.v01-editorial` and is gated by
`body:has(.v01-editorial)`, so it is inert on pages that do not use this layout.

## 3. Load the fonts

In `_includes/head.liquid`, inside the `<head>`, add the Google Fonts links
near the other font/`<link rel="stylesheet">` tags:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300..700;1,8..60,300..700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
```

## 4. Front-matter on `_pages/about.md`

Leave the existing `layout: about` and `permalink: /` in place. The body of
`about.md` (the lab statement) is rendered as the abstract. The decorative
`subtitle:` block is no longer used by this layout (the title and acronym
mark are hard-coded in the layout) and can be removed or left alone.

Recommended front matter:

```yaml
---
layout: about
title: About
permalink: /
news: true
selected_papers: false   # the layout supplies its own typeset reference list;
                         # flip to true if you want al-folio's selected_papers
                         # include to render inside the references shell.
social: true
---
```

## 5. Profile image

This variant intentionally omits `prof_pic.png` from the homepage; the
director appears as a typeset authors-line. No `profile:` block is needed.

## 6. Nav / footer

No nav changes required. The al-folio top navbar and site footer continue to
render through `layout: default`, which this `about.liquid` extends.
