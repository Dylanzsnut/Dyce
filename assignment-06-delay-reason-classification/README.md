# Assignment 06: Logistics - Delay Reason Classification using Maintenance Logs

## Overview
This module implements a hybrid two-stage Natural Language Processing (NLP) classification pipeline designed to categorize free-text delivery, maintenance, and driver incident logs into standardized operational delay categories:
1. **Stage 1 (Heuristic Pre-classifier - `initial_classify`)**: Fast keyword lookup for unambiguous logs (sub-millisecond latency, zero API cost).
2. **Stage 2 (LLM Refinement Layer - `refine_classification`)**: Context-aware verification and correction powered by Azure OpenAI (`gpt-4o-mini`, `temperature=0`) for nuanced or ambiguous logs.

---

## Directory Structure
```
assignment-06-delay-reason-classification/
├── log_classifier.py            # Complete hybrid classification pipeline
├── dataset.csv                  # 10 course mock maintenance & delivery log entries
├── classification_results.md    # Formatted Markdown report with predicted categories
├── classification_results.csv   # Structured tabular CSV export
├── prompts.md                   # Technical prompt specifications & RAG comparison
├── GENERATION_PROMPT.md         # Auto-refined meta-prompt used for construction
├── test_assignment_06.py        # Automated test suite (6 tests)
├── requirements.txt             # Dependency definitions
├── .env.example                 # Environment configuration template
└── README.md                    # Module documentation & architectural analysis
```

---

## How to Run

### 1. Installation
Install the lightweight dependencies:
```bash
pip install -r requirements.txt
```

### 2. Live Azure OpenAI Mode
Create a `.env` file from the provided template:
```bash
copy .env.example .env
```
Populate your Azure OpenAI credentials in `.env`:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-07-01-preview
```

Execute the pipeline:
```bash
python log_classifier.py
```

### 3. Offline Demonstration / Autograder Mode
To run without Azure credentials (or in automated grading sandboxes):
```bash
python log_classifier.py --demo
```

Custom CLI options:
- `--csv <path.csv>`: Pass an external CSV dataset containing a `log_entry` column.
- `--demo`: Force offline mock engine execution.

---

## Predicted Categories for Sample Log Entries

| ID | Log Entry | Heuristic Category | Final Predicted Category | Agreement |
| :--- | :--- | :--- | :--- | :--- |
| **1** | *"Driver reported heavy traffic on highway due to construction"* | Traffic | **Traffic** | Confirmed |
| **2** | *"Package not accepted, customer unavailable at given time"* | Customer Issue | **Customer Issue** | Confirmed |
| **3** | *"Vehicle engine failed during route, replacement dispatched"* | Vehicle Issue | **Vehicle Issue** | Confirmed |
| **4** | *"Unexpected rainstorm delayed loading at warehouse"* | Weather | **Weather** | Confirmed |
| **5** | *"Sorting label missing, required manual barcode scan"* | Sorting/Labeling Error | **Sorting/Labeling Error** | Confirmed |
| **6** | *"Driver took a wrong turn and had to reroute"* | Human Error | **Human Error** | Confirmed |
| **7** | *"No issue reported, arrived on time"* | Other | **Other** | Confirmed |
| **8** | *"Address was incorrect, customer unreachable"* | Customer Issue | **Customer Issue** | Confirmed |
| **9** | *"System glitch during check-in at loading dock"* | Technical System Failure | **Technical System Failure** | Confirmed |
| **10** | *"Road accident caused a long halt near delivery point"* | Traffic | **Traffic** | Confirmed |

---

## Architectural Comparison: Hybrid Heuristic + LLM vs. Retrieval-Based (RAG) Pipelines

### 1. How This Approach Differs from Retrieval-Based Pipelines
- **Retrieval-Based / RAG Classification**:
  - In a retrieval-based pipeline, each log entry is converted into a high-dimensional vector embedding (e.g. via `text-embedding-3-small`). The embedding is compared against a pre-indexed vector database containing thousands of historical classified logs using cosine similarity or k-Nearest Neighbors ($k$-NN). The retrieved examples are either voted upon or injected as few-shot context into an LLM prompt.
- **Hybrid Heuristic + LLM Refinement (This Approach)**:
  - This architecture combines deterministic rule-based keyword matching with direct generative instruction. When a high-confidence keyword is matched, the log can be classified immediately. For uncertain or complex logs, an LLM evaluates the raw text directly against the fixed category taxonomy without requiring a vector database or historical training embeddings.

### 2. Tradeoff Analysis
| Factor | Hybrid Heuristic + LLM (Current) | Retrieval-Based / RAG |
| :--- | :--- | :--- |
| **Infrastructure Overhead** | **Low**: Requires no vector database (Pinecone, Qdrant, Chroma) or embedding index pipelines. | **High**: Requires embedding models, index management, and continuous re-indexing of historical logs. |
| **Cold-Start Capability** | **Immediate**: Works instantly with zero prior historical data. | **Poor**: Requires thousands of historical labeled entries to populate vector clusters accurately. |
| **Taxonomy Adaptability** | **Instant**: Adding a new category requires editing the prompt list in one place. | **Slow**: Requires re-labeling and re-clustering historical vector databases. |
| **Semantic & Negation Handling** | **High**: LLMs understand nuance (e.g. *"Engine had no problems, but customer was absent"* correctly maps to `Customer Issue`, whereas keyword/embedding models might confuse `engine`). | **Moderate**: Short embedding vectors can be dominated by secondary keywords. |
| **Cost at Massive Scale** | Moderate (scales with LLM API token calls unless cached). | **Low**: Vector searches are sub-cent per thousand queries once embeddings are created. |

### 3. Where Each Approach Fits Best
- **Hybrid Heuristic + LLM fits best for**:
  - Rapidly evolving logistics operations where incident codes and delivery exception categories change frequently.
  - Early-to-medium scale applications (< 100,000 incident logs/day) where eliminating vector infrastructure reduces operational complexity.
  - Real-time operational incident triage where contextual understanding of driver notes is paramount.
- **Retrieval-based pipelines fit best for**:
  - Massive scale historical warehousing (> 5,000,000 logs/day) where static categories are frozen for years and sub-cent vector search cost dominates latency requirements.

---

## Automated Verification Suite
Run the verification test suite:
```bash
python test_assignment_06.py
```
**Test Coverage:**
1. Exact function signatures and constants presence (`initial_classify`, `refine_classification`, `classify_log`, `CATEGORIES`, `log_entries`).
2. Heuristic rule verification and invalid type guards.
3. Model output sanitizer resilience (stripping quotes, prefixes, conversational filler).
4. Full classification accuracy across all 10 sample log entries.
5. LLM mock correction test verifying `temperature=0` behavior.
6. Dataset CSV, Markdown results table, and prompt file presence.
