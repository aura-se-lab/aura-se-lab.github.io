import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

/**
 * People — one Markdown file per member in src/content/people/.
 * The frontmatter is the single source of truth for the publications pipeline
 * (scripts/pubs reads the same files to learn each member's author IDs).
 */
const people = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/people" }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      /** Short display name used in author lists, e.g. "S. Afrin" is derived; this is the full name */
      role: z.enum([
        "director",
        "phd",
        "msc",
        "undergrad",
        "postdoc",
        "visitor",
        "alumni",
        "collaborator",
      ]),
      title: z.string().optional(), // e.g. "Ph.D. Student", "Assistant Professor"
      status: z.enum(["current", "alumni", "external"]).default("current"),
      order: z.number().default(100),
      photo: image().optional(),
      joined: z.string().optional(), // ISO date or YYYY-MM
      left: z.string().optional(),
      /** Where they went after the lab (alumni) */
      next: z.string().optional(),
      coadvised: z.string().optional(),
      interests: z.array(z.string()).default([]),
      /** Research thread slugs this person mainly works on */
      threads: z.array(z.string()).default([]),
      email: z.string().optional(),
      links: z
        .object({
          website: z.string().url().optional(),
          scholar: z.string().url().optional(),
          github: z.string().url().optional(),
          linkedin: z.string().url().optional(),
          x: z.string().url().optional(),
          bluesky: z.string().url().optional(),
          orcid: z.string().url().optional(),
          dblp: z.string().url().optional(),
        })
        .default({}),
      /**
       * Author identifiers used by scripts/pubs to collect this person's papers.
       * `since` limits which of their papers count as lab output (defaults to `joined`).
       */
      ids: z
        .object({
          dblp: z.string().optional(), // DBLP pid, e.g. "132/9621"
          scholar: z.string().optional(), // Google Scholar user id
          semanticscholar: z.union([z.string(), z.array(z.string())]).optional(),
          openalex: z.string().optional(), // e.g. "A5012345678"
          orcid: z.string().optional(),
          /** Set true to also search arXiv by this member's name */
          arxiv: z.boolean().optional(),
          /** Extra name spellings to match in author lists */
          aliases: z.array(z.string()).default([]),
        })
        .default({ aliases: [] }),
      awards: z
        .array(z.object({ title: z.string(), year: z.number().optional(), note: z.string().optional() }))
        .default([]),
    }),
});

/** News — short announcements. Drafts are written by the pubs bot and hidden until draft: false. */
const news = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/news" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    kind: z
      .enum(["paper", "award", "grant", "people", "talk", "service", "event", "misc"])
      .default("misc"),
    /** Publication key this item is about (links the card to the paper page) */
    publication: z.string().optional(),
    /** Person slugs mentioned (links to profiles) */
    people: z.array(z.string()).default([]),
    /** Pinned items float to the top of the homepage feed */
    pinned: z.boolean().default(false),
    draft: z.boolean().default(false),
    /** Set true to have the social workflow post this item once it lands on main */
    social: z.boolean().default(false),
    /** External link the card points to (optional) */
    link: z.string().url().optional(),
  }),
});

/** Research threads — the A·U·R·A structure. Keywords feed the pipeline's area classifier. */
const research = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/research" }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      letter: z.string().max(2), // "A", "U", "R", "A"
      short: z.string(), // one-line summary
      order: z.number(),
      tags: z.array(z.string()).default([]),
      /** Lower-cased keywords used to auto-assign publications to this thread */
      keywords: z.array(z.string()).default([]),
      image: image().optional(),
      /** Publication keys to always show first on this thread page */
      featured: z.array(z.string()).default([]),
    }),
});

export const collections = { people, news, research };
