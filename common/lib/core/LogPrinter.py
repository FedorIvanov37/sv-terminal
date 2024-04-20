from logging import debug, info, warning, error
from common.lib.data_models.Transaction import Transaction
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.core.Parser import Parser
from common.lib.toolkit.toolkit import mask_pan, mask_secret
from common.lib.data_models.Config import Config
from common.lib.enums.TextConstants import TextConstants
from common.lib.enums.ReleaseDefinition import ReleaseDefinition
from common.lib.enums.TermFilesPath import TermFilesPath
from PyQt6.QtCore import QObject


class LogPrinter(QObject):
    spec: EpaySpecification = EpaySpecification()
    default_level = info

    def __init__(self, config: Config):
        super().__init__()
        self.config = config

    @staticmethod
    def print_multi_row(data: str, level=default_level):
        for string in data.splitlines():
            level(string)

        level("")

    @staticmethod
    def startup_finished(level=default_level):
        level("Startup finished")

    def print_startup_info(self, level=default_level):
        LogPrinter.print_multi_row(TextConstants.HELLO_MESSAGE)
        self.print_config(self.config, level=level)

    def print_config(self, config: Config | None = None, path=TermFilesPath.CONFIG, level=default_level):
        if config is None:
            config = self.config

        config_data = f"## Configuration parameters ##\n\n"
        config_data = f"{config_data}Path: {path}\n\n"
        config_data = f"{config_data}Data:\n{config.model_dump_json(indent=4)}\n\n"
        config_data = f"{config_data}## End of configuration parameters ##"

        self.print_multi_row(config_data, level=level)

    def print_dump(self, transaction: Transaction, level=debug):
        if not(dump := Parser.create_sv_dump(transaction)):
            return

        self.print_multi_row(dump, level)

    def print_about(self):
        elements = [
            TextConstants.HELLO_MESSAGE,
            "Use only on test environment",
            f"Version {ReleaseDefinition.VERSION}",
            f"Released in {ReleaseDefinition.RELEASE}",
            f"Developed by {ReleaseDefinition.AUTHOR}",
            f"Contact {ReleaseDefinition.EMAIL}"
        ]

        message = "\n\n  ".join(elements)

        self.print_multi_row(message)

    def print_transaction(self, transaction: Transaction, level=default_level):
        if transaction.is_keep_alive:
            return

        level("")

        bitmap = ", ".join(transaction.data_fields.keys())
        trans_id = transaction.trans_id

        if transaction.matched and not transaction.is_request:
            trans_id = transaction.match_id

        level(f"[TRANS_ID][{trans_id}]")

        if transaction.utrnno:
            level(f"[UTRNNO  ][{transaction.utrnno}]")

        level(f"[MSG_TYPE][{transaction.message_type}]")
        level(f"[BITMAP  ][{bitmap}]")

        for field, field_data in transaction.data_fields.items():
            if field == self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY:
                continue

            hide_secrets: bool = self.config.fields.hide_secrets

            if self.spec.is_field_complex([field]) and isinstance(field_data, dict):
                try:
                    field_data = Parser.join_complex_field(field, field_data)
                except Exception as parsing_error:
                    error(f"Cannot print field {field}: {parsing_error}")
                    continue

            if all((hide_secrets, self.spec.is_field_complex([field]), isinstance(field_data, str))):
                try:
                    split_field_data: dict = Parser.split_complex_field(field, field_data)
                    field_data: str = Parser.join_complex_field(field, split_field_data, hide_secrets=hide_secrets)

                except Exception as field_parsing_error:
                    warning(field_parsing_error)

            match field:
                case self.spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
                    field_data: str = mask_pan(field_data)

                case _:
                    if all((hide_secrets, self.spec.is_secret([field]))):
                        field_data: str = mask_secret(field_data)

            length = str(len(field_data))

            message = str()

            for element in field, length, field_data:
                size: int = int() if element is field_data else 3
                message: str = message + f"[{element.zfill(size)}]"

            level(message)

        level("")

    @staticmethod
    def print_version(level=default_level):
        level(f"SIGNAL {ReleaseDefinition.VERSION} | {ReleaseDefinition.RELEASE}")
