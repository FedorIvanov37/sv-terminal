#
# SIGNAL GUI run script
#


__author__ = "Fedor Ivanov"
__version__ = "v0.17"


def run_signal_gui():
    from sys import exit
    from signal.gui.core.SignalGui import SignalGui
    from signal.lib.enums.TermFilesPath import TermFilesPath
    from signal.lib.data_models.Config import Config

    with open(TermFilesPath.CONFIG) as json_file:
        config: Config = Config.model_validate_json(json_file.read())

    terminal: SignalGui = SignalGui(config)

    status: int = terminal.run()

    exit(status)
