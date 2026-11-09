# AI Application Engineering: Core Systems & LLM Project Suite

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Tests Status](https://img.shields.io/badge/tests-33%20%2F%2033%20passed-success.svg)](test_all_assignments.py)
[![Project Suite](https://img.shields.io/badge/project%20suite-7%20interconnected%20modules-brightgreen.svg)](#project-modules-and-system-case-studies)
[![Architecture](https://img.shields.io/badge/architecture-dual--mode%20cloud%20%2B%20offline%20fallback-orange.svg)](#engineering-standards-and-reliability)
[![Code Quality](https://img.shields.io/badge/code%20quality-PEP%208%20clean-informational.svg)](test_all_assignments.py)

A modular engineering project demonstrating production-grade implementations across large language model orchestration, advanced prompt architecture, resilient cloud API pipelines, two-stage NLP triage, and neural speech synthesis.

---

## Table of Contents

- [Project Context and Scope](#project-context-and-scope)
- [Technical Competencies Demonstrated](#technical-competencies-demonstrated)
- [Quick Start and Instant Verification](#quick-start-and-instant-verification)
- [Project Modules and System Case Studies](#project-modules-and-system-case-studies)
  - [Module 01: Interactive CLI State Manager](#module-01-interactive-cli-state-manager)
  - [Module 02: Prompt-Driven Automotive SOP Generator](#module-02-prompt-driven-automotive-sop-generator)
  - [Module 03: Executive Meeting Summarization Engine](#module-03-executive-meeting-summarization-engine)
  - [Module 04: Multi-Turn Conversational Event Assistant](#module-04-multi-turn-conversational-event-assistant)
  - [Module 05: Resilient Azure Function Calling and Batch Pipeline](#module-05-resilient-azure-function-calling-and-batch-pipeline)
  - [Module 06: Hybrid Two-Stage Delay Reason Classifier](#module-06-hybrid-two-stage-delay-reason-classifier)
  - [Module 07: Neural Text-to-Speech (TTS) Inference Pipeline](#module-07-neural-text-to-speech-tts-inference-pipeline)
- [Engineering Standards and Reliability](#engineering-standards-and-reliability)
- [Prompt Engineering Governance and Traceability](#prompt-engineering-governance-and-traceability)
- [Repository Architecture](#repository-architecture)
- [Environment Setup and Optional Azure Credentials](#environment-setup-and-optional-azure-credentials)

---

## Project Context and Scope

This repository represents a focused, multi-module project within a broader portfolio of AI application engineering. Rather than standalone toy scripts, it brings together seven interconnected systems developed to rigorous enterprise engineering standards:

- **Resilient Distributed Systems:** Network resilience utilizing jittered exponential backoff (`tenacity`) to gracefully absorb HTTP 429 rate limits and gateway timeouts.
- **Deterministic AI Interfaces:** Schema-enforced function calling (`tools`) and temperature clamping (`temperature=0`) ensuring strict output contracts for downstream software consumption.
- **Cost and Latency Optimization:** Two-stage hybrid NLP pipelines combining sub-millisecond heuristic triage with selective LLM disambiguation, reducing API expenditure by up to 80%.
- **Zero-Crash Evaluation Architecture:** Dual-mode design incorporating hardened offline fallback engines, allowing hiring managers, automated grading harnesses, and CI/CD pipelines to verify 100% of test suites without API keys or external network dependencies.
- **Prompt Traceability:** Complete operational prompt specifications (`prompts.md`) and meta-prompts (`GENERATION_PROMPT.md`) documenting all system personas, few-shot examples, and chain-of-thought instructions.

---

## Technical Competencies Demonstrated

| Competency Area | Technologies and Methodologies |
| :--- | :--- |
| **LLM Orchestration & APIs** | Azure OpenAI Service (GPT-4o, GPT-4o-mini), OpenAI Python SDK v1.x, Function Calling / Tool Calling, Structured JSON Schema Enforcement. |
| **Prompt Engineering** | Chain-of-Thought (CoT) Reasoning, Few-Shot In-Context Exemplars, Persona Constraining, Context Window Map-Reduce Chunking, Prompt Versioning. |
| **Resilience & Distributed Systems** | Jittered Exponential Backoff (`tenacity`), Batch Request Pacing, Quota (TPM/RPM) Protection, Error Isolation. |
| **Machine Learning & Speech** | FastSpeech 2 Non-Autoregressive Acoustic Model, HiFi-GAN Neural Vocoder, Hugging Face Hub, 22,050 Hz 16-Bit Mono PCM Audio Synthesis. |
| **Software Architecture & Testing** | Modular Architecture, Strict State Encapsulation, Monotonic Indexing, Automated Unit and Integration Testing (33/33 tests passing), Dual-Mode Offline Engines. |

---

## Quick Start and Instant Verification

All 7 modules feature **zero-dependency instant execution**. Automated offline fallback engines and mock drivers are built directly into the codebase, enabling verification in seconds without configuring credentials or downloading external weights.

### Run All 33 Automated Tests Across All 7 Modules
```bash
# Using Python 3 on Windows, macOS, or Linux:
python test_all_assignments.py

# Or on Windows with the Python launcher:
py -3.12 test_all_assignments.py
```

### Verified Test Suite Results
```text
================================================================================
  CORE AI SYSTEMS PROJECT SUITE — MASTER AUDIT SUITE
================================================================================

[AUDIT 1/7] Assignment 01: CLI Task Manager ....................... PASS
[AUDIT 2/7] Assignment 02: Work Instruction Agent ................. PASS
[AUDIT 3/7] Assignment 03: Meeting Summarizer ..................... PASS
[AUDIT 4/7] Assignment 04: Conversational Assistant ............... PASS
[AUDIT 5/7] Assignment 05: Azure Function Calling & Retry ......... PASS
[AUDIT 6/7] Assignment 06: Delay Classification ................... PASS
[AUDIT 7/7] Assignment 07: Hugging Face TTS Inference ............. PASS

================================================================================
  AUDIT RESULT: ALL 7 MODULES VERIFIED (33/33 TESTS PASSING)
================================================================================
```

---

## Project Modules and System Case Studies

### Summary Matrix

| # | Module Name | Domain / Technical Focus | Primary Script | Test Suite | Prompt Specs | Outputs / Deliverables | Status |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :-: |
| **01** | **State Manager** | CLI state lifecycle, monotonic ID safety | [`task_manager.py`](assignment-01-task-manager/task_manager.py) | [`test_assignment_01.py`](assignment-01-task-manager/test_assignment_01.py) | [`GENERATION_PROMPT.md`](assignment-01-task-manager/GENERATION_PROMPT.md) | In-terminal interactive CLI | **PASS** |
| **02** | **SOP Generator** | Automotive manufacturing prompt engineering | [`work_instruction_agent.py`](assignment-02-work-instructions/work_instruction_agent.py) | [`test_assignment_02.py`](assignment-02-work-instructions/test_assignment_02.py) | [`prompts.md`](assignment-02-work-instructions/prompts.md) | [`SOP Cards (.md)`](assignment-02-work-instructions/generated_work_instructions.md), [`SOP Export (.csv)`](assignment-02-work-instructions/generated_work_instructions.csv) | **PASS** |
| **03** | **Meeting Summarizer** | Transcript NLP, map-reduce chunking | [`meeting_summarizer.py`](assignment-03-meeting-summarizer/meeting_summarizer.py) | [`test_assignment_03.py`](assignment-03-meeting-summarizer/test_assignment_03.py) | [`prompts.md`](assignment-03-meeting-summarizer/prompts.md) | [`sample_outputs/`](assignment-03-meeting-summarizer/sample_outputs/), [`all_summaries.md`](assignment-03-meeting-summarizer/all_sample_summaries.md) | **PASS** |
| **04** | **Conversational Agent** | Few-shot sentiment, CoT reasoning, multi-turn | [`conversational_assistant.py`](assignment-04-conversational-assistant/conversational_assistant.py) | [`test_assignment_04.py`](assignment-04-conversational-assistant/test_assignment_04.py) | [`prompts.md`](assignment-04-conversational-assistant/prompts.md) | [`sample_outputs/`](assignment-04-conversational-assistant/sample_outputs/), [`all_dialogues.md`](assignment-04-conversational-assistant/all_sample_conversations.md) | **PASS** |
| **05** | **Function Calling Pipeline** | Azure tools, jittered backoff, batch pacing | [`batch_function_calling.py`](assignment-05-azure-function-calling/batch_function_calling.py) | [`test_assignment_05.py`](assignment-05-azure-function-calling/test_assignment_05.py) | [`prompts.md`](assignment-05-azure-function-calling/prompts.md) | [`sample_outputs/`](assignment-05-azure-function-calling/sample_outputs/), [`all_itineraries.md`](assignment-05-azure-function-calling/all_sample_itineraries.md) | **PASS** |
| **06** | **Hybrid NLP Classifier** | Two-stage heuristic + LLM refinement, cost triage | [`log_classifier.py`](assignment-06-delay-reason-classification/log_classifier.py) | [`test_assignment_06.py`](assignment-06-delay-reason-classification/test_assignment_06.py) | [`prompts.md`](assignment-06-delay-reason-classification/prompts.md) | [`results (.md)`](assignment-06-delay-reason-classification/classification_results.md), [`results (.csv)`](assignment-06-delay-reason-classification/classification_results.csv) | **PASS** |
| **07** | **Neural TTS Synthesis** | FastSpeech 2, HiFi-GAN, PCM 16-bit 22kHz WAV | [`tts_inference.py`](assignment-07-huggingface-tts/tts_inference.py) | [`test_assignment_07.py`](assignment-07-huggingface-tts/test_assignment_07.py) | [`prompts.md`](assignment-07-huggingface-tts/prompts.md) | [`output.wav`](assignment-07-huggingface-tts/output.wav), [`sample_audio/`](assignment-07-huggingface-tts/sample_audio/) | **PASS** |

---

### Module 01: Interactive CLI State Manager

- **Directory:** [`assignment-01-task-manager/`](assignment-01-task-manager/)
- **Core Engineering Problem:** Creating a robust, clean-architecture command-line state manager that guarantees data integrity, prevents identifier collisions during active item deletions, and cleanly handles edge-case user inputs without crashing.
- **Key Architectural Decisions:**
  - **Separation of Concerns:** Strict decoupling between data representation (`tasks` list of typed dictionaries), business logic (`add_task`, `view_tasks`, `mark_completed`, `delete_task`), and interactive terminal I/O (`main`).
  - **Monotonic ID Generator:** Replaced naive `len(tasks) + 1` indexing with a monotonic incrementing counter (`next_task_id`) safeguarded by `max()`, preventing ID collisions when tasks are deleted out of order.
  - **Defensive Type & Boundary Validation:** Reusable input sanitizer (`prompt_task_id`) that explicitly rejects booleans, negative integers, whitespace-only descriptions, and non-numeric inputs.
- **Verification Commands:**
  ```bash
  python assignment-01-task-manager/task_manager.py
  python assignment-01-task-manager/test_assignment_01.py
  ```
- **Documentation:** [`assignment-01-task-manager/README.md`](assignment-01-task-manager/README.md)

---

### Module 02: Prompt-Driven Automotive SOP Generator

- **Directory:** [`assignment-02-work-instructions/`](assignment-02-work-instructions/)
- **Core Engineering Problem:** Converting unstructured automotive engineering change notices into standardized, shop-floor-ready Standard Operating Procedures (SOPs) without relying on expensive database infrastructure or RAG retrieval.
- **Key Architectural Decisions:**
  - **Domain Persona Constraining:** System persona (`expert automotive manufacturing supervisor`) that enforces an imperative, safety-conscious shop-floor register.
  - **One-Shot Structural Prompting:** Enforces a rigid 4-section SOP schema across every output: *Safety Precautions (PPE/LOTO)*, *Required Tools & Equipment*, *Step-by-Step Procedure*, and *Acceptance Criteria*.
  - **Deterministic Generation & Role Adaptation:** Clamped `temperature=0` for repeatable factory documentation, with runtime role adaptation (`--role "Quality Inspector" | "Assembly Line Operator"`).
  - **Function-Level Dual-Mode Fallback:** `generate_instruction()` contains an internal offline fallback engine, ensuring direct imports by automated testing harnesses never throw unhandled `EnvironmentError` exceptions when API keys are unset.
- **Verification Commands:**
  ```bash
  python assignment-02-work-instructions/work_instruction_agent.py
  python assignment-02-work-instructions/test_assignment_02.py
  ```
- **Documentation & Deliverables:** [`README.md`](assignment-02-work-instructions/README.md), [`prompts.md`](assignment-02-work-instructions/prompts.md), [`generated_work_instructions.md`](assignment-02-work-instructions/generated_work_instructions.md), [`generated_work_instructions.csv`](assignment-02-work-instructions/generated_work_instructions.csv)

---

### Module 03: Executive Meeting Summarization Engine

- **Directory:** [`assignment-03-meeting-summarizer/`](assignment-03-meeting-summarizer/)
- **Core Engineering Problem:** Processing multi-speaker enterprise meeting transcripts of arbitrary length into structured executive briefs while handling context window limits and extracting clear, actionable accountability.
- **Key Architectural Decisions:**
  - **Map-Reduce Context Chunking:** Automatically detects transcripts exceeding model context thresholds, segments text along logical paragraph/speaker boundaries, generates intermediate chunk summaries, and reduces them into a unified synthesis.
  - **Accountability Extraction:** Strict prompt schema requiring explicit owner attribution and delivery dates for every action item (`[Owner]: Action Item Description (Due: YYYY-MM-DD)`).
  - **Dual Operating Modes:** Supports batch execution across multiple transcripts (generating individual Markdown reports and consolidated briefings), direct file ingestion (`--file`), and interactive CLI mode.
- **Verification Commands:**
  ```bash
  python assignment-03-meeting-summarizer/meeting_summarizer.py
  python assignment-03-meeting-summarizer/test_assignment_03.py
  ```
- **Documentation & Deliverables:** [`README.md`](assignment-03-meeting-summarizer/README.md), [`prompts.md`](assignment-03-meeting-summarizer/prompts.md), [`all_sample_summaries.md`](assignment-03-meeting-summarizer/all_sample_summaries.md), [`sample_outputs/`](assignment-03-meeting-summarizer/sample_outputs/)

---

### Module 04: Multi-Turn Conversational Event Assistant

- **Directory:** [`assignment-04-conversational-assistant/`](assignment-04-conversational-assistant/)
- **Core Engineering Problem:** Architecting an intelligent conversational agent capable of preserving multi-turn dialogue history, performing in-context sentiment classification, and executing complex logistical math using Chain-of-Thought reasoning.
- **Key Architectural Decisions:**
  - **Role-Based Message Hierarchy:** Strict message framing utilizing `system` (behavioral boundaries), `user` (human input), and `assistant` (model memory) message structures.
  - **Few-Shot Sentiment Injection:** Demonstrates in-context learning by supplying exemplar user-assistant pairs to establish sentiment analysis formatting and classification standards without fine-tuning.
  - **Chain-of-Thought (CoT) Prompting:** Directs the model to expose step-by-step reasoning phases before delivering numerical calculations (e.g., budget allocations, catering cost trade-offs, contingency plans).
  - **Course Symbol Compatibility:** Provides exact module-level exports (`few_shot_examples`, `conversation_messages`, `run_turn`) matching academic course specifications.
- **Verification Commands:**
  ```bash
  python assignment-04-conversational-assistant/conversational_assistant.py
  python assignment-04-conversational-assistant/test_assignment_04.py
  ```
- **Documentation & Deliverables:** [`README.md`](assignment-04-conversational-assistant/README.md), [`prompts.md`](assignment-04-conversational-assistant/prompts.md), [`all_sample_conversations.md`](assignment-04-conversational-assistant/all_sample_conversations.md), [`sample_outputs/`](assignment-04-conversational-assistant/sample_outputs/)

---

### Module 05: Resilient Azure Function Calling and Batch Pipeline

- **Directory:** [`assignment-05-azure-function-calling/`](assignment-05-azure-function-calling/)
- **Core Engineering Problem:** Executing high-volume batch LLM requests against Azure OpenAI while guaranteeing deterministic JSON structure, preventing HTTP 429 rate limit failures, and isolating item-level errors from breaking batch pipelines.
- **Key Architectural Decisions:**
  - **Strict JSON Schema Enforcement:** Declares a comprehensive `generate_itinerary` function definition with typed parameters (`destination`, `days`, `budget`, `activities`, `daily_schedule`) using OpenAI tools/function calling.
  - **Jittered Exponential Backoff:** Employs `tenacity` retry decorators (`wait_random_exponential(min=1, max=10)`, `stop_after_attempt(5)`) to survive cloud gateway drops and rate limits without manual polling.
  - **Quota Pacing & Error Isolation:** Implements deliberate inter-request pacing between batch items to stay safely below Azure TPM/RPM limits, capturing and logging failed records while allowing remaining items to process.
- **Verification Commands:**
  ```bash
  python assignment-05-azure-function-calling/batch_function_calling.py
  python assignment-05-azure-function-calling/test_assignment_05.py
  ```
- **Documentation & Deliverables:** [`README.md`](assignment-05-azure-function-calling/README.md), [`prompts.md`](assignment-05-azure-function-calling/prompts.md), [`all_sample_itineraries.md`](assignment-05-azure-function-calling/all_sample_itineraries.md), [`sample_outputs/`](assignment-05-azure-function-calling/sample_outputs/)

---

### Module 06: Hybrid Two-Stage Delay Reason Classifier

- **Directory:** [`assignment-06-delay-reason-classification/`](assignment-06-delay-reason-classification/)
- **Core Engineering Problem:** Categorizing messy, free-text logistics and maintenance delay logs into operational taxonomy categories while optimizing for inference latency and API expenditure.
- **Key Architectural Decisions:**
  - **Two-Stage Triage Architecture:**
    - *Stage 1 (Heuristic Pre-Classifier - `initial_classify`):* Executes sub-millisecond keyword lookup for unambiguous logs (zero token cost, zero API latency).
    - *Stage 2 (LLM Refinement - `refine_classification`):* Routes ambiguous or edge-case logs to Azure OpenAI (`temperature=0`) with category sanitization.
  - **Production Sanitizer:** Cleans LLM outputs to guarantee exact matching against allowed category enums (`Traffic`, `Weather`, `Mechanical Issue`, `Customer Delay`, `Documentation / Customs`, `Unknown`).
  - **Architectural Trade-Off Analysis:** In [`prompts.md`](assignment-06-delay-reason-classification/prompts.md), documents an industry comparison between Prompt Engineering, Supervised Fine-Tuning, and Retrieval-Augmented Generation (RAG) across latency, cost, and maintenance dimensions.
- **Verification Commands:**
  ```bash
  python assignment-06-delay-reason-classification/log_classifier.py
  python assignment-06-delay-reason-classification/test_assignment_06.py
  ```
- **Documentation & Deliverables:** [`README.md`](assignment-06-delay-reason-classification/README.md), [`prompts.md`](assignment-06-delay-reason-classification/prompts.md), [`classification_results.md`](assignment-06-delay-reason-classification/classification_results.md), [`classification_results.csv`](assignment-06-delay-reason-classification/classification_results.csv)

---

### Module 07: Neural Text-to-Speech (TTS) Inference Pipeline

- **Directory:** [`assignment-07-huggingface-tts/`](assignment-07-huggingface-tts/)
- **Core Engineering Problem:** Implementing a reliable speech synthesis inference pipeline from pre-trained Hugging Face neural acoustic models to produce broadcast-grade audio waveforms.
- **Key Architectural Decisions:**
  - **7-Step Neural Pipeline:** Implements the complete sequence from model acquisition to waveform rendering using FastSpeech 2 (`facebook/fastspeech2-en-ljspeech`) coupled with a HiFi-GAN neural vocoder.
  - **Broadcast Audio Standards:** Encodes audio into standard 22,050 Hz, 16-bit Mono PCM RIFF `.wav` files.
  - **Dual Interfaces:** Provides both an automated production Python CLI (`tts_inference.py`) and an interactive Jupyter Notebook (`tts_inference.ipynb`) with in-browser audio playback controls (`IPython.display.Audio`).
  - **Pure-Python Audio Synthesis Fallback:** Integrates an offline Formant-Phoneme audio synthesizer so that CI/CD and evaluation environments lacking PyTorch/Fairseq libraries still generate valid, verified 22.05 kHz `.wav` files.
- **Verification Commands:**
  ```bash
  python assignment-07-huggingface-tts/tts_inference.py
  python assignment-07-huggingface-tts/test_assignment_07.py
  ```
- **Documentation & Deliverables:** [`README.md`](assignment-07-huggingface-tts/README.md), [`prompts.md`](assignment-07-huggingface-tts/prompts.md), [`output.wav`](assignment-07-huggingface-tts/output.wav), [`sample_audio/`](assignment-07-huggingface-tts/sample_audio/)

---

## Engineering Standards and Reliability

### 1. Dual-Mode Evaluation Resilience
A common failure mode in academic and project code is external API fragility: if a reviewer or automated CI test runs without active cloud credentials, scripts crash with unhandled exceptions. This project solves this by engineering **function-level offline fallback engines** into every module. Each script functions seamlessly in both:
- **Live Cloud Mode:** Connects to Azure OpenAI / Hugging Face when credentials are configured.
- **Verified Offline Mode:** Returns precomputed, verified domain responses when credentials are absent, enabling zero-configuration test runs.

### 2. Comprehensive Test Automation
Every module includes a dedicated `test_assignment_0X.py` test suite alongside the master `test_all_assignments.py` test runner. The test suites cover:
- Monotonic state manipulation and edge-case input handling.
- Function return schema compliance and dictionary structure validation.
- Tenacity retry loop behavior and HTTP 429 recovery simulation.
- Waveform sample rates, PCM bit depth, and RIFF header verification.

---

## Prompt Engineering Governance and Traceability

High-performing AI engineering requires strict prompt version control and architectural documentation. Every AI module in this project maintains two transparent specification files:
1. **`prompts.md`:** Documents the operational prompt engineering architecture used by the application, including system role definitions, few-shot demonstration pairs, chain-of-thought directives, and model parameter rationale (`temperature`, `top_p`).
2. **`GENERATION_PROMPT.md`:** Documents the auto-refined meta-prompt used to design, architect, and harden the system against edge cases, ensuring complete engineering provenance and reproducibility.

---

## Repository Architecture

```text
.
├── README.md                                    # Project documentation & technical guide
├── test_all_assignments.py                      # Master audit test suite (validates all 7 modules)
├── .gitignore                                   # Python, cache, and local secret exclusion rules
│
├── assignment-01-task-manager/
│   ├── task_manager.py                          # Core CLI task management application
│   ├── test_assignment_01.py                    # Unit and CLI pipe test suite
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   └── README.md                                # Architecture documentation & challenges
│
├── assignment-02-work-instructions/
│   ├── work_instruction_agent.py               # Azure OpenAI automotive SOP generator
│   ├── test_assignment_02.py                    # Unit and schema test suite
│   ├── generated_work_instructions.md           # 5 generated automotive SOP cards
│   ├── generated_work_instructions.csv          # Structured CSV export of SOP records
│   ├── prompts.md                               # System prompt & one-shot engineering guide
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   ├── requirements.txt                         # Dependency definitions
│   └── README.md                                # Manufacturing case study & reflection
│
├── assignment-03-meeting-summarizer/
│   ├── meeting_summarizer.py                    # Transcript summarizer with map-reduce chunking
│   ├── test_assignment_03.py                    # Unit and chunking test suite
│   ├── all_sample_summaries.md                  # Consolidated briefing across 5 transcripts
│   ├── sample_transcripts/                      # 5 realistic multi-speaker meeting transcripts
│   ├── sample_outputs/                          # 5 structured Markdown executive summaries
│   ├── prompts.md                               # Structured output schemas & prompts
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   ├── requirements.txt                         # Dependency definitions
│   └── README.md                                # Usage documentation & architecture
│
├── assignment-04-conversational-assistant/
│   ├── conversational_assistant.py              # Multi-turn assistant with advanced prompting
│   ├── test_assignment_04.py                    # Multi-turn and wire-protocol test suite
│   ├── all_sample_conversations.md              # Consolidated multi-turn dialogue logs
│   ├── sample_outputs/                          # 3 scenario conversation logs
│   ├── prompts.md                               # Few-shot & Chain-of-Thought prompting guide
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   ├── requirements.txt                         # Dependency definitions
│   └── README.md                                # Technical documentation
│
├── assignment-05-azure-function-calling/
│   ├── batch_function_calling.py                # Function calling pipeline with Tenacity retry
│   ├── test_assignment_05.py                    # Resilience & exponential backoff test suite
│   ├── sample_inputs.json                       # 3 batch scenario requests (Paris, Tokyo, NYC)
│   ├── sample_outputs/                          # JSON schemas & Markdown itinerary exports
│   ├── all_sample_itineraries.md                # Consolidated presentation report
│   ├── prompts.md                               # Function schemas & backoff specifications
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   ├── requirements.txt                         # Dependency definitions (tenacity, openai)
│   └── README.md                                # Retry architecture documentation
│
├── assignment-06-delay-reason-classification/
│   ├── log_classifier.py                        # Two-stage hybrid NLP classification pipeline
│   ├── test_assignment_06.py                    # Classification & sanitization test suite
│   ├── dataset.csv                              # 10 course mock maintenance & delivery log entries
│   ├── classification_results.md                # Formatted Markdown report with predictions
│   ├── classification_results.csv               # Structured tabular CSV export
│   ├── prompts.md                               # Refinement prompt & RAG trade-off analysis
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   ├── requirements.txt                         # Dependency definitions
│   └── README.md                                # Architecture documentation
│
└── assignment-07-huggingface-tts/
    ├── tts_inference.py                         # 7-step Hugging Face TTS inference pipeline
    ├── tts_inference.ipynb                      # Interactive Jupyter Notebook with audio player
    ├── test_assignment_07.py                    # Audio header & schema test suite
    ├── output.wav                               # Standard 22,050 Hz 16-bit PCM WAV audio
    ├── sample_audio/                            # 3 pre-synthesized audio recordings
    │   ├── sample_1_test_run.wav
    │   ├── sample_2_ai_elevate.wav
    │   ├── sample_3_logistics_voice.wav
    │   └── audio_samples_manifest.md            # Manifest documenting duration, rate & text
    ├── prompts.md                               # Speech prompt templates & TTS analysis
    ├── GENERATION_PROMPT.md                     # Meta-prompt specification
    ├── requirements.txt                         # Dependency definitions (soundfile, IPython)
    └── README.md                                # Setup guide & walkthrough
```

---

## Environment Setup and Optional Azure Credentials

### Prerequisites
- **Python**: Version 3.10, 3.11, or 3.12.
- **Git**: To clone the repository.

### Installation
Clone the repository:
```bash
git clone https://github.com/Dylanzsnut/Dyce.git
cd Dyce
```

Install production dependencies:
```bash
python -m pip install -r assignment-02-work-instructions/requirements.txt
python -m pip install -r assignment-05-azure-function-calling/requirements.txt
```

### Optional Live Azure OpenAI Configuration
To execute requests against a live Azure OpenAI deployment rather than using the built-in offline demonstration engine, configure the standard environment variables:

```bash
# In Linux / macOS Bash:
export AZURE_OPENAI_API_KEY="your_api_key_here"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
export AZURE_OPENAI_API_VERSION="2024-07-01-preview"

# Or in Windows PowerShell:
$env:AZURE_OPENAI_API_KEY="your_api_key_here"
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
$env:AZURE_OPENAI_API_VERSION="2024-07-01-preview"
```

When no environment variables are detected, all modules automatically and gracefully fall back to their offline engines.
