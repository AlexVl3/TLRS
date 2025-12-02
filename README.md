# TLRS — Title-and-List Retrieval System
**A Symbolic Memory Layer for Efficient, Explainable LLM Agents**  
Author: AlexVl3  
First public disclosure: December 02, 2025

### Abstract
TLRS is a lightweight symbolic memory system that indexes long-term agent memory using **human-readable titles** and **keyword lists** as primary retrieval keys. It delivers precise recall with 40–120 tokens vs. 400–2000+ for vector RAG, while staying fully explainable.

### Core Components
- Symbolic Title → primary key (e.g. `uk_dividend_tax_2025`)
- Keyword List → 5–15 tokens for disambiguation
- 1–3 sentence Summary → semantic preview
- Optional Full Content → lazy-loaded
- Metadata (timestamp, source, etc.)

### Advantages (local 2025 benchmarks)
| Metric                  | Vector RAG | MemGPT | TLRS     |
|-------------------------|------------|--------|----------|
| Tokens per recall       | 400–2000+  | 150–800| 40–120   |
| Precision on named topics| ~75 %     | ~85 %  | 94–98 %  |
| Explainability          | Low        | Medium | High     |

MIT licensed · Works with LangGraph, CrewAI, Ollama, or any LLM today.
