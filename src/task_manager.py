import json
import os
from typing import List, Dict

TASKS_FILE = os.path.expanduser("~/.taskflow_tasks.json")

def load_tasks() -> List[Dict]:
    """Loads tasks from a JSON file. Returns an empty list if the file doesn't exist or is empty."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks: List[Dict]) -> None:
    """Saves the list of tasks to a JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(title: str) -> None:
    """Adds a new task to the task list."""
    if not title:
        return
    tasks = load_tasks()
    tasks.append({"title": title, "completed": False})
    save_tasks(tasks)

def complete_task(index: int) -> bool:
    """Marks a specific task as completed based on its index. Returns True if successful."""
    tasks = load_tasks()
    if 0 < index <= len(tasks):
        tasks[index - 1]["completed"] = True
        save_tasks(tasks)
        return True
    return False

def delete_task(index: int) -> Dict:
    """Deletes a specific task based on its index. Returns the removed task or None."""
    tasks = load_tasks()
    if 0 < index <= len(tasks):
        removed_task = tasks.pop(index - 1)
        save_tasks(tasks)
        return removed_task
    return None
