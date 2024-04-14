from os import listdir
from os.path import normpath, basename, isfile
from glob import glob
from pydantic import ValidationError
from logging import info, error
from datetime import datetime
from time import sleep
from argparse import ArgumentParser
from signal import signal, SIG_DFL, SIGINT
from PyQt6.QtCore import QCoreApplication, QTimer, pyqtSignal
from common.lib.data_models.Transaction import Transaction
from common.lib.data_models.Config import Config
from common.lib.enums.TextConstants import TextConstants
from common.lib.enums.ReleaseDefinition import ReleaseDefinition
from common.lib.constants.LogDefinition import DebugLevels
from common.cli.data_models.CliConfig import CliConfig
from common.lib.core.Terminal import Terminal
from common.lib.enums.TermFilesPath import TermFilesPath


class SignalCli(Terminal):
    _cli_config: CliConfig = None
    _finished: pyqtSignal = pyqtSignal()

    def __init__(self, config: Config):
        super(SignalCli, self).__init__(config)
        self.config: Config = config
        self.application = QCoreApplication([])
        self.run_timer = QTimer()
        self.connect_all()
        self.setup()

    def setup(self):
        self.logger.create_logger()

        signal(SIGINT, SIG_DFL)

        cli_args_parser: ArgumentParser = ArgumentParser(description=TextConstants.CLI_DESCRIPTION)

        cli_args_parser.add_argument("-c", "--console-mode", action="store_true", required=True, help="Run SIGNAL in Command Line Interface mode")
        cli_args_parser.add_argument("-f", "--file", type=str, default=None, help="File or file-mask to parse")
        cli_args_parser.add_argument("-d", "--dir", type=str, default=None, help="Directory with files to parse. SIGNAL will try all of the files from the directory")
        cli_args_parser.add_argument("-a", "--address", default=self.config.host.host, action="store", help="Host TCP/IP address")
        cli_args_parser.add_argument("-p", "--port", type=int, default=self.config.host.port, action="store", help="TCP/IP port to connect")
        cli_args_parser.add_argument("-r", "--repeat", action="store_true", help="Repeat transactions after sending")
        cli_args_parser.add_argument("-l", "--log-level", type=str, default=DebugLevels.INFO, action="store", help=f"Debug level {DebugLevels.DEBUG}, {DebugLevels.INFO}, etc")
        cli_args_parser.add_argument("-i", "--interval", type=int, default=0, action="store", help="Wait (seconds) before send next transaction")
        cli_args_parser.add_argument("--parallel", action="store_true", help="Send new transaction with no waiting of answer for previous one")
        cli_args_parser.add_argument("-t", "--timeout", type=int, default=60, help="Timeout of waiting resp")
        cli_args_parser.add_argument("--about", action="store_true", help="Show info about the SIGNAL")
        cli_args_parser.add_argument("-e", "--echo-test", action="store_true", help="Send echo-test")
        cli_args_parser.add_argument("--default", action="store_true", help="Send default transaction message")
        cli_args_parser.add_argument("-v", "--version", action="store_true", help="Print current version of SIGNAL")

        cli_arguments = cli_args_parser.parse_args()

        try:
            self._cli_config = CliConfig.model_validate(cli_arguments.__dict__)
        except (ValidationError, ValueError) as arg_parsing_error:
            error(arg_parsing_error)
            return

        try:
            self.parse_cli_config(self._cli_config)
        except ValueError:
            error("Error run in Console Mode")
            self._finished.emit()

        self.logger.set_debug_level()

        if self._cli_config.version:
            self.version()

        if self._cli_config.about:
            self.log_printer.print_about()

        if not any([self._cli_config.version, self._cli_config.about]):
            info("## Running SIGNAL in Console mode ##")
            info("Press CTRL+C to exit")
            info(str())

    def connect_all(self):
        self.run_timer.timeout.connect(self.main)
        self._finished.connect(self.application.quit)

    def print_transaction(self, transaction):
        try:
            self.log_printer.print_transaction(transaction)
        except Exception as print_error:
            error(print_error)

    def run_application(self):
        self.run_timer.setSingleShot(True)
        self.run_timer.start(0)
        self.application.exec()

    def main(self):
        if not (filenames := self.get_files_to_process()):
            if not any([self._cli_config.about, self._cli_config.version]):
                error("Cannot found specified files")

            return

        while True:

            for file in filenames:
                info(str())
                info(f"Processing file {basename(file)}")

                try:
                    transaction: Transaction = self.parser.parse_file(file)
                except Exception as parsing_error:
                    error(parsing_error)
                    continue

                self.send(transaction)

                if not self._cli_config.parallel:
                    self.wait_response(transaction)

                for _ in range(self._cli_config.interval * 10):
                    self.wait(0.1)

            if not self._cli_config.repeat:
                break

    def get_files_to_process(self) -> list[str]:
        filenames: list[str] = list()

        if self._cli_config.echo_test:
            filenames.append(TermFilesPath.ECHO_TEST)

        if self._cli_config.default:
            filenames.append(TermFilesPath.DEFAULT_FILE)

        if self._cli_config.dir:
            dir_files = listdir(self._cli_config.dir)
            dir_files = ["/".join([str(self._cli_config.dir), file]) for file in dir_files]

            filenames.extend(dir_files)

        if self._cli_config.file:
            filenames.extend(glob(self._cli_config.file))

        filenames = map(normpath, filenames)
        filenames = [filename for filename in filenames if isfile(filename)]
        filenames = list(set(filenames))

        return filenames

    def parse_cli_config(self, cli_config: CliConfig):
        self.config.host.host = str(cli_config.address) if cli_config.address else self.config.host.host
        self.config.host.port = int(cli_config.port) if cli_config.port else self.config.host.port
        self.config.debug.level = cli_config.log_level if cli_config.log_level else self.config.debug.level

    def wait_response(self, request: Transaction):
        while not request.matched:
            if (datetime.now() - request.sending_time).total_seconds() > self._cli_config.timeout:
                return

            self.wait(0.1)

    def wait(self, sec):
        sleep(sec)
        self.application.processEvents()

    @staticmethod
    def version():
        info(f"SIGNAL {ReleaseDefinition.VERSION} | {ReleaseDefinition.RELEASE}")
