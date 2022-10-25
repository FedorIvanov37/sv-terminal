from datetime import datetime
from random import randint, choice
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.data_models.message import Message
from common.app.exceptions.exceptions import ParsingError


class FieldsGenerator(object):
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    def __init__(self, config):
        self.config = config

    @staticmethod
    def trans_id() -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S_%f") + str(randint(0, 999)).zfill(3)

    def generate_original_data_elements(self, message: Message) -> str:
        try:
            mti: str = message.transaction.message_type
            stan: str = message.transaction.fields[self.spec.FIELD_SET.FIELD_011_SYSTEM_TRACE_AUDIT_NUMBER]
            date: str = message.transaction.fields[self.spec.FIELD_SET.FIELD_007_TRANSMISSION_DATE_AND_TIME]
        except KeyError:
            raise ParsingError("Original data elements generating error!")

        return f"{mti}{stan}{date}"

    def set_trans_id_to_47_072(self, message: Message) -> Message:  # TODO
        if not message.transaction.id:
            message = self.trans_id()

        try:
            message.transaction.fields["47"]["072"] = message.transaction.id
        except (KeyError, TypeError):
            ...

        return message

    def set_generated_fields(self, message: Message) -> Message:
        for field in message.config.generate_fields:
            message.transaction.fields[field] = self.generate_field(field)

        return message

    def generate_field(self, field: str):
        if field == self.spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT:
            max_amount = str(randint(0, int(self.config.fields.max_amount) * 100))
            max_amount = max_amount.zfill(self.spec.get_field_length(self.spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT))

            return max_amount

        if date_format := self.spec.get_field_date_format(field):
            return datetime.strftime(datetime.now(), date_format)

        data_kit = self.spec.get_field_data_kit([field])
        length = self.spec.get_field_length(field)
        data = (choice(data_kit) for _ in range(length))
        data = "".join(data)

        return data
