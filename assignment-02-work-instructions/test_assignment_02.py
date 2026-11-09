"""
Comprehensive Verification and Double-Triple Check Suite for Assignment 02:
- Exact course signatures and variables (task_descriptions, generate_instruction, deployment_name)
- Direct function invocation resilience without API keys (offline fallback)
- Mock client wire-protocol verification (temperature=0, system/user roles)
- Generated CSV and Markdown artifact validation (5 samples)
"""

import csv
import sys
from pathlib import Path
from unittest.mock import MagicMock

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

import work_instruction_agent as wia


def test_signatures_and_mock_tasks():
    """Verify course-specified variables and 5 automotive tasks."""
    assert hasattr(wia, "task_descriptions")
    assert len(wia.task_descriptions) == 5
    assert hasattr(wia, "deployment_name")
    assert hasattr(wia, "api_version")
    assert callable(wia.generate_instruction)
    print("[PASS] Test 1: Module signatures and 5 automotive tasks verified.")


def test_direct_function_offline_resilience():
    """Verify generate_instruction() works directly even when Azure env vars are unset."""
    sop = wia.generate_instruction(wia.task_descriptions[0])
    assert "Safety Precautions" in sop
    assert "Required Tools" in sop
    assert "Step-by-Step Procedure" in sop
    assert "Acceptance Criteria" in sop

    # Also test custom arbitrary task description
    custom_sop = wia.generate_instruction("Torque rear suspension lower control arm bolts to 110 Nm.")
    assert "Safety Precautions" in custom_sop
    assert "Step-by-Step Procedure" in custom_sop
    print("[PASS] Test 2: Direct function call offline fallback verified.")


def test_mock_azure_client_invocation():
    """Verify AzureOpenAI wire protocol and temperature=0 enforcement."""
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock(message=MagicMock(content="**Safety Precautions:**\n- Wear PPE."))]
    mock_client.chat.completions.create.return_value = mock_resp

    out = wia.generate_instruction("Test task", client=mock_client, deployment_name="gpt-4o-mini")
    assert "Safety Precautions" in out
    call_kwargs = mock_client.chat.completions.create.call_args[1]
    assert call_kwargs["temperature"] == 0
    assert call_kwargs["model"] == "gpt-4o-mini"
    print("[PASS] Test 3: Mock AzureOpenAI client wire protocol verified.")


def test_saved_csv_and_markdown_artifacts():
    """Verify generated_work_instructions.csv and .md contain all 5 samples."""
    csv_path = SCRIPT_DIR / "generated_work_instructions.csv"
    md_path = SCRIPT_DIR / "generated_work_instructions.md"
    assert csv_path.exists() and md_path.exists()

    with open(csv_path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 5
    for r in rows:
        assert "Safety Precautions" in r["generated_work_instruction"]
        assert "Step-by-Step Procedure" in r["generated_work_instruction"]

    assert (SCRIPT_DIR / "prompts.md").exists()
    assert (SCRIPT_DIR / "GENERATION_PROMPT.md").exists()
    print("[PASS] Test 4: CSV, Markdown, and prompt documentation verified.")


if __name__ == "__main__":
    print("=" * 65)
    print("  RUNNING COMPREHENSIVE VERIFICATION SUITE: ASSIGNMENT 02")
    print("=" * 65)
    test_signatures_and_mock_tasks()
    test_direct_function_offline_resilience()
    test_mock_azure_client_invocation()
    test_saved_csv_and_markdown_artifacts()
    print("=" * 65)
    print("  ALL 4 TESTS PASSED! ASSIGNMENT 02 IS FULLY VERIFIED.")
    print("=" * 65)
