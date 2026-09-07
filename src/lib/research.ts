/**
 * Shared data for the research-page design studies. Everything here is read
 * from the real record — no direction gets a claim the papers do not support.
 */
import { getCollection } from "astro:content";
import { publications, isReviewed, venueLabel, type Publication } from "@/lib/pubs";

export interface Direction {
  id: string;
  letter: string;
  title: string;
  short: string;
  tags: string[];
  order: number;
  papers: Publication[];
  reviewed: Publication[];
  venues: string[];
  span: string;
  /** The question the direction is trying to answer. */
  q: string;
  /** Where the answer stands today, in one sentence. */
  a: string;
}

const QA: Record<string, { q: string; a: string }> = {
  "efficient-models": {
    q: "How small can a code model get before it stops being right?",
    a: "Quantization and parameter-efficient tuning hold functional correctness far further than expected — but code quality degrades before accuracy does, and the two are usually measured as one.",
  },
  "neurosymbolic-interpretability": {
    q: "Can we read what a code model is doing, rather than only what it emits?",
    a: "Grammars, type systems and program analysis give a model structure to be checked against; feature-level explanations turn token probabilities into something a developer can argue with.",
  },
  "reliable-evaluation": {
    q: "When a benchmark says a model is better, is it?",
    a: "Often not. Scores move with prompt language, quantization, dataset provenance and the judge itself — so we build the counterfactuals and causal analyses that separate the effect from the setup.",
  },
  "agents-lifecycle": {
    q: "What can an agent actually be trusted to finish on its own?",
    a: "Task-aware automation beats one-size-fits-all assistance across triage, review, documentation and test generation — measured end to end rather than at a single step.",
  },
};

export async function directions(): Promise<Direction[]> {
  const threads = (await getCollection("research")).sort((a, b) => a.data.order - b.data.order);
  return threads.map((t) => {
    const papers = publications
      .filter((p) => p.threads?.includes(t.id))
      .sort((a, b) => b.year - a.year || (b.citations?.count ?? 0) - (a.citations?.count ?? 0));
    const reviewed = papers.filter((p) => isReviewed(p));
    const years = [...new Set(papers.map((p) => p.year))].sort();
    return {
      id: t.id,
      letter: t.data.letter,
      title: t.data.title,
      short: t.data.short,
      tags: t.data.tags ?? [],
      order: t.data.order,
      papers,
      reviewed,
      venues: [...new Set(reviewed.map((p) => venueLabel(p)).filter((v) => v && v !== "—"))],
      span: years.length ? (years[0] === years.at(-1) ? String(years[0]) : `${years[0]}–${years.at(-1)}`) : "",
      ...QA[t.id],
    };
  });
}
