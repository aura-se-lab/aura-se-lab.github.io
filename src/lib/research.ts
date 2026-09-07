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
    a: "Smaller than the field feared. Quantized code models pass tests at rates comparable to full precision, keep the maintainability and structural properties developers look for, and in our robustness study stood up to adversarial prompts better than their full-precision counterparts. The cost is real but it sits elsewhere — in which compression method you choose, and in what a pass@k number never showed you.",
  },
  "neurosymbolic-interpretability": {
    q: "Can we read what a code model is doing, rather than only what it emits?",
    a: "Only partly, and the gap is the work. Attention traces and rationale extraction tell us something about a decision, but not enough to act on. The programme is to lift what interpretability recovers into symbolic form — grammars, types, static constraints — so a claim about a model becomes something a checker can test rather than something a reader must trust.",
  },
  "reliable-evaluation": {
    q: "When a benchmark says a model is better, is it?",
    a: "Often not. Scores move with things that have nothing to do with ability — the language the prompt is written in, the system prompt around it, the precision it was served at, how the dataset was built, and the judge doing the scoring. The work is separating the effect from the setup, and publishing the infrastructure that lets someone else check.",
  },
  "agents-lifecycle": {
    q: "What can an agent actually be trusted to finish on its own?",
    a: "Less than the demos suggest. The record here is mostly empirical groundwork — what developers admit to using generative AI for, how the models and datasets underneath are documented, how much a task's framing moves the output. The agentic work builds on that, and we would rather say so than claim it early.",
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
