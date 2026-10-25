"""
Command-Line Task Manager in Python
-----------------------------------
A modular command-line application that allows users to manage daily tasks:
- Add new tasks
- View all tasks
- Mark tasks as completed
- Delete tasks

Concepts Demonstrated:
- Variables and Data Types (int, str, bool)
- Lists and Dictionaries (list of task dictionaries)
- Control Flow (if-elif-else statements, while/for loops)
- Modular Functions
- Robust User Input Handling and Validation
"""

# Step 1: Define the Data Structure
# List holding all task dictionaries. Each dictionary follows the schema:
# {
#     "id": int,           # Unique positive integer task ID
#     "description": str,  # Non-empty task description
#     "completed": bool    # Completion status (True = Done, False = Pending)
# }
tasks = []


# Step 2: Implement Core Functions
def add_task(description):
    """Add a new task to the task list after validating its description."""
    if not isinstance(description, str) or not description.strip():
        print("Error: Task description cannot be empty.")
        return None

    cleaned_description = description.strip()

    # Determine unique task ID based on current tasks list
    task_id = max((t["id"] for t in tasks), default=0) + 1

    task = {
        "id": task_id,
        "description": cleaned_description,
        "completed": False,
    }
    tasks.append(task)
    print(f"Task '{cleaned_description}' added with ID {task_id}.")
    return task


def view_tasks():
    """Display all tasks currently in the task list with their status."""
    if not tasks:
        print("No tasks available.")
        return

    for task in tasks:
        status = "Done" if task["completed"] else "Pending"
        print(f"{task['id']}: {task['description']} [{status}]")


def mark_completed(task_id):
    """Mark a specific task as completed by its unique task ID."""
    if isinstance(task_id, str) and task_id.strip().isdigit():
        task_id = int(task_id.strip())

    if not isinstance(task_id, int) or isinstance(task_id, bool) or task_id <= 0:
        print("Invalid task ID.")
        return False

    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print(f"Task ID {task_id} is already marked as completed.")
            else:
                task["completed"] = True
                print(f"Task ID {task_id} marked as completed.")
            return True

    print(f"No task found with ID {task_id}.")
    return False


def delete_task(task_id):
    """Delete a specific task from the task list by its unique task ID."""
    global tasks

    if isinstance(task_id, str) and task_id.strip().isdigit():
        task_id = int(task_id.strip())

    if not isinstance(task_id, int) or isinstance(task_id, bool) or task_id <= 0:
        print("Invalid task ID.")
        return False

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            removed_task = tasks.pop(index)
            print(f"Task ID {task_id} deleted successfully.")
            return True

    print(f"No task found with ID {task_id}.")
    return False


def prompt_task_id(prompt_message):
    """
    Prompt the user for a task ID and validate that the input is a positive integer.
    Returns the integer ID if valid, or None if invalid.
    """
    raw_input = input(prompt_message).strip()
    if not raw_input:
        print("Invalid task ID.")
        return None

    try:
        task_id = int(raw_input)
        if task_id <= 0:
            print("Invalid task ID. Please enter a positive integer.")
            return None
        return task_id
    except ValueError:
        print("Invalid task ID.")
        return None


# Step 3: Create the User Interface Loop
def main():
    """Run the interactive command-line interface loop."""
    print("=========================================")
    print("   Welcome to Command-Line Task Manager  ")
    print("=========================================")

    while True:
        try:
            print("\nOptions: add, view, complete, delete, exit")
            choice = input("Enter command: ").strip().lower()

            if choice == "add":
                desc = input("Enter task description: ").strip()
                add_task(desc)

            elif choice == "view":
                view_tasks()

            elif choice == "complete":
                task_id = prompt_task_id("Enter task ID to mark complete: ")
                if task_id is not None:
                    mark_completed(task_id)

            elif choice == "delete":
                task_id = prompt_task_id("Enter task ID to delete: ")
                if task_id is not None:
                    delete_task(task_id)

            elif choice == "exit":
                print("Exiting Task Manager. Goodbye!")
                break

            else:
                print("Invalid command.")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting Task Manager. Goodbye!")
            break


if __name__ == "__main__":
    main()
