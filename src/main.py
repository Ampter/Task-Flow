import sys

def main():
    """
    Main execution logic for TaskFlow.
    Delegates to either the CLI or GUI based on command-line arguments.
    """
    if len(sys.argv) > 1:
        # Import and run the CLI if arguments are provided
        from cli import main as cli_main
        cli_main()
    else:
        # Attempt to import and run the GUI if no arguments are provided
        try:
            from gui import main as gui_main
            gui_main()
        except ImportError:
            # Handle case where PyQt6 is missing (e.g., in headless environments)
            print("Error: PyQt6 is not installed. GUI cannot be launched.")
            print("To use the CLI, provide flags (e.g., taskflow --list).")
            sys.exit(1)

if __name__ == "__main__":
    main()
