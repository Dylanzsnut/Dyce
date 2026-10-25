# AI-Powered Meeting Summarizer Using Azure OpenAI API

A functional, production-ready Python application that ingests raw meeting transcripts and leverages Azure OpenAI's GPT models to produce structured, concise summaries highlighting **Executive Overview**, **Key Points**, **Decisions Made**, and **Action Items** with assigned owners and deadlines.

---

## 1. Project Overview & Features

- **Azure OpenAI Integration:** Uses the official `openai` Python SDK with `AzureOpenAI` client, configured via environment variables or a `.env` file.
- **Structured Prompt Design:** Prompts GPT models (`gpt-4o-mini`) with a dedicated system role and structured output format to reliably capture:
  1. **Executive Overview:** High-level summary of meeting goals and key results.
  2. **Key Points:** In-depth breakdown of metrics, technical trade-offs, and discussion points.
  3. **Decisions Made:** Explicit commitments and consensus reached by attendees.
  4. **Action Items:** Itemized next steps with explicit owners and due dates (`[Owner]: Task (Due: Date)`).
- **Large Transcript Handling (Map-Reduce Chunking):** Automatically splits transcripts exceeding context thresholds along paragraph boundaries and summarizes them via a multi-stage map-reduce pass.
- **Multiple Execution Modes:**
  - **Batch Mode (Default):** Processes all 5 included sample transcripts and exports individual Markdown reports into `sample_outputs/` and a consolidated `all_sample_summaries.md`.
  - **Single File Mode (`--file`):** Ingests any custom `.txt` meeting transcript and outputs the summary to terminal or a file (`--output`).
  - **Interactive CLI UI (`--interactive`):** Presents an interactive menu allowing users to select sample files, input custom file paths, or run batch operations.

---

## 2. Directory Structure

```text
assignment-03-meeting-summarizer/
├── .env.example                               # Template for Azure OpenAI credentials
├── requirements.txt                           # Python dependencies (openai, python-dotenv)
├── meeting_summarizer.py                      # Main application script
├── README.md                                  # Documentation and run instructions
├── all_sample_summaries.md                    # Consolidated view of 5 transcripts + outputs
├── sample_transcripts/                        # 5 realistic, multi-speaker test transcripts
│   ├── sample_01_product_roadmap_sync.txt
│   ├── sample_02_sprint_retrospective.txt
│   ├── sample_03_incident_postmortem.txt
│   ├── sample_04_client_onboarding_kickoff.txt
│   └── sample_05_marketing_launch_planning.txt
└── sample_outputs/                            # 5 generated structured summary outputs
    ├── summary_01_product_roadmap_sync.md
    ├── summary_02_sprint_retrospective.md
    ├── summary_03_incident_postmortem.md
    ├── summary_04_client_onboarding_kickoff.md
    └── summary_05_marketing_launch_planning.md
```

---

## 3. Environment Setup & Configuration

### Prerequisites
- Python 3.12+ installed
- Azure OpenAI Resource with an active deployment (e.g. `gpt-4o-mini`)

### Install Dependencies
```powershell
py -3.12 -m pip install -r requirements.txt
```

### Configure Credentials
Copy `.env.example` to `.env` in this directory:
```ini
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-07-01-preview
```

Alternatively, set environment variables directly in PowerShell:
```powershell
$env:AZURE_OPENAI_API_KEY="your_api_key"
$env:AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
```

---

## 4. How to Run

### Option A: Batch Process All 5 Sample Transcripts (Default)
```powershell
py -3.12 meeting_summarizer.py
```
This runs all 5 sample transcripts, prints the summaries to terminal, and writes individual markdown files to `sample_outputs/` as well as `all_sample_summaries.md`.

### Option B: Summarize a Specific Transcript File
```powershell
py -3.12 meeting_summarizer.py --file sample_transcripts/sample_01_product_roadmap_sync.txt
```
To save the output directly to a file:
```powershell
py -3.12 meeting_summarizer.py --file sample_transcripts/sample_01_product_roadmap_sync.txt --output my_summary.md
```

### Option C: Interactive Command-Line Interface
```powershell
py -3.12 meeting_summarizer.py --interactive
```
Launches an interactive menu to browse and summarize transcripts step-by-step.

---

## 5. Sample Transcripts & Example Outputs (5 Samples)

| # | Sample Meeting Topic | Input Transcript | Example Summary Output |
| :---: | :--- | :--- | :--- |
| **1** | Q4 AI Product Roadmap & Translation Scope | [`sample_01_product_roadmap_sync.txt`](sample_transcripts/sample_01_product_roadmap_sync.txt) | [`summary_01_product_roadmap_sync.md`](sample_outputs/summary_01_product_roadmap_sync.md) |
| **2** | Engineering Sprint 14 Retro & CI/CD Bottlenecks | [`sample_02_sprint_retrospective.txt`](sample_transcripts/sample_02_sprint_retrospective.txt) | [`summary_02_sprint_retrospective.md`](sample_outputs/summary_02_sprint_retrospective.md) |
| **3** | SEV-2 Payment Gateway Latency Post-Mortem | [`sample_03_incident_postmortem.txt`](sample_transcripts/sample_03_incident_postmortem.txt) | [`summary_03_incident_postmortem.md`](sample_outputs/summary_03_incident_postmortem.md) |
| **4** | Enterprise Healthcare Client Onboarding Kickoff | [`sample_04_client_onboarding_kickoff.txt`](sample_transcripts/sample_04_client_onboarding_kickoff.txt) | [`summary_04_client_onboarding_kickoff.md`](sample_outputs/summary_04_client_onboarding_kickoff.md) |
| **5** | Mobile App 3.0 Marketing Launch Planning | [`sample_05_marketing_launch_planning.txt`](sample_transcripts/sample_05_marketing_launch_planning.txt) | [`summary_05_marketing_launch_planning.md`](sample_outputs/summary_05_marketing_launch_planning.md) |

Refer to [`all_sample_summaries.md`](all_sample_summaries.md) to inspect all 5 full transcripts and generated summaries in a single document.
