# Command-Line Task Manager in Python

A modular, interactive command-line application built in Python 3 to manage daily tasks—allowing users to add, view, complete, and delete tasks with input validation and clear status tracking.

---

## 1. Explanation of Approach

The application is designed around clean separation of concerns between **data representation**, **core business logic**, and the **command-line user interface (CLI)**:

1. **Data Structure (`tasks` list of dictionaries):**
   - All tasks are stored in a central list named `tasks`.
   - Each task is represented as a Python dictionary containing three typed fields:
     - `"id"` (`int`): A unique, strictly incrementing positive integer identifier.
     - `"description"` (`str`): The trimmed text describing the task.
     - `"completed"` (`bool`): The completion state (`False` for `"Pending"`, `True` for `"Done"`).

2. **Modular Core Functions:**
   - `add_task(description)`: Validates that the task description is non-empty, assigns a unique incrementing ID, appends the dictionary to `tasks`, and confirms creation.
   - `view_tasks()`: Checks whether `tasks` is empty; otherwise iterates through the list to print each task's ID, description, and status (`Pending` or `Done`), followed by a summary count.
   - `mark_completed(task_id)`: Searches `tasks` by ID, updates `"completed"` to `True` (or notifies the user if it is already completed), and handles missing IDs clearly.
   - `delete_task(task_id)`: Searches `tasks` by ID, removes the matching dictionary if present, and informs the user whether the task was deleted or not found.

3. **Interactive CLI Loop (`main` & `prompt_task_id`):**
   - Uses a continuous `while True` loop that normalizes user input with `.strip().lower()` and routes commands (`add`, `view`, `complete`, `delete`, `exit`) via `if-elif-else` control flow.

---

## 2. Challenges Faced and How They Were Addressed

| Challenge | How It Was Addressed |
| :--- | :--- |
| **1. Task ID reuse after deleting the latest task** | Relying solely on `tasks[-1]["id"] + 1` causes an ID to be reused if the user adds Task 2, deletes Task 2, and adds another task. To ensure IDs always increment monotonically, a dedicated `next_task_id` counter is maintained alongside a `max()` safeguard. |
| **2. Non-numeric, empty, or negative task IDs** | Entering letters, blank input, or negative numbers into `int()` raises a `ValueError` or produces invalid lookups. Added a reusable `prompt_task_id()` helper that catches `ValueError`, rejects empty inputs, and enforces positive integers (`task_id > 0`). |
| **3. Blank or whitespace-only task descriptions** | Users accidentally pressing `Enter` when adding a task could create empty entries. Added `.strip()` normalization and an explicit empty-string check in `add_task()` before creating a task. |
| **4. Ambiguous feedback when deleting or re-completing tasks** | A list comprehension filter alone does not tell the user whether the task ID actually existed. Updated `delete_task()` to locate and remove the matching task explicitly so it reports either exact confirmation or `"No task found with ID ..."`, and updated `mark_completed()` to notify the user if a task was already completed. |

---

## 3. Enhancements & Input Validation Implemented

- **Comprehensive Input Validation:** Rejects empty task descriptions, non-integer task IDs, boolean/negative/zero task IDs, and unrecognized menu commands without crashing.
- **Explicit Deletion & Completion Feedback:** Reports clearly whether a deleted task existed or if a task was already marked as completed.
- **Task Summary Footer:** `view_tasks()` displays total, completed (`Done`), and remaining (`Pending`) task counts alongside the required per-task output lines.
- **Graceful Exit Handling:** Catches `KeyboardInterrupt` (`Ctrl+C`) and `EOFError` so exiting abruptly prints a clean goodbye message rather than a Python traceback.

---

## 4. How to Run and Test

### Prerequisites
- Python 3.x installed (`python --version` or `py --version`).

### Run the Application
```bash
python task_manager.py
```

### Sample Interaction
```text
=========================================
   Welcome to Command-Line Task Manager  
=========================================

Options: add, view, complete, delete, exit
Enter command: add
Enter task description: Finish Python Assignment 01
Task 'Finish Python Assignment 01' added with ID 1.

Options: add, view, complete, delete, exit
Enter command: add
Enter task description: Review OpenAI API documentation
Task 'Review OpenAI API documentation' added with ID 2.

Options: add, view, complete, delete, exit
Enter command: view

--- Current Tasks ---
1: Finish Python Assignment 01 [Pending]
2: Review OpenAI API documentation [Pending]
---------------------
Total: 2 | Done: 0 | Pending: 2

Options: add, view, complete, delete, exit
Enter command: complete
Enter task ID to mark complete: 1
Task ID 1 marked as completed.

Options: add, view, complete, delete, exit
Enter command: delete
Enter task ID to delete: 2
Task ID 2 ('Review OpenAI API documentation') deleted successfully.

Options: add, view, complete, delete, exit
Enter command: exit
Exiting Task Manager. Goodbye!
```
