import rss from "@astrojs/rss";
import type { APIContext } from "astro";
import { publications, displayName } from "@/lib/pubs";
import { lab } from "@/lib/lab";

/** Atom/RSS feed of publications — newest first. Peers can subscribe instead of polling Scholar. */
export async function GET(context: APIContext) {
  const items = [...publications].sort((a, b) => (b.date ?? String(b.year)).localeCompare(a.date ?? String(a.year))).slice(0, 100);
  return rss({
    title: `${lab.name} — Publications`,
    description: `New papers, preprints and columns from the AURA Lab at ${lab.institution.name}.`,
    site: context.site!,
    items: items.map((p) => {
      const d = p.date && p.date.length === 10 ? new Date(p.date) : new Date(Date.UTC(p.year, (p.month ?? 1) - 1, 1));
      return {
        title: p.title,
        pubDate: d,
        link: `/publications/${p.key}/`,
        description: `${p.authors.map((a) => displayName(a.name)).join(", ")}. ${p.venue_info?.name ?? p.venue_raw} (${p.year}).${p.abstract ? " " + p.abstract : ""}`,
        categories: [p.type, ...(p.threads ?? [])],
        ...(p.doi ? { customData: `<guid isPermaLink="false">doi:${p.doi}</guid>` } : {}),
      };
    }),
    customData: `<language>en-us</language>`,
  });
}
