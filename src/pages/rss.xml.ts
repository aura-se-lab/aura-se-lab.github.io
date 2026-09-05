import rss from "@astrojs/rss";
import type { APIContext } from "astro";
import { getCollection } from "astro:content";
import { lab } from "@/lib/lab";

export async function GET(context: APIContext) {
  const items = (await getCollection("news", ({ data }) => !data.draft)).sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
  return rss({
    title: `${lab.name} — News`,
    description: `News from the AURA Lab (${lab.acronym.expansion}) at ${lab.institution.name}.`,
    site: context.site!,
    items: items.map((i) => ({
      title: i.data.title,
      pubDate: i.data.date,
      link: `/news/${i.id}/`,
      description: (i.body ?? "").replace(/\[([^\]]+)\]\([^)]+\)/g, "$1").replace(/[*_#>]/g, "").trim(),
      categories: [i.data.kind],
    })),
    customData: `<language>en-us</language><managingEditor>${lab.contact.email} (${lab.director.name})</managingEditor>`,
  });
}
