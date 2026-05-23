# AURA Lab — Site Variants

Ten distinct redesign directions for the AURA Lab homepage (`/`, served by
`_layouts/about.liquid` + `_pages/about.md`), each produced as a
Jekyll-droppable bundle plus a standalone preview.

## Audience the variants optimize for

**Peer / academic credibility.** Prospective collaborators, program-committee
members, tenure reviewers, and fellow SE/AI researchers. The hierarchy that
matters: research agenda → selected publications → venues → people → news.
Aesthetic boldness is encouraged, but recruiting / marketing copy is not.

## Variant directory layout

Each variant lives under `variants/v<NN>-<short-name>/` and contains:

```
variants/v<NN>-<short-name>/
├── preview.html         # self-contained static render — open directly in a browser, no Jekyll required
├── styles.css           # the same CSS used by preview.html (referenced, not inlined, where reasonable)
├── jekyll/
│   ├── _layouts/about.liquid    # drop-in replacement for _layouts/about.liquid
│   ├── _sass/_variant.scss      # drop-in sass partial; @import from _sass/_base.scss
│   └── _includes/<...>          # any header/footer overrides this variant requires
└── PORT.md              # 1-page instructions: which files to copy where, which @import lines to add, which fonts to load
```

The `preview.html` is the artifact the LLM-as-judge panel evaluates. The
`jekyll/` tree is what actually ships if the variant wins.

## Hard quality bar

A variant ships **only** if all of the following hold:

- Every section in `_content.md` (below) is rendered. No `lorem ipsum`,
  no `<!-- TODO -->`, no missing team members or publications.
- The layout works at 1440px, 1024px, and 375px without horizontal
  scrollbars or overlapping text.
- Typography hierarchy reads cleanly: a peer skimming for 5 seconds
  can locate (a) what the lab does, (b) recent publications, (c) the
  director's name.
- The `jekyll/` files are real, not stubs — `about.liquid` renders
  with `{% include news.liquid %}` style hooks intact where applicable.

If a variant cannot meet the bar, **delete its folder** and report the cut
in this README under "Cut variants" with one line of why.

## Canonical content

All variants render the same source content, defined once in
[`_content.md`](./_content.md). Do not invent publications, team members,
or news items. Do not paraphrase the lab description into a different
research agenda.

## Cut variants

_(none yet)_
