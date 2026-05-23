# v15 — aura-05-task-aware · Lab-as-Patchset · Port notes

## Concept
The homepage IS the lab's patchset: every canonical content item is a
merged PR against `main`. The structural choice itself argues for the
Task-Aware Code Automation avenue (issues + diffs + repo-aware guidance).

## Inheritance from v02-brutalist-terminal
- `:root` token block copied verbatim (palette, type scale).
- IBM Plex Mono only.
- ASCII `AURA` wordmark plate, identical glyphs.
- Fake terminal window chrome (title relabeled to
  `aura-se-lab.github.io / tty5 / git log`).

## What is unique here
- Filter toolbar (GitHub-style) showing `25 Merged · 0 Open · 0 Draft`,
  filter tokens `is:merged author:aura-lab sort:created-asc`, count.
- 25 PR cards (#0 — #24), each with: header strip (PR id, title, merged
  date in lime, green `✓`), diff body, label chips.
- Diff bodies contain real canonical content only: actual bibtex for the
  six pubs, real roster YAML for the eight students + director + five
  collaborators, real news bodies, the verbatim mission, the four+1
  research avenue blurbs.
- PR #5 (Task-Aware) carries `pr--feat` accent — the variant's tell.
- PR #24 is `HEAD → main` (director registration), keeping head pinned.

## Files
- `preview.html` — self-contained static demo.
- `styles.css`   — companion stylesheet.
- `jekyll/_layouts/about.liquid` — data-driven port reading
  `site.data.patchset.prs[]` with fields `{id, title, merged, file,
  diff[{kind,text}], labels[], feat?, head?}`.
- `jekyll/_sass/_variant.scss` — scoped under `.v15-task-aware` so it
  coexists with al-folio chrome on non-homepage routes.

## Integration TODO (for porter)
1. Drop `_layouts/about.liquid` into the Jekyll site.
2. Import `_sass/_variant.scss` from `_sass/main.scss`.
3. Author `_data/patchset.yml` mirroring `preview.html` PR order so the
   layout's `pr_count` matches the visible count.

## Responsive
Verified at 1440, 1024, 375. PR header collapses to two rows under 720px;
diff hunk font-size steps down at 480px. Logo clips gracefully.

## Caveats
- 25 results, not 18 as the brief estimated. Count was driven by
  one-PR-per-canonical-item discipline.
- No "open" or "draft" PRs rendered — `_content.md` contained no honest
  open todos. Tab counters show `0 Open · 0 Draft`.
