
<h1><b><em>Efficiency &amp; Resource‑Aware Automation</em></b></h1>

------------------

As demand for AI‑assisted software engineering grows, the decisive constraint is no longer
“can a large model do it?” but “can we afford to train, adapt, and serve it responsibly?” We align
quantization, parameter‑efficient fine‑tuning (e.g., QLoRA), and knowledge distillation into a
pragmatic pipeline that cuts training and inference cost while retaining task performance.
This avenue merges efficiency‑themed material across the prior drafts into a single, coherent
program with shared assumptions (datasets, metrics, deployment targets). <em class="smallnote">Justification:
materials that treated cost/performance trade‑offs and model adaptation overlapped heavily,
so they are merged here; distinct neurosymbolic or task‑aware themes are covered in separate avenues.</em>
</p>

<p>
    Practically, we standardize evaluation for low‑precision and PEFT variants on code intelligence tasks
    (summarization, defect detection, review support), and we report energy/time savings alongside quality
    metrics. The goal is to make “GreenAI‑by‑design” the default for SE automation, not an afterthought.
    <em>Alternate image placement:</em> a small energy‑meters strip under the opening paragraph.
</p>

<p>
    <strong>Representative publications:</strong>
    <ul class="card-text font-weight-light list-group list-group-flush">
    <li class="list-group-item">
        <strong>Is Quantization a Deal-breaker? (ICSME ’25)</strong> — AWQ on CodeLlama/DeepSeekCoder; functional correctness and key quality attributes largely preserved. <a href="https://antoniomastropaolo.com">[1]</a>
    </li>
    <li class="list-group-item">
        <strong>Resource-Efficient &amp; Effective Code Summarization (FORGE ’25)</strong> — QLoRA for Java/Python code→NL; evidence toward greener fine-tuning in SE. <a href="https://antoniomastropaolo.com">[1]</a>
    </li>
    <li class="list-group-item">
        <strong>Optimizing Datasets for Code Summarization: Is Code-Comment Coherence Enough? (ICPC ’25)</strong> — study on dataset design and coherence signals for code→NL quality. <a href="https://antoniomastropaolo.com">[1]</a>
    </li>
    </ul>
</p>











title: Advancing Efficient and Sustainable Software Engineering Automation via, Quantization, Knowledge Distillation and PEFT
img: assets/img/sustainability/main.png
importance: 1
category: work
related_publications: false
---

As the demand for automated solutions in software engineering continues to rise, the efficiency of training and deploying large language models (LLMs) becomes a critical concern. Efficient software engineering automation aims to tackle this challenge by adopting techniques that optimize resource utilization while preserving high performance.

Parameter-Efficient Fine-Tuning (PEFT) allows large models to be adapted to new tasks by updating only a small portion of their parameters, significantly lowering computational overhead. Quantization reduces model size and accelerates inference by decreasing numerical precision, all while maintaining acceptable levels of accuracy. Knowledge distillation transfers the capabilities of a large model into a smaller, faster one, preserving much of the original performance at a fraction of the computational cost.

Our ongoing research investigates the use and combination of these methods to develop efficient, cost-effective, and scalable approaches for automating software engineering tasks—advancing practical, high-performance AI-driven development workflows.

---

<div class="row">
    <div class="col-sm mt-9 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/sustainability/cost-llm.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>