// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Canonical origin. Override with SITE_URL when building a preview
// (e.g. SITE_URL=https://auralab-site.<account>.workers.dev npm run build).
const site = process.env.SITE_URL ?? "https://auralab.sh";

export default defineConfig({
  site,
  trailingSlash: "always",
  build: {
    format: "directory",
    inlineStylesheets: "auto",
  },
  integrations: [
    sitemap({
      filter: (page) => !page.includes("/og/") && !page.includes("/drafts/"),
      changefreq: "weekly",
    }),
  ],
  image: {
    // Sharp is the default service; kept explicit so the intent is visible.
    service: { entrypoint: "astro/assets/services/sharp" },
  },
  prefetch: {
    prefetchAll: true,
    defaultStrategy: "hover",
  },
  markdown: {
    shikiConfig: { theme: "github-light" },
  },
});
