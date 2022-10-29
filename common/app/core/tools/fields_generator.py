from datetime import datetime
from random import randint, choice
from common.app.exceptions.exceptions import ParsingError
from common.app.data_models.transaction import Transaction
from common.app.core.tools.epay_specification import EpaySpecification


class FieldsGenerator(object):
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

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

    @staticmethod
    def set_trans_id_to_47_072(transaction: Transaction) -> Transaction:  # TODO
        try:
            transaction.data_fields["47"]["072"] = transaction.trans_id
        except (KeyError, TypeError):
            ...

        return transaction

    def set_generated_fields(self, transaction: Transaction) -> Transaction:
        for field in transaction.generate_fields:
            if not self.spec.can_be_generated([field]):
                continue

            transaction.data_fields[field] = self.generate_field(field, max_amount=transaction.max_amount)

        transaction.data_fields = {
            field: transaction.data_fields[field] for field in sorted(transaction.data_fields, key=int)
        }

        return transaction

    def generate_field(self, field: str, max_amount="100"):
        if field == self.spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT:
            max_amount = str(randint(0, int(max_amount) * 100))
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

    def add_logical_fields(self, transaction: Transaction) -> Transaction:
        transaction.trans_id = self.trans_id() if not transaction.trans_id else transaction.trans_id
        transaction.is_request = self.spec.is_request(transaction)
        transaction.is_reversal = self.spec.is_reversal(transaction.message_type)

        if transaction.is_request:
            return transaction

        try:
            transaction.utrnno = transaction.data_fields["47"]["064"]
        except KeyError:
            transaction.utrnno = ""

        if transaction.data_fields.get(self.spec.FIELD_SET.FIELD_039_AUTHORIZATION_RESPONSE_CODE) == "00":
            transaction.success = True

        return transaction

    def merge_trans_data(self, request: Transaction, response: Transaction):
        for message in (request, response):
            self.add_logical_fields(message)

        request.utrnno = response.utrnno
        request.success = response.success
        request.resp_time_seconds = response.resp_time_seconds
        response.generate_fields = request.generate_fields
