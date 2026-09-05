# Moving the automation onto Cloudflare

How the publications fetcher and the rest of the pipeline would work as Cloudflare
Workers, what that buys, what it costs, and what should *not* move.

Written against the platform limits published on 2026-09-05 (linked inline —
re-check before committing to a phase, they move).

---

## 1. Where things stand

The site is a Worker with static assets (`auralab-site`, `wrangler.jsonc`), deployed
from a workstation with `npx wrangler deploy`. Everything that keeps it current runs
in GitHub Actions:

| job | trigger | what it does |
|---|---|---|
| `pubs-sync.yml` | Mondays 06:17 UTC | `scripts/pubs/sync.py` — 1,610 lines of Python across 6 sources, opens a PR |
| `previews.py` | manual | `pdftoppm` page 1 of each arXiv PDF → `src/assets/papers/<key>.jpg` |
| `social-post.yml` | push to main touching `src/content/news/**` | posts flagged news to Bluesky / X |
| `legacy-redirect.yml` | push to main | publishes the redirect stub to `gh-pages` |
| `deploy.yml` | push to main | builds; deploys only if the Cloudflare secrets exist |

It works. The problems are specific, and worth naming before proposing to replace
anything:

1. **The HTTP cache is disposable.** `data/cache/` is restored by `actions/cache`,
   which evicts after 7 days idle and at a 10 GB repo cap. A cold run re-fetches
   every DBLP, Crossref, S2 and OpenAlex record — the exact behaviour that got DBLP
   returning 503 during the original build.
2. **Citation counts are frozen between merges.** The site says "52 publications ·
   synced Sep 5"; the numbers behind it only move when someone merges a PR. There is
   no live surface, so the "impact over time" view has nothing to draw.
3. **Binaries live in git.** 24 preview JPEGs today (~1.8 MB), one per paper,
   growing with every arXiv posting, plus any accepted manuscripts added to
   `public/papers/`.
4. **Deploys need a Cloudflare API token in GitHub.** Not set, so `deploy.yml`
   builds but skips deploying, and shipping is manual.
5. **Nothing records history.** Each sync overwrites `metrics.json`. Last week's
   citation count is gone.

Note what is *not* on that list: the fetching itself. A weekly cron in GitHub
Actions is free, observable, and already correct. Moving it for its own sake buys
nothing.

---

## 2. Platform limits that decide the design

| | Workers Free | Workers Paid |
|---|---|---|
| External subrequests per invocation | **50** | 10,000 (raisable to 10M via `limits.subrequests`) |
| Subrequests to CF services | 1,000 | matches the configured limit |
| CPU per HTTP request | **10 ms** | 30 s default, up to 5 min |
| CPU per Cron Trigger | **10 ms** | 30 s (< 1 h interval) · **15 min (≥ 1 h interval)** |
| Browser Run | 10 min/day, 3 concurrent | 10 h/month, 10 concurrent, then $0.09/browser-hour |

Sources: [Workers limits](https://developers.cloudflare.com/workers/platform/limits/),
[subrequest change, Feb 2026](https://developers.cloudflare.com/changelog/post/2026-02-11-subrequests-limit/),
[Browser Run pricing](https://developers.cloudflare.com/browser-run/pricing/).

**This settles one question immediately.** A sync run touches DBLP (9 member pids +
search fallbacks), Crossref by DOI, an S2 batch, OpenAlex, and arXiv — comfortably
over 50 external subrequests, and the merge over ~52 records is well past 10 ms of
CPU. **The fetcher cannot run on the Workers free plan.** On Paid, a weekly cron
(interval ≥ 1 h) gets 15 minutes of CPU and 10,000 subrequests, which is ample.

So: any phase below that puts fetching on Workers requires Workers Paid ($5/month).
Phases that only add an API and storage fit inside the free plan.

---

## 3. Target architecture

```
                        ┌─────────────────────────────────────────┐
   Mondays 06:17 UTC ──▶│  auralab-sync         (Cron Trigger)    │
                        │  runs Workflow PubsSync, step per source│
                        └───┬───────────────┬──────────────┬──────┘
                            │               │              │
                    ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼─────────────┐
                    │ KV  PUBS     │ │ D1 CITATIONS│ │ Queue PREVIEWS    │
                    │ http cache   │ │ one row per │ │ new arXiv papers  │
                    │ current json │ │ paper/week  │ │                   │
                    └───────┬──────┘ └──────┬──────┘ └─────┬─────────────┘
                            │               │              │
                            │               │      ┌───────▼────────────┐
                            │               │      │ auralab-previews   │
                            │               │      │ Browser Run → R2   │
                            │               │      └───────┬────────────┘
                            │               │              │
                            │               │        ┌─────▼─────┐
                            │               │        │ R2 PAPERS │
                            │               │        └─────┬─────┘
                            ▼               ▼              ▼
                        ┌─────────────────────────────────────────┐
                        │  auralab-site   (static assets + /api)  │
                        │  auralab.sh · www.auralab.sh            │
                        └─────────────────────────────────────────┘
                            ▲
                            │ Workers Builds on push to main
                        ┌───┴──────────────┐
                        │ GitHub: PR gate  │  ← a human still reviews every sync
                        └──────────────────┘
```

The review gate does not move. The sync opens a pull request exactly as it does
today; nothing reaches the site without a person merging it.

---

## 4. Components

### 4.1 `auralab-site` — Workers Builds

No code change. Connect the Worker to `aura-se-lab/aura-se-lab.github.io` in the
dashboard (Settings → Builds → Connect), production branch `main`, build command
`npm run build`, deploy command `npx wrangler deploy`.

Removes the need for `CLOUDFLARE_API_TOKEN` in GitHub entirely — Cloudflare pulls
the repo itself. `deploy.yml` can then be deleted, and `ci.yml` keeps doing the
build-and-link-check on pull requests.

Cost: free. Time: minutes. **Do this first regardless of the rest.**

### 4.2 `auralab-api` — read-only JSON at the edge

A route inside `auralab-site` rather than a separate Worker, so it shares the
domain and needs no CORS.

```
GET /api/metrics          → { total, reviewed, citations, by_year, updated }
GET /api/publications     → the same array the build consumes
GET /api/citations/:key   → [{ week, count, source }]   ← from D1
```

Reads from KV, `Cache-Control: public, max-age=900, stale-while-revalidate=86400`.
CPU per request is a KV read and a JSON passthrough — inside the free plan's 10 ms.

What it unlocks: the landing rail and the stat row can show *today's* citation
count rather than the number frozen at last merge, and the impact trend has a real
series behind it. Both must degrade to the build-time JSON when the API is
unreachable — the page is static first, live second, never blank.

### 4.3 `auralab-sync` — the fetcher, as a Workflow

A [Workflow](https://developers.cloudflare.com/workflows/) rather than a plain cron
handler, because each step gets independent retries and durable state: DBLP going
503 retries that step alone instead of losing the run.

```ts
export class PubsSync extends WorkflowEntrypoint<Env, Params> {
  async run(event, step) {
    const cfg     = await step.do("load config",   () => loadFromGitHub(env));
    const dblp    = await step.do("dblp",     retry3, () => fetchDblp(cfg));
    const crossref= await step.do("crossref", retry3, () => fetchCrossref(cfg));
    const s2      = await step.do("s2",       retry3, () => fetchS2(cfg));
    const openalex= await step.do("openalex", retry3, () => fetchOpenAlex(cfg));
    const arxiv   = await step.do("arxiv",    retry3, () => fetchArxiv(cfg));

    const merged  = await step.do("merge",  () => merge([dblp,crossref,s2,openalex,arxiv], cfg));
    const diff    = await step.do("diff",   () => diffAgainst(env.PUBS, merged));
    await step.do("persist", () => writeAll(env.PUBS, env.CITATIONS, merged));
    await step.do("queue previews", () => enqueueNew(env.PREVIEWS, diff.added));
    await step.do("open PR", () => openOrUpdatePR(env, merged, diff));
  }
}
```

```jsonc
// wrangler.jsonc — the sync Worker
{
  "name": "auralab-sync",
  "main": "src/sync/index.ts",
  "compatibility_date": "2026-09-01",
  "compatibility_flags": ["nodejs_compat"],
  "triggers": { "crons": ["17 6 * * 1"] },
  "limits": { "cpu_ms": 900000, "subrequests": 20000 },
  "kv_namespaces":  [{ "binding": "PUBS", "id": "…" }],
  "d1_databases":   [{ "binding": "CITATIONS", "database_name": "auralab", "database_id": "…" }],
  "queues": { "producers": [{ "binding": "PREVIEWS", "queue": "auralab-previews" }] },
  "workflows": [{ "binding": "PUBS_SYNC", "name": "pubs-sync", "class_name": "PubsSync" }]
}
```

Secrets, set with `wrangler secret put`: `S2_API_KEY`, `OPENALEX_API_KEY`,
`GITHUB_TOKEN` (contents + pull-requests write, repo-scoped fine-grained).

**The cost of this phase is the port.** `scripts/pubs/` is 1,610 lines of working,
debugged Python: union-find clustering by DOI/arXiv/normalised title, field-level
source priority, venue mapping, thread classification, override merging. Rewriting
it in TypeScript is roughly two days plus a period of running both and diffing the
output until they agree. That is the honest number, and it is the reason this phase
is third rather than first.

### 4.4 `auralab-previews` — first pages without poppler

`pdftoppm` and Pillow cannot run in a Worker; there is no way around that. The
Cloudflare-native replacement is [Browser Run](https://developers.cloudflare.com/browser-run/):
load the arXiv PDF in headless Chrome and screenshot the first page.

```ts
const shot = await env.BROWSER.quickAction("screenshot", {
  url: `https://arxiv.org/pdf/${arxivId}`,
  viewport: { width: 1020, height: 1320 },   // 17:22, the card's aspect
});
await env.PAPERS.put(`papers/${key}.jpg`, shot);
```

Served from `/papers/*` bound to R2, or committed into the sync PR so previews stay
reviewable alongside the metadata.

**This needs a spike before it is promised.** Chrome renders PDFs through PDFium in
its built-in viewer, and the screenshot may include viewer chrome (toolbar, page
shadow) that has to be cropped, or may refuse to render at all under `quickAction`.
Budget half a day to find out. If it does not work cleanly, the fallback is
unglamorous and fine: keep `previews.py` in a GitHub Actions job and have it upload
to R2 with an API token instead of committing JPEGs.

Volume is trivial either way — the lab published 30 papers in 2026, so a page render
every week or two sits inside the free 10 minutes/day.

### 4.5 D1 — the citation history

The one genuinely new capability, and the answer to "show the overall trend, and
impact of the research" without a citation-index headline number.

```sql
CREATE TABLE citations (
  key        TEXT NOT NULL,       -- publication key, e.g. afrin2025quantization
  source     TEXT NOT NULL,       -- s2 | openalex | scholar
  count      INTEGER NOT NULL,
  observed_at TEXT NOT NULL,      -- ISO date of the sync run
  PRIMARY KEY (key, source, observed_at)
);
CREATE INDEX citations_by_date ON citations (observed_at);
```

One row per paper per source per weekly run — about 100 rows a week, 5,000 a year.
Far inside D1's free tier. After a year it supports a per-paper sparkline and a
lab-wide cumulative curve, both drawn from real observations rather than a single
scraped total.

---

## 5. Staged plan

| phase | what | plan needed | effort | payoff |
|---|---|---|---|---|
| **0** | Workers Builds on `auralab-site`; delete `deploy.yml` | Free | ~30 min | pushes to main deploy themselves; no Cloudflare token in GitHub |
| **1** | KV + D1 + `/api/*`; existing Python job POSTs its results to an authenticated Worker endpoint at the end of each run | Free | ~half a day | live citation counts on the site; citation history starts accumulating from the first run |
| **2** | Port the fetcher to a Workflow; retire `pubs-sync.yml` | **Paid ($5/mo)** | ~2 days + a diffing period | the pipeline no longer depends on GitHub Actions; durable per-source retries; the HTTP cache stops evaporating |
| **3** | Previews through Browser Run into R2; drop JPEGs from git | Free tier suffices | ~half a day + a spike | binaries leave the repo; new papers get covers without a local poppler |

**Recommendation: do 0 and 1, and stop there for now.** They are cheap, they fix the
two problems that actually show on the site (manual deploys, stale citations), and
they add the trend data. Phase 2 is a rewrite of working code whose only failure
mode so far has been an upstream 503 — worth doing when the Python job starts
costing time, not before. Phase 3 is worth it the moment a second batch of papers
needs covers.

---

## 6. Open questions

1. **Workers Paid** — phase 2 requires it. $5/month; worth confirming that comes
   out of a budget that exists before the port is scheduled.
2. **Does Browser Run screenshot a PDF cleanly?** Unknown until spiked. Everything
   in phase 3 depends on the answer.
3. **Where do previews live — R2 or git?** R2 keeps the repo clean; git keeps them
   reviewable in the sync PR alongside the metadata they belong to. Leaning git for
   now, since the volume is small and the review gate is the point.
4. **Should `/api/*` be public?** It exposes only what the site already ships in its
   build output, so there is nothing to protect, but a rate limit is cheap insurance.
5. **Six DBLP author ids are still missing** from `src/content/people/*.md`. No
   architecture fixes that — those members' papers are found only by name matching
   until the ids are filled in.
