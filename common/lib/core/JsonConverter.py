from json import dumps
from pydantic import ValidationError
from common.lib.data_models.Transaction import Transaction, OldTransactionModel


# Temporary solution for backward compatibility of JSON transaction messages


class JsonConverter:

    @staticmethod
    def convert(filename):
        if JsonConverter.get_transaction_model(filename) is OldTransactionModel:
            JsonConverter.convert_json(filename)

    @staticmethod
    def convert_json(filename: str):
        old_transaction = OldTransactionModel.parse_file(filename)

        transaction = Transaction(
            trans_id=old_transaction.transaction.id,
            message_type=old_transaction.transaction.message_type,
            max_amount=old_transaction.config.max_amount,
            generate_fields=old_transaction.config.generate_fields,
            data_fields=old_transaction.transaction.fields,
        )

        with open(filename, 'w') as file:
            file.write(dumps(transaction.dict(), indent=4))

        return transaction

    @staticmethod
    def get_transaction_model(filename):  # Temporary solution for transfer period
        try:
            OldTransactionModel.parse_file(filename)
            return OldTransactionModel

        except ValidationError as validation_error:
            err = validation_error.errors()[0]

            if err["loc"][0] == 'config' and err["msg"] == 'field required':
                return Transaction

            raise validation_error
