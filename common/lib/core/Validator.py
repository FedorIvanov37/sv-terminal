from string import digits, ascii_letters, punctuation
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.Transaction import Transaction, TypeFields


class Validator(object):
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    def validate_transaction(self, transaction: Transaction):
        self.validate_mti(transaction.message_type)
        self.validate_fields(transaction.data_fields)

    def validate_mti(self, mti):
        if mti not in self.spec.get_mti_codes():
            raise ValueError(f"Unknown MTI: {mti}")

    def validate_fields(self, fields: TypeFields, field_path: list[str] | None = None):
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

    def validate_field_number(self, field_number: int | str, is_top_level_field=True):
        if not field_number:
            raise ValueError("Lost field number")

        try:
            field_number = int(field_number)
        except ValueError:
            raise ValueError(f'Non-digit field number "{field_number}"')

        if not is_top_level_field:
            return

        if field_number not in range(1, self.spec.MessageLength.second_bitmap_capacity):
            error_text = f"Incorrect field number {field_number}. Top level " \
                         f"field number must be in range 1 - {self.spec.MessageLength.second_bitmap_capacity}"

            raise ValueError(error_text)

    def validate_field_path(self, path: list[str]):
        def path_to_str(field_path: list[str]):
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
                raise ValueError(f"{validation_error} {str_path}")

        if not self.spec.get_field_spec(path=path):
            raise ValueError(f"Lost spec for field {str_path}")

    def validate_field_data(self, field_path: list[str], value: TypeFields | str):
        alphabetic = ascii_letters
        numeric = digits
        specials = punctuation + " "
        valid_values = alphabetic + numeric + specials
        path = ".".join(field_path)
        length = len(value)
        validation_errors: set = set()

        if not (field_spec := self.spec.get_field_spec(list(field_path))):
            raise ValueError(f"Lost spec for field {path}")

        if isinstance(value, dict):
            self.validate_fields(value, field_path)
            return

        if not value:
            raise ValueError(f"Lost field value for field {path}")

        if not all(field for field in field_path if field.isdigit()):
            raise ValueError(f"Field numbers can be digits only. {path} is wrong value")

        if length > field_spec.max_length:
            validation_errors.add(f"Field {path} over MaxLength. Max length: {field_spec.max_length} got: {length}")

        if length < field_spec.min_length:
            validation_errors.add(f"Field {path} less MinLength. Min length: {field_spec.min_length} got: {length}")

        for letter in value:
            if letter not in valid_values:
                validation_errors.add(f"Incorrect letters in field {path}. Seems like a problem with encoding")

            if letter in ascii_letters and not field_spec.alpha:
                validation_errors.add(f"Alphabetic values not allowed in field {path} - {field_spec.description}")

            if letter in digits and not field_spec.numeric:
                validation_errors.add(f"Numeric values not allowed in field {path} - {field_spec.description}")

            if letter in specials and not field_spec.special:
                validation_errors.add(f"Special values not allowed in field {path} - {field_spec.description}")

        if not validation_errors:
            return

        raise ValueError("\n".join(validation_errors))
