import raw from "@/data/publications.json";
import metricsRaw from "@/data/metrics.json";

export type PubType = "journal" | "conference" | "workshop" | "magazine" | "preprint" | "thesis" | "book" | "other";
export type PubStatus = "published" | "accepted" | "preprint";

export interface PubAuthor {
  name: string;
  member?: string;
}
export interface Publication {
  key: string;
  title: string;
  authors: PubAuthor[];
  year: number;
  month?: number;
  date?: string;
  type: PubType;
  status: PubStatus;
  venue?: string;
  venue_raw?: string;
  venue_info: { key: string; name: string; type: string; url?: string | null; rank?: string | null };
  volume?: string;
  number?: string;
  pages?: string;
  publisher?: string;
  doi?: string;
  arxiv?: string;
  url?: string;
  pdf?: string;
  code?: string;
  data?: string;
  slides?: string;
  video?: string;
  abstract?: string;
  keywords?: string[];
  threads?: string[];
  selected: boolean;
  award?: string;
  note?: string;
  citations?: { count?: number; by_source?: Record<string, number> };
  sources?: Record<string, string>;
  bibtex: string;
}

export interface Metrics {
  updated: string;
  total: number;
  reviewed: number;
  by_year: Record<string, number>;
  by_type: Record<string, number>;
  citations: number;
  venues: string[];
  members_current: number;
  phd_current: number;
  scholar?: { citedby?: number; hindex?: number; i10index?: number } | null;
}

export const publications = raw as unknown as Publication[];
export const metrics = metricsRaw as Metrics;

export const REVIEWED: PubType[] = ["journal", "conference", "workshop"];
export const isReviewed = (p: Publication) => REVIEWED.includes(p.type);

/** "Reviewed" (journal/conference/workshop), "magazine", or "preprint" — the three tabs on the publications page. */
export const bucketOf = (p: Publication): "reviewed" | "magazine" | "preprint" | "other" =>
  isReviewed(p) ? "reviewed" : p.type === "magazine" ? "magazine" : p.type === "preprint" ? "preprint" : "other";

export const selectedPubs = (n = 6) => {
  const sel = publications.filter((p) => p.selected);
  const sorted = sel.sort((a, b) => (b.date ?? String(b.year)).localeCompare(a.date ?? String(a.year)));
  if (sorted.length >= n) return sorted.slice(0, n);
  // top up with the most-cited recent reviewed papers
  const extra = publications
    .filter((p) => !p.selected && isReviewed(p))
    .sort((a, b) => (b.citations?.count ?? 0) - (a.citations?.count ?? 0));
  return [...sorted, ...extra].slice(0, n);
};

export const pubsByMember = (slug: string) => publications.filter((p) => p.authors.some((a) => a.member === slug));
export const pubsByThread = (slug: string) => publications.filter((p) => p.threads?.includes(slug));
export const pubByKey = (key: string) => publications.find((p) => p.key === key);

export const groupByYear = (pubs: Publication[]) => {
  const m = new Map<number, Publication[]>();
  for (const p of pubs) {
    if (!m.has(p.year)) m.set(p.year, []);
    m.get(p.year)!.push(p);
  }
  return [...m.entries()].sort((a, b) => b[0] - a[0]);
};

/** "A. Mastropaolo" style short author names. */
export function shortName(full: string): string {
  const { given, family } = splitName(full);
  const initials = given
    .split(/\s+/)
    .filter(Boolean)
    .map((g) => g.split("-").map((p) => p[0] + ".").join("-"))
    .join(" ");
  return `${initials} ${family}`.trim();
}

export function splitName(full: string): { given: string; family: string } {
  const name = full.trim().replace(/\s+/g, " ");
  if (name.includes(",")) {
    const [family, given] = name.split(",", 2).map((s) => s.trim());
    return { given: given ?? "", family };
  }
  const parts = name.split(" ");
  if (parts.length === 1) return { given: "", family: parts[0] };
  const particles = new Set(["di", "de", "del", "della", "van", "von", "der", "da", "dos", "la", "le"]);
  let i = parts.length - 1;
  while (i - 1 > 0 && particles.has(parts[i - 1].toLowerCase())) i--;
  return { given: parts.slice(0, i).join(" "), family: parts.slice(i).join(" ") };
}

export function displayName(full: string): string {
  const { given, family } = splitName(full);
  return given ? `${given} ${family}` : family;
}

/** Primary landing link for a paper: DOI → arXiv → url. */
export function primaryLink(p: Publication): string | undefined {
  if (p.doi) return `https://doi.org/${p.doi}`;
  if (p.arxiv) return `https://arxiv.org/abs/${p.arxiv}`;
  return p.url;
}

export function pubLinks(p: Publication): { label: string; href: string; kind: string }[] {
  const links: { label: string; href: string; kind: string }[] = [];
  if (p.doi) links.push({ label: "DOI", href: `https://doi.org/${p.doi}`, kind: "doi" });
  if (p.arxiv) links.push({ label: "arXiv", href: `https://arxiv.org/abs/${p.arxiv}`, kind: "arxiv" });
  if (p.pdf && !(p.arxiv && p.pdf.includes(p.arxiv))) links.push({ label: "PDF", href: p.pdf, kind: "pdf" });
  else if (p.arxiv) links.push({ label: "PDF", href: `https://arxiv.org/pdf/${p.arxiv}`, kind: "pdf" });
  if (p.code) links.push({ label: "Code", href: p.code, kind: "code" });
  if (p.data) links.push({ label: "Data", href: p.data, kind: "data" });
  if (p.slides) links.push({ label: "Slides", href: p.slides, kind: "slides" });
  if (p.video) links.push({ label: "Video", href: p.video, kind: "video" });
  if (p.url && !p.doi && !p.arxiv) links.push({ label: "Link", href: p.url, kind: "url" });
  return links;
}

export function venueLabel(p: Publication): string {
  return p.venue ?? p.venue_info?.key ?? (p.type === "preprint" ? "arXiv" : "—");
}

export const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
export function pubDateLabel(p: Publication): string {
  return p.month ? `${MONTHS[p.month - 1]} ${p.year}` : String(p.year);
}
