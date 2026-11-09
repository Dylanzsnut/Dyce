"""
Comprehensive Verification and Double-Triple Check Suite for Assignment 06:
- Exact signature and variable presence (CATEGORIES, log_entries, initial_classify, refine_classification, classify_log)
- Heuristic pre-classifier keyword accuracy and edge cases
- Output sanitization & normalization resilience
- Two-stage classification pipeline end-to-end verification
- LLM correction verification (initial misclassification corrected by refinement)
- Dataset and output file integrity
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Add module directory to sys.path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

import log_classifier as lc


def test_signatures_and_constants():
    """Verify all expected functions, constants, and data collections exist."""
    assert hasattr(lc, "CATEGORIES"), "CATEGORIES list missing"
    assert len(lc.CATEGORIES) == 8, f"Expected 8 categories, got {len(lc.CATEGORIES)}"
    for cat in ["Traffic", "Customer Issue", "Vehicle Issue", "Weather", "Sorting/Labeling Error", "Human Error", "Technical System Failure", "Other"]:
        assert cat in lc.CATEGORIES, f"Missing category: {cat}"

    assert hasattr(lc, "log_entries"), "log_entries list missing"
    assert len(lc.log_entries) == 10, f"Expected 10 log entries, got {len(lc.log_entries)}"

    assert callable(lc.initial_classify), "initial_classify missing"
    assert callable(lc.refine_classification), "refine_classification missing"
    assert callable(lc.classify_log), "classify_log missing"
    print("[PASS] Test 1: Signatures, constants, and datasets verified.")


def test_heuristic_pre_classifier():
    """Verify keyword mapping and edge cases in the heuristic stage."""
    # Direct keyword matches
    assert lc.initial_classify("Heavy traffic ahead") == "Traffic"
    assert lc.initial_classify("Customer not home") == "Customer Issue"
    assert lc.initial_classify("Engine smoking on highway") == "Vehicle Issue"
    assert lc.initial_classify("Severe thunderstorm") == "Weather"
    assert lc.initial_classify("Damaged barcode scan") == "Sorting/Labeling Error"
    assert lc.initial_classify("Driver took a wrong turn") == "Human Error"
    assert lc.initial_classify("Check-in system glitch") == "Technical System Failure"

    # Edge cases
    assert lc.initial_classify("Everything went smoothly") == "Other"
    assert lc.initial_classify("") == "Other"
    assert lc.initial_classify(None) == "Other"
    assert lc.initial_classify(12345) == "Other"
    print("[PASS] Test 2: Heuristic pre-classifier rules and edge cases verified.")


def test_sanitizer_resilience():
    """Verify that verbose LLM outputs are normalized into exact category strings."""
    assert lc.sanitize_category("Traffic") == "Traffic"
    assert lc.sanitize_category("  traffic. ") == "Traffic"
    assert lc.sanitize_category('"Vehicle Issue"') == "Vehicle Issue"
    assert lc.sanitize_category("**Weather**") == "Weather"
    assert lc.sanitize_category("`Customer Issue`") == "Customer Issue"
    assert lc.sanitize_category("The most appropriate category is Weather.") == "Weather"
    assert lc.sanitize_category("Predicted Category: Technical System Failure") == "Technical System Failure"
    assert lc.sanitize_category("Completely unrecognized nonsense") == "Other"
    assert lc.sanitize_category(None) == "Other"
    print("[PASS] Test 3: Output sanitizer and normalizer verified.")


def test_ten_sample_logs_classification():
    """Verify that all 10 sample logs classify into their expected ground truth categories."""
    expected = [
        ("Driver reported heavy traffic on highway due to construction", "Traffic"),
        ("Package not accepted, customer unavailable at given time", "Customer Issue"),
        ("Vehicle engine failed during route, replacement dispatched", "Vehicle Issue"),
        ("Unexpected rainstorm delayed loading at warehouse", "Weather"),
        ("Sorting label missing, required manual barcode scan", "Sorting/Labeling Error"),
        ("Driver took a wrong turn and had to reroute", "Human Error"),
        ("No issue reported, arrived on time", "Other"),
        ("Address was incorrect, customer unreachable", "Customer Issue"),
        ("System glitch during check-in at loading dock", "Technical System Failure"),
        ("Road accident caused a long halt near delivery point", "Traffic"),
    ]

    for log_text, expected_category in expected:
        res = lc.classify_log(log_text)
        assert isinstance(res, dict)
        assert res["log"] == log_text
        assert res["final"] == expected_category, f"Log: '{log_text}' -> Expected: {expected_category}, Got: {res['final']}"

    # Test pipeline with empty/None/whitespace inputs
    assert lc.classify_log("") == {"log": "", "initial": "Other", "final": "Other"}
    assert lc.classify_log("   ") == {"log": "   ", "initial": "Other", "final": "Other"}
    assert lc.classify_log(None) == {"log": None, "initial": "Other", "final": "Other"}

    print("[PASS] Test 4: All 10 course sample log entries and extreme edge cases classified correctly.")


def test_llm_refinement_mock_correction():
    """Verify that LLM refinement corrects a miscategorized or unmatched initial label."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Weather"))]
    mock_client.chat.completions.create.return_value = mock_response

    # Ambiguous log entry where initial heuristic produces 'Other'
    log_text = "Severe atmospheric flash flooding washed out the loading bay"
    initial = lc.initial_classify(log_text)
    assert initial == "Other", "Initial heuristic should default to Other"

    res = lc.classify_log(log_text, active_client=mock_client)
    assert res["initial"] == "Other"
    assert res["final"] == "Weather"

    # Verify that the client was called with temperature 0
    call_kwargs = mock_client.chat.completions.create.call_args[1]
    assert call_kwargs["temperature"] == 0
    assert "logistics assistant" in call_kwargs["messages"][0]["content"]
    print("[PASS] Test 5: LLM refinement layer and temperature=0 correction verified.")


def test_exported_artifacts_and_dataset():
    """Verify that dataset.csv, classification_results.md, and documentation files exist."""
    dataset_csv = SCRIPT_DIR / "dataset.csv"
    assert dataset_csv.exists(), "dataset.csv missing"
    assert len(dataset_csv.read_text(encoding="utf-8").strip().splitlines()) == 11  # header + 10 rows

    res_md = SCRIPT_DIR / "classification_results.md"
    assert res_md.exists(), "classification_results.md missing"
    res_text = res_md.read_text(encoding="utf-8")
    assert "Traffic" in res_text and "Customer Issue" in res_text

    res_csv = SCRIPT_DIR / "classification_results.csv"
    assert res_csv.exists(), "classification_results.csv missing"

    assert (SCRIPT_DIR / "prompts.md").exists(), "prompts.md missing"
    assert (SCRIPT_DIR / "GENERATION_PROMPT.md").exists(), "GENERATION_PROMPT.md missing"
    print("[PASS] Test 6: Artifacts, dataset CSV, and documentation files verified.")


if __name__ == "__main__":
    print("=" * 65)
    print("  RUNNING COMPREHENSIVE VERIFICATION SUITE: ASSIGNMENT 06")
    print("=" * 65)
    test_signatures_and_constants()
    test_heuristic_pre_classifier()
    test_sanitizer_resilience()
    test_ten_sample_logs_classification()
    test_llm_refinement_mock_correction()
    test_exported_artifacts_and_dataset()
    print("=" * 65)
    print("  ALL 6 TESTS PASSED! ASSIGNMENT 06 IS FULLY VERIFIED.")
    print("=" * 65)
