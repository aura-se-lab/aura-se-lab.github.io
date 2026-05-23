# LLM-as-judge panel — AURA Lab variants

- **Panel:** 3 judges per candidate via HuggingFace router (`DeepSeek-V4-Pro`,
  `DeepSeek-V4-Flash`, `DeepSeek-V3.1`)
- **Target:** `variants/_content.md` (canonical content fixture) +
  `variants/_judge_brief.md` (audience + scoring brief)
- **Caveat:** single-vendor panel (Anthropic / OpenAI / Google keys were not
  available in this session). The signal is mostly a within-vendor stability
  check, not a true cross-vendor cross-validation. Treat the rankings as
  directional, not authoritative.
- **Rubric mapping** (lower = better, all on 0..1):
  - `fid` = `functional_correctness` → target fidelity (canonical content
    rendered, no inventions)
  - `cite` = `security_posture` → publication-citation integrity
  - `fin` = `structural_integrity` → typography / hierarchy / responsive finish
  - `peer` = `prompt_fidelity` → distinctness from generic template +
    peer credibility
  - `cd` = consensus distance from target across active checks
    (`faithfulness, coverage, hallucination`)
  - `diss` = dissent (max − min distance across judges)
- **Composite** = `0.7 × mean(fid,cite,fin,peer) + 0.3 × cd`

## Ranking

| # | Variant | Verdict | cd | diss | fid | cite | fin | peer | comp |
|---|---------|---------|----|------|-----|------|-----|------|------|
| 1 | **v02 brutalist-terminal** | **ACCEPT** | 0.06 | 0.03 | 0.00 | 0.00 | 0.08 | 0.08 | **0.05** |
| 2 | v01 editorial-manuscript   | REVIEW     | 0.07 | 0.20 | 0.00 | 0.00 | 0.17 | 0.08 | 0.06 |
| 3 | v05 swiss-minimal          | REVIEW     | 0.11 | 0.23 | 0.08 | 0.00 | 0.17 | 0.00 | 0.08 |
| 4 | v08 research-graph         | REVIEW     | 0.08 | 0.25 | 0.08 | 0.00 | 0.17 | 0.08 | 0.08 |
| 5 | v06 documentation          | REVIEW     | 0.15 | 0.30 | 0.12 | 0.00 | 0.05 | 0.15 | 0.10 |
| 6 | v03 research-index         | REVIEW     | 0.18 | 0.17 | 0.20 | 0.03 | 0.05 | 0.02 | 0.11 |
| 7 | v09 studio-longform        | REVIEW     | 0.27 | 0.47 | 0.13 | 0.00 | 0.12 | 0.07 | 0.14 |
| 8 | v04 distill-notebook       | REVIEW     | 0.47 | 0.50 | 0.17 | 0.00 | 0.08 | 0.08 | 0.20 |
| 9 | v07 editorial-magazine     | REVIEW     | 0.28 | 0.55 | 0.12 | 0.00 | 0.25 | 0.33 | 0.21 |
| 10| v10 dashboard-telemetry    | REVIEW     | 0.32 | 0.55 | 0.17 | 0.25 | 0.08 | 0.25 | 0.23 |

Only **v02** crossed the strict ACCEPT thresholds (`cd < 0.15` AND
`dissent < 0.20`). The other nine fell into REVIEW — most due to dissent on
"is this faithful?" rather than on content inventions. Per the panel: zero
variants are REJECT.

## Best-for-peer-audience pick

**v01 editorial-manuscript** is the strongest pick for the stated audience
(peer / academic credibility). It scored a perfect 0.00 on both content
fidelity AND citation integrity — judges found zero invented papers, people,
or news — and its TOSEM-/arXiv-style typesetting reads natively to
program-committee members and tenure reviewers. **v02 brutalist-terminal** is
the formal-verdict winner with the best raw scores (only ACCEPT verdict,
lowest dissent), but a minority judge explicitly flagged the terminal
aesthetic as "potentially seen as gimmicky by peers" — a risk worth
considering if the page must read as serious-on-first-sight.

## Consensus / notable issues to fix before shipping

These are the panel-flagged items most worth addressing on whichever variant
gets shipped (each is a real defect the judges agreed on, not a stylistic
preference):

- **v03 research-index** — missing the verbatim lab-statement paragraph
  (`_content.md` says "use verbatim or lightly trimmed"). Easy fix: add the
  statement as an intro block above the publication grid.
- **v06 documentation** — mission statement is paraphrased instead of
  verbatim; the "v2024.fall" version label is an invention not in the
  target. Drop the version label and restore the verbatim statement.
- **v05 swiss-minimal** — acronym expansion ("AI for Understandable and
  Responsible Automation") not in visible body, only in the page title.
  Add it as a subline under the giant lab name.
- **v10 dashboard-telemetry** — one judge flagged "fabricated statistics"
  for the bar charts (even though counts are derived). Add a small
  monospace footnote on each chart panel: "derived from publication list
  in _content.md" so it's audit-trail-explicit.
- **v04 distill-notebook** — the "Eq. 1" equation block (`AURA = f(...)`)
  and several margin notes were flagged as "unsourced editorial content
  not in target." Either move them into an explicit "Editor's notes"
  framing or remove them.
- **v07 editorial-magazine** — "Lead Story" tag and "Quarterly Issue 01"
  framing were flagged as "marketing-like language" and "fictional
  metadata." Rename "Lead Story" to a neutral label like "Featured paper"
  and drop the fictional issue number.
- **v02 brutalist-terminal** — minority view: terminal aesthetic may read
  as gimmicky to senior peers. Not a content issue; a positioning risk.
- **v01 editorial-manuscript** — no consensus issues. Minority view
  cautioned the manuscript treatment "may risk appearing overly
  stylized." Ship-ready as-is.

## Where to find the raw reports

- Per-variant JSON: `variants/.judge/v01.json` … `variants/.judge/v10.json`
- Each contains: full system prompt, user turn, per-judge verdicts +
  rationales, dimension flags, aggregate scores
- Replay any single panel without API calls:
  `python3 ~/.claude/skills/llms-as-judge/scripts/judge.py --replay variants/.judge/v02.json`
