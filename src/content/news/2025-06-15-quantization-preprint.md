---
title: "\"Is Quantization a Deal-breaker?\" now on arXiv"
date: 2025-06-15
kind: paper
publication: afrin2025quantization
people: [saima-afrin]
---

Our paper *Is Quantization a Deal-breaker? Empirical Insights from Large Code Models* — by [Saima Afrin](/people/saima-afrin/), Bowen Xu and Antonio Mastropaolo — is now available on [arXiv](https://arxiv.org/abs/2507.09665). It was subsequently accepted at **ICSME 2025**.

Quantization reduces a model's parameter precision — 16 bit down to 4, say — and with it the memory and compute a deployment needs, along with the carbon that follows. Recent work had established it as promising for large code models specifically. What that work had not established is what it costs, because it looked almost exclusively at whether the generated code still passes its tests.

Functional correctness is not the whole of code quality, and it is arguably not the part a maintainer cares about most. This paper asks the rest of the question: under quantization, what happens to **reliability, maintainability and security** — the static attributes developers actually read a diff for?

The answer is more reassuring than the title suggests. Quantized code models pass test cases at rates comparable to their full-precision counterparts, and they preserve the qualitative attributes and static features developers look for, maintainability and structural complexity among them. Quantization survives the harder test, not just the easy one — which makes it a genuine option for deployment rather than a compromise to apologise for.
