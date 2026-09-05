/**
 * Open Graph cards, rendered at build time with satori → resvg.
 *   /og/site.png, /og/publications.png, /og/people.png, /og/news.png, /og/research.png, /og/join.png
 *   /og/publications-<key>.png, /og/people-<slug>.png, /og/research-<slug>.png, /og/news-<slug>.png
 */
import type { APIRoute, GetStaticPaths } from "astro";
import { getCollection } from "astro:content";
import satori from "satori";
import { Resvg } from "@resvg/resvg-js";
import { readFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { publications, displayName, venueLabel } from "@/lib/pubs";
import { lab } from "@/lib/lab";
import glyphSvg from "@/assets/img/aura-glyph.svg?raw";

const require = createRequire(import.meta.url);
const fontPath = (w: number) => require.resolve(`@fontsource/inter-tight/files/inter-tight-latin-${w}-normal.woff`);

interface Card {
  kicker: string;
  title: string;
  sub?: string;
  foot?: string;
}

export const getStaticPaths: GetStaticPaths = async () => {
  const people = await getCollection("people");
  const threads = await getCollection("research");
  const news = await getCollection("news", ({ data }) => !data.draft);
  const cards: { slug: string; card: Card }[] = [
    { slug: "site", card: { kicker: `${lab.institution.name} · Computer Science`, title: lab.tagline, sub: lab.acronym.expansion } },
    { slug: "publications", card: { kicker: "Publications", title: "Publication index", sub: `${publications.length} papers, preprints and columns — refreshed automatically` } },
    { slug: "people", card: { kicker: "People", title: "Lab members", sub: "Ph.D. students, undergraduates, alumni and collaborators" } },
    { slug: "news", card: { kicker: "News", title: "Lab news", sub: "Acceptances, awards, funding and people" } },
    { slug: "research", card: { kicker: "Research", title: "Four threads, one aura", sub: threads.map((t) => t.data.title).join(" · ") } },
    { slug: "join", card: { kicker: "Join", title: "Work with us", sub: "Ph.D. students · undergraduate researchers · collaborators" } },
    ...threads.map((t) => ({ slug: `research-${t.id}`, card: { kicker: `Research thread · ${t.data.letter}`, title: t.data.title, sub: t.data.short } })),
    ...people.map((p) => ({ slug: `people-${p.id}`, card: { kicker: p.data.title ?? p.data.role, title: p.data.name, sub: p.data.interests.join(" · ") } })),
    ...publications.map((p) => ({
      slug: `publications-${p.key}`,
      card: { kicker: `${venueLabel(p)} · ${p.year}`, title: p.title, sub: p.authors.map((a) => displayName(a.name)).join(", "), foot: p.venue_info?.name ?? p.venue_raw },
    })),
    ...news.map((n) => ({ slug: `news-${n.id}`, card: { kicker: `News · ${n.data.date.toISOString().slice(0, 10)}`, title: n.data.title } })),
  ];
  return cards.map(({ slug, card }) => ({ params: { slug }, props: { card } }));
};

const glyphUri = `data:image/svg+xml;base64,${Buffer.from(glyphSvg).toString("base64")}`;

const fonts = await Promise.all(
  [300, 500, 600].map(async (w) => ({ name: "Inter Tight", data: await readFile(fontPath(w)), weight: w as 300 | 500 | 600, style: "normal" as const }))
);

const h = (type: string, props: Record<string, unknown>, ...children: unknown[]) => ({
  type,
  props: { ...props, children: children.length === 0 ? undefined : children.length === 1 ? children[0] : children },
});

function clamp(s: string, n: number) {
  return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, "") + "…" : s;
}

export const GET: APIRoute = async ({ props }) => {
  const { card } = props as { card: Card };
  const title = clamp(card.title, 120);
  const titleSize = title.length > 90 ? 44 : title.length > 60 ? 52 : title.length > 36 ? 60 : 72;
  const tree = h(
    "div",
    { style: { width: 1200, height: 630, display: "flex", flexDirection: "column", background: "#ffffff", color: "#050505", fontFamily: "Inter Tight", position: "relative" } },
    h("div", { style: { height: 8, background: "#15803d", width: "100%" } }),
    h(
      "div",
      { style: { display: "flex", flexDirection: "column", flex: 1, padding: "52px 64px 44px 64px" } },
      h(
        "div",
        { style: { display: "flex", alignItems: "center", gap: 14, fontSize: 20, fontWeight: 500, letterSpacing: 1.5, textTransform: "uppercase", color: "#4a4a4a" } },
        h("span", { style: { color: "#15803d", fontWeight: 600 } }, "AURA Lab"),
        h("span", {}, "·"),
        h("span", {}, clamp(card.kicker, 70))
      ),
      h("div", { style: { marginTop: 28, fontSize: titleSize, fontWeight: 600, lineHeight: 1.08, letterSpacing: -1.5, display: "flex", maxWidth: 1040 } }, title),
      card.sub ? h("div", { style: { marginTop: 22, fontSize: 26, fontWeight: 300, lineHeight: 1.35, color: "#2c2c2c", display: "flex", maxWidth: 1000 } }, clamp(card.sub, 150)) : h("div", {}),
      h("div", { style: { flex: 1 } }),
      h(
        "div",
        { style: { display: "flex", alignItems: "center", justifyContent: "space-between", borderTop: "1px solid #ececec", paddingTop: 22 } },
        h(
          "div",
          { style: { display: "flex", alignItems: "center", gap: 16 } },
          h("img", { src: glyphUri, width: 52, height: 52 }),
          h("div", { style: { display: "flex", flexDirection: "column" } }, h("span", { style: { fontSize: 22, fontWeight: 600 } }, "auralab.sh"), h("span", { style: { fontSize: 16, color: "#8a8a8a" } }, `${lab.acronym.expansion}`))
        ),
        h("div", { style: { fontSize: 18, color: "#4a4a4a", display: "flex", maxWidth: 420, textAlign: "right" } }, clamp(card.foot ?? `${lab.institution.department} · ${lab.institution.name}`, 80))
      )
    )
  );
  const svg = await satori(tree as any, { width: 1200, height: 630, fonts });
  const png = new Resvg(svg, { fitTo: { mode: "width", value: 1200 } }).render().asPng();
  return new Response(new Uint8Array(png), { headers: { "Content-Type": "image/png", "Cache-Control": "public, max-age=604800" } });
};
