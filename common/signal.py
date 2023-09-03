#
# SIGNAL starting file
#
# This file runs SIGNAL GUI. The GUI runs once the file is imported, no additional actions are required
#
# e.g.: "import common.signal" or "from common import signal"
#


# Correct way to run
if __name__ != "__main__":  # Runs only by import command
    from common.gui.core.SvTerminalGui import SvTerminalGui
    from common.lib.constants.TermFilesPath import TermFilesPath
    from common.lib.data_models.Config import Config
    from sys import exit

    config: Config = Config.parse_file(TermFilesPath.CONFIG)
    terminal: SvTerminalGui = SvTerminalGui(config)
    status: int = terminal.run()
    exit(status)


# Incorrect way to run
if __name__ == "__main__":  # Do not run directly
    error_message = """
The file common/signal.py should be imported from the main working directory, the direct run has no effect
The GUI runs once the file is imported, no additional actions are required
Please, refer to the SvTerminal documentation to read more about how to run the application 
"""

    raise RuntimeError(error_message)
