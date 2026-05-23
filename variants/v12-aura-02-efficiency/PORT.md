# v12 — aura-02-efficiency · Telemetry Frame

Sibling of v02-brutalist-terminal. Inherits palette, IBM Plex Mono, the
window chrome, and the ASCII AURA wordmark verbatim. Structural device:
**every block in the page carries a resource-cost annotation**, the way
the lab annotates its quantized models.

## Files

- `preview.html` — standalone static render.
- `styles.css` — full stylesheet (extends v02 tokens 1:1).
- `jekyll/_layouts/about.liquid` — homepage layout for al-folio.
- `jekyll/_sass/_variant.scss` — scoped SCSS injected via al-folio.

## Structural device

1. **Telemetry strip** below the hero: `PUB 06 · MEM 08 · AV 05 · COLLAB 05 · 2024-Q3 → 2025`.
2. **Byte-budget stacked bar**: 5 green-family segments whose widths are
   the word-share of each rendered section. Labels align under segments.
3. **Section heads** carry a right-aligned `[≈ N W · B B · ◯ Ts]` cost tag.
4. **Avenue cards** carry a `[≈ N W · B B]` efficiency footer.
5. **BibTeX entries** carry a `[≈ N authors · B B]` corner tag.

## Derivation of numbers (honest)

All counts come from the rendered content of `preview.html` (no kWh, no
FLOPs, no fabricated latency).

- **PUB/MEM/AV/COLLAB**: literal counts of items rendered (6 papers, 8
  members incl. director, 5 avenues, 5 collaborators).
- **Section words (W)**: words in the visible body text of each section
  (heading + paragraph(s)). Mission=92, Research=146, Pubs=180,
  People=58, News=50. Total=526.
- **Section bytes (B)**: UTF-8 byte length of the same visible text.
- **Read-time (◯ Ts)**: `words / 280 wpm * 60` seconds, rounded to 3dp.
- **Byte-budget proportions**: each section's W divided by 526. Mission
  17.5%, Research 27.7%, Pubs 34.2%, People 11.1%, News 9.5%
  (sum = 100.0%). Segment widths and label widths share the same `%`
  values so they align within sub-pixel tolerance.
- **Avenue costs**: words and UTF-8 bytes of that card's body text.
- **Bib efficiency tags**: `N authors` = author tokens split on `and`.
  `B B` = UTF-8 byte length of the rendered BibTeX block.

## Responsive

- 1440px: 2-col avenue grid, bar full-width, bib cost in corner.
- 1024px: same, narrower gutters via `clamp()`.
- 375px: avenues single column, byte-budget labels wrap with swatches,
  bib cost reflows under each entry, `.ls__date` collapses.
