from common.gui.core.terminal import SvTerminalGui
from common.gui.constants.TermFilesPath import TermFilesPath
from common.lib.data_models.Config import Config


config: Config = Config.parse_file(TermFilesPath.CONFIG)


sv_terminal_gui: SvTerminalGui = SvTerminalGui(config)
status: int = sv_terminal_gui.run()
exit(status)




# try:
#     sv_terminal: SvTerminal = SvTerminal()
#     sv_terminal.run()
#
# except Exception as execution_error:
#     ErrorWindow(exception=execution_error).exec()
