# The AURA Lab — auralab.sh

**AI for Understandable and Responsible Automation in Software Engineering** · William & Mary

This repository is the source of the lab website, served at **https://auralab.sh** from Cloudflare. It is an [Astro](https://astro.build) static site whose publication list is maintained by an automated pipeline (DBLP · Crossref · Semantic Scholar · OpenAlex · arXiv), reviewed by humans through pull requests.

```
├── src/
│   ├── content/            ← what humans edit
│   │   ├── people/*.md     one file per member (bio + author IDs used by the pipeline)
│   │   ├── news/*.md       announcements (the bot drafts paper news here as draft: true)
│   │   └── research/*.md   the four A·U·R·A threads (keywords drive paper classification)
│   ├── data/               ← generated: publications.json, metrics.json (do not hand-edit)
│   ├── pages/              routes (home, research, publications, people, news, join, feeds, OG images)
│   ├── components/         Nav, Footer, PubRow, PersonCard, …
│   └── styles/global.css   design tokens — aligned with antoniomastropaolo.io
├── data/
│   ├── lab.yml             lab identity, contacts, funding, nav
│   ├── venues.yml          venue → badge/name/type mapping
│   ├── collaborators.yml   frequent external co-authors
│   ├── publications.local.bib       manual entries & abstracts (merged, never duplicated)
│   └── publications.overrides.yml   per-paper fixes, include/exclude rules
├── scripts/
│   ├── pubs/               publications pipeline (python)  →  docs/AUTOMATION.md
│   ├── social/             Bluesky / X poster
│   ├── legacy-redirect/    the stub that keeps aura-se-lab.github.io links alive
│   └── screenshots.mjs     visual QA at 1440 / 1024 / 390 px
├── public/                 static files, _headers, _redirects, aura.bib (generated)
├── .github/workflows/      ci · deploy · pubs-sync · social-post · legacy-redirect
├── wrangler.jsonc          Cloudflare Workers static-assets config (custom domains)
└── DEPLOY.md               one-time setup + how deploys work
```

## Everyday tasks

| I want to… | Do this |
|---|---|
| Add a lab member | Copy any file in `src/content/people/`, add a photo under `src/assets/people/`, fill `ids:` (DBLP pid, Scholar id…). The next sync picks up their papers. |
| Someone graduated | Set `status: alumni`, `left: YYYY-MM`, `next: "Where they went"`. |
| Post news | Add `src/content/news/YYYY-MM-DD-slug.md`. Set `social: true` to have it posted to Bluesky/X on merge. |
| Fix a paper's venue / add code link / feature it | Add an entry under `entries:` in `data/publications.overrides.yml` (matched by key). |
| Add a paper the sources missed | Append a BibTeX entry to `data/publications.local.bib`. |
| Hide a wrongly attributed paper | Add it under `exclude:` in the overrides file. |
| Run the sync locally | `pip install -r scripts/pubs/requirements.txt && npm run sync:pubs` |
| Preview the site | `npm install && npm run dev` → http://localhost:4321 |

## Develop

```bash
npm install
npm run dev          # live preview
npm run build        # static build → dist/
npm run sync:pubs    # refresh publications from the bibliographic sources
node scripts/screenshots.mjs   # full-page screenshots of the build into .screens/
```

Requires Node ≥ 22 and Python ≥ 3.11.

## Automation (summary)

- **Publications sync** — every Monday (and on demand) a workflow collects the lab's papers, merges/deduplicates them, refreshes citation counts and links, classifies them into research threads, regenerates `public/aura.bib`, drafts a news post for each new paper, and opens a pull request with a human-readable report. Details: [docs/AUTOMATION.md](docs/AUTOMATION.md).
- **Deploy** — every push to `main` builds and deploys to auralab.sh; every pull request gets a preview URL.
- **Social** — news items flagged `social: true` are posted to Bluesky/X once they land on `main` (at most once, ever).
- **SEO & indexing** — every paper page carries Google Scholar `citation_*` tags and JSON-LD; the site ships RSS feeds for news and publications, a sitemap, and per-page Open Graph cards.

## Design

Typography and palette mirror the director's site (Inter Tight, JetBrains Mono, near-black ink, a single green accent, hairline rules). Tokens live in `src/styles/global.css`.

## License

Code: MIT (see `LICENSE`). Content (texts, photos, papers) © The AURA Lab and respective authors.
