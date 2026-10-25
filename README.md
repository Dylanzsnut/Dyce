# AI Elevate: AI Application Engineer — Core Assignments

This repository contains the complete source code, test suites, documentation, and sample output artifacts for the **AI Application Engineer** program.

---

## Repository Structure

```text
.
├── .gitignore
├── README.md
│
├── assignment-01-task-manager/
│   ├── task_manager.py              # CLI task manager application
│   └── README.md                    # Assignment 1 documentation & reflection
│
├── assignment-02-work-instructions/
│   ├── work_instruction_agent.py   # Azure OpenAI prompt-driven SOP generator
│   ├── generated_work_instructions.md # 5 complete generated SOP samples
│   ├── generated_work_instructions.csv# CSV table of generated SOPs
│   ├── .env.example                 # Azure OpenAI environment variable template
│   ├── requirements.txt             # Dependencies (openai, python-dotenv)
│   └── README.md                    # Assignment 2 documentation & manufacturing reflection
│
└── assignment-03-meeting-summarizer/
    ├── meeting_summarizer.py        # Azure OpenAI meeting summarization application
    ├── all_sample_summaries.md      # Consolidated report of 5 transcripts + summaries
    ├── sample_transcripts/          # 5 realistic multi-speaker meeting transcripts
    │   ├── sample_01_product_roadmap_sync.txt
    │   ├── sample_02_sprint_retrospective.txt
    │   ├── sample_03_incident_postmortem.txt
    │   ├── sample_04_client_onboarding_kickoff.txt
    │   └── sample_05_marketing_launch_planning.txt
    ├── sample_outputs/              # 5 individual structured Markdown summaries
    │   ├── summary_01_product_roadmap_sync.md
    │   ├── summary_02_sprint_retrospective.md
    │   ├── summary_03_incident_postmortem.md
    │   ├── summary_04_client_onboarding_kickoff.md
    │   └── summary_05_marketing_launch_planning.md
    ├── .env.example                 # Azure OpenAI environment variable template
    ├── requirements.txt             # Dependencies (openai, python-dotenv)
    └── README.md                    # Assignment 3 documentation & usage guide
```

---

## Assignment Summaries

### 1. Assignment 01: Command-Line Task Manager
- **Language/Framework:** Pure Python 3.12 (Standard Library)
- **Features:** Add, view, complete, and delete tasks with strictly incrementing IDs, input validation against non-numeric/empty values, and summary metrics.
- **Run:**
  ```powershell
  py -3.12 assignment-01-task-manager/task_manager.py
  ```

### 2. Assignment 02: Prompt-Driven Agent for Automotive Work Instructions
- **Language/Framework:** Python 3.12, Azure OpenAI (`gpt-4o-mini`, `temperature=0`)
- **Features:** Transforms terse engineering notes into shop-floor Standard Operating Procedures (SOPs) including Safety Precautions, Required Tools & Equipment, Numbered Steps, and Acceptance Criteria without RAG.
- **Run:**
  ```powershell
  py -3.12 assignment-02-work-instructions/work_instruction_agent.py
  ```

### 3. Assignment 03: AI-Powered Meeting Summarizer
- **Language/Framework:** Python 3.12, Azure OpenAI (`gpt-4o-mini`, `temperature=0.3`)
- **Features:** Ingests raw meeting transcripts and generates structured summaries covering Executive Overview, Key Points, Decisions Made, and Action Items (with owners and deadlines). Includes map-reduce chunking for large transcripts and an interactive CLI UI.
- **Run:**
  ```powershell
  py -3.12 assignment-03-meeting-summarizer/meeting_summarizer.py
  ```
