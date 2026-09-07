---
title: Neurosymbolic Program Reasoning & Interpretability
label: Neurosymbolic Reasoning
letter: U
short: "Pairing neural code models with the symbolic machinery software engineering already has — grammars, type systems, program analysis — and recovering explanations detailed enough to check rather than merely read."
order: 2
tags: [Program analysis, Neurosymbolic, Constrained decoding, Feature attribution, Explainability]
keywords: [neurosymbolic, neuro-symbolic, symbolic, interpretab, explainab, explanation, attention, rationale, probing, program comprehension, causal, transparen, trustworth, black-box, reasoning]
featured: [mastropaolo2025path, velasco2025toward]
---

A code model that is right for the wrong reason is a liability, and today we mostly cannot tell the difference. Scale has papered over this: outputs improved while the account of *why* they improved did not. Our position is that the next gain comes from the other direction — pairing the neural model with the symbolic machinery software engineering already has, rather than asking for a larger one.

Two lines run in parallel. The first is **explanation**: recovering the rationale behind a change rather than restating the diff, and probing what a model actually attended to when it answered. The second is **grounding**: giving the model a structure it can be checked against — a grammar, a type system, a static constraint — so that an explanation becomes verifiable instead of merely plausible.

The failure modes we find are the argument for both. A multimodal model asked to read a repeated interface completes the pattern rather than reading the pixels in front of it, and sometimes identifies the anomalous element and overrides it anyway. That behaviour is invisible to a score and obvious to a symbolic check. The programme is to lift what interpretability recovers into symbolic form, so that a claim about a model is something a checker can test rather than something a reader must trust.
