import os
import pytest
from task_manager import load_tasks, save_tasks, add_task, complete_task, delete_task, TASKS_FILE

@pytest.fixture(autouse=True)
def cleanup():
    """Removes the tasks file before and after each test."""
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
    yield
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)

def test_add_task():
    add_task("Test Task")
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test Task"
    assert tasks[0]["completed"] is False

def test_complete_task():
    add_task("Task to complete")
    success = complete_task(1)
    assert success is True
    tasks = load_tasks()
    assert tasks[0]["completed"] is True

def test_delete_task():
    add_task("Task to delete")
    removed_task = delete_task(1)
    assert removed_task["title"] == "Task to delete"
    tasks = load_tasks()
    assert len(tasks) == 0

def test_invalid_complete():
    add_task("Task")
    success = complete_task(2) # Invalid index
    assert success is False
    tasks = load_tasks()
    assert tasks[0]["completed"] is False

def test_invalid_delete():
    add_task("Task")
    removed_task = delete_task(2) # Invalid index
    assert removed_task is None
    tasks = load_tasks()
    assert len(tasks) == 1
