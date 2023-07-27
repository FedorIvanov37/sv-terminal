from json import dumps
from logging import debug, info, error
from common.gui.constants.TextConstants import TextConstants
from common.lib.data_models.Config import Config
from common.lib.data_models.Transaction import Transaction
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.core.Parser import Parser
from common.lib.toolkit.toolkit import mask_pan


class LogPrinter:
    spec: EpaySpecification = EpaySpecification()
    default_level = info

    @staticmethod
    def print_multi_row(data: str, level=default_level):
        for string in data.splitlines():
            level(string)

        level("")

    def print_startup_info(self, config: Config, level=default_level):
        LogPrinter.print_multi_row(TextConstants.HELLO_MESSAGE)
        config_data = dumps(config.dict(), indent=4)
        config_data = f"## Configuration parameters ##\n{config_data}\n## End of configuration parameters ##"
        self.print_multi_row(config_data, level=level)

    def print_dump(self, transaction: Transaction, level=debug):
        if not(dump := Parser.create_sv_dump(transaction)):
            return

        self.print_multi_row(dump, level)

    def print_transaction(self, transaction: Transaction, level=default_level):
        def put(string: str, size=0):
            return f"[{string.zfill(size)}]"

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

            if level is not debug and field == self.spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
                field_data = mask_pan(field_data)

            if isinstance(field_data, dict):
                try:
                    field_data = Parser.join_complex_field(field, field_data)
                except Exception as parsing_error:
                    error(f"Cannot print field {field}")
                    error(f"data parsing error: {parsing_error}")
                    continue

            length = str(len(field_data))
            level(f"{put(field, size=3)}{put(length, size=3)}{put(field_data)}")

        level("")
