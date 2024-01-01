from logging import warning, error
from common.lib.core.validators.Validator import Validator
from common.lib.data_models.Config import Config, ValidationMode
from common.lib.data_models.ValidationResult import ValidationResult
from common.lib.data_models.Transaction import Transaction, TypeFields
from common.lib.data_models.Types import FieldPath


class TransValidator(Validator):
    def __init__(self, config: Config):
        super(TransValidator, self).__init__()
        self.config = config

    def validate_transaction(self, transaction: Transaction):
        self.validate_mti(transaction.message_type)
        validation_result: ValidationResult = self.validate_fields(transaction.data_fields)

        try:
            self.process_validation_result(validation_result)
        except ValueError as E:
            error(E)

    def process_validation_result(self, validation_result: ValidationResult):
        errors: set[str] = set()

        for error_set in validation_result.errors.values():
            if not isinstance(error_set, set):
                continue

            errors.update(error_set)

        if not errors:
            return

        match self.config.validation.validation_mode:
            case ValidationMode.IGNORE:
                return

            case ValidationMode.ERROR:
                raise ValueError("\n".join(errors))

            case ValidationMode.WARNING:
                for error_desc in errors:
                    warning(error_desc)

            case ValidationMode.FLEXIBLE:
                check_types = [check_type for check_type in validation_result.errors if validation_result.errors.get(check_type)]
                ...


    def validate_fields(self, fields: TypeFields, field_path: FieldPath | None = None, validation_result: ValidationResult = None) -> ValidationResult:
        if validation_result is None:
            validation_result: ValidationResult = ValidationResult()

        if field_path is None:
            field_path = []

        for field, value in fields.items():
            field_path.append(field)

            if isinstance(value, dict):
                self.validate_fields(fields=value, field_path=field_path, validation_result=validation_result)
                field_path.pop()
                continue

            validation_result: ValidationResult = self.validate_field_data(field_path, value, validation_result)

            field_path.pop()

        return validation_result
