from datetime import datetime
from random import randint, choice
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.exceptions.exceptions import ParsingError
from common.app.data_models.transaction import Transaction


class FieldsGenerator(object):
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    def __init__(self, config):
        self.config = config

    @staticmethod
    def trans_id() -> str:
        return f"{datetime.now():%Y%m%d_%H%M%S_%f}{randint(0, 999):03}"

    def generate_original_data_elements(self, transaction: Transaction) -> str:
        try:
            mti: str = transaction.message_type
            stan: str = transaction.data_fields[self.spec.FIELD_SET.FIELD_011_SYSTEM_TRACE_AUDIT_NUMBER]
            date: str = transaction.data_fields[self.spec.FIELD_SET.FIELD_007_TRANSMISSION_DATE_AND_TIME]
        except KeyError:
            raise ParsingError("Original data elements generating error!")

        return f"{mti}{stan}{date}"

    def set_trans_id_to_47_072(self, transaction: Transaction) -> Transaction:  # TODO
        if not transaction.trans_id:
            transaction.trans_id = self.trans_id()

        try:
            transaction.data_fields["47"]["072"] = transaction.trans_id
        except (KeyError, TypeError):
            ...

        return transaction

    def set_generated_fields(self, transaction: Transaction) -> Transaction:
        for field in transaction.generate_fields:
            transaction.data_fields[field] = self.generate_field(field)

        return transaction

    def generate_field(self, field: str):
        if field == self.spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT:
            max_amount = str(randint(0, int(self.config.fields.max_amount) * 100))
            field_length = self.spec.get_field_length(self.spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT)
            max_amount = max_amount.zfill(field_length)

            return max_amount

        if date_format := self.spec.get_field_date_format(field):
            return f"{datetime.now():{date_format}}"

        data_kit = self.spec.get_field_data_kit([field])
        length = self.spec.get_field_length(field)
        data = (choice(data_kit) for _ in range(length))
        data = "".join(data)

        return data
