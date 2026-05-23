# Port v08 "Research Graph" into Jekyll

This variant renders the AURA Lab homepage as an interactive SVG knowledge graph
(hand-positioned, no graph library) with a linear text fallback below.

## 1. Copy files

From the repo root:

```
cp variants/v08-research-graph/jekyll/_layouts/about.liquid _layouts/about.liquid
cp variants/v08-research-graph/jekyll/_sass/_variant.scss   _sass/_variant.scss
cp variants/v08-research-graph/app.js                       assets/js/v08-research-graph.js
```

Back up the original `_layouts/about.liquid` first — it will be overwritten.

## 2. Wire the SCSS partial

Add one line near the bottom of `_sass/_base.scss` (after the theme imports):

```scss
@import "variant";
```

The partial is namespaced under `.v08-research-graph` and is gated by
`body:has(.v08-research-graph)`, so it is inert on every other page.

## 3. Load the fonts

In `_includes/head.liquid`, inside the `<head>`, add the Google Fonts links
near the existing font links:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

## 4. Front matter on `_pages/about.md`

Keep `layout: about` and `permalink: /`. The body of `about.md` (the lab
statement) is rendered inside the fallback "text view" section. The
decorative `subtitle:` and `profile:` blocks are no longer used by this
layout and can be removed or left alone.

Recommended front matter:

```yaml
---
layout: about
title: About
permalink: /
news: true
selected_papers: false   # flip to true if you want al-folio's selected_papers
                         # include to render inside the fallback list shell.
social: true
---
```

## 5. Profile image

This variant omits `prof_pic.png` from the homepage; the director is
represented by a labeled green node in the graph and is named in the page
header. No `profile:` block needed.

## 6. JS asset

The layout references `/assets/js/v08-research-graph.js`. Copy `app.js`
there (step 1 above). The script is vanilla JS, ~330 lines, no dependencies.

## 7. Nav / footer

No nav changes required. al-folio's top navbar and site footer continue to
render through `layout: default`, which this `about.liquid` extends. The
sticky `.v08-chrome` strip sits below the al-folio navbar.
