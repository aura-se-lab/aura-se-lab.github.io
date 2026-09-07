---
title: Resource-Efficient Foundation Models for Code
label: Resource-Efficient Models
letter: A
short: "Sustainable and efficient code intelligence: quantization, parameter-efficient fine-tuning, and training-data reduction that make foundation models efficient enough to run at developer scale — measured on energy and latency as well as on whether the code they produce is still any good."
order: 1
tags: [Quantization, PEFT, LoRA / QLoRA, Distillation, Pruning, Green AI]
keywords: [quantiz, parameter-efficient, peft, lora, qlora, distill, prun, green ai, energy, resource-efficient, efficient, compression, sustainab, carbon, training data, elite samples, selective data, dataset]
featured: [afrin2025quantization, afrin2025systematic, afrin2025resource]
---

The useful question is no longer what a large model can do for software engineering, but what it costs to keep one running and what is lost on the way down. This avenue is about making code intelligence **sustainable and efficient** at once — the two are not the same claim, and a result that improves one while quietly spending the other is not a result. We work the levers that make a code model affordable — **quantization**, **parameter-efficient fine-tuning**, and reducing what the model is trained on — and we measure what each one takes with it.

The answer so far has been less alarming than the field expected. Quantized code models generate code that passes tests at rates comparable to full precision, and they hold onto the qualitative attributes developers actually look at — maintainability, structural complexity, security. Tested against adversarial prompts and architectural noise, they were often *more* robust than the models they were compressed from, not less. Multi-task QLoRA matches or beats both single-task adaptation and multi-task full fine-tuning at 1.5B, 3B and 7B. And in code summarization, which tokens you keep turns out to matter more than how many you remove.

Where the cost hides is in the choices around the compression rather than in the compression itself: six post-training quantization methods do not behave alike, and accuracy and energy have to be read on one scale rather than reported in separate papers. Which is why every study here puts energy and latency next to quality, and code quality next to correctness. Efficiency is not a footnote to the result; it is half of it.
