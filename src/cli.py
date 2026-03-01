import argparse
import sys
from task_manager import load_tasks, add_task, complete_task, delete_task

def list_tasks() -> None:
    """
    Retrieves and prints all current tasks.
    Each task is displayed with its index, completion status, and title.
    """
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    # Iterate through tasks and print with a 1-based index
    for i, task in enumerate(tasks, 1):
        status = "[X]" if task["completed"] else "[ ]"
        print(f"{i}. {status} {task['title']}")

def main():
    """
    Main entry point for the TaskFlow CLI.
    Uses argparse to handle flags for adding, listing, completing, and deleting tasks.
    """
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description="TaskFlow CLI To-Do App",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Define optional arguments (flags)
    # Using flags instead of subparsers to allow for more flexible usage (e.g., combining commands)
    parser.add_argument(
        "-a", "--add",
        type=str,
        metavar="TITLE",
        help="Add a new task with the specified title"
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all tasks"
    )
    parser.add_argument(
        "-c", "--complete",
        type=int,
        metavar="INDEX",
        help="Mark the task at the given index as completed"
    )
    parser.add_argument(
        "-d", "--delete",
        type=int,
        metavar="INDEX",
        help="Delete the task at the given index"
    )

    # Parse arguments from sys.argv
    args = parser.parse_args()

    # If no arguments were provided, display the help message
    # This is useful when the user runs the CLI directly without any flags
    if not any(vars(args).values()):
        parser.print_help()
        return

    # Handle the 'add' flag
    if args.add:
        add_task(args.add)
        print(f"Task added: '{args.add}'")

    # Handle the 'complete' flag
    # Check for None because 0 is a valid integer but evaluates to False
    if args.complete is not None:
        if complete_task(args.complete):
            print(f"Task {args.complete} marked as completed.")
        else:
            print(f"Error: Task {args.complete} does not exist.")

    # Handle the 'delete' flag
    if args.delete is not None:
        removed_task = delete_task(args.delete)
        if removed_task:
            print(f"Task {args.delete} deleted: '{removed_task['title']}'")
        else:
            print(f"Error: Task {args.delete} does not exist.")

    # Handle the 'list' flag
    # We do this last so that any changes made by other flags are reflected in the list
    if args.list:
        list_tasks()

if __name__ == "__main__":
    main()
