from common.app.core.windows.error_window import ErrorWindow
from common.app.core.tools.terminal import SvTerminalGui
from common.app.constants.FilePath import FilePath
from common.lib.data_models.Config import Config
from common.lib.Terminal import SvTerminal


DEBUG_MODE = True


config: Config = Config.parse_file(FilePath.CONFIG)


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
