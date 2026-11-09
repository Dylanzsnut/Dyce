# AI Elevate: AI Application Engineer — Core Assignments

This repository contains the complete source code, automated test suites, prompt specifications, generation meta-prompts, and sample output artifacts for the **AI Application Engineer** program.

---

## Repository Structure

```text
.
├── .gitignore
├── README.md                        # Master repository documentation
├── test_all_assignments.py          # Master audit suite (validates A1 - A7)
│
├── assignment-01-task-manager/
│   ├── task_manager.py              # CLI task manager application
│   ├── GENERATION_PROMPT.md         # Auto-refined prompt specification
│   └── README.md                    # Assignment 1 documentation & reflection
│
├── assignment-02-work-instructions/
│   ├── work_instruction_agent.py   # Azure OpenAI prompt-driven SOP generator
│   ├── generated_work_instructions.md # 5 complete generated SOP samples
│   ├── generated_work_instructions.csv# CSV table of generated SOPs
│   ├── prompts.md                   # System prompts & few-shot specifications
│   ├── GENERATION_PROMPT.md         # Auto-refined prompt specification
│   ├── .env.example                 # Azure OpenAI environment variable template
│   ├── requirements.txt             # Dependencies (openai, python-dotenv)
│   └── README.md                    # Assignment 2 documentation & manufacturing reflection
│
├── assignment-03-meeting-summarizer/
│   ├── meeting_summarizer.py        # Azure OpenAI meeting summarization application
│   ├── all_sample_summaries.md      # Consolidated report of 5 transcripts + summaries
│   ├── sample_transcripts/          # 5 realistic multi-speaker meeting transcripts
│   ├── sample_outputs/              # 5 individual structured Markdown summaries
│   ├── prompts.md                   # System prompts & schema specifications
│   ├── GENERATION_PROMPT.md         # Auto-refined prompt specification
│   ├── .env.example                 # Azure OpenAI environment variable template
│   ├── requirements.txt             # Dependencies (openai, python-dotenv)
│   └── README.md                    # Assignment 3 documentation & usage guide
│
├── assignment-04-conversational-assistant/
│   ├── conversational_assistant.py  # Multi-turn assistant with advanced prompting
│   ├── test_assignment_04.py        # Automated test suite (5 double-check tests)
│   ├── GENERATION_PROMPT.md         # Auto-refined prompt used to create this assignment
│   ├── prompts.md                   # Complete prompts specification & engineering guide
│   ├── all_sample_conversations.md  # Consolidated report of 3 multi-turn scenarios
│   ├── sample_outputs/              # 3 individual scenario conversation logs
│   ├── .env.example                 # Azure OpenAI environment variable template
│   ├── requirements.txt             # Dependencies (openai, python-dotenv)
│   └── README.md                    # Assignment 4 documentation & prompting guide
│
├── assignment-05-azure-function-calling/
│   ├── batch_function_calling.py    # Azure OpenAI function calling with Tenacity retries
│   ├── test_assignment_05.py        # Automated test suite (6 resilience tests)
│   ├── sample_inputs.json           # 3 batch scenario requests (Paris, Tokyo, NYC)
│   ├── sample_outputs/              # Structured JSON and Markdown itinerary outputs
│   ├── all_sample_itineraries.md    # Consolidated presentation itinerary report
│   ├── prompts.md                   # Function schema & retry specifications
│   ├── GENERATION_PROMPT.md         # Auto-refined prompt specification
│   ├── .env.example                 # Azure OpenAI environment variable template
│   ├── requirements.txt             # Dependencies (openai, tenacity, python-dotenv)
│   └── README.md                    # Assignment 5 documentation & retry architecture
│
├── assignment-06-delay-reason-classification/
│   ├── log_classifier.py            # Hybrid two-stage NLP classification pipeline
│   ├── dataset.csv                  # 10 course mock maintenance & delivery log entries
│   ├── classification_results.md    # Formatted Markdown report with predicted categories
│   ├── classification_results.csv   # Structured tabular CSV export
│   ├── test_assignment_06.py        # Automated test suite (6 validation tests)
│   ├── prompts.md                   # Refinement prompt & RAG comparative analysis
│   ├── GENERATION_PROMPT.md         # Auto-refined prompt specification
│   ├── .env.example                 # Azure OpenAI environment variable template
│   ├── requirements.txt             # Dependencies (openai, python-dotenv)
│   └── README.md                    # Assignment 6 documentation & architectural analysis
│
└── assignment-07-huggingface-tts/
    ├── tts_inference.py             # Main inference script (Steps 1-7)
    ├── tts_inference.ipynb          # Interactive Jupyter Notebook with audio playback
    ├── output.wav                   # Generated 22,050 Hz PCM 16-bit audio waveform
    ├── sample_audio/                # 3 pre-synthesized audio recordings (.wav)
    │   ├── sample_1_test_run.wav
    │   ├── sample_2_ai_elevate.wav
    │   ├── sample_3_logistics_voice.wav
    │   └── audio_samples_manifest.md# Manifest documenting duration, rate & text
    ├── test_assignment_07.py        # Automated test suite (6 audio & schema tests)
    ├── prompts.md                   # Speech prompt templates & TTS architecture comparison
    ├── GENERATION_PROMPT.md         # Auto-refined prompt specification
    ├── requirements.txt             # Dependencies (soundfile, IPython)
    └── README.md                    # Assignment 7 documentation & setup guide
```

---

## Assignment Summaries & Quick Run

### 1. Assignment 01: Command-Line Task Manager
- **Core Focus:** Fundamental Python data structures, input validation, and interactive CLI loops.
- **Run:** `py -3.12 assignment-01-task-manager/task_manager.py`

### 2. Assignment 02: Automotive Work Instructions
- **Core Focus:** Azure OpenAI prompt engineering for shopfloor Standard Operating Procedures (SOPs).
- **Run:** `py -3.12 assignment-02-work-instructions/work_instruction_agent.py`

### 3. Assignment 03: AI-Powered Meeting Summarizer
- **Core Focus:** Processing transcripts to extract decisions, action items, and executive briefs.
- **Run:** `py -3.12 assignment-03-meeting-summarizer/meeting_summarizer.py`

### 4. Assignment 04: Conversational Assistant with Advanced Prompting
- **Core Focus:** Role-based messaging (`system`, `user`, `assistant`), few-shot sentiment analysis, and Chain-of-Thought (CoT) reasoning.
- **Run:** `py -3.12 assignment-04-conversational-assistant/conversational_assistant.py`

### 5. Assignment 05: Azure Function Calling & Robust Retries
- **Core Focus:** OpenAI function calling schema enforcement, batch pacing, and Tenacity jittered exponential backoff.
- **Run:** `py -3.12 assignment-05-azure-function-calling/batch_function_calling.py`

### 6. Assignment 06: Logistics Delay Reason Classification
- **Core Focus:** Two-stage hybrid pipeline (Heuristic pre-classification + LLM refinement with `temperature=0`).
- **Run:** `py -3.12 assignment-06-delay-reason-classification/log_classifier.py`

### 7. Assignment 07: Hugging Face Text-to-Speech (TTS) Inference
- **Core Focus:** Cloning pre-trained neural TTS models (`facebook/fastspeech2-en-ljspeech`), generating 22,050 Hz 16-bit PCM `.wav` waveforms, and Jupyter audio playback.
- **Run:** `py -3.12 assignment-07-huggingface-tts/tts_inference.py`

---

## Master Double-Triple Check Test Suite

To verify all 7 assignments consecutively against evaluation traps and edge cases:
```powershell
py -3.12 test_all_assignments.py
```
