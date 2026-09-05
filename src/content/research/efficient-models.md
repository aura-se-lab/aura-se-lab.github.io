---
title: Resource-Efficient Foundation Models for Code
letter: A
short: Quantization, parameter-efficient fine-tuning, and distillation that make code-intelligence models cheap enough to deploy at developer scale — without sacrificing functional or non-functional code quality.
order: 1
tags: [Quantization, PEFT, LoRA / QLoRA, Distillation, Pruning, Green AI]
keywords: [quantiz, parameter-efficient, peft, lora, qlora, distill, prun, green ai, energy, resource-efficient, efficient, compression, sustainab, carbon, training data, elite samples, selective data, dataset]
featured: [afrin2025quantization, afrin2025systematic, afrin2025resource]
---

As AI-assisted software engineering matures, the central question is not just *what* large models can do, but *how sustainably* we can train, adapt, and serve them. This thread advances **cost- and energy-aware automation** by combining three complementary strategies: **Parameter-Efficient Fine-Tuning (PEFT)** to adapt models by updating only small adapters; **quantization** to reduce memory footprint and accelerate inference via lower-precision weights; and **knowledge distillation** to transfer capabilities from a large teacher to a compact student. Together, these techniques preserve task performance while dramatically lowering compute, latency, and carbon costs.

We standardize evaluation for low-precision and PEFT variants on software-engineering tasks (code summarization, review support, defect detection), reporting energy and time savings *alongside* quality metrics — and, crucially, alongside the **non-functional** qualities of generated code such as maintainability, complexity, and security. This "efficiency-first" mindset aims to make **Green AI by design** the default for SE automation, so teams can deploy capable assistants on modest hardware, in CI, and at the edge, without sacrificing reliability or maintainability.

Practically, we explore pipelines that (1) fine-tune with PEFT/QLoRA on project-specific data, (2) distill into smaller students for fast iteration loops, and (3) quantize for production serving. The outcome is a spectrum of models — full, adapted, distilled, and quantized — so organizations can pick the right balance of **speed, cost, and quality** for each workflow. This line of work is supported by our NSF CRII award on energy-efficient large language models for code.
