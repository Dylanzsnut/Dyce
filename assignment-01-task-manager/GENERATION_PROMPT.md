# Assignment 01: Auto-Refined Generation Prompt & Architectural Specification

## Meta-Prompt Used for Implementation

```markdown
Role: Senior Python Software Engineer & Pedagogical Code Architect
Task: Implement Assignment 01 - Command-Line Task Manager in Python

Core Objectives & Evaluation Rubrics:
1. Core Concepts Demonstrated:
   - Variables and primitive data types (int, str, bool).
   - In-memory data structures: List of Task dictionaries with keys `id`, `description`, `completed`.
   - Control flow: while loops, if-elif-else branching, for loops.
   - Modular functional decomposition: `add_task()`, `view_tasks()`, `mark_completed()`, `delete_task()`, `show_menu()`.

2. Robust Input Handling & Autograder Defense:
   - Handle empty strings, whitespace-only strings gracefully with descriptive error feedback.
   - Disallow non-integer, negative, or boolean IDs (e.g. `isinstance(True, int)` trap in Python).
   - Safe ID generation: Compute `max((t["id"] for t in tasks), default=0) + 1` so clearing or deleting tasks never produces duplicate IDs.
   - Graceful termination on invalid menu options and EOF/KeyboardInterrupt.

3. Interactive CLI & Programmatic Dual Interface:
   - Standard CLI loop accepting pipe or terminal inputs.
   - Clean programmatic importability so automated testing scripts (`pytest` or test harnesses) can import and test individual functions directly.
```
