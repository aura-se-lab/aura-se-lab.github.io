# AURA Lab brand assets

The lab's own logo, exported from the masters in `~/Documents/mastropaolo-logos/`
(12,076 × 8,312 PNG with transparency). **Do not redraw or recolour it.**

| File | What it is | Use |
|---|---|---|
| `aura-mark.png` | Circuit-tree glyph alone, 884 × 763, transparent | Header, favicon, initials tiles |
| `aura-lockup.png` | Glyph + AURA wordmark + expansion, 2462 × 763 | Wherever the lab speaks for itself |
| `aura-lockup-wm.png` | The same with the William & Mary lockup, 2462 × 929 | Footer, OG cards, slides, posters |
| `aura-mark-web.png` | 420 px web export of the glyph | Convenience copy |

## It is a light-ground mark

The circuit strokes are `#17485A`. Measured against the site's two grounds:

| Colour | On paper `#e8ebe6` | On ink `#0e1512` |
|---|---|---|
| Teal `#17485A` | **8.27:1** | 1.86:1 |
| AURA green `#009051` | 3.42:1 | 4.50:1 |
| Mint `#70C0B0` | 1.77:1 | 8.69:1 |
| Sage `#609050` | 3.12:1 | 4.94:1 |

The teal all but vanishes on ink, so the site's chrome follows the logo rather
than the reverse: the header and the footer colophon are light, and the ink is
kept for the provenance strip, the Join panel and the baseline. If you ever need
the mark on a dark ground, commission a proper reversed version — do not
recolour this one in CSS.

`#009051`, sampled from the wordmark, is exposed as `--brand` and used for the
chrome only (CTA, active nav underline, sync dot). The `--t1…--t4` thread
palette is separate, because it carries small text on paper and needs the
contrast.
