---
title: Reliability, Causality & Honest Evaluation
label: Reliability & Evaluation
letter: R
short: "Evaluation that survives someone else running it: causal and counterfactual analysis, calibrated LLM-as-a-Judge, and benchmarks built so a score reflects the model rather than the setup around it."
order: 3
tags: [Causal inference, Counterfactuals, LLM-as-Judge, Robustness, Reproducibility, Benchmarks]
keywords: [evaluation, benchmark, llm-as-a-judge, judge, reliab, robust, counterfactual, causal, reproducib, code-comment coherence, coherence, metric, human study, empirical study, quality]
featured: [vitale2025optimizing, 10.1145/3709360]
---

Fluency is not correctness, and a benchmark number is not a finding. As generated code and documentation reach real projects, the field's measurement apparatus is carrying more weight than it was built for, and it shows.

We study where it gives. An LLM judge agrees with human raters in some regimes and is systematically off in others, and knowing which is which is a prerequisite for using one. A curated multilingual benchmark shows generation quality shifting with the language of the prompt alone. Quantization moves scores in ways a deployment decision needs to know about. The system prompt wrapped around a request moves them too. And dataset construction choices — code–comment coherence among them — propagate straight into the results they are supposed to be neutral about.

Underneath is a methodological commitment: **causal and counterfactual analysis**, to ask why a model behaves as it does rather than only whether it passed. And an operational one — benchmarking infrastructure, protocols and artifacts released so that a result survives contact with someone else's machine.
