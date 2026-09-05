---
title: Neurosymbolic Program Reasoning & Interpretability
letter: U
short: Combining neural language models with grammars, type systems, and program analysis — plus feature-level explanations that move beyond opaque token-by-token predictions toward something developers can actually read.
order: 2
tags: [Program analysis, Neurosymbolic, Constrained decoding, Feature attribution, Explainability]
keywords: [neurosymbolic, neuro-symbolic, symbolic, interpretab, explainab, explanation, attention, rationale, probing, program comprehension, causal, transparen, trustworth, black-box, reasoning]
featured: [mastropaolo2025path, velasco2025toward, mastropaolo2025code]
---

Large Code Models (LCMs) have reshaped software engineering automation by leveraging two primary drivers: abundant code-rich datasets and increasingly large neural architectures. Tools such as GitHub Copilot and ChatGPT illustrate this transformation, acting as "artificial collaborators" across the lifecycle. Yet these gains come with clear trade-offs: training and maintaining larger models demands immense computational resources, while their opaque decision processes raise concerns about bias, trust, and accountability. With data availability plateauing and diminishing returns from sheer scale, continued progress requires a different path forward.

Our approach promotes **neurosymbolic AI for software engineering** by advancing explainability and interpretability as core enablers. Interpretability methods — attention analysis, rationale extraction, behavior probing — let us uncover patterns and decision traces from neural code models. These insights can then be elevated into symbolic representations that serve as the reasoning layer of neurosymbolic systems. In doing so, we preserve the adaptability of LLMs while adding a fast, deterministic, and verifiable component that strengthens reliability and trust.

Practically, we develop **explain-then-edit** workflows, where every automated change is accompanied by human-readable rationales, highlighted evidence (files, tests, diffs), and, when applicable, counterfactual examples. These explanations make model outputs reviewable and debuggable, and enable downstream symbolic checks (e.g., enforcing contracts or static constraints). Our position papers on *Neurosymbolic Software Engineering* lay out the paradigm; our empirical work builds the first pieces of it.
