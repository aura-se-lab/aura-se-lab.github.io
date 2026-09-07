---
title: "Khai's paper on multimodal pattern bias accepted at ASE 2026"
date: 2026-08-20
kind: paper
publication: nguyen2026pattern
people: [khai-nguyen-nguyen]
pinned: true
---

*Pattern over Pixels: Measuring Pattern Completion Bias in Multimodal Code Generation* — by [Khai-Nguyen Nguyen](/people/khai-nguyen-nguyen/), Oscar Chaparro and Antonio Mastropaolo — has been accepted at **ASE 2026**, the IEEE/ACM International Conference on Automated Software Engineering.

Multimodal models are increasingly asked to turn a screenshot of a page into the front-end code behind it. The paper asks what happens when the page contains a **repeated UI pattern and one element breaks it** — a single card with a different width, one label at a different font size. Does the model read the pixels, or does it complete the pattern?

It introduces the first benchmark for that failure: starting from 30 webpages curated out of Design2Code, one localised element in a repeated pattern is perturbed and the model has to recover the masked width or font-size value from the screenshot and the surrounding HTML. **1,440 evaluated screenshots**, structural and text-style patterns, with and without noise overlaid.

Five frontier multimodal models are all strongly biased toward the repeated baseline. Mean bias reaches **69.78% on card-width perturbations and 80.22% on text font-size**, where mean accuracy is only 21.17% and 7.89%. More reasoning effort correlates with less bias — but the qualitative evidence shows models that identify the anomalous element and override it anyway with the pattern-consistent answer.
