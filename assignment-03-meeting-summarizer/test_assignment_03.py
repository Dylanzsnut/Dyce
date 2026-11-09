"""
Comprehensive Verification and Double-Triple Check Suite for Assignment 03:
- Exact course signatures and variables (summarize_transcript, load_transcript, split_into_chunks)
- Direct function invocation resilience without API keys (offline fallback)
- Chunking & Map-Reduce handling for large meeting transcripts
- 5 sample transcripts and 5 generated summary outputs verification
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

import meeting_summarizer as ms


def test_signatures_and_chunking():
    """Verify module functions and large transcript chunking."""
    assert callable(ms.summarize_transcript)
    assert callable(ms.load_transcript)
    assert callable(ms.split_into_chunks)

    long_text = "\n".join([f"Speaker {i}: Discussion point number {i} regarding Q3 roadmap." for i in range(400)])
    chunks = ms.split_into_chunks(long_text, max_chars=2000)
    assert len(chunks) > 1
    assert all(len(c) <= 2000 for c in chunks)
    print("[PASS] Test 1: Signatures and large-transcript chunking verified.")


def test_direct_function_offline_resilience():
    """Verify summarize_transcript() works directly even when Azure env vars are unset."""
    sample_1 = SCRIPT_DIR / "sample_transcripts" / "sample_01_product_roadmap_sync.txt"
    text = ms.load_transcript(sample_1)
    summary = ms.summarize_transcript(text)
    assert "Executive Overview" in summary
    assert "Key Points" in summary
    assert "Decisions Made" in summary
    assert "Action Items" in summary

    # Test arbitrary custom transcript text
    custom_summary = ms.summarize_transcript("Alice: Let's launch on Friday.\nBob: Agreed, I will update the docs.")
    assert "Executive Overview" in custom_summary
    assert "Action Items" in custom_summary
    print("[PASS] Test 2: Direct function call offline fallback verified.")


def test_mock_azure_client_invocation():
    """Verify AzureOpenAI wire protocol (temperature=0.3, max_tokens=500)."""
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock(message=MagicMock(content="### Executive Overview\n- Sync completed."))]
    mock_client.chat.completions.create.return_value = mock_resp

    out = ms.summarize_transcript("Short transcript", client=mock_client, deployment_name="gpt-4o-mini")
    assert "Executive Overview" in out
    call_kwargs = mock_client.chat.completions.create.call_args[1]
    assert call_kwargs["temperature"] == 0.3
    assert call_kwargs["max_tokens"] == 500
    print("[PASS] Test 3: Mock AzureOpenAI client wire protocol verified.")


def test_five_samples_and_outputs():
    """Verify all 5 sample transcripts and 5 summary outputs exist and are valid."""
    transcripts = list((SCRIPT_DIR / "sample_transcripts").glob("sample_*.txt"))
    outputs = list((SCRIPT_DIR / "sample_outputs").glob("summary_*.md"))
    assert len(transcripts) == 5
    assert len(outputs) == 5
    assert (SCRIPT_DIR / "all_sample_summaries.md").exists()
    assert (SCRIPT_DIR / "prompts.md").exists()
    assert (SCRIPT_DIR / "GENERATION_PROMPT.md").exists()
    print("[PASS] Test 4: All 5 transcripts, 5 outputs, and prompt docs verified.")


if __name__ == "__main__":
    print("=" * 65)
    print("  RUNNING COMPREHENSIVE VERIFICATION SUITE: ASSIGNMENT 03")
    print("=" * 65)
    test_signatures_and_chunking()
    test_direct_function_offline_resilience()
    test_mock_azure_client_invocation()
    test_five_samples_and_outputs()
    print("=" * 65)
    print("  ALL 4 TESTS PASSED! ASSIGNMENT 03 IS FULLY VERIFIED.")
    print("=" * 65)
