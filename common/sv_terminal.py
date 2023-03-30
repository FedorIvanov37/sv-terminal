from common.gui.core.terminal import SvTerminalGui
from common.gui.constants.TermFilesPath import TermFilesPath
from common.lib.data_models.Config import Config

DEBUG_MODE = True


config: Config = Config.parse_file(TermFilesPath.CONFIG)


if DEBUG_MODE:
    sv_terminal_gui: SvTerminalGui = SvTerminalGui(config)
    sv_terminal_gui.run()
    exit()

# try:
#     sv_terminal: SvTerminal = SvTerminal()
#     sv_terminal.run()
#
# except Exception as execution_error:
#     ErrorWindow(exception=execution_error).exec()
