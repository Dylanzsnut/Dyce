# Prompt-Driven Agent for Generating Work Instructions for New Car Models

An AI-powered assistant built with Python and **Azure OpenAI (`AzureOpenAI`)** that transforms high-level automotive engineering notes into standardized, shop-floor-ready work instructions using pure **prompt engineering** (without Retrieval-Augmented Generation).

---

## 1. Approach & Prompt Engineering Design

1. **System Persona (`SYSTEM_PROMPT`):**
   - Assigns the LLM the role of an *expert automotive manufacturing supervisor and process engineer*, constraining tone and vocabulary to clear, imperative shop-floor Standard Operating Procedures (SOPs).
2. **One-Shot Structured User Prompt (`build_user_prompt`):**
   - Uses a one-shot example and explicit structural rules so every generated work instruction consistently includes four shop-floor sections:
     1. **Safety Precautions** (PPE, Lockout/Tagout, hazard controls)
     2. **Required Tools & Equipment**
     3. **Step-by-Step Procedure** (numbered imperative steps)
     4. **Acceptance Criteria & Quality Check**
3. **Deterministic & Customizable Generation (`generate_instruction`):**
   - Uses `temperature=0` so identical engineering inputs yield consistent, repeatable instructions across runs.
   - Accepts a customizable `target_role` parameter (e.g., *Assembly Line Worker*, *Technician*, or *Quality Inspector*) via CLI (`--role`) or function call.

---

## 2. Environment Setup

### Install Dependencies
```powershell
py -3.12 -m pip install -r requirements.txt
```

### Configure Azure OpenAI Environment Variables
Copy `.env.example` to `.env` (or export environment variables directly in PowerShell):
```powershell
$env:AZURE_OPENAI_API_KEY="your_api_key"
$env:AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
```

---

## 3. How to Run

### Generate Instructions for All 5 Mock Car Model Tasks
```powershell
py -3.12 work_instruction_agent.py
```
This runs all 5 mock engineering tasks from the assignment and automatically saves:
- `generated_work_instructions.md` — Formatted Markdown table + detailed shop-floor cards for all 5 samples
- `generated_work_instructions.csv` — Structured CSV table of all 5 task descriptions and generated instructions

### Optional: Customize Role or Test a Custom Task
```powershell
py -3.12 work_instruction_agent.py --role "Quality Inspector" --task "Inspect panoramic sunroof seal alignment and perform water-spray booth test."
```

---

## 4. Reflection: Standardizing & Accelerating Automotive Work Instructions with Prompt-Driven AI Agents

When automotive manufacturers introduce a new vehicle platform or model-year refresh, hundreds of assembly, calibration, sealing, and ECU-flashing stations require updated Standard Operating Procedures (SOPs). Historically, converting terse engineering change notices (ECNs) into shop-floor instructions requires manual drafting across manufacturing engineering, EHS (safety), and quality teams—leading to bottlenecks, inconsistent formatting across stations, and omitted safety or verification steps.

A **prompt-driven LLM agent** addresses both speed and standardization:
- **Consistent Structure Across Every Station:** By embedding mandatory sections (*Safety Precautions*, *Required Tools*, *Numbered Steps*, and *Acceptance Criteria*) alongside a one-shot canonical example and `temperature=0`, every station receives uniform, easy-to-scan instructions regardless of who wrote the original engineering note.
- **Rapid First-Draft Turnaround:** Process engineers can generate complete first-draft SOPs for dozens of stations in seconds rather than days, shifting human effort from repetitive formatting to high-value engineering review and torque/tolerance verification.
- **Role-Based Customization Without Rewriting:** By adjusting prompt parameters (such as targeting an *Assembly Line Operator* vs. a *Quality Inspector*), the same engineering note can immediately produce role-appropriate instructions tailored to assembly execution or final audit checks.
- **Human-in-the-Loop Governance:** Because a pure prompt-driven agent (without RAG) does not pull exact proprietary numeric specs (such as model-specific Newton-meter torque figures or psi limits) from an engineering database, pairing AI-generated procedural drafts with a final human engineer sign-off ensures both rapid authoring and strict manufacturing compliance.
