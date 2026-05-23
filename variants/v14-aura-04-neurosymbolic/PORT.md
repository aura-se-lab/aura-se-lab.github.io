# v14 — aura-04-neurosymbolic · Spec / Prose Pairs

## Structural device
Every claim on the homepage renders twice: a typed predicate on the
left, the canonical prose on the right, vertically aligned by a hairline.
A phosphor-green turnstile `⊢` in the gutter reads "this prose is
entailed by the spec." The layout itself is an argument for the
**Neurosymbolic AI for SE** avenue.

## Inheritance from v02
- `:root` token block copied verbatim (deep-forest greens, phosphor accent).
- IBM Plex Mono only. ASCII `AURA` wordmark plate is identical.
- Fake-terminal window chrome retained; title relabeled to
  `aura-se-lab.github.io / tty4 / spec.aura`.

## Files
- `preview.html` — self-contained homepage with all canonical content.
- `styles.css` — pair-grid layout + syntax coloring for specs.
- `jekyll/_layouts/about.liquid` — al-folio drop-in for `/`.
- `jekyll/_sass/_variant.scss` — SCSS port of the stylesheet.

## Spec language (handcrafted, no MathJax)
- Records and sum types: `record Lab where { … }`, `type Avenue = …`.
- Pub signatures: `mastropaolo2024triumph : Insight → Trajectory(SE)`.
- Predicates use Unicode glyphs: `∀ ∃ → ⊢ ∧ ∈ ⊆ ⊕ ↔`.
- Italic type variables, bold constructors, dim comments.
- Every constructor traces to canonical content
  (avenues / pubs / people / news). No invented concepts.

## Responsive
- Desktop (1440 / 1024): two-column grid, ⊢ in gutter.
- `<860px`: stacks to a single column; `⊢` becomes inline and is
  decorated with the word "entails" so the semantics survive.
- `<520px`: facts collapse, font-size tightens.

## Porting to the live site
1. Drop `_variant.scss` into `_sass/` and `@import` it last.
2. Replace `_layouts/about.liquid` with the one in `jekyll/`.
3. Author the homepage body in markdown using
   `<div class="pair">…</div>` blocks per claim.
4. No JS required; the only dynamic element is the blinking cursor.

## Caveats
- The `⊢` glyph relies on IBM Plex Mono including U+22A2. The font
  ships with it, but if you swap fonts retest.
- BibTeX bodies are still rendered in `<pre>` inside the prose column
  to preserve formatting; the type signature in the spec column is the
  "abstract" of the paper.
