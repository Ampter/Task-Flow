import sys
import os

# Add src to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """
    Main entry point for TaskFlow.
    If arguments are provided, it runs the CLI.
    Otherwise, it attempts to launch the GUI.
    """
    if len(sys.argv) > 1:
        # Import CLI only when needed to avoid unnecessary dependency checks (like PyQt6)
        from cli import main as cli_main
        cli_main()
    else:
        # Import GUI only when needed
        try:
            from gui import main as gui_main
            gui_main()
        except ImportError:
            print("Error: PyQt6 is not installed. GUI cannot be launched.")
            print("To use the CLI, provide arguments (e.g., taskflow --list).")
            sys.exit(1)

if __name__ == "__main__":
    main()
