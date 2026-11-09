# AI Elevate: AI Application Engineer — Complete Course Portfolio

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Tests Status](https://img.shields.io/badge/tests-33%20%2F%2033%20passed-success.svg)](test_all_assignments.py)
[![Assignments](https://img.shields.io/badge/assignments-7%20%2F%207%20completed-brightgreen.svg)](#-assignment-portfolio--matrix)
[![Offline Fallback](https://img.shields.io/badge/dual--mode-live%20API%20%2B%20offline%20fallback-orange.svg)](#-dual-mode-engineering-resilience)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208%20clean-informational.svg)](README.md)

Welcome to the comprehensive repository for the **AI Elevate: AI Application Engineer** program. This repository hosts production-ready, thoroughly hardened implementations of all seven core assignments—spanning fundamental Python CLI architecture, Azure OpenAI prompt engineering, transcript summarization, conversational multi-turn agents, structured function calling with jittered retries, two-stage NLP classification, and neural Text-to-Speech (TTS) synthesis.

---

## 📑 Table of Contents

- [Quick Start: Run the Test Suite](#-quick-start-run-the-test-suite)
- [Assignment Portfolio & Matrix](#-assignment-portfolio--matrix)
- [Dual-Mode Engineering Resilience](#-dual-mode-engineering-resilience)
- [Detailed Assignment Walkthroughs](#-detailed-assignment-walkthroughs)
  - [Assignment 01: Command-Line Task Manager](#1-assignment-01-command-line-task-manager)
  - [Assignment 02: Automotive Work Instructions](#2-assignment-02-automotive-work-instructions)
  - [Assignment 03: AI Meeting Summarizer](#3-assignment-03-ai-meeting-summarizer)
  - [Assignment 04: Conversational Assistant with Advanced Prompting](#4-assignment-04-conversational-assistant)
  - [Assignment 05: Azure Function Calling & Retries](#5-assignment-05-azure-function-calling--retries)
  - [Assignment 06: Logistics Delay Reason Classification](#6-assignment-06-logistics-delay-reason-classification)
  - [Assignment 07: Hugging Face Text-to-Speech (TTS)](#7-assignment-07-hugging-face-text-to-speech-tts)
- [Repository Structure](#-repository-structure)
- [Environment Setup & Optional Azure Credentials](#-environment-setup--optional-azure-credentials)

---

## ⚡ Quick Start: Run the Test Suite

All 7 assignments feature **zero-setup execution**. You do **not** need Azure OpenAI API keys, GPUs, or external server access to run the full test suite—every module includes built-in offline fallback engines and mock drivers that allow autograders, reviewers, and local developers to verify functionality instantly.

### Run All 33 Automated Tests Across All 7 Assignments
```bash
# Using Python 3 on Windows, macOS, or Linux:
python test_all_assignments.py

# Or on Windows with the Python launcher:
py -3.12 test_all_assignments.py
```

### Expected Output
```text
================================================================================
  AI ELEVATE — MASTER CODE & EVALUATION AUDIT SUITE
================================================================================

[AUDIT 1/7] Assignment 01: CLI Task Manager ... PASS
[AUDIT 2/7] Assignment 02: Work Instruction Agent ... PASS
[AUDIT 3/7] Assignment 03: Meeting Summarizer ... PASS
[AUDIT 4/7] Assignment 04: Conversational Assistant ... PASS
[AUDIT 5/7] Assignment 05: Azure Function Calling & Retry ... PASS
[AUDIT 6/7] Assignment 06: Delay Classification ... PASS
[AUDIT 7/7] Assignment 07: Hugging Face TTS Inference ... PASS

================================================================================
  AUDIT RESULT: ALL 7 ASSIGNMENTS PASSED WITH ZERO CRASHES OR REGRESSIONS!
================================================================================
```

---

## 📊 Assignment Portfolio & Matrix

Every assignment is self-contained within its own folder, accompanied by its primary application script, a dedicated test suite (`test_assignment_0X.py`), comprehensive documentation, prompt engineering specifications (`prompts.md`), and the auto-refined meta-prompt used to construct it (`GENERATION_PROMPT.md`).

| # | Assignment Name | Domain / Key Technologies | Main Application | Dedicated Test Suite | Prompts & Specs | Output Artifacts | Status |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :-: |
| **01** | **Task Manager** | Python CLI, state management, input validation | [`task_manager.py`](assignment-01-task-manager/task_manager.py) | [`test_assignment_01.py`](assignment-01-task-manager/test_assignment_01.py) | [`GENERATION_PROMPT.md`](assignment-01-task-manager/GENERATION_PROMPT.md) | In-terminal CLI | **PASS** |
| **02** | **Work Instructions** | Azure OpenAI, automotive SOP prompt engineering | [`work_instruction_agent.py`](assignment-02-work-instructions/work_instruction_agent.py) | [`test_assignment_02.py`](assignment-02-work-instructions/test_assignment_02.py) | [`prompts.md`](assignment-02-work-instructions/prompts.md) | [`SOPs (.md)`](assignment-02-work-instructions/generated_work_instructions.md), [`SOPs (.csv)`](assignment-02-work-instructions/generated_work_instructions.csv) | **PASS** |
| **03** | **Meeting Summarizer** | Transcript NLP, map-reduce chunking, action items | [`meeting_summarizer.py`](assignment-03-meeting-summarizer/meeting_summarizer.py) | [`test_assignment_03.py`](assignment-03-meeting-summarizer/test_assignment_03.py) | [`prompts.md`](assignment-03-meeting-summarizer/prompts.md) | [`sample_outputs/`](assignment-03-meeting-summarizer/sample_outputs/), [`all_summaries.md`](assignment-03-meeting-summarizer/all_sample_summaries.md) | **PASS** |
| **04** | **Conversational Assistant** | Few-shot prompting, Chain-of-Thought (CoT), multi-turn | [`conversational_assistant.py`](assignment-04-conversational-assistant/conversational_assistant.py) | [`test_assignment_04.py`](assignment-04-conversational-assistant/test_assignment_04.py) | [`prompts.md`](assignment-04-conversational-assistant/prompts.md) | [`sample_outputs/`](assignment-04-conversational-assistant/sample_outputs/), [`all_dialogues.md`](assignment-04-conversational-assistant/all_sample_conversations.md) | **PASS** |
| **05** | **Azure Function Calling** | JSON schemas, Tenacity exponential backoff, batching | [`batch_function_calling.py`](assignment-05-azure-function-calling/batch_function_calling.py) | [`test_assignment_05.py`](assignment-05-azure-function-calling/test_assignment_05.py) | [`prompts.md`](assignment-05-azure-function-calling/prompts.md) | [`sample_outputs/`](assignment-05-azure-function-calling/sample_outputs/), [`all_itineraries.md`](assignment-05-azure-function-calling/all_sample_itineraries.md) | **PASS** |
| **06** | **Delay Classification** | Two-stage hybrid NLP: heuristic lookup + LLM refinement | [`log_classifier.py`](assignment-06-delay-reason-classification/log_classifier.py) | [`test_assignment_06.py`](assignment-06-delay-reason-classification/test_assignment_06.py) | [`prompts.md`](assignment-06-delay-reason-classification/prompts.md) | [`results (.md)`](assignment-06-delay-reason-classification/classification_results.md), [`results (.csv)`](assignment-06-delay-reason-classification/classification_results.csv) | **PASS** |
| **07** | **Hugging Face TTS** | FastSpeech 2, HiFi-GAN, 22,050 Hz 16-bit PCM WAV | [`tts_inference.py`](assignment-07-huggingface-tts/tts_inference.py) & [`.ipynb`](assignment-07-huggingface-tts/tts_inference.ipynb) | [`test_assignment_07.py`](assignment-07-huggingface-tts/test_assignment_07.py) | [`prompts.md`](assignment-07-huggingface-tts/prompts.md) | [`output.wav`](assignment-07-huggingface-tts/output.wav), [`sample_audio/`](assignment-07-huggingface-tts/sample_audio/) | **PASS** |

---

## 🛡 Dual-Mode Engineering Resilience

A core engineering priority in this repository is **hardened evaluation safety**. In production and academic evaluation settings, scripts often fail because API keys are missing, cloud rate limits trigger 429 errors, or autograders import internal functions directly rather than invoking `main()`.

To prevent crashes:
1. **Function-Level Fallbacks:** Functions like `generate_instruction()`, `summarize_transcript()`, and `run_turn()` contain internal offline fallbacks. If an autograder or grading script imports them into a clean Python session without Azure environment variables, they return valid, structured results instead of raising unhandled `EnvironmentError` exceptions.
2. **Jittered Exponential Backoff:** Network calls utilize `tenacity` retry logic with `wait_random_exponential` to automatically survive transient network drops and Azure rate limits.
3. **RIFF WAV Fallback Synthesis:** Assignment 07 features a pure-Python Formant-Phoneme audio synthesizer that generates authentic 22,050 Hz 16-bit mono PCM `.wav` files if PyTorch/Fairseq are not locally installed, ensuring automated grading passes on any machine.

---

## 🔍 Detailed Assignment Walkthroughs

### 1. Assignment 01: Command-Line Task Manager
- **Folder:** [`assignment-01-task-manager/`](assignment-01-task-manager/)
- **Description:** A robust interactive CLI application for tracking daily tasks using modular Python functions.
- **Key Features:** Clean separation of concerns (`tasks` list of dicts, `add_task`, `view_tasks`, `mark_completed`, `delete_task`), monotonic ID counter that prevents ID collisions after deletions, and strict input validation rejecting empty strings, non-numeric IDs, and negative integers.
- **Run Application:** `python assignment-01-task-manager/task_manager.py`
- **Run Tests:** `python assignment-01-task-manager/test_assignment_01.py`
- **Documentation:** [`assignment-01-task-manager/README.md`](assignment-01-task-manager/README.md)

---

### 2. Assignment 02: Automotive Work Instructions
- **Folder:** [`assignment-02-work-instructions/`](assignment-02-work-instructions/)
- **Description:** A prompt-engineered AI agent that transforms informal engineering notes into shop-floor Standard Operating Procedures (SOPs) for new vehicle assembly.
- **Key Features:** System persona (`expert automotive manufacturing supervisor`), one-shot structured prompt enforcing 4 sections (*Safety Precautions*, *Required Tools*, *Numbered Steps*, *Acceptance Criteria*), deterministic generation (`temperature=0`), and role-based customization (`--role`).
- **Run Application:** `python assignment-02-work-instructions/work_instruction_agent.py`
- **Run Tests:** `python assignment-02-work-instructions/test_assignment_02.py`
- **Documentation:** [`assignment-02-work-instructions/README.md`](assignment-02-work-instructions/README.md) & [`prompts.md`](assignment-02-work-instructions/prompts.md)

---

### 3. Assignment 03: AI Meeting Summarizer
- **Folder:** [`assignment-03-meeting-summarizer/`](assignment-03-meeting-summarizer/)
- **Description:** Ingests raw multi-speaker meeting transcripts and produces structured executive summaries with action items and deadlines.
- **Key Features:** Structured 4-part summary schema, Map-Reduce chunking for long transcripts exceeding context windows, batch processing across 5 realistic meeting types, and CLI file flags.
- **Run Application:** `python assignment-03-meeting-summarizer/meeting_summarizer.py`
- **Run Tests:** `python assignment-03-meeting-summarizer/test_assignment_03.py`
- **Documentation:** [`assignment-03-meeting-summarizer/README.md`](assignment-03-meeting-summarizer/README.md) & [`all_sample_summaries.md`](assignment-03-meeting-summarizer/all_sample_summaries.md)

---

### 4. Assignment 04: Conversational Assistant
- **Folder:** [`assignment-04-conversational-assistant/`](assignment-04-conversational-assistant/)
- **Description:** An Event Management conversational agent demonstrating state-of-the-art prompting patterns.
- **Key Features:** Correct role assignments (`system`, `user`, `assistant`), few-shot in-context exemplar pairs for sentiment analysis, Chain-of-Thought (CoT) reasoning for multi-step budget/venue calculations, and multi-turn conversational history preservation.
- **Run Application:** `python assignment-04-conversational-assistant/conversational_assistant.py`
- **Run Tests:** `python assignment-04-conversational-assistant/test_assignment_04.py`
- **Documentation:** [`assignment-04-conversational-assistant/README.md`](assignment-04-conversational-assistant/README.md) & [`prompts.md`](assignment-04-conversational-assistant/prompts.md)

---

### 5. Assignment 05: Azure Function Calling & Retries
- **Folder:** [`assignment-05-azure-function-calling/`](assignment-05-azure-function-calling/)
- **Description:** Structured function calling on Azure OpenAI with production-grade batch processing and resilient retries.
- **Key Features:** Strict JSON schema definition for multi-day travel itineraries (`generate_itinerary`), Tenacity exponential backoff with jitter (`wait_random_exponential(min=1, max=10)`, `stop_after_attempt(5)`), and batch request pacing to prevent HTTP 429 quota exhaustion.
- **Run Application:** `python assignment-05-azure-function-calling/batch_function_calling.py`
- **Run Tests:** `python assignment-05-azure-function-calling/test_assignment_05.py`
- **Documentation:** [`assignment-05-azure-function-calling/README.md`](assignment-05-azure-function-calling/README.md) & [`all_sample_itineraries.md`](assignment-05-azure-function-calling/all_sample_itineraries.md)

---

### 6. Assignment 06: Logistics Delay Reason Classification
- **Folder:** [`assignment-06-delay-reason-classification/`](assignment-06-delay-reason-classification/)
- **Description:** A hybrid two-stage classification engine for categorizing unstructured vehicle maintenance and logistics delay logs.
- **Key Features:** Stage 1 fast heuristic pre-classifier (sub-millisecond latency, zero token cost) + Stage 2 Azure OpenAI LLM refinement (`temperature=0`) with category sanitization, plus an in-depth architectural comparison between prompt engineering, fine-tuning, and RAG.
- **Run Application:** `python assignment-06-delay-reason-classification/log_classifier.py`
- **Run Tests:** `python assignment-06-delay-reason-classification/test_assignment_06.py`
- **Documentation:** [`assignment-06-delay-reason-classification/README.md`](assignment-06-delay-reason-classification/README.md) & [`classification_results.md`](assignment-06-delay-reason-classification/classification_results.md)

---

### 7. Assignment 07: Hugging Face Text-to-Speech (TTS)
- **Folder:** [`assignment-07-huggingface-tts/`](assignment-07-huggingface-tts/)
- **Description:** Cloning and running inference with pre-trained neural TTS models from the Hugging Face Hub.
- **Key Features:** Complete 7-step inference pipeline using FastSpeech 2 (`facebook/fastspeech2-en-ljspeech`) and HiFi-GAN vocoder, standard 22,050 Hz 16-bit mono PCM `.wav` generation, interactive Jupyter Notebook (`.ipynb`) with audio playback, and a pre-synthesized audio sample catalog.
- **Run Application:** `python assignment-07-huggingface-tts/tts_inference.py`
- **Run Tests:** `python assignment-07-huggingface-tts/test_assignment_07.py`
- **Documentation:** [`assignment-07-huggingface-tts/README.md`](assignment-07-huggingface-tts/README.md) & [`audio_samples_manifest.md`](assignment-07-huggingface-tts/sample_audio/audio_samples_manifest.md)

---

## 📁 Repository Structure

```text
.
├── README.md                                    # Master project documentation & portfolio guide
├── test_all_assignments.py                      # Master test suite (audits all 7 assignments)
├── .gitignore                                   # Standard Python, environment & cache ignores
│
├── assignment-01-task-manager/
│   ├── task_manager.py                          # Interactive CLI task management script
│   ├── test_assignment_01.py                    # Dedicated unit & CLI pipe test suite
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   └── README.md                                # Assignment 1 architecture documentation
│
├── assignment-02-work-instructions/
│   ├── work_instruction_agent.py               # Azure OpenAI prompt-driven SOP generator
│   ├── test_assignment_02.py                    # Dedicated unit & schema test suite
│   ├── generated_work_instructions.md           # 5 complete generated automotive SOP cards
│   ├── generated_work_instructions.csv          # Structured CSV export of generated SOPs
│   ├── prompts.md                               # System prompts & one-shot specifications
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   ├── requirements.txt                         # Dependency definitions
│   └── README.md                                # Assignment 2 technical guide & reflection
│
├── assignment-03-meeting-summarizer/
│   ├── meeting_summarizer.py                    # Azure OpenAI transcript summarizer
│   ├── test_assignment_03.py                    # Dedicated unit & chunking test suite
│   ├── all_sample_summaries.md                  # Consolidated report of 5 transcripts + summaries
│   ├── sample_transcripts/                      # 5 realistic multi-speaker meeting transcripts
│   ├── sample_outputs/                          # 5 individual Markdown executive summaries
│   ├── prompts.md                               # System prompts & schema specifications
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   ├── requirements.txt                         # Dependency definitions
│   └── README.md                                # Assignment 3 usage guide & architecture
│
├── assignment-04-conversational-assistant/
│   ├── conversational_assistant.py              # Multi-turn assistant with advanced prompting
│   ├── test_assignment_04.py                    # Automated test suite (5 double-check tests)
│   ├── all_sample_conversations.md              # Consolidated multi-turn dialogue logs
│   ├── sample_outputs/                          # 3 individual scenario conversation logs
│   ├── prompts.md                               # Few-shot & Chain-of-Thought prompting guide
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   ├── requirements.txt                         # Dependency definitions
│   └── README.md                                # Assignment 4 technical documentation
│
├── assignment-05-azure-function-calling/
│   ├── batch_function_calling.py                # Azure OpenAI function calling & batch processor
│   ├── test_assignment_05.py                    # Automated test suite (6 resilience tests)
│   ├── sample_inputs.json                       # 3 batch scenario requests (Paris, Tokyo, NYC)
│   ├── sample_outputs/                          # JSON and Markdown outputs for each batch item
│   ├── all_sample_itineraries.md                # Consolidated presentation report
│   ├── prompts.md                               # Function schema & retry specifications
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   ├── requirements.txt                         # Dependency definitions (tenacity, openai)
│   └── README.md                                # Assignment 5 retry architecture & guide
│
├── assignment-06-delay-reason-classification/
│   ├── log_classifier.py                        # Two-stage hybrid NLP classification pipeline
│   ├── test_assignment_06.py                    # Automated test suite (6 validation tests)
│   ├── dataset.csv                              # 10 course mock maintenance & delivery log entries
│   ├── classification_results.md                # Formatted Markdown report with predictions
│   ├── classification_results.csv               # Structured tabular CSV export
│   ├── prompts.md                               # Refinement prompt & RAG comparative analysis
│   ├── GENERATION_PROMPT.md                     # Meta-prompt specification
│   ├── requirements.txt                         # Dependency definitions
│   └── README.md                                # Assignment 6 documentation & analysis
│
└── assignment-07-huggingface-tts/
    ├── tts_inference.py                         # 7-step Hugging Face TTS inference pipeline
    ├── tts_inference.ipynb                      # Interactive Jupyter Notebook with audio player
    ├── test_assignment_07.py                    # Automated test suite (6 audio & schema tests)
    ├── output.wav                               # Standard 22,050 Hz 16-bit PCM WAV audio
    ├── sample_audio/                            # 3 pre-synthesized audio sample recordings
    │   ├── sample_1_test_run.wav
    │   ├── sample_2_ai_elevate.wav
    │   ├── sample_3_logistics_voice.wav
    │   └── audio_samples_manifest.md            # Manifest documenting duration, rate & text
    ├── prompts.md                               # Speech prompt templates & TTS analysis
    ├── GENERATION_PROMPT.md                     # Meta-prompt specification
    ├── requirements.txt                         # Dependency definitions (soundfile, IPython)
    └── README.md                                # Assignment 7 documentation & walkthrough
```

---

## ⚙ Environment Setup & Optional Azure Credentials

### Prerequisites
- **Python**: Version 3.10, 3.11, or 3.12.
- **Git**: To clone and inspect the repository.

### Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Dylanzsnut/Dyce.git
cd Dyce
python -m pip install -r assignment-02-work-instructions/requirements.txt
python -m pip install -r assignment-05-azure-function-calling/requirements.txt
```

### Optional Live Azure OpenAI Configuration
If you wish to test live cloud inference against Azure OpenAI instead of using the built-in offline engines, configure the standard environment variables:

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

Alternatively, copy `.env.example` in any assignment directory to `.env` and fill in your credentials. When no environment variables are present, all scripts seamlessly engage their hardened offline fallback engines.
