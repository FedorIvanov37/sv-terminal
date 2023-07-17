from common.gui.core.SvTerminalGui import SvTerminalGui
from common.gui.constants.TermFilesPath import TermFilesPath
from common.gui.windows.error_window import ErrorWindow
from common.lib.data_models.Config import Config
from sys import exit

status: int = int()


try:
    config: Config = Config.parse_file(TermFilesPath.CONFIG)
    sv_terminal_gui: SvTerminalGui = SvTerminalGui(config)
    status: int = sv_terminal_gui.run()

except SystemExit:
    exit(status)

except Exception as exception:
    ErrorWindow(exception).exec()

else:
    exit(status)
