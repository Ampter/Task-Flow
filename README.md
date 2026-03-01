# TaskFlow

A simple To-Do application written in Python, featuring separate CLI and GUI versions.

## Features

- **CLI Version**: Efficient command-line interface for quick task management using flags.
- **GUI Version**: User-friendly graphical interface for interactive task management.
- Add, List, Complete, and Delete tasks.
- Persistent storage using a JSON file (`~/.taskflow_tasks.json`).

## Installation

From source:

```bash
git clone https://github.com/Ampter/TaskFlow
cd TaskFlow
pip install .
```

## Usage

### Using TaskFlow
You can use the `taskflow` command for both CLI and GUI versions:
- Running `taskflow` without arguments launches the **GUI**.
- Running `taskflow` with flags (e.g., `taskflow --list`) uses the **CLI**.

Alternatively, you can use the dedicated commands:
- `taskflow-gui`: Launches the graphical interface.
- `taskflow-cli`: Manages tasks from the command line using flags.

### CLI Flags
- `-a`, `--add TITLE`: Add a new task with the specified title.
- `-l`, `--list`: List all tasks.
- `-c`, `--complete INDEX`: Mark the task at the given index as completed.
- `-d`, `--delete INDEX`: Delete the task at the given index.

### Examples
```bash
# Launch GUI
taskflow

# Add task via CLI
taskflow --add "Buy groceries"
# or
taskflow -a "Buy groceries"

# List tasks via CLI
taskflow --list
# or
taskflow -l

# Complete task 1
taskflow --complete 1

# Delete task 1
taskflow --delete 1
```

## Project Structure

- `taskflow.py`: Main entry point (root directory).
- `src/main.py`: Main execution logic.
- `src/task_manager.py`: Core logic for task operations.
- `src/cli.py`: CLI implementation.
- `src/gui.py`: GUI implementation.
- `~/.taskflow_tasks.json`: Data persistence.

## Testing

```bash
pytest
```
