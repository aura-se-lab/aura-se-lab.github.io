# Judge brief — AURA Lab homepage redesign

You are judging one of ten redesign variants of the AURA Lab homepage.
The **target** file is the canonical content fixture all variants must
render faithfully (`variants/_content.md`). The **candidate** file is a
single variant's static `preview.html` (the rendered output a peer would
see in a browser). The candidate is HTML — read it as you would the
rendered page; you are judging the visible result, not the markup style.

## Who the page is for

Peer / academic credibility. Audience = fellow software-engineering /
AI-for-SE researchers, ICSE / FSE / ASE / TOSEM program-committee
members, and tenure reviewers. Not undergraduate recruitment. Not VC
pitch. Score what a senior peer would think on a 5-second skim and a
2-minute read.

## What to score (in addition to the standard checks)

When the quality-rubric dimensions are evaluated, interpret them as
follows for this artifact:

- **functional_correctness** → **target fidelity**. Does the candidate
  render ALL the canonical content from the target file — the lab
  identity, the five research avenues, at least four real publications
  (with correct venues + years), the director + at least four named
  PhD students, and at least three news items? Penalize: invented
  papers, invented people, paraphrased away research avenues, missing
  sections.

- **security_posture** → **citation / hallucination integrity**. Are
  the publication citations exactly the six listed in the target?
  Are author names, venues (TOSEM, ICPC, FORGE, ICSME, FSE), and years
  preserved? Flag any year/venue substitution or fabricated co-author.

- **structural_integrity** → **finish quality**. Typography hierarchy,
  responsive integrity (the page should work at 1440 / 1024 / 375px),
  layout coherence, code structure. Flag: broken grids at narrow
  widths, missing fallbacks, inconsistent spacing, accidental lorem
  ipsum, half-styled sections.

- **prompt_fidelity** → **distinctness + peer credibility**. Two
  sub-questions: (a) does this variant diverge meaningfully from a
  generic academic-lab template (al-folio default = centered avatar
  + serif body + news list), or is it a recolor? (b) would a peer
  take this lab seriously on sight — does the typographic discipline,
  hierarchy, and tone read as a serious research operation rather
  than as a marketing landing page or a startup site? Flag: emoji,
  gradient hero, glassmorphism, AI-template aesthetic.

## Hard "do not accept" rules

- Any fabricated publication, person, or news item beyond what's in
  the target file. (You may verify by checking that every author name
  and paper title in the candidate appears in the target.)
- Any obviously broken responsive behavior (only judgeable from CSS;
  flag suspicious patterns like `width: 100vw` without a min-width
  fallback, or grid templates that have no breakpoint).
- Any lorem ipsum, TODO, FIXME, or placeholder text in the rendered
  body.
- Marketing language ("transform your codebase," "unlock the power
  of AI," etc.) is grounds for REJECT — the audience is academic.

## Output

Standard judge.py JSON contract. Be terse in `flags` — one sentence
each, prefixed with the dimension. Examples of useful flags:

- `[target fidelity] missing 4th publication (Velasco et al., ICPC 2025)`
- `[citation integrity] author "Smith" appears in candidate but not in target — likely fabricated`
- `[finish quality] team grid uses fixed 4-column at all breakpoints; will overflow at 375px`
- `[distinctness] essentially al-folio default + palette swap; minimal divergence`
