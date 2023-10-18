from json import dumps
from logging import debug, info, error
from common.lib.constants import TextConstants
from common.lib.data_models.Transaction import Transaction
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.core.Parser import Parser
from common.lib.toolkit.toolkit import mask_pan, mask_secret
from common.lib.data_models.Config import Config


class LogPrinter:
    spec: EpaySpecification = EpaySpecification()
    default_level = info

    def __init__(self, config: Config):
        self.config = config

    @staticmethod
    def print_multi_row(data: str, level=default_level):
        for string in data.splitlines():
            level(string)

        level("")

    def print_startup_info(self, level=default_level):
        LogPrinter.print_multi_row(TextConstants.HELLO_MESSAGE)
        config_data = dumps(self.config.model_dump(), indent=4)
        config_data = f"## Configuration parameters ##\n{config_data}\n## End of configuration parameters ##"
        self.print_multi_row(config_data, level=level)

    def print_dump(self, transaction: Transaction, level=debug):
        if not(dump := Parser.create_sv_dump(transaction)):
            return

        self.print_multi_row(dump, level)

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

            if all((hide_secrets, self.spec.is_field_complex([field]), isinstance(field_data, str))):
                try:
                    field_data = Parser.split_complex_field(field, field_data)
                except Exception:
                    pass

            if isinstance(field_data, dict):
                try:
                    field_data: str = Parser.join_complex_field(field, field_data, hide_secrets=hide_secrets)
                except Exception as parsing_error:
                    error(f"Cannot print field {field}")
                    error(f"data parsing error: {parsing_error}")
                    continue

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
