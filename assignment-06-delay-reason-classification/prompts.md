# Prompts and Classification Specifications: Assignment 06

## 1. Domain Overview
In freight and delivery logistics, driver and maintenance teams log operational delays in free-text form. This module uses a two-stage hybrid classification architecture:
1. **Stage 1 (Heuristic Pre-classifier):** Instantaneous sub-millisecond keyword matching.
2. **Stage 2 (Azure OpenAI Refinement Layer):** High-precision contextual classification for nuanced, multi-cause, or negation-heavy logs.

---

## 2. Predefined Category Schema
The pipeline maps all incident logs into one of eight standardized categories:

| Category | Typical Scope | Representative Keywords |
| :--- | :--- | :--- |
| **Traffic** | Congestion, highway bottlenecks, road accidents, detours | traffic, road accident, highway, congestion, halt |
| **Customer Issue** | Recipient unavailable, incorrect address, refusal of delivery | customer, unavailable, package not accepted, unreachable |
| **Vehicle Issue** | Mechanical breakdown, flat tires, engine failures, battery drain | engine, vehicle, flat tire, transmission, breakdown |
| **Weather** | Floods, storms, extreme snow, hurricane delays, heavy rain | rain, storm, snow, blizzard, hail, flooded |
| **Sorting/Labeling Error**| Missing barcodes, damaged packing labels, warehouse sorting bugs | label, barcode, missing scan, sorting hub |
| **Human Error** | Driver taking wrong turns, forgotten manifest, procedural misses | wrong turn, reroute, forgot keys, missed exit |
| **Technical System Failure**| Dock check-in portal down, EDI handshake failure, ERP glitches | system, glitch, server down, database timeout |
| **Other** | Normal on-time deliveries, uncategorized edge cases, force majeure | arrived on time, no issue, unknown |

---

## 3. LLM Refinement Prompt Template
```text
You are a logistics assistant. A log entry has been auto-categorized as "{initial_label}". Please confirm or correct it by choosing one of the following categories:

- Traffic
- Customer Issue
- Vehicle Issue
- Weather
- Sorting/Labeling Error
- Human Error
- Technical System Failure
- Other

Log Entry:
"""{text}"""

Return only the most appropriate category from the list.
```

---

## 4. Architectural Comparison: Hybrid Heuristic + LLM vs. Retrieval-Based (RAG)

| Dimension | Hybrid Heuristic + LLM Refinement (This Solution) | Retrieval-Based (Vector Search / RAG / kNN) |
| :--- | :--- | :--- |
| **Operational Mechanism** | Exact keyword rules act as a fast pass; LLM resolves ambiguous/unmatched entries. | Vector embedding generated via text-embedding-3-small, followed by cosine similarity search against historic labeled log vectors. |
| **Latency & Cost** | Near-zero cost for high-confidence keyword hits; LLM called only when needed or for final sanity check. | Requires embedding API call for every query + vector DB lookup (50-200ms). |
| **Cold Start / Data Needs** | Works immediately with zero historical data; taxonomy can be updated in prompt in seconds. | Requires thousands of pre-labeled historical log embeddings to achieve high classification accuracy. |
| **Contextual Nuance** | Handles negations and complex sentences easily (e.g. *"Engine fine, but driver got lost"*). | Embedding similarity can struggle with short sentences containing conflicting keywords. |
| **Best Fit** | Dynamic operational logging, evolving incident categories, rapid prototyping, and mixed simple/complex logs. | Very large-scale historical analytics (>1M logs/day) where fixed taxonomies justify pre-computed vector indices. |
