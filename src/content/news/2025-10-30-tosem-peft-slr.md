---
title: "PEFT systematic literature review accepted at TOSEM"
date: 2025-10-30
kind: paper
publication: afrin2025systematic
people: [saima-afrin, md-zahidul-haque-alvi]
---

*A Systematic Literature Review of Parameter-Efficient Fine-Tuning for Large Code Models* has been accepted for publication in **ACM Transactions on Software Engineering and Methodology (TOSEM)**. The preprint is on [arXiv](https://arxiv.org/abs/2504.21569). A masterful job by Ph.D. students [Saima Afrin](/people/saima-afrin/) and [Alvi](/people/md-zahidul-haque-alvi/) — well done.

Large language models for code have automated a great deal — generation, defect detection, repair — and have made themselves expensive to train and adapt while doing it. That expense is the obstacle to adoption anywhere the hardware budget is finite, which is most places. **Parameter-Efficient Fine-Tuning (PEFT)** is the field's answer: adapt a large model by updating a small subset of its parameters instead of all of them.

The literature on this has grown quickly and unevenly, across different techniques, architectures and tasks, which makes it hard to say what has actually been established and what has merely been tried. This review examines that body of work across the range of software engineering tasks it has been applied to, and how the methods are used to optimize different deep-learning architectures.

Its central contribution is a **taxonomy** organising PEFT usage by task type, separating generative from non-generative settings — a map of what is known, intended to be useful both to the next study and to a team deciding what to deploy.
