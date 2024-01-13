from common.lib.core.validators.Validator import Validator
from common.lib.data_models.Config import Config
from common.lib.data_models.Validation import ValidationResult
from common.lib.data_models.Transaction import Transaction
from common.lib.exceptions.exceptions import DataValidationError, DataValidationWarning


class TransValidator(Validator):
    def __init__(self, config: Config):
        super(TransValidator, self).__init__(config)
        self.config = config

    def validate_transaction(self, transaction: Transaction):
        self.validate_mti(transaction.message_type)
        validation_result: ValidationResult = self.validate_fields(transaction.data_fields)
        self.process_validation_result(validation_result)
