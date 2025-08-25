## Task-Aware Code Automation

AI copilots are increasingly valuable, but a one-size-fits-all model cannot cover the full spectrum of software engineering activities—coding, reviewing, debugging, documenting—each with unique goals and constraints. **Task-aware automation** addresses this gap by tailoring AI to the specific context of the developer’s work. Instead of treating all inputs equally, these systems leverage repository history, issue discussions, diffs, and runtime traces to make outputs more precise and actionable.

Domain-specialized LLMs illustrate this trend. For instance, CodeLlama and Incoder outperform generic LLMs on code benchmarks by emphasizing syntax and semantics relevant to programming. Building on this idea, task-aware assistants can adjust behavior depending on the task: adopting a conservative, test-oriented style for bug fixing; offering higher-level summaries for documentation; or suggesting creative alternatives for feature development. Our work extends this vision by fine-tuning lightweight models for targeted tasks (e.g., summarization, test generation) and coordinating them under a unified, context-sensitive framework.

The key benefit is **relevance**. An assistant aware it is reviewing code can prioritize stylistic and correctness checks, while one tasked with documentation can optimize for clarity and brevity. Our early results show that task-tuned summarization yields higher-quality results with lower compute costs. Similarly, program translation enhanced with symbolic checks maintains functional equivalence between source and target code, demonstrating how task-aware design improves reliability.

### Representative Publications
- Afrin, Saima, et al. *"Resource-Efficient & Effective Code Summarization."* 2025 IEEE/ACM Second International Conference on AI Foundation Models and Software Engineering (FORGE). IEEE, 2025.  

- Mastropaolo, Antonio, et al. *"Toward Automatically Completing GitHub Workflows."* Proceedings of the 2024 IEEE/ACM International Conference on Software Engineering (ICSE). ACM, 2024.  

### Key Contributions
- Demonstrated that **task-tailored LLMs** outperform general models on targeted SE activities such as code generation.  
- Developed a **resource-efficient summarization** approach (FORGE ’25) that reduces overhead without sacrificing quality.  
- Proposed a **blueprint for context-aware assistants**, where specialized models collaborate across coding, testing, and documentation tasks.