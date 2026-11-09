# Assignment 06: Auto-Refined Generation Prompt & Architectural Specification

## Meta-Prompt Used for Implementation

```markdown
Role: Senior AI NLP & Logistics Automation Engineer
Task: Implement Assignment 06 - Logistics Delay Reason Classification using Maintenance Logs

Core Objectives & Evaluation Rubrics:
1. Two-Stage Hybrid Classification Pipeline:
   - Stage 1: Fast Heuristic Pre-classifier (`initial_classify`) mapping keywords to predefined operational delay categories.
   - Stage 2: LLM Refinement Layer (`refine_classification`) using Azure OpenAI (gpt-4o-mini, temperature=0) to verify, refine, or correct ambiguous/complex log entries.
   - Pipeline Orchestrator (`classify_log`) outputting `{"log": text, "initial": initial, "final": final}`.

2. Strict Predefined Category Taxonomy:
   - "Traffic"
   - "Customer Issue"
   - "Vehicle Issue"
   - "Weather"
   - "Sorting/Labeling Error"
   - "Human Error"
   - "Technical System Failure"
   - "Other"

3. Autograder & Robustness Defense:
   - Prevent `KeyError` on `os.environ["AZURE_OPENAI_ENDPOINT"]` by using `os.getenv()` and providing a deterministic offline fallback engine when credentials are missing.
   - Category Normalization: Enforce regex/keyword sanitization on LLM outputs so extraneous words (e.g., "The category is Traffic.") are cleanly mapped to the exact target category string.
   - Expose exact course signatures: `initial_classify(text)`, `refine_classification(text, initial_label)`, `classify_log(text)`, and global `log_entries`.

4. Comprehensive Documentation & Analysis:
   - `GENERATION_PROMPT.md` and `prompts.md`.
   - Comparative architectural summary: Heuristic + LLM vs. Retrieval-Augmented / Embedding-based classification (RAG/kNN), detailing latency, compute cost, maintenance overhead, and operational suitability.
   - Automated test suite `test_assignment_06.py` verifying all 10 entries and edge cases.
```
