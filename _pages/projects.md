---
layout: page
title: Projects
permalink: /projects/
---

<!-- Conceptual checklist, kept concise -->
- Consolidate and harmonize content from 1_project.md → 4_project.md using 1_project.md as the style baseline.
- Produce exactly five research avenues, each as a prose section with an inline image and suggested alternates.
- Merge where overlap exists; call out standalone cases where merging would dilute focus.
- Attribute relevant **Mastropaolo et al.** contributions succinctly with links.
- Avoid “cards”; rely on paragraphs and light, responsive layout akin to the People section.
- Keep a stable, navigable structure for long-term maintenance.

<style>
/* Lightweight, self-contained layout to echo the People section’s rhythm */
.projects-grid { display: grid; gap: 2.25rem; }
.project {
  display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 1.25rem; align-items: start;
}
.project.alt { grid-template-columns: 0.9fr 1.1fr; }
.project h2 { margin-top: 0.2rem; }
.project p { margin: 0.6rem 0; line-height: 1.6; }
.project .media { text-align: center; }
.project .media img {
  max-width: 100%; height: auto; border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.08);
}
@media (max-width: 900px) {
  .project, .project.alt { grid-template-columns: 1fr; }
}
.smallnote { font-size: 0.95rem; opacity: 0.85; }
</style>

<div class="projects-grid">

<section class="project">
  <div>
    <h2>Efficiency &amp; Resource‑Aware Automation</h2>
    <p>
      As demand for AI‑assisted software engineering grows, the decisive constraint is no longer
      “can a large model do it?” but “can we afford to train, adapt, and serve it responsibly?” We align
      quantization, parameter‑efficient fine‑tuning (e.g., QLoRA), and knowledge distillation into a
      pragmatic pipeline that cuts training and inference cost while retaining task performance.
      This avenue merges efficiency‑themed material across the prior drafts into a single, coherent
      program with shared assumptions (datasets, metrics, deployment targets). <em class="smallnote">Justification:
      materials that treated cost/performance trade‑offs and model adaptation overlapped heavily,
      so they are merged here; distinct neurosymbolic or task‑aware themes are covered in separate avenues.</em>
    </p>
    <p>
      Practically, we standardize evaluation for low‑precision and PEFT variants on code intelligence tasks
      (summarization, defect detection, review support), and we report energy/time savings alongside quality
      metrics. The goal is to make “GreenAI‑by‑design” the default for SE automation, not an afterthought.
      <em>Alternate image placement:</em> a small energy‑meters strip under the opening paragraph.
    </p>

    <h3>### Mastropaolo et al Contributions</h3>
    <ul>
      <li><strong>Is Quantization a Deal‑breaker? (ICSME’25)</strong> — AWQ on CodeLlama/DeepSeekCoder; functional correctness and key quality attributes largely preserved. <a href="https://antoniomastropaolo.com">[1]</a></li>
      <li><strong>Resource‑Efficient &amp; Effective Code Summarization (FORGE’25)</strong> — QLoRA for Java/Python code→NL; evidence for GreenAI fine‑tuning in SE. <a href="https://antoniomastropaolo.com">[1]</a></li>
      <li><strong>Optimizing Datasets for Code Summarization: Is Code‑Comment Coherence Enough? (ICPC’25)</strong>. <a href="https://antoniomastropaolo.com">[1]</a></li>
    </ul>

    <h3>### Suggested Images</h3>
    <ul>
      <li>Energy‑leaf / sustainability glyph (GreenAI motif)</li>
      <li>Side‑by‑side “full‑precision vs quantized” chip pictogram</li>
      <li>Pipeline sketch: Distillation → PEFT → Quantization</li>
    </ul>
  </div>
  <div class="media">
    <img alt="GreenAI/efficiency icon" src="https://commons.wikimedia.org/wiki/Special:FilePath/WP20Symbols_environment.svg">
    <div class="smallnote">Image: Wikimedia Commons, CC0/Public Domain.</div>
  </div>
</section>

<section class="project alt">
  <div class="media">
    <img alt="Magnifying glass for explainability" src="https://commons.wikimedia.org/wiki/Special:FilePath/Magnifying_glass_icon_mgx2.svg">
    <div class="smallnote">Image: Wikimedia Commons, Public Domain.</div>
  </div>
  <div>
    <h2>Explainability &amp; Interpretability</h2>
    <p>
      Modern Large Code Models boost developer productivity yet obscure <em>why</em> a suggestion or
      fix is plausible. We pursue model‑and‑artifact‑level interpretability: probing attention/rationale
      patterns, surfacing decision paths as symbolic traces, and emitting checkable constraints alongside
      code changes. This yields <em>transparent</em> behavior that can be reviewed, debugged, and trusted.
      <em class="smallnote">Justification: the interpretability scope overlaps with neurosymbolic validation
      but remains distinct—here we focus on <em>explaining</em> model behavior, not enforcing correctness.</em>
    </p>
    <p>
      Concretely, we design “explain‑then‑edit” workflows where every automated change carries a crisp,
      human‑readable rationale, salient evidence spans, and optional counterfactuals. <em>Alternate image
      placement:</em> a small inline lens icon next to the section title.
    </p>

    <h3>### Mastropaolo et al Contributions</h3>
    <p class="smallnote">Interpretability is a cross‑cutting concern; see related entries under Neurosymbolic AI (ERA ICPC’25) for early hybrid reasoning steps.</p>

    <h3>### Suggested Images</h3>
    <ul>
      <li>“Model → rationale → diff” schematic</li>
      <li>Heatmap over a code snippet (attention/provenance)</li>
      <li>Flowchart: evidence → hypothesis → explanation</li>
    </ul>
  </div>
</section>

<section class="project">
  <div>
    <h2>Neurosymbolic AI for Software Engineering</h2>
    <p>
      We integrate LLM strengths (patterning, synthesis) with symbolic engines (program analysis,
      constraint solving) so that generated artifacts are not only useful but <em>verifiably</em> correct.
      For example, a suggested fix is accompanied by static checks or property‑based tests the system
      itself generates and runs. <em class="smallnote">Justification: prior neurosymbolic discussions were
      distinct from efficiency/interpretability; keeping this avenue standalone avoids diluting either goal.</em>
    </p>
    <p>
      The research thrust: define hybrid pipelines where the LLM proposes, the symbolic layer verifies,
      and discrepancies feed back as counterexamples to refine the next proposal. <em>Alternate image placement:</em>
      a thin validator badge under the closing paragraph.
    </p>

    <h3>### Mastropaolo et al Contributions</h3>
    <ul>
      <li><strong>Toward Neurosymbolic Program Comprehension (ICPC’25 ERA)</strong> — early results and vision for hybrid reasoning over code. <a href="https://antoniomastropaolo.com">[1]</a></li>
      <li><strong>A Path Less Traveled: Reimagining Software Engineering Automation via a Neurosymbolic Paradigm</strong>. <a href="https://antoniomastropaolo.com">[1]</a></li>
    </ul>

    <h3>### Suggested Images</h3>
    <ul>
      <li>Two‑lane pipeline: “LLM propose → Symbolic verify”</li>
      <li>Constraint‑check stamp overlay on code</li>
      <li>Hybrid block diagram integrating AST + prompts</li>
    </ul>
  </div>
  <div class="media">
    <img alt="Neurosymbolic brain motif" src="https://commons.wikimedia.org/wiki/Special:FilePath/WP20Symbols_brain.svg">
    <div class="smallnote">Image: Wikimedia Commons, CC0/Public Domain.</div>
  </div>
</section>

<section class="project alt">
  <div class="media">
    <img alt="Task and planning icon" src="https://commons.wikimedia.org/wiki/Special:FilePath/WP20Symbols_PENANDPAPER.svg">
    <div class="smallnote">Image: Wikimedia Commons, CC0/Public Domain.</div>
  </div>
  <div>
    <h2>Task‑Aware Code Automation</h2>
    <p>
      Assistants become truly useful when they are <em>repository‑aware</em> and <em>issue‑aware</em>:
      they fuse tickets, diffs, tests, logs, and CI signals into actionable next steps. We target
      automation that drafts plans, summarizes discussions, prioritizes TODOs, and proposes diffs that
      match project standards. <em class="smallnote">Justification: while adjacent to multi‑agent orchestration,
      this avenue stands alone because the unit of reasoning is the <em>software task</em> and its artifacts.</em>
    </p>
    <p>
      Our pipelines integrate VCS history, static analysis, and feedback loops to keep suggestions fresh
      as the codebase evolves. <em>Alternate image placement:</em> a small checklist graphic in the right margin.
    </p>

    <h3>### Mastropaolo et al Contributions</h3>
    <ul>
      <li><strong>Toward Automatically Completing GitHub Workflows (ICSE’24)</strong> — context (history/CI/process) improves task execution suggestions. <a href="https://scholar.google.com">[2]</a></li>
      <li><strong>Log Statements in Test Code (TOSEM’25)</strong> — benchmarks PLMs/LLMs for injecting test logs. <a href="https://antoniomastropaolo.com">[1]</a></li>
      <li><strong>Code Review Automation (TSE’25)</strong> — failure/success taxonomy; motivates task‑specialized, repository‑aware assistants. <a href="https://antoniomastropaolo.com">[1]</a></li>
    </ul>

    <h3>### Suggested Images</h3>
    <ul>
      <li>Kanban‑style “issue → plan → PR” strip</li>
      <li>Log icon + test tube (runtime signals)</li>
      <li>Diff snippet with inline policy badges</li>
    </ul>
  </div>
</section>

<section class="project">
  <div>
    <h2>Multi‑Agent LLMs for SE</h2>
    <p>
      Single‑agent copilots struggle with system‑level context. We explore multi‑agent systems with
      specialized roles (architecture, test, security, docs) that collaborate to produce coherent,
      end‑to‑end artifacts—particularly for scalable, layered documentation and cross‑module reasoning.
      <em class="smallnote">Justification: we keep this standalone; although it benefits from efficiency
      methods and feeds task‑aware workflows, the core research is agent coordination and robustness.</em>
    </p>
    <p>
      Key open problems include cost‑aware coordination, consistency guarantees across agents, and
      synchronizing partial context at different abstraction levels. <em>Alternate image placement:</em>
      a small “handshake” icon after the first sentence.
    </p>

    <h3>### Mastropaolo et al Contributions</h3>
    <p class="smallnote">Multi‑agent orchestration builds on the other avenues; see efficiency (for budgeted collaboration) and task‑aware automation (for repository grounding).</p>

    <h3>### Suggested Images</h3>
    <ul>
      <li>“Specialist agents around a repo” ring diagram</li>
      <li>Swimlanes: design ↔ code ↔ test ↔ docs</li>
      <li>Message‑passing sketch with checkpoints</li>
    </ul>
  </div>
  <div class="media">
    <img alt="Collaboration motif" src="https://commons.wikimedia.org/wiki/Special:FilePath/Adapted_Wikipedia20symbols_collaboration_w.svg">
    <div class="smallnote">Image: Wikimedia Commons, CC0/Public Domain.</div>
  </div>
</section>

</div>

<!-- Footnotes used for contribution links -->
[1]: https://antoniomastropaolo.com/
[2]: https://scholar.google.com/