from signal.lib.core.validators.Validator import Validator
from signal.lib.data_models.Config import Config
from signal.lib.data_models.Transaction import Transaction
from signal.lib.data_models.Validation import ValidationResult


class TransValidator:
    def __init__(self, config: Config):
        self.config = config
        self.validator = Validator(self.config)

    def validate_transaction(self, transaction: Transaction) -> None:
        validation_result: ValidationResult = ValidationResult()
        validation_result = self.validator.validate_mti(transaction.message_type, validation_result)
        validation_result = self.validator.validate_fields(transaction.data_fields, validation_result)
        self.validator.process_validation_result(validation_result)

    def validate_fields(self, fields) -> None:
        validation_result: ValidationResult = self.validator.validate_fields(fields, ValidationResult())
        self.validator.process_validation_result(validation_result)

    def validate_field_spec(self, field_path: list[str]) -> None:
        validation_result: ValidationResult = self.validator.validate_field_spec(field_path, ValidationResult())
        self.validator.process_validation_result(validation_result)
