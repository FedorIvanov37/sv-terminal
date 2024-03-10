#
# SIGNAL starting file
#
# This file runs SIGNAL GUI. The GUI runs once the file is imported, no additional actions are required
#
# e.g.: "import common.signal"
#


__author__ = "Fedor Ivanov"
__version__ = "v0.17"


# Correct way to run
if __name__ != "__main__":  # Runs only by import command
    try:
        from sys import exit
        from common.gui.core.SignalGui import SignalGui
        from common.lib.enums.TermFilesPath import TermFilesPath
        from common.lib.data_models.Config import Config

        with open(TermFilesPath.CONFIG) as json_file:
            config: Config = Config.model_validate_json(json_file.read())

        terminal: SignalGui = SignalGui(config)

        status: int = terminal.run()

        exit(status)

    except Exception as run_signal_exception:
        print(run_signal_exception)
        exit(100)

# Incorrect way to run
if __name__ == "__main__":  # Do not run directly
    error_message = """
The file common/common.py should be imported from the main working directory, the direct run has no effect
The GUI runs once the file is imported, no additional actions are required
Please, refer to the SvTerminal documentation to read more about how to run the application
"""

    raise RuntimeError(error_message)
