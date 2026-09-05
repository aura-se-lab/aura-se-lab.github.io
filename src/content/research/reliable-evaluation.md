---
title: Reliability, Causality & Honest Evaluation
letter: R
short: Causal reasoning and counterfactual analysis to understand cause-and-effect in software systems — and evaluation methodologies (including LLM-as-a-Judge) that measure what matters, not what's easy.
order: 3
tags: [Causal inference, Counterfactuals, LLM-as-Judge, Robustness, Reproducibility, Benchmarks]
keywords: [evaluation, benchmark, llm-as-a-judge, judge, reliab, robust, counterfactual, causal, reproducib, code-comment coherence, coherence, metric, human study, empirical study, quality]
featured: [vitale2025optimizing, 10.1145/3709360]
---

Fluency is not correctness. As AI-generated code and documentation flood real projects, the field needs evaluation methodologies that distinguish models that are *actually right* from models that are merely *plausible*. This thread studies how we measure AI for software engineering — the datasets we train and test on, the metrics we trust, and the human and automated judges we rely on.

We investigate the quality of the data itself (for example, whether code–comment coherence is a useful lens for optimizing code-summarization datasets), the validity of automatic metrics against human judgment, and the emerging practice of **LLM-as-a-Judge** evaluation — where it works, where it is systematically biased, and how to calibrate it. We complement this with **causal and counterfactual analysis** to understand *why* a model behaves the way it does, rather than only *whether* it passes a test.

The goal is honest evaluation as a first-class research output: reproducible artifacts, transparent protocols, and results that hold up when someone else runs them.
