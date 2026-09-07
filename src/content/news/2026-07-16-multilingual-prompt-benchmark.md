---
title: "A curated benchmark for code generation from multilingual prompts"
date: 2026-07-16
kind: paper
publication: afrin2026large
people: [saima-afrin]
pinned: true
---

*Large Language Models for Code Generation from Multilingual Prompts: A Curated Benchmark and a Study on Code Quality* — led by [Saima Afrin](/people/saima-afrin/), with Alessandro Midolo, Camilo Escobar-Velásquez, Mario Linares-Vásquez, Weiyuan Ding, Bowen Xu, Massimiliano Di Penta and Antonio Mastropaolo — is on [arXiv](https://arxiv.org/abs/2607.14816).

Benchmarks for code generation are written in English, and so most of what we know about these models assumes an English prompt. The paper builds a **curated multilingual benchmark** and asks the obvious follow-up: does the language you write the prompt in change the code you get back?

Two findings stand out. **English prompts do not consistently produce the best result** — neither for functional correctness nor for code quality. And the effect is not a single language penalty: it depends on the **programming language and the model together**, so a prompt language that helps in one pairing hurts in another. The generated code also frequently carries quality issues that a correctness-only evaluation never sees.
