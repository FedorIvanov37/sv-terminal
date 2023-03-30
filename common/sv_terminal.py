from common.app.core.windows.error_window import ErrorWindow
from common.app.core.tools.terminal import SvTerminalForm
from common.app.constants.FilePath import FilePath
from common.lib.data_models.Config import Config
from common.lib.Terminal import SvTerminal


DEBUG_MODE = True


config: Config = Config.parse_file(FilePath.CONFIG)


if DEBUG_MODE:
    t = SvTerminal(config)
    t.echo_test()

    # sv_terminal: SvTerminalForm = SvTerminalForm(config)
    # sv_terminal.run()
    # exit()
#
# try:
#     sv_terminal: SvTerminal = SvTerminal()
#     sv_terminal.run()
#
# except Exception as execution_error:
#     ErrorWindow(exception=execution_error).exec()
