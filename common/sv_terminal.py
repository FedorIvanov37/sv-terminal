from common.app.core.windows.error_window import ErrorWindow
from common.app.core.tools.terminal import SvTerminal

try:
    sv_terminal: SvTerminal = SvTerminal()
    sv_terminal.run()

except Exception as execution_error:
    ErrorWindow(exception=execution_error).exec_()
