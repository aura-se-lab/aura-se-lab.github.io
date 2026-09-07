---
title: "Two papers accepted at ICPC 2025"
date: 2025-01-12
kind: paper
publication: vitale2025optimizing
people: [aya-garryyeva]
---

Two AURA Lab papers will appear at the **33rd IEEE/ACM International Conference on Program Comprehension (ICPC 2025)**, one on each side of the lab's work — one on what training data is worth keeping, one on what a model can be made to explain.

*Optimizing Datasets for Code Summarization: Is Code-Comment Coherence Enough?* (Research Track), with Antonio Vitale, Rocco Oliveto, Massimiliano Di Penta and Simone Scalabrino, asks a question with a direct bearing on cost. Code-summarization datasets are mined from GitHub at scale and carry whatever errors and mismatches came with them. Earlier work showed that simple rule-based filtering shrinks a training set substantially without hurting the models trained on it. We push on that: can **code–comment coherence**, a specific quality attribute of a summary, identify more of what should be dropped — and does removing incoherent pairs actually improve the result rather than merely shrink the bill?

*Toward Neurosymbolic Program Comprehension* (Early Research Achievements Track), with Alejandro Velasco, [Aya Garryyeva](/people/aya-garryyeva/), David Nader Palacio and Denys Poshyvanyk, argues the case for pairing neural models with symbolic reasoning rather than scaling further, and sketches what that would mean for program comprehension specifically.

Two tracks, two problems, one underlying position: the next gains come from being more careful about data and structure, not from more parameters.
