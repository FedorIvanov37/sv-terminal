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
        return datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    def generate_field(self, field, max_amount=None):
        if field == self.spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT:  # A crutch for avoiding huge amounts

            if max_amount is None:
                max_amount: int | str = self.config.fields.max_amount

            max_amount = int(max_amount)
            max_amount = str(randint(0, max_amount * 100))
            max_amount = max_amount.zfill(self.spec.get_field_length(self.spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT))

            return max_amount

        length = self.spec.get_field_length(str(field))
        date_format = self.spec.get_field_date_format(field)
        data_kit = self.spec.get_field_data_kit(field)

        if not date_format:
            data = [choice(data_kit) for _ in range(length)]
            data = "".join(data)
        else:
            data = datetime.strftime(datetime.now(), date_format)

        return data

    def generate_original_data_elements(self, message: Message) -> str:
        try:
            mti: str = message.transaction.message_type_indicator
            stan: str = message.transaction.fields[self.spec.FIELD_SET.FIELD_011_SYSTEM_TRACE_AUDIT_NUMBER]
            date: str = message.transaction.fields[self.spec.FIELD_SET.FIELD_007_TRANSMISSION_DATE_AND_TIME]
        except KeyError:
            raise ParsingError("Original data elements generating error!")

        return f"{mti}{stan}{date}"
