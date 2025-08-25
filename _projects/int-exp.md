## Promoting Neurosymbolic AI for SE via Explainability and Interpretability

Large Code Models (LCMs) have reshaped software engineering automation by leveraging two primary drivers: abundant code-rich datasets and increasingly large neural architectures. Together, these forces enable models to internalize programming idioms, structural patterns, and cross-file relationships at scale—unlocking forms of assistance once thought unattainable. Tools such as GitHub Copilot and ChatGPT illustrate this transformation, acting as “artificial collaborators” that support developers across the lifecycle.

Yet, these gains come with clear trade-offs. Training and maintaining larger models demands immense computational resources, while their opaque decision processes introduce concerns about bias, trust, and accountability. With data availability plateauing and diminishing returns from sheer scale, continued progress requires a different path forward.

Our approach promotes **neurosymbolic AI for software engineering** by advancing explainability and interpretability as core enablers. Interpretability methods—such as attention analysis, rationale extraction, and behavior probing—allow us to uncover patterns and decision traces from neural code models. These insights can then be elevated into symbolic representations that serve as the reasoning layer of neurosymbolic systems. In doing so, we preserve the adaptability of LLMs while adding a fast, deterministic, and verifiable component that strengthens reliability and trust.

Practically, we develop **explain-then-edit** workflows, where every automated change is accompanied by human-readable rationales, highlighted evidence (files, tests, diffs), and, when applicable, counterfactual examples. These explanations directly benefit developers by making model outputs reviewable and debuggable, while also enabling downstream symbolic checks (e.g., enforcing contracts or static constraints). By embedding interpretability into neurosymbolic pipelines, we aim to promote SE automation that is not only powerful but also transparent, accountable, and sustainable.

### Representative Publications

- Velasco, Alejandro, et al. *"Toward Neurosymbolic Program Comprehension."* 2025 IEEE/ACM International Conference on Program Comprehension (ICPC), Early Research Achievements Track. IEEE, 2025.  

- Mastropaolo, Antonio, et al. *"A Path Less Traveled: Reimagining Software Engineering Automation via a Neurosymbolic Paradigm."* Proceedings of the 2025 International Workshop on AI for Software Development Lifecycle (AI-SDLC). ACM, 2025.