# v13 — aura-03-multi-agent / Agent Transcript — PORT

## Concept
A coherent family member with v02-brutalist-terminal. The page is
co-authored by four named agents — `planner`, `coder`, `tester`,
`reviewer` — whose turns are rendered as a left transcript column.
The right column carries the canonical content. Multi-agent SE IS the
rendering pipeline; the layout itself argues for the avenue.

## Files
- `preview.html` — self-contained reference render
- `styles.css` — preview stylesheet
- `jekyll/_layouts/about.liquid` — al-folio layout
- `jekyll/_sass/_variant.scss` — scoped under `.v13`
- `PORT.md` — this file

## How to port into al-folio
1. Copy `jekyll/_layouts/about.liquid` to `_layouts/about.liquid`.
2. Copy `jekyll/_sass/_variant.scss` to `_sass/_variant.scss` and add
   `@import "variant";` to `assets/css/main.scss`.
3. Populate `_data/lab.yml` with keys: `statement`, `avenues[]`
   (`title`, `body`, `supporting?`), `publications[]` (`type`, `key`,
   `authors`, `title`, `venue`, `year`), `students[]`
   (`handle`, `joined`), `collaborators[]`, `news[]`
   (`hash`, `date`, `message`).
4. Set the homepage front-matter `layout: about`.
5. Load `IBM+Plex+Mono` (weights 300–700) via the existing fonts include.

## Hard-inherited from v02
- Color tokens copied verbatim.
- IBM Plex Mono everywhere.
- ASCII AURA block-letter wordmark plate identical to v02.
- Fake-terminal window chrome — title relabelled to
  `aura-se-lab.github.io / tty3 / agents.log`.

## Unique structural device
- Two-column "loop" per section: 240px transcript on desktop,
  160px on tablet, inline log above section on <768px.
- Each loop has 4 monospace log lines: planner → coder → tester →
  reviewer, sealed by an `approved` stamp.
- PID + monotonic timestamps: 00:00.04 → 00:00.16 (loop 1) through
  00:01.18 (loop 5). PIDs cycle a01–a04.
- Tester checks render real counts that match the DOM:
  5/5 avenues, 6/6 pubs, 8/8 members (1 director + 7 phd),
  5/5 collaborators, 4/4 news items.

## Responsive
- 1440: sticky transcript column @ 240px; 2-col avenue grid.
- 1024: transcript shrinks to 160px.
- 768: transcript becomes a dashed inline log above its section.
- 375: gitlog and ls collapse columns; window title hidden.

## Caveats
- Transcript is sticky on desktop; users who scroll fast through a
  long content block briefly see the next section's transcript before
  it pops. Acceptable for a brutalist log aesthetic.
- Liquid layout assumes `_data/lab.yml` exists; fallbacks are inline
  for the mission statement only — empty avenues/pubs render an
  empty section.
- No JS. All interactivity is anchor-based / CSS.
