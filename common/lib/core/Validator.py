from datetime import datetime
from string import digits, ascii_letters, punctuation
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.Transaction import Transaction, TypeFields
from common.lib.data_models.Types import FieldPath
from common.lib.constants import ValidationParams
from common.gui.constants import FieldTypeParams
from common.lib.data_models.Countries import Countries
from common.lib.data_models.Currencies import Currencies


class Validator(object):
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    def __init__(self, countries_dictionary: Countries | None, currencies_dictionary: Currencies | None):
        self.countries_dictionary = countries_dictionary
        self.currencies_dictionary = currencies_dictionary

    def validate_transaction(self, transaction: Transaction):
        self.validate_mti(transaction.message_type)
        self.validate_fields(transaction.data_fields)

    def validate_mti(self, mti):
        if mti not in self.spec.get_mti_codes():
            raise ValueError(f"Unknown MTI: {mti}")

    def validate_fields(self, fields: TypeFields, field_path: FieldPath | None = None):
        if field_path is None:
            field_path = []

        for field, value in fields.items():
            field_path.append(field)

            if isinstance(value, dict):
                self.validate_fields(fields=value, field_path=field_path)
                field_path.pop()
                continue

            self.validate_field_data(field_path, value)

            field_path.pop()

        return fields

    @staticmethod
    def check_luhn(value: str) -> bool:  # Taken from https://en.wikipedia.org/wiki/Luhn_algorithm
        def digits_of(val):
            return [int(dig) for dig in str(val)]

        digits = digits_of(value)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)

        for digit in even_digits:
            checksum += sum(digits_of(digit * 2))

        return checksum % 10 == int()

    def validate_field_number(self, field_number: int | str, is_top_level_field=True):
        if not field_number:
            raise ValueError("Lost field number")

        try:
            field_number = int(field_number)
        except ValueError:
            raise ValueError(f'Non-digit field number "{field_number}"')

        if not is_top_level_field:
            return

        if field_number not in range(1, self.spec.MessageLength.SECOND_BITMAP_CAPACITY):
            error_text = f"Incorrect field number {field_number}. Top level field number must be in range 1 " \
                         f"- {self.spec.MessageLength.SECOND_BITMAP_CAPACITY}"

            raise ValueError(error_text)

    def validate_field_path(self, path: FieldPath):
        def path_to_str(field_path: FieldPath):
            return ".".join(field_path)

        if not path:
            raise ValueError("Lost field path")

        if str() in path:
            path: map = map(lambda field_data: field_data if field_data else '<empty>', path)
            path: str = path_to_str(list(path))
            raise ValueError(f"Empty field number in field path: {path}")

        str_path = path_to_str(path)

        for level, field in enumerate(path, start=1):
            try:
                self.validate_field_number(field, is_top_level_field=level == 1)

            except ValueError as validation_error:
                raise ValueError(f"{validation_error}. Path: {str_path}")

        if not self.spec.get_field_spec(path=path):
            raise ValueError(f"Lost spec for field {str_path}")

    def validate_field_data(self, field_path: FieldPath, field_value: TypeFields | str):
        def pre_validations():
            if not field_value:  # Field should contain the data
                raise ValueError(f"Lost field value for field {path}")

            if not all(field for field in field_path if field.isdigit()):  # Field number should be digit
                raise ValueError(f"Field numbers can be digits only. {path} is wrong value")

            if length > field_spec.max_length:  # Max length validation
                validation_errors.add(f"Field {path} over MaxLength. Max length: {field_spec.max_length} got: {length}")

            if length < field_spec.min_length:  # Min length validation
                validation_errors.add(f"Field {path} less MinLength. Min length: {field_spec.min_length} got: {length}")

        def main_validations():
            for letter in field_value:
                if letter not in valid_values:  # Only ascii-printable allowed
                    validation_errors.add(f"Non-printable letters in field {path}. Seems like a problem with encoding")

                if letter in ascii_letters and not field_spec.alpha:  # Validation charset - alphabetic
                    validation_errors.add(f"Alphabetic values not allowed in field {path_desc}")

                if letter in digits and not field_spec.numeric:  # Validation charset - numeric
                    validation_errors.add(f"Numeric values not allowed in field {path_desc}")

                if letter in specials and not field_spec.special:  # Validation charset - special
                    validation_errors.add(f"Special values not allowed in field {path_desc}")

        def custom_validations():
            for validation, patterns in field_spec.validators.model_dump().items():  # Custom validations
                if not isinstance(patterns, list):
                    continue

                if not patterns:
                    continue

                match validation:
                    case ValidationParams.VALID_VALUES:  # Exact allowed value validation
                        if not field_value in patterns:
                            bad_patterns = ", ".join(patterns)
                            validation_errors.add(f'Field {path_desc} must contain one of the following: {bad_patterns}')

                    case ValidationParams.INVALID_VALUES:  # Exact not allowed value validation
                        if field_value in patterns:
                            bad_patterns = ", ".join(patterns)
                            validation_errors.add(f'Field {path_desc} must not contain one of the following: {bad_patterns}')

                for pattern in patterns:
                    match validation:
                        case ValidationParams.MUST_CONTAIN:
                            if pattern not in field_value:
                                validation_errors.add(f'Field {path_desc} must contain "{pattern}"')

                        case ValidationParams.MUST_CONTAIN_ONLY:
                            bad_patterns = ", ".join(patterns)

                            if [letter for letter in field_value if letter not in patterns]:
                                validation_errors.add(f"Field {path_desc} must contain only one or multiple: {bad_patterns}")

                        case ValidationParams.MUST_NOT_CONTAIN:
                            if pattern in field_value:
                                validation_errors.add(f'Field {path_desc} must not contain {pattern}')

                        case ValidationParams.MUST_NOT_CONTAIN_ONLY:
                            if not [letter for letter in field_value if letter not in pattern]:
                                validation_errors.add(f"Field {path_desc} must not contain only one or multiple {pattern}")

                        case ValidationParams.MUST_START_WITH:
                            if not field_value.startswith(pattern):
                                validation_errors.add(f"Field {path_desc} must start with {pattern}")

                        case ValidationParams.MUST_NOT_START_WITH:
                            if field_value.startswith(pattern):
                                validation_errors.add(f"Field {path_desc} must not start with {pattern}")

                        case ValidationParams.MUST_END_WITH:
                            if not field_value.endswith(pattern):
                                validation_errors.add(f"Field {path_desc} must end with {pattern}")

                        case ValidationParams.MUST_NOT_END_WITH:
                            if field_value.endswith(pattern):
                                validation_errors.add(f"Field {path_desc} must not end with {pattern}")

        def country_validations():
            if self.countries_dictionary is None:
                return

            for field, value in field_spec.validators.field_type_validators.model_dump().items():
                if not value:
                    continue

                if field == "country_a3":
                    if field_value not in self.countries_dictionary.countries_a3:
                        validation_errors.add(f"Field {path_desc} must contain valid {FieldTypeParams.COUNTRY_CODE_A3}")

                if field == "country_n3":
                    if field_value not in self.countries_dictionary.countries_n3:
                        validation_errors.add(f"Field {path_desc} must contain valid {FieldTypeParams.COUNTRY_CODE_N3}")

                if field == "country_a2":
                    if field_value not in self.countries_dictionary.countries_a2:
                        validation_errors.add(f"Field {path_desc} must contain valid {FieldTypeParams.COUNTRY_CODE_A2}")

        def currency_validation():
            if self.currencies_dictionary is None:
                return

            for field, value in field_spec.validators.field_type_validators.model_dump().items():
                if not value:
                    continue

                if field == "currency_a3":
                    if field_value not in self.currencies_dictionary.currencies_a3:
                        validation_errors.add(f"Field {path_desc} must contain valid {FieldTypeParams.CURRENCY_CODE_A3}")

                if field == "currency_n3":
                    if value and field_value not in self.currencies_dictionary.currencies_n3:
                        validation_errors.add(f"Field {path_desc} must contain valid {FieldTypeParams.CURRENCY_CODE_N3}")

        def extended_validations():
            for field, value in field_spec.validators.field_type_validators.model_dump().items():
                if not value:
                    continue

                if field == "mcc":
                    if field_value not in ["6533", "8999"]:
                        validation_errors.add(f"Field {path_desc} must contain valid {FieldTypeParams.MCC_ISO}")

                if field == "date":
                    date = None

                    try:
                        date = datetime.strptime(field_value, field_spec.validators.field_type_validators.date_format)
                    except ValueError:
                        validation_errors.add(f"Field {path_desc} must contain date in {field_spec.validators.field_type_validators.date_format}")

                    if date is not None:
                        if date < datetime.now() and not field_spec.validators.field_type_validators.past:
                            validation_errors.add(f"Field {path_desc} past time not allowed")

                        if date > datetime.now() and not field_spec.validators.field_type_validators.future:
                            validation_errors.add(f"Field {path_desc} future time not allowed")

                if field == "check_luhn":
                    if not self.check_luhn(field_value):
                        validation_errors.add(f"Field {path_desc} does not pass check by Luhn algorithm")

                if field == "only_upper":
                    for letter in field_value:
                        if value and not letter.isupper():
                            validation_errors.add(f"Field {path_desc} allowed UPPER case only")
                            break

                if field == "only_lower":
                    for letter in field_value:
                        if value and not letter.isupper():
                            validation_errors.add(f"Field {path_desc} allowed lower case only")
                            break

        alphabetic = ascii_letters
        numeric = digits
        specials = punctuation + " "
        valid_values = alphabetic + numeric + specials
        path = ".".join(field_path)
        length = len(field_value)
        validation_errors: set = set()

        if not (field_spec := self.spec.get_field_spec(list(field_path))):
            raise ValueError(f"Lost spec for field {path}")

        if field_spec.validators.field_type_validators.do_not_validate:
            return

        path_desc = f"{path} - {field_spec.description}"

        if isinstance(field_value, dict):
            self.validate_fields(field_value, field_path)
            return

        validators = pre_validations, main_validations, custom_validations, extended_validations, country_validations, currency_validation

        for validator in validators:
            try:
                validator()
            except Exception as validation_exception:
                validation_errors.add(f"Validation error: {validation_exception}")

        if validation_errors:
            raise ValueError("\n".join(validation_errors))
