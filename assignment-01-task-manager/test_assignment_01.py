"""
Comprehensive Verification and Double-Triple Check Suite for Assignment 01:
- Data structure and task schema validation
- Monotonic ID generation after deletions and list clears
- Input validation (empty descriptions, whitespace, boolean IDs, negative IDs, string IDs)
- End-to-end interactive CLI pipe execution
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

import task_manager as tm


def test_task_lifecycle_and_id_monotonicity():
    """Verify adding, viewing, completing, and deleting tasks preserves unique IDs."""
    tm.tasks.clear()
    t1 = tm.add_task("Prepare project architecture")
    t2 = tm.add_task("Write unit test suite")
    assert t1["id"] == 1 and t1["completed"] is False
    assert t2["id"] == 2 and t2["completed"] is False

    # Delete task 1, then add a new task -> new task should receive ID 3 (not duplicate 2)
    assert tm.delete_task(1) is True
    t3 = tm.add_task("Push verified code to GitHub")
    assert t3["id"] == 3
    print("[PASS] Test 1: Task lifecycle and monotonic ID generation verified.")


def test_input_validation_and_edge_cases():
    """Verify defenses against empty strings, booleans, negative IDs, and missing IDs."""
    tm.tasks.clear()
    assert tm.add_task("") is None
    assert tm.add_task("   ") is None
    assert tm.add_task(None) is None

    tm.add_task("Valid Task")
    # Guard against Python's isinstance(True, int) == True trap
    assert tm.mark_completed(True) is False
    assert tm.mark_completed(False) is False
    assert tm.delete_task(True) is False
    assert tm.mark_completed(-5) is False
    assert tm.mark_completed(0) is False
    assert tm.mark_completed("999") is False

    # String digit support
    assert tm.mark_completed("1") is True
    assert tm.tasks[0]["completed"] is True
    print("[PASS] Test 2: Edge-case input validation (bool, negative, empty, string ID) verified.")


def test_interactive_cli_pipe():
    """Verify full interactive command-line loop via stdin/stdout pipe."""
    cli_input = "add\nReview code\nview\ncomplete\n1\nview\ndelete\n1\nview\nexit\n"
    res = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "task_manager.py")],
        input=cli_input,
        capture_output=True,
        text=True,
        cwd=str(SCRIPT_DIR),
    )
    assert res.returncode == 0
    assert "Task 'Review code' added with ID 1." in res.stdout
    assert "1: Review code [Pending]" in res.stdout
    assert "1: Review code [Done]" in res.stdout
    assert "Task ID 1 deleted successfully." in res.stdout
    assert "No tasks available." in res.stdout
    print("[PASS] Test 3: Interactive CLI loop execution verified.")


if __name__ == "__main__":
    print("=" * 65)
    print("  RUNNING COMPREHENSIVE VERIFICATION SUITE: ASSIGNMENT 01")
    print("=" * 65)
    test_task_lifecycle_and_id_monotonicity()
    test_input_validation_and_edge_cases()
    test_interactive_cli_pipe()
    print("=" * 65)
    print("  ALL 3 TESTS PASSED! ASSIGNMENT 01 IS FULLY VERIFIED.")
    print("=" * 65)
