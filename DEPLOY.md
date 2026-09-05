# Deploying auralab.sh

The site is a static build (`dist/`) served by **Cloudflare Workers (static assets)** and attached to the `auralab.sh` zone through Workers *custom domains*. All of it is declared in `wrangler.jsonc`; deploys run from GitHub Actions.

## One-time setup (≈10 minutes)

1. **Cloudflare API token** — dash.cloudflare.com → *My Profile → API Tokens → Create Token → "Edit Cloudflare Workers"* template. Scope it to the account and to the `auralab.sh` zone. Copy the token.
2. **Account ID** — visible on the right side of any zone overview page, or *Workers & Pages → Overview*.
3. **Workers subdomain** (for PR previews) — *Workers & Pages → Overview → Subdomain* (e.g. `aura-se-lab`). If you have never set one, pick it there.
4. **GitHub secrets** — repository → *Settings → Secrets and variables → Actions*:

   | Secret | Value |
   |---|---|
   | `CLOUDFLARE_API_TOKEN` | the token from step 1 |
   | `CLOUDFLARE_ACCOUNT_ID` | step 2 |
   | `CLOUDFLARE_WORKERS_SUBDOMAIN` | step 3 (only used to build preview URLs) |
   | `S2_API_KEY` | optional — [Semantic Scholar key](https://www.semanticscholar.org/product/api#api-key-form), raises rate limits for the sync |
   | `OPENALEX_API_KEY` | optional — [OpenAlex key](https://openalex.org/pricing) (their API is metered now; the sync skips OpenAlex without it) |
   | `BLUESKY_HANDLE` / `BLUESKY_APP_PASSWORD` | optional — for social posting (create an *app password* in Bluesky settings) |
   | `X_API_KEY` / `X_API_SECRET` / `X_ACCESS_TOKEN` / `X_ACCESS_SECRET` | optional — X developer app with *Read and write* |

5. **DNS** — the zone currently has records that answer for `auralab.sh` / `www` (they return a 404 today). Workers custom domains *cannot be created on a hostname that already has a CNAME/A record*, so delete those two records in *DNS → Records* first. The first deploy then creates the right records and certificates automatically.
6. **Merge the `astro-rebuild` branch into `main`** (or push to `main`). The *Deploy (Cloudflare)* workflow runs and the site is live at https://auralab.sh within a minute. `www.auralab.sh` 301-redirects to the apex (see `public/_redirects`).
7. **Old GitHub Pages URL** — repository → *Settings → Pages* → Source: *Deploy from a branch* → `gh-pages` / root. Then run the *Legacy redirect* workflow once (Actions → *Legacy redirect (GitHub Pages)* → Run). `aura-se-lab.github.io/*` now forwards to the same path on auralab.sh.

## How deploys work afterwards

- **Push to `main`** → `npm run build` → `wrangler deploy` → production.
- **Pull request** → build with `SITE_URL` pointing at the preview host → `wrangler versions upload --preview-alias pr-N` → the preview URL is posted as a PR comment. Previews live on `*.workers.dev`; production stays untouched until merge.
- **Manual deploy from your laptop** (rarely needed):

  ```bash
  npx wrangler login          # once
  npm run deploy              # build + deploy to production
  ```

## Checks after the first deploy

- https://auralab.sh/ loads with a valid certificate; https://www.auralab.sh/ redirects.
- https://auralab.sh/sitemap-index.xml, `/rss.xml`, `/publications.xml`, `/aura.bib` respond.
- Paste a paper URL into https://search.google.com/test/rich-results — it should detect a *ScholarlyArticle*.
- Submit the sitemap in Google Search Console (add the `auralab.sh` property; verify via the Cloudflare DNS TXT method).
- Ask Google Scholar to (re)crawl: the `citation_*` tags on `/publications/<key>/` follow the [inclusion guidelines](https://scholar.google.com/intl/en/scholar/inclusion.html#indexing).

## Rollback

*Workers & Pages → auralab-site → Deployments* lists every version with a one-click *Rollback*. Or `git revert` on `main`.

## Costs

Workers static assets are free at this scale (unlimited static requests, no bandwidth charge). GitHub Actions minutes for the weekly sync are negligible.
