"""
SIGNAL starting file

This file runs SIGNAL GUI. The GUI runs once the file is imported, no additional actions are required

e.g.: "import signal"
"""


# Correct way to run
if __name__ != "__main__":  # Runs only by import command
    from signal import signal

    try:
        signal.run_signal_gui()
    except Exception as run_signal_exception:
        print(run_signal_exception)
        exit(100)


# Incorrect way to run
if __name__ == "__main__":  # Do not run directly
    error_message = """
The file common/signal.py should be imported from the main working directory, the direct run has no effect
The GUI runs once the file is imported, no additional actions are required
Please, refer to the SvTerminal documentation to read more about how to run the application
"""

    raise RuntimeError(error_message)
