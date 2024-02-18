from typing import Callable
from datetime import datetime
from string import digits, ascii_letters, punctuation, whitespace 
from pydantic import AnyHttpUrl
from copy import deepcopy
from logging import error, warning
from signal.lib.exceptions.exceptions import DataValidationError, DataValidationWarning
from signal.lib.core.EpaySpecification import EpaySpecification
from signal.lib.data_models.Types import FieldPath
from signal.lib.data_models.Config import Config
from signal.lib.data_models.Validation import ValidationResult, ValidationTypes
from signal.lib.enums.Validation import ValidationMode, CustomValidations, ExtendedValidations
from signal.lib.data_models.Transaction import TypeFields
from signal.gui.enums.FieldTypeParams import FieldTypeParams
from signal.lib.enums.MessageLength import MessageLength
from signal.lib.core.Parser import Parser


class Validator:
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    def __init__(self, config: Config):
        self.config = config

    @staticmethod
    def validate_url(url: str):
        AnyHttpUrl(url)

    def validate_mti(self, mti):
        if mti in self.spec.get_mti_codes():
            return

        raise DataValidationError(f"Unknown MTI: {mti}")

    @staticmethod
    def check_luhn(value: str) -> bool:  # Based on code example from https://en.wikipedia.org/wiki/Luhn_algorithm
        def digits_of(val):
            return [int(dig) for dig in str(val)]

        if not value.isdigit():
            return False

        digits_kit: list[int] = digits_of(value)
        odd_digits: list[int] = digits_kit[-1::-2]
        even_digits: list[int] = digits_kit[-2::-2]
        checksum: int = int()
        checksum += sum(odd_digits)

        for digit in even_digits:
            checksum += sum(digits_of(digit * 2))

        status: bool = checksum % 10 == int()

        return status

    @staticmethod
    def validate_field_number(field_number: int | str, is_top_level_field=True):
        # Field number validations, such as the number should contain digits only, etc

        if not field_number:
            raise ValueError("Lost field number")

        try:
            field_number = int(field_number)
        except ValueError:
            raise ValueError(f'Non-digit field number "{field_number}"')

        if not is_top_level_field:
            return

        if field_number not in range(1, MessageLength.SECOND_BITMAP_CAPACITY):
            error_text = f"Incorrect field number {field_number}. Top level field number must be in range 1 " \
                         f"- {MessageLength.SECOND_BITMAP_CAPACITY}"

            raise ValueError(error_text)

    def validate_field_path(self, path: FieldPath):
        def path_to_str(field_path: FieldPath):
            return ".".join(field_path)

        if not path:
            raise ValueError("Lost field path")

        if str() in path:
            path: map = map(lambda field_data: field_data if field_data else '<empty>', path)
            path: str = path_to_str(list(path))
            raise ValueError(f"{path} - empty field number in field path")

        str_path = path_to_str(path)

        for level, field in enumerate(path, start=1):
            try:
                self.validate_field_number(field, is_top_level_field=level == 1)

            except ValueError as validation_error:
                raise ValueError(f"{validation_error}. Path: {str_path}")

        if not self.spec.get_field_spec(path=path):
            raise ValueError(f"{str_path} - lost spec for field")

    def validate_field_data(self, field_path: FieldPath, field_value: str, validation_result: ValidationResult):
        path = ".".join(field_path)
        field_spec = self.spec.get_field_spec(field_path)
        path_desc: str = f"{path} - {field_spec.description}"

        def fields_pre_validation():
            errors: set[str] = set()
            length = len(field_value)

            if not field_value:  # Field should contain the data
                errors.add(f"{path} - lost field value for field")

            if not all(field.isdigit() for field in field_path):  # Field number should be digit
                errors.add(f"Field numbers can be digits only. {path} is wrong value")

            if length > field_spec.max_length:  # Max length validation
                errors.add(f"Field {path} - over MaxLength. Max length: {field_spec.max_length} got: {length}")

            if length < field_spec.min_length:  # Min length validation
                errors.add(f"Field {path} - less MinLength. Min length: {field_spec.min_length} got: {length}")

            return errors

        def main_validations(): # ANS-validation. Checks the occurrence of non-allowed charset
            errors: set[str] = set()
            alphabetic: str = ascii_letters
            numeric: str = digits
            specials: str = punctuation + whitespace 
            valid_values: str = alphabetic + numeric + specials

            for letter in field_value:
                if letter not in valid_values:  # Only ascii-printable allowed
                    errors.add(f"Field {path} - non-printable letters in field. Seems like a problem with encoding")

                if letter in ascii_letters and not field_spec.alpha:  # Validation charset - alphabetic
                    errors.add(f"Field {path_desc} - alphabetic values not allowed")

                if letter in digits and not field_spec.numeric:  # Validation charset - numeric
                    errors.add(f"Field {path_desc} - numeric values not allowed")

                if letter in specials and not field_spec.special:  # Validation charset - special
                    errors.add(f"Field {path_desc} - special values not allowed")

            return errors

        def custom_validations():  # Custom validations set by user
            errors: set[str] = set()

            for validation, patterns in field_spec.validators.model_dump().items():
                if not patterns or not isinstance(patterns, list):
                    continue

                match validation:
                    case CustomValidations.VALID_VALUES:  # Exact allowed value validation
                        if not field_value in patterns:
                            bad_patterns = ", ".join(patterns)
                            errors.add(f'Field {path_desc} must contain one of the following: {bad_patterns}')

                    case CustomValidations.INVALID_VALUES:  # Exact not allowed value validation
                        if field_value in patterns:
                            bad_patterns = ", ".join(patterns)
                            errors.add(f'Field {path_desc} must not contain one of the following: {bad_patterns}')

                for pattern in patterns:
                    match validation:
                        case CustomValidations.MUST_CONTAIN:
                            if pattern not in field_value:
                                errors.add(f'Field {path_desc} must contain "{pattern}"')

                        case CustomValidations.MUST_CONTAIN_ONLY:
                            bad_patterns = ", ".join(patterns)

                            if [letter for letter in field_value if letter not in patterns]:
                                errors.add(f"Field {path_desc} must contain only one or multiple: {bad_patterns}")

                        case CustomValidations.MUST_NOT_CONTAIN:
                            if pattern in field_value:
                                errors.add(f'Field {path_desc} must not contain {pattern}')

                        case CustomValidations.MUST_NOT_CONTAIN_ONLY:
                            if not [letter for letter in field_value if letter not in pattern]:
                                errors.add(f"Field {path_desc} must not contain only one or multiple {pattern}")

                        case CustomValidations.MUST_START_WITH:
                            if not field_value.startswith(pattern):
                                errors.add(f"Field {path_desc} must start with {pattern}")

                        case CustomValidations.MUST_NOT_START_WITH:
                            if field_value.startswith(pattern):
                                errors.add(f"Field {path_desc} must not start with {pattern}")

                        case CustomValidations.MUST_END_WITH:
                            if not field_value.endswith(pattern):
                                errors.add(f"Field {path_desc} must end with {pattern}")

                        case CustomValidations.MUST_NOT_END_WITH:
                            if field_value.endswith(pattern):
                                errors.add(f"Field {path_desc} must not end with {pattern}")

            return errors

        def country_validations(): # Validation ISO-4217 country codes
            errors: set[str] = set()
            allowed_country_codes: list[str] = list()

            if field_spec.validators.field_type_validators.country_a2:
                allowed_country_codes.extend([country.code_a2 for country in self.spec.dictionary.countries.countries])

            if field_spec.validators.field_type_validators.country_a3:
                allowed_country_codes.extend([country.code_a3 for country in self.spec.dictionary.countries.countries])

            if field_spec.validators.field_type_validators.country_n3:
                allowed_country_codes.extend([country.code_n3 for country in self.spec.dictionary.countries.countries])

            for field, value in field_spec.validators.field_type_validators.model_dump().items():
                if not value:
                    continue

                if field not in (ExtendedValidations.COUNTRY_A3, ExtendedValidations.COUNTRY_N3, ExtendedValidations.COUNTRY_A2):
                    continue

                if field_value in allowed_country_codes:
                    continue

                errors.add(f"Field {path_desc} must contain valid ISO country code")

            return errors

        def currency_validation():
            errors: set[str] = set()
            allowed_currency_codes: list[str] = list()

            if field_spec.validators.field_type_validators.currency_a3:
                allowed_currency_codes.extend([curr.code_a3 for curr in self.spec.dictionary.currencies.currencies])

            if field_spec.validators.field_type_validators.currency_n3:
                allowed_currency_codes.extend([curr.code_n3 for curr in self.spec.dictionary.currencies.currencies])

            for field, value in field_spec.validators.field_type_validators.model_dump().items():
                if not value:
                    continue

                if field not in (ExtendedValidations.CURRENCY_A3, ExtendedValidations.COUNTRY_N3):
                    continue

                if field_value in allowed_currency_codes:
                    continue

                errors.add(f"Field {path_desc} must contain valid ISO currency code")

            return errors

        def extended_validations(): # Extended, logical validation, based on business-purpose of the data field
            errors: set[str] = set()

            for field, value in field_spec.validators.field_type_validators.model_dump().items():
                if not value:
                    continue

                match field:
                    case ExtendedValidations.CHECK_LUHN:  # Check by the Luhn algorithm
                        if not self.check_luhn(field_value):
                            errors.add(f"Field {path_desc} - did not pass validation by the Luhn algorithm")

                    case ExtendedValidations.MCC:  # Valid merchant category code
                        mcc_list = (mcc.code for mcc in self.spec.dictionary.merch_cat_codes.merchant_category_codes)

                        if field_value not in mcc_list:
                            errors.add(f"Field {path_desc} - must contain valid {FieldTypeParams.MCC_ISO}")

                    case ExtendedValidations.ONLY_UPPER:  # Only UPPER case allowed
                        if not field_value.isupper():
                            errors.add(f"Field {path_desc} - allowed UPPER case only")

                    case ExtendedValidations.ONLY_LOWER:  # Only lower case allowed
                        if not field_value.islower():
                            errors.add(f"Field {path_desc} - allowed lower case only")

                    case ExtendedValidations.DATE_FORMAT:  # Date format and timeframes
                        date: datetime | None = None
                        date_format: str = field_spec.validators.field_type_validators.date_format

                        if field_spec.validators.field_type_validators.date_format:
                            try:
                                date: datetime = datetime.strptime(field_value, date_format)
                            except ValueError:
                                errors.add(f'Field {path_desc} - must contain date in the following format: "{date_format}"')

                        if date is not None:
                            current_date = datetime.strptime(datetime.strftime(datetime.now(), date_format), date_format)

                            if not field_spec.validators.field_type_validators.past and date < current_date:
                                errors.add(f"Field {path_desc} - past time not allowed")

                            if not field_spec.validators.field_type_validators.future and date > current_date:
                                errors.add(f"Field {path_desc} - future time not allowed")

                            if not field_spec.validators.field_type_validators.present and date == current_date:
                                errors.add(f"Field {path_desc} - present time not allowed")

            return errors

        if field_spec.validators.field_type_validators.do_not_validate:  # When all the field validations should be ignored
            validation_result.errors = deepcopy(ValidationResult().errors)  # Clean the errors
            return validation_result

        validators_map: dict[ValidationTypes, Callable] = {
            ValidationTypes.FIELD_DATA_PRE_VALIDATION: fields_pre_validation,
            ValidationTypes.FIELD_DATA_MAIN_VALIDATION: main_validations,
            ValidationTypes.FIELD_DATA_CUSTOM_VALIDATION: custom_validations,
            ValidationTypes.EXTENDED_VALIDATION: extended_validations,
            ValidationTypes.CURRENCY_VALIDATION: currency_validation,
            ValidationTypes.COUNTRY_VALIDATION: country_validations,
        }

        for check_type, validator in validators_map.items():
            validation_errors: set[str] = validator()

            if validation_result.errors.get(check_type) is None:
                validation_result.errors[check_type] = set()

            validation_result.errors[check_type].update(validation_errors)

        return validation_result

    def process_validation_result(self, validation_result: ValidationResult):
        errors: set[str] = set()

        for error_set in validation_result.errors.values():
            if not isinstance(error_set, set):
                continue

            errors.update(error_set)

        if not errors:
            return

        errors_string = "\n".join(errors)

        match self.config.validation.validation_mode:
            case ValidationMode.ERROR:
                raise DataValidationError(errors_string)

            case ValidationMode.WARNING:
                raise DataValidationWarning(errors_string)

            case ValidationMode.FLEXIBLE:
                for check_type in validation_result.errors:
                    if not validation_result.errors.get(check_type):
                        continue

                    if check_type in validation_result.critical_validation_types:
                        raise DataValidationError(errors_string)

                    raise DataValidationWarning(errors_string)

    def validate_fields(self, fields: TypeFields, field_path: FieldPath | None = None, validation_result: ValidationResult = None, val_error: bool = False):
        if validation_result is None:
            validation_result: ValidationResult = ValidationResult()

        if field_path is None:
            field_path = []

        for field, value in fields.items():
            field_path.append(field)

            if self.spec.is_field_complex(field_path):
                field_value_dict = value

                if not isinstance(value, dict):
                    field_value_dict = Parser.split_complex_field(field_path[int()], value)

                self.validate_fields(fields=field_value_dict, field_path=field_path, validation_result=validation_result, val_error=val_error)
                field_path.pop()
                continue

            validation_result: ValidationResult = self.validate_field_data(field_path, value, ValidationResult())

            try:
                self.process_validation_result(validation_result)

            except DataValidationError as validation_error:
                [error(f"Validation: {err}") for err in str(validation_error).splitlines()]
                val_error = True

            except DataValidationWarning as validation_warning:
                [warning(warn) for warn in str(validation_warning).splitlines()]

            field_path.pop()

        return val_error
