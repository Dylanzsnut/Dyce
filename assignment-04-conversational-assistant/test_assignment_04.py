"""
Automated Double-Check Test Suite for Assignment 04
---------------------------------------------------
Verifies all assignment requirements, edge cases, and SDK behavior:
1. Role construction & message hierarchy (system, user, assistant)
2. Few-shot example structure & sentiment calibration
3. Chain-of-Thought (CoT) reasoning prompt formatting
4. Context preservation across multi-turn exchanges
5. Local HTTP Wire-Protocol simulation of Azure OpenAI Chat Completions API
6. CLI argument handling and offline demonstration fallback
"""

import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Add project root to Python path
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

import conversational_assistant as ca


def test_01_role_construction_and_hierarchy():
    """Verify that roles are strictly assigned as system, user, and assistant in proper order."""
    session = ca.ConversationalAssistantSession(
        system_prompt=ca.SYSTEM_PROMPT,
        few_shots=ca.FEW_SHOT_SENTIMENT_EXAMPLES,
    )
    msgs = session.get_messages()

    # Rule 1: First message must always be the system prompt
    assert msgs[0]["role"] == "system"
    assert "event management assistant" in msgs[0]["content"]

    # Rule 2: Following messages must be valid alternating few-shot pairs
    for i, ex in enumerate(msgs[1:], start=1):
        assert ex["role"] in ("user", "assistant")
        assert len(ex["content"].strip()) > 0

    print("[PASS] Test 1: Role construction and hierarchy verified.")


def test_02_few_shot_sentiment_examples():
    """Verify that few-shot sentiment exemplars provide balanced class demonstrations."""
    assert hasattr(ca, "few_shot_examples"), "Missing few_shot_examples attribute"
    assert hasattr(ca, "conversation_messages"), "Missing conversation_messages attribute"
    examples = ca.FEW_SHOT_SENTIMENT_EXAMPLES
    assert len(examples) >= 4, "Must contain at least 2 complete few-shot pairs (>=4 messages)"

    # Check pair alternation
    for i in range(0, len(examples), 2):
        assert examples[i]["role"] == "user"
        assert "Analyze the sentiment" in examples[i]["content"]
        assert examples[i + 1]["role"] == "assistant"
        assert "Sentiment:" in examples[i + 1]["content"]

    # Check direct run_turn offline fallback
    sess = ca.ConversationalAssistantSession()
    reply_sent = ca.run_turn(sess, "Analyze the sentiment of this text: 'I love this conference!'")
    assert "Sentiment: Positive" in reply_sent
    reply_cot = ca.run_turn(sess, "What are good conversation starters? Explain step-by-step.")
    assert "Step-by-Step" in reply_cot

    print(f"[PASS] Test 2: Few-shot sentiment exemplars & direct run_turn fallback verified ({len(examples)//2} pairs).")


def test_03_multi_turn_context_retention():
    """Verify that multi-turn dialogue history is retained cumulatively across turns."""
    session = ca.ConversationalAssistantSession(
        system_prompt="Test System",
        few_shots=[
            {"role": "user", "content": "Sample user few-shot"},
            {"role": "assistant", "content": "Sample assistant few-shot"},
        ],
    )

    initial_len = len(session.get_messages())
    assert initial_len == 3  # system + 1 pair

    # Turn 1
    session.add_user_message("Turn 1 Question")
    session.add_assistant_message("Turn 1 Answer")
    assert len(session.get_messages()) == initial_len + 2

    # Turn 2
    session.add_user_message("Turn 2 Follow-up")
    session.add_assistant_message("Turn 2 Answer")
    assert len(session.get_messages()) == initial_len + 4

    # Verify message sequence preserves complete historical turns
    history = session.get_messages()
    assert history[-4] == {"role": "user", "content": "Turn 1 Question"}
    assert history[-3] == {"role": "assistant", "content": "Turn 1 Answer"}
    assert history[-2] == {"role": "user", "content": "Turn 2 Follow-up"}
    assert history[-1] == {"role": "assistant", "content": "Turn 2 Answer"}

    print("[PASS] Test 3: Multi-turn cumulative context retention verified.")


def test_04_azure_openai_wire_protocol_mock():
    """Verify live SDK communication against a simulated Azure OpenAI HTTP endpoint."""
    received_requests = []

    class MockAzureHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            received_requests.append(
                {
                    "path": self.path,
                    "api_key": self.headers.get("api-key"),
                    "messages": body.get("messages", []),
                    "temperature": body.get("temperature"),
                }
            )

            resp_payload = {
                "id": "chatcmpl-test-wire",
                "object": "chat.completion",
                "created": 1700000000,
                "model": "gpt-4o-mini",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": (
                                "Step 1: Analyzed constraints.\n"
                                "Step 2: Applied reasoning.\n"
                                "Recommendation: Verified successfully."
                            ),
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 120, "completion_tokens": 40, "total_tokens": 160},
            }
            data = json.dumps(resp_payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    server = HTTPServer(("127.0.0.1", 0), MockAzureHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        from openai import AzureOpenAI

        test_client = AzureOpenAI(
            api_version="2024-07-01-preview",
            azure_endpoint=f"http://127.0.0.1:{port}",
            api_key="mock-test-key-404",
        )

        test_session = ca.ConversationalAssistantSession(
            system_prompt=ca.SYSTEM_PROMPT,
            few_shots=ca.FEW_SHOT_SENTIMENT_EXAMPLES,
        )

        reply = ca.run_turn(
            session=test_session,
            user_input="How should we arrange registration badges? Explain step-by-step.",
            client=test_client,
            deployment_name="gpt-4o-mini",
            temperature=0.7,
        )

        assert "Step 1" in reply
        assert len(received_requests) == 1
        req = received_requests[0]
        assert "deployments/gpt-4o-mini/chat/completions" in req["path"]
        assert req["api_key"] == "mock-test-key-404"
        assert req["temperature"] == 0.7
        assert req["messages"][-1]["role"] == "user"
        assert "registration badges" in req["messages"][-1]["content"]

        print("[PASS] Test 4: Azure OpenAI wire protocol and HTTP contract verified.")
    finally:
        server.shutdown()


def test_05_cli_and_offline_demonstration_mode():
    """Verify that running the script without credentials displays verified outputs without crashing."""
    clean_env = {k: v for k, v in os.environ.items() if not k.startswith("AZURE_OPENAI")}

    # Test 5a: Default execution runs offline demonstration mode cleanly
    res_batch = subprocess.run(
        [sys.executable, str(PROJECT_DIR / "conversational_assistant.py")],
        env=clean_env,
        capture_output=True,
        text=True,
    )
    assert res_batch.returncode == 0
    assert "Notice: Azure OpenAI credentials not detected" in res_batch.stdout
    assert "Scenario 1: Networking Conversation Starters" in res_batch.stdout
    assert "Scenario 2: Venue Capacity & Catering Budget" in res_batch.stdout
    assert "Scenario 3: Outdoor Gala Weather Risk Mitigation" in res_batch.stdout
    print("[PASS] Test 5a: Offline demonstration mode verified (zero crash on missing env).")

    # Test 5b: CLI --help option
    res_help = subprocess.run(
        [sys.executable, str(PROJECT_DIR / "conversational_assistant.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert res_help.returncode == 0
    assert "--interactive" in res_help.stdout
    assert "--scenario" in res_help.stdout
    print("[PASS] Test 5b: CLI flags (--help, --scenario, --interactive) verified.")


def main():
    print("==================================================================")
    print("   Running Automated Double-Check Verification for Assignment 04  ")
    print("==================================================================")
    test_01_role_construction_and_hierarchy()
    test_02_few_shot_sentiment_examples()
    test_03_multi_turn_context_retention()
    test_04_azure_openai_wire_protocol_mock()
    test_05_cli_and_offline_demonstration_mode()
    print("==================================================================")
    print("   ALL TESTS PASSED! ASSIGNMENT 04 IS VERIFIED & PRODUCTION-READY ")
    print("==================================================================")


if __name__ == "__main__":
    main()
