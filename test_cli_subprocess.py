import subprocess
import os
import json
import pytest
from task_manager import TASKS_FILE

def run_taskflow(*args):
    """
    Executes the taskflow.py wrapper with the provided arguments.
    Sets the PYTHONPATH to 'src' to ensure modules are found correctly.
    """
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"

    # We use taskflow.py as the entry point to test the wrapper's sys.path manipulation
    result = subprocess.run(
        ["python3", "taskflow.py"] + list(args),
        capture_output=True,
        text=True,
        env=env
    )
    return result

@pytest.fixture(autouse=True)
def setup_teardown():
    """
    Ensures a clean task file before and after each test.
    This prevents cross-test contamination.
    """
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
    yield
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)

def test_cli_add_task_long_flag():
    """
    Tests adding a task using the --add flag.
    Verifies the output and the content of the task file.
    """
    result = run_taskflow("--add", "Buy groceries")
    assert "Task added: 'Buy groceries'" in result.stdout
    assert os.path.exists(TASKS_FILE)
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Buy groceries"

def test_cli_add_task_short_flag():
    """
    Tests adding a task using the -a short flag.
    """
    result = run_taskflow("-a", "Buy milk")
    assert "Task added: 'Buy milk'" in result.stdout
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
    assert tasks[0]["title"] == "Buy milk"

def test_cli_list_tasks_long_flag():
    """
    Tests listing tasks using the --list flag.
    First adds a few tasks to ensure the list is populated.
    """
    run_taskflow("-a", "Task 1")
    run_taskflow("-a", "Task 2")
    result = run_taskflow("--list")
    assert "1. [ ] Task 1" in result.stdout
    assert "2. [ ] Task 2" in result.stdout

def test_cli_list_tasks_short_flag():
    """
    Tests listing tasks using the -l short flag.
    """
    run_taskflow("-a", "Task 1")
    result = run_taskflow("-l")
    assert "1. [ ] Task 1" in result.stdout

def test_cli_complete_task_long_flag():
    """
    Tests marking a task as completed using the --complete flag.
    """
    run_taskflow("-a", "Task to complete")
    result = run_taskflow("--complete", "1")
    assert "Task 1 marked as completed." in result.stdout

    # Verify completion via --list
    list_result = run_taskflow("--list")
    assert "1. [X] Task to complete" in list_result.stdout

def test_cli_delete_task_long_flag():
    """
    Tests deleting a task using the --delete flag.
    """
    run_taskflow("-a", "Task to delete")
    result = run_taskflow("--delete", "1")
    assert "Task 1 deleted: 'Task to delete'" in result.stdout

    # Verify deletion via --list
    list_result = run_taskflow("--list")
    assert "No tasks found." in list_result.stdout

def test_cli_invalid_command():
    """
    Tests the CLI with an unrecognized flag.
    Ensures it fails with a usage message.
    """
    # This should trigger an argparse error
    result = run_taskflow("--invalid-flag")
    assert "unrecognized arguments: --invalid-flag" in result.stderr

def test_cli_multiple_flags():
    """
    Tests combining multiple flags in a single command.
    """
    # Add a task and list it immediately
    result = run_taskflow("-a", "Combined Task", "-l")
    assert "Task added: 'Combined Task'" in result.stdout
    assert "1. [ ] Combined Task" in result.stdout
