#
# SvTerminal starting file
#
# This file runs SvTerminal GUI. The GUI runs once the file is imported, no additional actions are required
#
# e.g.: "import common.sv_terminal" or "from common import sv_terminal"
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
    raise RuntimeError(f"The file common/sv_terminal.py should be imported from main working directory, "
                       "direct run has no effect")
