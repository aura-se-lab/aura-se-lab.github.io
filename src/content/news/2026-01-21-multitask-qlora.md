---
title: "Multi-task QLoRA: one adapter across generation, translation and summarization"
date: 2026-01-21
kind: paper
publication: haque2026parameter
people: [md-zahidul-haque-alvi, saima-afrin]
pinned: true
---

*Parameter-Efficient Multi-Task Fine-Tuning in Code-Related Tasks* — by [Md Zahidul Haque](/people/md-zahidul-haque-alvi/), [Saima Afrin](/people/saima-afrin/) and Antonio Mastropaolo — is now on [arXiv](https://arxiv.org/abs/2601.15094).

QLoRA already makes it cheap to specialise a large code model for **one** task. What has stayed unclear is whether that still holds when a **single** model is QLoRA fine-tuned for several code-related tasks at once, and what the interaction between multi-task training and quantised low-rank adaptation does to the code that comes out.

The paper studies three representative tasks — **code generation, code translation and code summarization** — at **1.5B, 3B and 7B** parameters, measuring functional correctness with execution-based and similarity-based metrics, and pairing that with a code-quality analysis that most prior work leaves out.

Multi-task QLoRA turns out to leverage transfer learning effectively: it is competitive with, or better than, both single-task QLoRA and multi-task **full** fine-tuning at every size tested. The larger models hold a more consistent balance between correctness and quality; the smaller ones keep functionality but show more quality-related issues in what they generate.
