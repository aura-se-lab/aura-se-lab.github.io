## Efficiency & Resource-Aware Automation

As AI-assisted software engineering matures, the central question is not just *what* large models can do, but *how sustainably* we can train, adapt, and serve them. This avenue advances **cost- and energy-aware automation** by combining three complementary strategies: **Parameter-Efficient Fine-Tuning (PEFT)** to adapt models by updating only small adapters; **quantization** to reduce memory footprint and accelerate inference via lower-precision weights; and **knowledge distillation** to transfer capabilities from a large teacher to a compact student. Together, these techniques preserve task performance while dramatically lowering compute, latency, and carbon costs.

We standardize evaluation for low-precision and PEFT variants on software-engineering tasks (e.g., code summarization, review support, defect detection), reporting energy/time savings *alongside* quality metrics. This “efficiency-first” mindset aims to make **GreenAI-by-design** the default for SE automation—so teams can deploy capable assistants on modest hardware, in CI, and at the edge, without sacrificing reliability or maintainability.

Practically, we explore pipelines that (1) fine-tune with PEFT/QLoRA on project-specific data, (2) distill into smaller students for fast iteration loops, and (3) quantize for production serving. The outcome is a spectrum of models—full, adapted, distilled, and quantized—so organizations can pick the right balance of **speed, cost, and quality** for each workflow.

*Image (inline suggestion):* a side-by-side “full model → distilled student → quantized deployable” diagram, with callouts for VRAM, latency, and energy.

### Representative Publications
- Mastropaolo, Antonio, et al. *"Is Quantization a Deal-breaker? Empirical Insights from Large Code Models."* Proceedings of the 2025 IEEE International Conference on Software Maintenance and Evolution (ICSME). IEEE, 2025.  

- Afrin, Saima, et al. *"Resource-Efficient & Effective Code Summarization."* 2025 IEEE/ACM Second International Conference on AI Foundation Models and Software Engineering (FORGE). IEEE, 2025.  

- Mastropaolo, Antonio, et al. *"Optimizing Datasets for Code Summarization: Is Code-Comment Coherence Enough?"* 2025 IEEE/ACM International Conference on Program Comprehension (ICPC). IEEE, 2025.