from common.app.core.windows.error_window import ErrorWindow
from common.app.core.tools.terminal import SvTerminal

try:
    terminal = SvTerminal()
    terminal.run_sv_terminal()

except Exception as execution_error:
    ErrorWindow(exception=execution_error).exec_()
