from common.app.core.windows.error_window import ErrorWindow
from common.app.core.tools.terminal import SvTerminal


DEBUG_MODE = True


if DEBUG_MODE:
    sv_terminal: SvTerminal = SvTerminal()
    sv_terminal.run()
    exit()

try:
    sv_terminal: SvTerminal = SvTerminal()
    sv_terminal.run()

except Exception as execution_error:
    ErrorWindow(exception=execution_error).exec()
