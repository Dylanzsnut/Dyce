"""
Assignment 02: Prompt-Driven Agent for Generating Work Instructions for New Car Models
--------------------------------------------------------------------------------------
Generates standardized, step-by-step shop-floor work instructions from high-level
automotive engineering notes using Azure OpenAI and structured prompt engineering
(without Retrieval-Augmented Generation).

Required Environment Variables:
- AZURE_OPENAI_API_KEY: Your Azure OpenAI resource API key
- AZURE_OPENAI_ENDPOINT: Your Azure OpenAI resource endpoint URL
- AZURE_OPENAI_DEPLOYMENT_NAME: Model deployment name (defaults to 'gpt-4o-mini')
"""

import argparse
import csv
import os
import sys
from pathlib import Path
from openai import AzureOpenAI, OpenAIError

try:
    from dotenv import load_dotenv

    # Load .env from the script's own folder regardless of current working directory,
    # plus fallback to the current working directory if present.
    load_dotenv(Path(__file__).resolve().parent / ".env")
    load_dotenv()
except ImportError:
    pass


# Step 1: Mock Input Data (5 Engineering Notes from Assignment Specification)
MOCK_TASKS = [
    {
        "id": 1,
        "task_description": (
            "Install the battery module in the rear compartment, connect to the "
            "high-voltage harness, and verify torque on fasteners."
        ),
    },
    {
        "id": 2,
        "task_description": (
            "Calibrate the ADAS (Advanced Driver Assistance Systems) radar sensors on "
            "the front bumper using factory alignment targets."
        ),
    },
    {
        "id": 3,
        "task_description": (
            "Apply anti-corrosion sealant to all exposed welds on the door panels "
            "before painting."
        ),
    },
    {
        "id": 4,
        "task_description": (
            "Perform leak test on coolant system after radiator installation. Record "
            "pressure readings and verify against specifications."
        ),
    },
    {
        "id": 5,
        "task_description": (
            "Program the infotainment ECU with the latest software package and "
            "validate connectivity with dashboard display."
        ),
    },
]

# Flat list matching the exact variable name in Section 6 of the assignment guide
task_descriptions = [item["task_description"] for item in MOCK_TASKS]

SYSTEM_PROMPT = (
    "You are an expert automotive manufacturing supervisor and process engineer. "
    "Your job is to convert high-level engineering notes for new car models into "
    "standardized, shop-floor-ready Standard Operating Procedures (SOPs). "
    "Always write clearly, concisely, and consistently without assuming external "
    "documents, using numbered procedural steps alongside explicit safety reminders, "
    "required tools/equipment, and acceptance criteria."
)


# Step 2: Azure OpenAI Client Setup
def create_azure_client():
    """Initialize and return the AzureOpenAI client and deployment name from env vars."""
    api_key = (os.getenv("AZURE_OPENAI_API_KEY") or "").strip()
    endpoint = (os.getenv("AZURE_OPENAI_ENDPOINT") or "").strip()
    api_version = (os.getenv("AZURE_OPENAI_API_VERSION") or "2024-07-01-preview").strip()
    deployment_name = (os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") or "gpt-4o-mini").strip()

    missing = []
    if not api_key:
        missing.append("AZURE_OPENAI_API_KEY")
    if not endpoint:
        missing.append("AZURE_OPENAI_ENDPOINT")

    if missing:
        raise EnvironmentError(
            f"Missing required environment variable(s): {', '.join(missing)}.\n"
            "Please set them in your terminal or create a .env file based on .env.example."
        )

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )
    return client, deployment_name


def build_user_prompt(task, target_role="Assembly Line Worker / Technician"):
    """Construct a structured prompt with few-shot guidance for consistent shop-floor output."""
    return f"""Generate detailed, step-by-step work instructions for the following new car model manufacturing task.
Target Audience: {target_role}

Follow these formatting rules strictly:
1. **Safety Precautions:** List mandatory PPE and hazard controls before starting work.
2. **Required Tools & Equipment:** List tools, gauges, consumables, or diagnostic devices needed.
3. **Step-by-Step Procedure:** Provide clear, numbered action steps (1, 2, 3, ...) written in imperative shop-floor language.
4. **Acceptance Criteria & Quality Check:** Specify verification checks and sign-off/logging requirements.

Example Input Task:
\"\"\"Mount the front brake caliper assembly onto the steering knuckle, connect the brake hose, and verify bolt torque.\"\"\"

Example Output Style:
**Safety Precautions:**
- Ensure vehicle is securely supported on lift locks and wear safety glasses, cut-resistant mechanics gloves, and steel-toe footwear.

**Required Tools & Equipment:**
- Calibrated digital torque wrench, socket set, brake hose line wrench, torque witness marker, MES/logbook terminal.

**Step-by-Step Procedure:**
1. Inspect the steering knuckle mounting bosses, brake rotor surface, and caliper guide pins for cleanliness or damage.
2. Position the front brake caliper assembly over the brake rotor without twisting or straining the flexible brake hose.
3. Thread upper and lower caliper mounting bolts by hand, then tighten to factory torque specifications using a calibrated torque wrench.
4. Route and secure the brake hose bracket, tighten the banjo bolt with new copper washers to specified torque, and apply witness marks.
5. Verify rotor spins freely without drag and record fastener torque values in the station logbook.

**Acceptance Criteria & Quality Check:**
- Caliper seated squarely with zero hose twist; mounting and banjo bolts within torque tolerance with witness marks applied; zero fluid leaks.

---
Now generate the work instructions for this task:
Task:
\"\"\"{task.strip()}\"\"\"

Work Instructions:
"""


def generate_instruction(
    task,
    client=None,
    deployment_name=None,
    target_role="Assembly Line Worker / Technician",
):
    """
    Generate step-by-step automotive work instructions for a single task description
    using Azure OpenAI Chat Completions.
    """
    if not isinstance(task, str) or not task.strip():
        raise ValueError("Task description must be a non-empty string.")

    if client is None or deployment_name is None:
        client, deployment_name = create_azure_client()

    prompt = build_user_prompt(task=task, target_role=target_role)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    content = response.choices[0].message.content or ""
    return content.strip()


def save_outputs(results, markdown_path, csv_path):
    """Save all task descriptions and generated instructions to Markdown and CSV files."""
    # Write CSV file
    with open(csv_path, mode="w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["id", "task_description", "generated_work_instruction"],
        )
        writer.writeheader()
        writer.writerows(results)

    # Write Markdown file with both summary table and full formatted cards
    lines = [
        "# Generated Automotive Work Instructions (5 Samples)\n",
        "Generated by `work_instruction_agent.py` using Azure OpenAI (`temperature=0`).\n",
        "## Summary Table\n",
        "| ID | Mock Task Description | Generated Work Instruction |",
        "| :---: | :--- | :--- |",
    ]

    for row in results:
        escaped_desc = row["task_description"].replace("|", "\\|")
        inline_instr = (
            row["generated_work_instruction"]
            .replace("|", "\\|")
            .replace("\r\n", "<br>")
            .replace("\n", "<br>")
        )
        lines.append(f"| {row['id']} | {escaped_desc} | {inline_instr} |")

    lines.append("\n---\n")
    lines.append("## Detailed Shop-Floor Work Instructions\n")

    for row in results:
        lines.append(f"### Sample {row['id']}")
        lines.append(f"**Engineering Note / Task Description:**  \n> {row['task_description']}\n")
        lines.append(f"{row['generated_work_instruction']}\n")
        lines.append("---\n")

    with open(markdown_path, mode="w", encoding="utf-8") as md_file:
        md_file.write("\n".join(lines))


# Step 3: Example Run / CLI Entry Point
def main():
    parser = argparse.ArgumentParser(
        description="Prompt-Driven Agent for Generating Automotive Work Instructions"
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Optional custom engineering task description to generate instructions for.",
    )
    parser.add_argument(
        "--role",
        type=str,
        default="Assembly Line Worker / Technician",
        help="Target shop-floor role (e.g., 'Assembly Line Worker', 'Technician', 'Quality Inspector').",
    )
    args = parser.parse_args()

    try:
        client, deployment_name = create_azure_client()
    except EnvironmentError as env_err:
        print(f"Configuration Error:\n{env_err}", file=sys.stderr)
        sys.exit(1)

    # Single custom task mode
    if args.task:
        try:
            instructions = generate_instruction(
                args.task,
                client=client,
                deployment_name=deployment_name,
                target_role=args.role,
            )
            print(f"\nTask: {args.task}\n\nWork Instructions:\n{instructions}\n")
        except (OpenAIError, ValueError) as err:
            print(f"Error generating instructions: {err}", file=sys.stderr)
            sys.exit(1)
        return

    # Default batch mode: Process all 5 mock engineering tasks from the assignment
    output_dir = Path(__file__).resolve().parent
    md_output_path = output_dir / "generated_work_instructions.md"
    csv_output_path = output_dir / "generated_work_instructions.csv"

    results = []
    print(f"Generating work instructions for {len(MOCK_TASKS)} mock tasks...\n")

    for item in MOCK_TASKS:
        task_id = item["id"]
        task_text = item["task_description"]
        try:
            instructions = generate_instruction(
                task_text,
                client=client,
                deployment_name=deployment_name,
                target_role=args.role,
            )
            print(f"=== Task {task_id}: {task_text} ===")
            print(f"Work Instructions:\n{instructions}\n")
            results.append(
                {
                    "id": task_id,
                    "task_description": task_text,
                    "generated_work_instruction": instructions,
                }
            )
        except OpenAIError as api_err:
            print(f"Azure OpenAI API error on Task {task_id}: {api_err}", file=sys.stderr)
            sys.exit(1)

    save_outputs(results, md_output_path, csv_output_path)
    print(f"Saved Markdown table & instructions to: {md_output_path}")
    print(f"Saved CSV table to: {csv_output_path}")


if __name__ == "__main__":
    main()
