# Automation

Everything that keeps auralab.sh current without anyone editing HTML.

## 1. Publications pipeline (`scripts/pubs/`)

```
             ┌──────────┐   ┌──────────┐   ┌───────────┐   ┌──────────┐   ┌───────┐
  members ──▶│  DBLP    │   │ Semantic │   │  arXiv    │   │ local    │   │ prev. │
  (ids in    │ pid XML  │   │ Scholar  │   │ by author │   │ .bib     │   │ json  │
  people/)   │ + search │   │ author   │   │           │   │          │   │       │
             └────┬─────┘   └────┬─────┘   └─────┬─────┘   └────┬─────┘   └───┬───┘
                  └──────────────┴───────┬───────┴──────────────┴─────────────┘
                                         ▼
                        relevance filter (member author ∧ date ≥ since)
                                         ▼
                   cluster by DOI / arXiv id / normalised title  (union-find)
                                         ▼
              enrich by identifier: Crossref (dates, pages) · S2 batch (citations, TL;DR, PDF)
                                    · OpenAlex (citations, OA)  · Google Scholar (opt-in)
                                         ▼
                 merge (field-level source priority) → stable keys → venue mapping
                 → status → thread classification → overrides → sort
                                         ▼
     src/data/publications.json · src/data/metrics.json · public/aura.bib · data/sync-report.md
                                         ▼
                    draft news posts for NEW papers (src/content/news/*.md, draft: true)
```

### Why several sources

Google Scholar has no API and forbids scraping; it is treated as an *optional* enrichment (`--scholar`), never as the backbone. DBLP is authoritative for CS venues but occasionally returns 503 (it did while this pipeline was being built — the search-API fallback and Semantic Scholar kept the run complete). Crossref knows exact dates and pages for DOIs; Semantic Scholar knows citations, open-access PDFs and TL;DRs; arXiv knows preprints and abstracts. The merge takes the best field from the most trustworthy source that has it:

| field | preferred source order |
|---|---|
| kind (journal / conference / preprint) | DBLP → Crossref → S2 → local |
| title, venue, volume, pages, dates | local overrides → Crossref → DBLP → S2 → arXiv |
| arXiv id, abstract, PDF | any source that has it (preprints are best at this) |
| citations | max over S2 / OpenAlex / Scholar, with provenance kept |

A preprint and its published version are merged into **one** record (the reviewed version wins; the arXiv id is kept as a link). Bibliographic details never leak from a CoRR record into a reviewed paper.

### What counts as a lab paper

A record is kept if at least one author matches a member (by name and aliases in `src/content/people/*.md`) **and** it is dated on/after `defaults.since` in `data/publications.overrides.yml` (currently `2024-09`, the lab's founding) — or after the member's own `joined` date, whichever is later. Force-include earlier work with `include:`; drop namesakes with `exclude:`.

### Human control points

| file | purpose |
|---|---|
| `src/content/people/<slug>.md` → `ids:` | DBLP pid / Scholar / Semantic Scholar / OpenAlex ids; `aliases` for alternative spellings |
| `data/venues.yml` | venue badge, full name, type, URL, rank; unmapped venues are listed in every report |
| `data/publications.overrides.yml` | per-paper patches (`selected`, `award`, `code`, `threads`, `venue`, `status`…), include/exclude |
| `data/publications.local.bib` | manual entries and abstracts; merged by DOI/arXiv/title, never duplicated |
| `src/content/research/*.md` → `keywords` / `featured` | drive thread classification |

### Running it

```bash
pip install -r scripts/pubs/requirements.txt
python3 scripts/pubs/sync.py                 # full run (≈1–2 min; HTTP responses cached 6 h in data/cache/)
python3 scripts/pubs/sync.py --dry-run       # report only
python3 scripts/pubs/sync.py --offline       # rebuild from cache
python3 scripts/pubs/sync.py --discover      # suggest DBLP ids for members lacking them
python3 scripts/pubs/sync.py --scholar       # also read Google Scholar (pip install scholarly)
```

Environment: `S2_API_KEY` (recommended), `OPENALEX_API_KEY` (optional), `PUBS_MAILTO` (polite-pool contact for Crossref/OpenAlex).

### The weekly PR

`.github/workflows/pubs-sync.yml` runs Mondays 06:17 UTC. It commits the regenerated files to the branch `bot/pubs-sync` and opens/updates a PR whose body is `data/sync-report.md`: new papers, changed fields (status, venue, citations), papers no longer found, unmapped venues, members missing ids, sources skipped. Review, fix via overrides if needed, merge. **Nothing is merged automatically.**

New papers also get a **draft news post** (`draft: true`, `social: true`). Flip `draft` to `false` in the PR to publish it — it will be posted to social networks on merge.

## 2. Deployment (`.github/workflows/deploy.yml`)

Push to `main` → build → `wrangler deploy` → auralab.sh. Pull requests get a preview URL. See `DEPLOY.md`.

## 3. Social posting (`scripts/social/post.py`)

On merge to `main`, every news item with `social: true` and `draft: false` that is not yet in `data/social-log.json` is posted to Bluesky and/or X (whichever secrets exist). The log is committed back, so nothing is posted twice. `--dry-run` prints the composed posts.

## 4. SEO & indexing (built into the site)

- `citation_*` meta tags on every paper page (Google Scholar indexing).
- JSON-LD: `ResearchOrganization` on every page, `ScholarlyArticle` per paper, `Person` per member, `NewsArticle` per news item.
- `sitemap-index.xml`, `rss.xml` (news), `publications.xml` (papers), `aura.bib` (all BibTeX, CORS-enabled).
- Per-page Open Graph cards rendered at build time (`/og/*.png`).
- `_redirects` keeps old al-folio paths and `www` working; `_headers` sets security and cache headers.

## 5. Ideas queued for later

- Software page synced from the `aura-se-lab` GitHub org (stars, last release) — the pipeline pattern is the same.
- Lab citation dashboard (h-index, citations/year) from `metrics.json` — the data is already collected.
- Per-paper "Reproduce in browser" buttons, an open peer-review archive, the Ph.D. onboarding kit — see `docs/features-brainstorm.md`.
