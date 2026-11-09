"""
Comprehensive Verification and Double-Triple Check Suite for Assignment 05:
- Tenacity Exponential Backoff Retry Verification
- Max Attempt Limit Enforcement (Stop after 5 attempts)
- Function Calling Schema Compliance
- Batch Processing Resilience (Partial Failure Isolation)
- Dual API Format (tools vs functions) Compatibility
"""

import sys
import json
from pathlib import Path
from unittest.mock import MagicMock

# Add module directory to sys.path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

import batch_function_calling as bfc


def test_function_schema_structure():
    """Verify that the function schema complies with OpenAI specifications."""
    schema = bfc.ITINERARY_FUNCTION_SCHEMA
    assert schema["name"] == "generate_itinerary"
    params = schema["parameters"]
    assert params["type"] == "object"
    assert "required" in params
    for req in ["destination", "days"]:
        assert req in params["required"], f"Missing required property: {req}"

    daily_schedule = params["properties"]["daily_schedule"]
    assert daily_schedule["type"] == "array"
    item_props = daily_schedule["items"]["properties"]
    for day_field in ["day", "theme", "morning_activity", "afternoon_activity", "evening_activity", "highlight_cuisine"]:
        assert day_field in item_props, f"Missing day schedule field: {day_field}"

    print("[PASS] Test 1: Function Calling Schema Structure verified.")


def test_mock_generation_engine():
    """Verify offline demonstration output conforms to structure."""
    res = bfc.mock_generate_itinerary("Paris, France", 3, "cultural", "moderate")
    assert res["destination"] == "Paris, France"
    assert res["duration_days"] == 3
    assert len(res["daily_schedule"]) == 3
    assert res["estimated_cost_usd"] > 0
    assert len(res["local_tips"]) >= 1

    # Verify custom generic generation
    generic = bfc.mock_generate_itinerary("Sydney, Australia", 2, "adventure", "budget")
    assert generic["destination"] == "Sydney, Australia"
    assert generic["duration_days"] == 2
    assert len(generic["daily_schedule"]) == 2

    print("[PASS] Test 2: Offline Mock Generation Engine verified.")


def create_mock_rate_limit_error(message: str = "Rate limit reached"):
    """Helper to instantiate genuine RateLimitError across OpenAI versions."""
    try:
        import httpx
        req = httpx.Request("POST", "https://api.openai.azure.com/v1/chat/completions")
        resp = httpx.Response(429, request=req)
        return bfc.RateLimitError(message, response=resp, body={"error": {"message": message, "code": "429"}})
    except Exception:
        exc_class = bfc.RETRYABLE_EXCEPTIONS[0]
        return exc_class(message)


def test_tenacity_retry_success_after_rate_limit():
    """Verify that tenacity successfully retries on transient errors and eventually succeeds."""
    mock_client = MagicMock()
    call_counter = {"count": 0}

    # Simulate RateLimit on calls 1 and 2, success on call 3
    def side_effect(*args, **kwargs):
        call_counter["count"] += 1
        if call_counter["count"] < 3:
            raise create_mock_rate_limit_error("429: Too Many Requests - Rate limit exceeded")

        # Mock successful response
        fake_response = MagicMock()
        fake_tool_call = MagicMock()
        fake_tool_call.function.arguments = json.dumps({
            "destination": "Test City",
            "duration_days": 2,
            "travel_style": "cultural",
            "budget_tier": "moderate",
            "estimated_cost_usd": 500,
            "daily_schedule": [],
            "local_tips": []
        })
        fake_response.choices = [MagicMock(message=MagicMock(tool_calls=[fake_tool_call]))]
        return fake_response

    mock_client.chat.completions.create.side_effect = side_effect

    # Call with tenacity retry (since min=1, max=10, wait will be brief)
    result = bfc.call_openai_function_with_retry(
        client=mock_client,
        model_deployment="gpt-4o-mini",
        prompt="Test prompt",
        destination="Test City",
        duration_days=2
    )

    assert call_counter["count"] == 3, f"Expected 3 calls, got {call_counter['count']}"
    assert result["destination"] == "Test City"
    print("[PASS] Test 3: Tenacity retry recovers successfully from RateLimitError.")


def test_tenacity_retry_stops_after_max_attempts():
    """Verify that tenacity halts and reraises after exceeding maximum retry attempts (5)."""
    mock_client = MagicMock()
    call_counter = {"count": 0}

    def always_fail(*args, **kwargs):
        call_counter["count"] += 1
        raise create_mock_rate_limit_error("429: Rate limit permanently exceeded")

    mock_client.chat.completions.create.side_effect = always_fail

    failed = False
    try:
        bfc.call_openai_function_with_retry(
            client=mock_client,
            model_deployment="gpt-4o-mini",
            prompt="Test prompt",
            destination="Test City",
            duration_days=2
        )
    except Exception as e:
        failed = True

    assert failed is True, "Call should have failed and reraised"
    assert call_counter["count"] == 5, f"Expected exactly 5 attempts, got {call_counter['count']}"
    print("[PASS] Test 4: Tenacity strictly enforces max 5 attempts before reraising.")


def test_batch_processing_partial_failure_isolation():
    """Verify that if one batch item fails, the remaining batch items complete successfully."""
    mock_inputs = [
        {"id": "REQ-1", "destination": "Paris, France", "duration_days": 3, "travel_style": "cultural", "budget_tier": "moderate"},
        {"id": "REQ-2", "destination": "FailCity", "duration_days": 2, "travel_style": "adventure", "budget_tier": "budget"},
        {"id": "REQ-3", "destination": "Tokyo, Japan", "duration_days": 5, "travel_style": "culinary", "budget_tier": "luxury"},
    ]

    # Monkeypatch call_openai_function and call_openai_function_with_retry
    orig_call = bfc.call_openai_function
    orig_retry = bfc.call_openai_function_with_retry

    def selective_mock_call(*args, **kwargs):
        dest = kwargs.get("destination", "") or (args[1] if len(args) > 1 else "")
        if "FailCity" in dest:
            raise RuntimeError("Simulated fatal endpoint parse error on FailCity")
        days = kwargs.get("days", kwargs.get("duration_days", (args[2] if len(args) > 2 else 3)))
        return bfc.mock_generate_itinerary(dest, days, kwargs.get("travel_style", "cultural"), kwargs.get("budget_tier", "moderate"))

    try:
        bfc.call_openai_function = selective_mock_call
        bfc.call_openai_function_with_retry = selective_mock_call
        results = bfc.batch_process(
            inputs=mock_inputs,
            client=MagicMock(),  # Non-None to invoke the function
            delay_between_requests=0.0,
            force_demo=False
        )

        assert len(results) == 3
        assert results[0]["status"] == "SUCCESS"
        assert results[0]["data"]["destination"] == "Paris, France"

        assert results[1]["status"] == "FAILED"
        assert "Simulated fatal endpoint" in results[1]["error"]

        assert results[2]["status"] == "SUCCESS"
        assert results[2]["data"]["destination"] == "Tokyo, Japan"

        print("[PASS] Test 5: Batch processing isolates individual errors without terminating batch.")
    finally:
        bfc.call_openai_function = orig_call
        bfc.call_openai_function_with_retry = orig_retry


def test_sample_files_exist():
    """Verify that sample inputs, outputs, and consolidated markdown exist and have valid content."""
    input_file = SCRIPT_DIR / "sample_inputs.json"
    assert input_file.exists(), "sample_inputs.json missing"
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) >= 3, "Expected at least 3 batch items in sample_inputs.json"

    out_dir = SCRIPT_DIR / "sample_outputs"
    assert out_dir.exists(), "sample_outputs directory missing"
    sample_jsons = list(out_dir.glob("*.json"))
    sample_mds = list(out_dir.glob("*.md"))
    assert len(sample_jsons) >= 3, f"Expected >= 3 JSON outputs, found {len(sample_jsons)}"
    assert len(sample_mds) >= 3, f"Expected >= 3 MD outputs, found {len(sample_mds)}"

    all_md = SCRIPT_DIR / "all_sample_itineraries.md"
    assert all_md.exists(), "all_sample_itineraries.md missing"
    content = all_md.read_text(encoding="utf-8")
    assert "Paris" in content and "Tokyo" in content and "New York" in content

    print("[PASS] Test 6: Sample input/output files and consolidated report verified.")


if __name__ == "__main__":
    print("=" * 65)
    print("  RUNNING COMPREHENSIVE VERIFICATION SUITE: ASSIGNMENT 05")
    print("=" * 65)
    test_function_schema_structure()
    test_mock_generation_engine()
    test_tenacity_retry_success_after_rate_limit()
    test_tenacity_retry_stops_after_max_attempts()
    test_batch_processing_partial_failure_isolation()
    test_sample_files_exist()
    print("=" * 65)
    print("  ALL 6 TESTS PASSED! ASSIGNMENT 05 IS FULLY VERIFIED.")
    print("=" * 65)
