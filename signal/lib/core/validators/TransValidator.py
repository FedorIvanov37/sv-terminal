from signal.lib.core.validators.Validator import Validator
from signal.lib.data_models.Config import Config
from signal.lib.exceptions.exceptions import DataValidationError
from signal.lib.data_models.Transaction import Transaction


class TransValidator(Validator):
    def __init__(self, config: Config):
        super(TransValidator, self).__init__(config)
        self.config = config

    def validate_transaction(self, transaction: Transaction) -> None:
        self.validate_mti(transaction.message_type)

        if self.validate_fields(transaction.data_fields):
            raise DataValidationError
