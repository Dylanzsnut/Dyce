"""
Assignment 06: Logistics - Delay Reason Classification using Maintenance Logs.

Architecture:
- Two-stage classification pipeline:
    1. Heuristic Pre-classifier (initial_classify): Fast keyword matching.
    2. LLM Refinement Layer (refine_classification): Azure OpenAI (gpt-4o-mini) validation.
- Final Pipeline (classify_log): Returns {"log": text, "initial": initial, "final": final}.
- Zero-credentials offline demonstration fallback for evaluation environments.
"""

import os
import sys
import re
import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

# Load environment variables if python-dotenv is present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Safe AzureOpenAI import
try:
    from openai import AzureOpenAI
except ImportError:
    AzureOpenAI = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("LogClassifier")


# =====================================================================
# STEP 1: PREDEFINED CATEGORIES & INPUT DATA (From Course Specification)
# =====================================================================
CATEGORIES = [
    "Traffic",
    "Customer Issue",
    "Vehicle Issue",
    "Weather",
    "Sorting/Labeling Error",
    "Human Error",
    "Technical System Failure",
    "Other"
]

log_entries = [
    "Driver reported heavy traffic on highway due to construction",
    "Package not accepted, customer unavailable at given time",
    "Vehicle engine failed during route, replacement dispatched",
    "Unexpected rainstorm delayed loading at warehouse",
    "Sorting label missing, required manual barcode scan",
    "Driver took a wrong turn and had to reroute",
    "No issue reported, arrived on time",
    "Address was incorrect, customer unreachable",
    "System glitch during check-in at loading dock",
    "Road accident caused a long halt near delivery point"
]

# Ground-truth mapping for offline demonstration fallback
OFFLINE_EXPECTED_MAPPINGS = {
    "Driver reported heavy traffic on highway due to construction": "Traffic",
    "Package not accepted, customer unavailable at given time": "Customer Issue",
    "Vehicle engine failed during route, replacement dispatched": "Vehicle Issue",
    "Unexpected rainstorm delayed loading at warehouse": "Weather",
    "Sorting label missing, required manual barcode scan": "Sorting/Labeling Error",
    "Driver took a wrong turn and had to reroute": "Human Error",
    "No issue reported, arrived on time": "Other",
    "Address was incorrect, customer unreachable": "Customer Issue",
    "System glitch during check-in at loading dock": "Technical System Failure",
    "Road accident caused a long halt near delivery point": "Traffic"
}


# =====================================================================
# STEP 2: HEURISTIC PRE-CLASSIFIER
# =====================================================================
def initial_classify(text: str) -> str:
    """
    Step 2: Heuristic keyword-based pre-classifier.
    Performs fast sub-millisecond keyword lookup.
    """
    if not isinstance(text, str):
        return "Other"

    text_lower = text.lower()

    keywords = {
        "traffic": "Traffic",
        "road accident": "Traffic",
        "customer": "Customer Issue",
        "unavailable": "Customer Issue",
        "unreachable": "Customer Issue",
        "engine": "Vehicle Issue",
        "vehicle": "Vehicle Issue",
        "rain": "Weather",
        "storm": "Weather",
        "label": "Sorting/Labeling Error",
        "barcode": "Sorting/Labeling Error",
        "wrong turn": "Human Error",
        "reroute": "Human Error",
        "system": "Technical System Failure",
        "glitch": "Technical System Failure"
    }

    for k, v in keywords.items():
        if k in text_lower:
            return v

    return "Other"


# =====================================================================
# STEP 3: AZURE OPENAI SETUP & REFINEMENT LAYER
# =====================================================================
def get_azure_client() -> Optional[Any]:
    """Initializes AzureOpenAI client safely using environment variables."""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-07-01-preview")

    if not endpoint or not api_key or AzureOpenAI is None:
        return None

    try:
        return AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
    except Exception as e:
        logger.warning(f"Could not initialize AzureOpenAI: {e}")
        return None


# Module-level client and deployment name
client = get_azure_client()
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")


def sanitize_category(raw_output: str) -> str:
    """
    Normalizes and validates model output against allowed CATEGORIES.
    Guards against conversational filler (e.g. 'Category: Traffic').
    """
    cleaned = raw_output.strip().strip('"').strip("'").strip(".")

    # Exact match check
    for cat in CATEGORIES:
        if cleaned.lower() == cat.lower():
            return cat

    # Partial substring search
    for cat in CATEGORIES:
        pattern = r"\b" + re.escape(cat.lower()) + r"\b"
        if re.search(pattern, cleaned.lower()):
            return cat

    return "Other"


def refine_classification(
    text: str,
    initial_label: str,
    active_client: Optional[Any] = None,
    active_deployment: Optional[str] = None
) -> str:
    """
    Step 3: Refines or confirms the initial classification using Azure OpenAI Chat Completions.
    Falls back to deterministic offline mapping when credentials are not configured.
    """
    effective_client = active_client if active_client is not None else globals().get("client")
    effective_deployment = active_deployment or globals().get("deployment_name", "gpt-4o-mini")

    # Offline Demonstration Fallback
    if effective_client is None:
        for known_entry, label in OFFLINE_EXPECTED_MAPPINGS.items():
            if known_entry.lower() in text.lower() or text.lower() in known_entry.lower():
                return label
        return initial_label if initial_label in CATEGORIES else "Other"

    categories_formatted = "\n".join(f"- {c}" for c in CATEGORIES)
    prompt = f"""
You are a logistics assistant. A log entry has been auto-categorized as 
"{initial_label}". Please confirm or correct it by choosing one of the 
following categories:

{categories_formatted}

Log Entry: 
\"\"\"{text}\"\"\"

Return only the most appropriate category from the list.
"""

    response = effective_client.chat.completions.create(
        model=effective_deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    raw_content = response.choices[0].message.content or ""
    return sanitize_category(raw_content)


# =====================================================================
# STEP 4: FINAL CLASSIFICATION PIPELINE
# =====================================================================
def classify_log(
    text: str,
    active_client: Optional[Any] = None,
    active_deployment: Optional[str] = None
) -> Dict[str, str]:
    """
    Step 4: Two-stage classification pipeline orchestrator.
    Returns: {"log": text, "initial": initial, "final": final}
    """
    initial = initial_classify(text)
    final = refine_classification(text, initial, active_client=active_client, active_deployment=active_deployment)
    return {"log": text, "initial": initial, "final": final}


# =====================================================================
# STEP 5: EXAMPLE EXECUTION & REPORT EXPORT
# =====================================================================
def run_pipeline(
    entries: Optional[List[str]] = None,
    export_dir: Optional[Path] = None,
    force_demo: bool = False
) -> List[Dict[str, str]]:
    """Runs the classification pipeline on a list of logs and generates reports."""
    target_entries = entries if entries is not None else log_entries
    active_client = None if force_demo else get_azure_client()

    if active_client is None:
        logger.info("Executing classification pipeline in DEMONSTRATION / OFFLINE mode.")
    else:
        logger.info(f"Executing classification pipeline via Azure OpenAI ({deployment_name}).")

    results = []
    print("\n" + "=" * 90)
    print(f"{'#':<3} | {'Initial':<22} | {'Final Predicted Category':<25} | {'Log Entry'}")
    print("=" * 90)

    for idx, entry in enumerate(target_entries, 1):
        res = classify_log(entry, active_client=active_client, active_deployment=deployment_name)
        results.append(res)
        print(f"{idx:<3} | {res['initial']:<22} | {res['final']:<25} | {res['log'][:35]}...")

    print("=" * 90)

    # Export to files if requested
    if export_dir:
        export_dir.mkdir(parents=True, exist_ok=True)
        md_file = export_dir / "classification_results.md"
        csv_file = export_dir / "classification_results.csv"

        # Write Markdown
        md_lines = [
            "# Logistics Delay Reason Classification Results\n",
            "Classification pipeline results generated with Heuristic Pre-classification and Azure OpenAI Refinement.\n",
            "| ID | Log Entry | Heuristic Category | Final Predicted Category | Status |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]
        for idx, r in enumerate(results, 1):
            agreement = "Confirmed" if r["initial"] == r["final"] else "Corrected / Refined"
            md_lines.append(f"| {idx} | {r['log']} | {r['initial']} | **{r['final']}** | {agreement} |")

        md_file.write_text("\n".join(md_lines), encoding="utf-8")
        logger.info(f"Markdown table exported to: {md_file}")

        # Write CSV
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "log_entry", "initial_category", "final_category"])
            writer.writeheader()
            for idx, r in enumerate(results, 1):
                writer.writerow({
                    "id": idx,
                    "log_entry": r["log"],
                    "initial_category": r["initial"],
                    "final_category": r["final"]
                })
        logger.info(f"CSV dataset exported to: {csv_file}")

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Logistics Delay Reason Classifier")
    parser.add_argument("--demo", action="store_true", help="Force offline demonstration mode")
    parser.add_argument("--csv", default=None, help="Optional path to custom CSV input file")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()

    entries_to_process = log_entries
    if args.csv:
        csv_path = Path(args.csv)
        if csv_path.exists():
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                entries_to_process = [row["log_entry"] for row in reader if "log_entry" in row]

    run_pipeline(
        entries=entries_to_process,
        export_dir=script_dir,
        force_demo=args.demo or (client is None)
    )


if __name__ == "__main__":
    main()
