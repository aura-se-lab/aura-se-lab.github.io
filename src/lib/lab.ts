import { parse } from "yaml";
// YAML is inlined at build time by Vite (`?raw`), so this works in the prerender bundle too.
import labRaw from "../../data/lab.yml?raw";
import collabRaw from "../../data/collaborators.yml?raw";

export interface Funding {
  id: string;
  program: string;
  agency: string;
  award?: string;
  title: string;
  amount?: string;
  period?: string;
  role?: string;
  status: "active" | "awarded" | "completed";
  url?: string;
  summary?: string;
}

export interface Lab {
  name: string;
  short_name: string;
  acronym: { letters: string[]; expansion: string; words: string[] };
  tagline: string;
  founded: string;
  url: string;
  legacy_url?: string;
  institution: {
    name: string;
    short: string;
    department: string;
    url: string;
    address: { building: string; street: string; city: string; region: string; postal: string; country: string };
  };
  director: { slug: string; name: string; site: string };
  contact: { email: string; lab_email?: string };
  social: Record<string, string>;
  statement: string;
  brief: string[];
  funding: Funding[];
  nav: { label: string; href: string }[];
  flagship_venues: string[];
}

export interface Collaborator {
  name: string;
  affiliation?: string;
  url?: string;
  note?: string;
}

export const lab: Lab = parse(labRaw);
export const collaborators: Collaborator[] = parse(collabRaw) ?? [];

export const foundedLabel = (() => {
  const [y, m] = lab.founded.split("-").map(Number);
  const season = m && m >= 8 ? "Fall" : m && m >= 5 ? "Summer" : "Spring";
  return `${season} ${y}`;
})();
