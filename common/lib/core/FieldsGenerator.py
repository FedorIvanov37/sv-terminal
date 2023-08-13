from datetime import datetime
from random import randint, choice
from common.lib.data_models.Transaction import Transaction
from common.lib.core.EpaySpecification import EpaySpecification


class FieldsGenerator:
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    def generate_original_data_elements(self, transaction: Transaction) -> str:
        try:
            mti: str = transaction.message_type
            stan: str = transaction.data_fields[self.spec.FIELD_SET.FIELD_011_SYSTEM_TRACE_AUDIT_NUMBER]
            date: str = transaction.data_fields[self.spec.FIELD_SET.FIELD_007_TRANSMISSION_DATE_AND_TIME]
        except KeyError:
            raise ValueError("Original data elements generating error!")

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

    @staticmethod
    def generate_field(field: str, max_amount: int = 100):
        spec = EpaySpecification()
        max_amount: str = str(max_amount)

        if field == spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT:
            max_amount = str(randint(1, int(max_amount) * 100))
            field_length = spec.get_field_length(spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT)
            max_amount = max_amount.zfill(field_length)

            return max_amount

        if date_format := spec.get_field_date_format(field):
            return f"{datetime.now():{date_format}}"

        data_kit = spec.get_field_data_kit([field])
        length = spec.get_field_length(field)
        data = (choice(data_kit) for _ in range(length))
        data = "".join(data)

        return data

    def add_logical_fields(self, transaction: Transaction) -> Transaction:
        transaction.is_request = self.spec.is_request(transaction)
        transaction.is_reversal = self.spec.is_reversal(transaction.message_type)

        if transaction.is_request:
            return transaction

        try:  # TODO
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
        response.is_keep_alive = request.is_keep_alive
