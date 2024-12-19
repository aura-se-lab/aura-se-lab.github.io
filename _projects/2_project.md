---
layout: page
title: Interpretability for Neurosymbolic Software Engineering
description: Decoding the Synergy of Neural and Symbolic Systems in Software Engineering
img: assets/img/interpretability/brain.png
importance: 2
category: work
giscus_comments: false
---

The recent rise of Large Code Models (LCMs) has undeniably transformed the automation of software engineering activities. Understanding the reasons behind this transformation requires focusing on two key factors: the availability of large, text-rich datasets that provide foundational knowledge for training these models, and the increasing scale of deep learning architectures, with some models now boasting trillions of parameters. Together, these advancements have not only expanded the ability of models to generalize vast amounts of programming knowledge but also enabled them to capture intricate patterns, structures, and relationships within the code. This synergy between extensive datasets and large-scale models has laid the foundation for achieving levels of automation in software engineering that were previously unimaginable.

Tools like GitHub Copilot and ChatGPT exemplify this progress, serving as “artificial collaborators” that assist developers in various phases of the software development lifecycle and enhance their understanding of code. While these advancements showcase the multifaceted potential of AI in software engineering, they also come with significant trade-offs. The increasing complexity and scale of these models demand substantial computational resources for training and maintenance. Additionally, issues such as bias, lack of trustworthiness, and limited interpretability in large deep learning models pose significant challenges, slowing further progress.

Scaling models indefinitely has often been viewed as the path to better performance. However, recent perspectives suggest that this approach may soon reach its limits, as the availability of relevant training data is expected to plateau within the coming years. This raises an important question: what if stepping back now could pave the way for greater advancements in the future? It may no longer be feasible to rely solely on scaling to drive innovation.

In response, we propose to shit the focus to the development of a new framework that combines the probabilistic capabilities of large language models with traditional symbolic reasoning. In particular, the aim is to construct the symbolic component of a neurosymbolic system using interpretability techniques applied to neural code models. This in turns, offer researcher the ability to demystify LCMs, gaining valuable insights into their internal decision-making processes and outputs. This enhanced understanding not only fosters trust but also streamlines debugging and optimization, ensuring these models are more effective and reliable.

Additionally, interpretability enables the extraction of meaningful patterns, logic, and relationships from neural models, which can be encoded as a symbolic component in the neurosymbolic system. This integration addresses the limitations of purely probabilistic approaches by introducing symbolic reasoning, which is inherently fast, deterministic, and robust. The symbolic layer complements the adaptability of neural networks with its precision and reliability, creating a balanced, high-performing hybrid system. Together, these advancements bridge the gap between machine learning and human understanding, offering scalable, efficient, and explainable AI-driven solutions tailored to the evolving needs of software engineering.

---

<div class="row">
    <div class="col-sm mt-9 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/interpretability/llm.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
