# AURA Lab brand assets

The lab's logo, adopted November 2026. Master: `aura-lab-wm/design` →
`logos/AURA-logo.svg` (outlined Aleo lettering, W&M colours only). The files
here are derived from it by copying the geometry verbatim. **Do not redraw it.**
To refresh them, re-derive from the master rather than editing paths by hand.

| File | What it is | Used by |
|---|---|---|
| `aura-symbol.svg` | The lattice symbol alone, viewBox cropped to the ink | Header (`Nav.astro`), OG cards |
| `aura-logo.svg` | Symbol + AURA wordmark + rule + expansion, cropped to the ink | Footer, landing-page Reach band |
| `wm-logo.svg` | William & Mary wordmark | Header |

## Colours

Only the two W&M colours, each exposed as a CSS variable with the master
colour as its fallback:

    --mk-green   symbol, wordmark, tagline, rule   #004E38  (W&M green)
    --mk-gold    centre square, rule marker        #B79257  (W&M gold)

On a light ground use the defaults. On the black chrome the site sets
`--mk-green: #fff` and leaves the gold: the W&M white-and-gold reversal, as on
the lab sign and the slide masthead. Nothing else is recoloured.

Renderers without CSS (resvg for the OG cards) resolve each `var(--x, #hex)`
to its fallback; see `src/pages/og/[...slug].png.ts`.

## Public copies

| Path | What |
|---|---|
| `public/favicon.svg` | Symbol; green turns white in a dark browser tab |
| `public/apple-touch-icon.png` | 180 px symbol on white |
| `public/img/aura-symbol.png`, `.svg` | 512 px / vector symbol; the JSON-LD organisation logo |
| `public/img/aura-logo.svg` | Full logo, plain colours |
| `public/img/aura-glyph.svg` | Old URL kept alive for hotlinks; now serves the new symbol |

## Superseded

`superseded/circuit-tree/` — the circuit-tree glyph and lockup the site used
until November 2026, with their PNG exports and the September proposals.
`superseded/aura-*.svg` — the four-arc glyph from the first rebuild pass.
Neither is referenced by the site.
