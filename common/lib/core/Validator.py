from string import digits, ascii_letters, punctuation
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.Config import Config
from common.lib.decorators.singleton import singleton
from common.lib.data_models.Transaction import Transaction, TypeFields


@singleton
class Validator(object):
    _spec: EpaySpecification = EpaySpecification()
    _config: Config = None

    @property
    def spec(self):
        return self._spec

    def __init__(self, config: Config = None):
        if config is not None:
            self._config = config

    def validate_transaction(self, transaction: Transaction):
        self.validate_mti(transaction.message_type)
        self.validate_fields(transaction.data_fields)

    def validate_mti(self, mti):
        if mti not in self.spec.get_mti_codes():
            raise ValueError(f"Unknown MTI: {mti}")

    def validate_fields(self, fields: TypeFields, field_path: list[str] | None = None):
        if self._config is None:
            return

        if not self._config.fields.validation:
            return fields

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

    def validate_field_item(self, item):
        if not item.field_number:
            raise ValueError(f"Lost field number. The field will not be sent")

        if not item.field_number.isdigit():
            raise ValueError(f"Non-numeric field number found: {item.get_field_path(string=True)}")

        # if item.is_duplicated():
        #     raise ValueError(f"Duplicated field number {item.get_field_path(string=True)} found")

        if not (item.field_data or item.generate_checkbox_checked() or item.get_children()):
            raise ValueError(f"No value for field {item.get_field_path(string=True)}. The field cannot be sent")

        self.validate_field_data(item.get_field_path(), item.field_data)

    def validate_field_data(self, field_path: list[str], value: TypeFields | str):
        alphabetic = ascii_letters
        numeric = digits
        specials = punctuation + " "
        valid_values = alphabetic + numeric + specials
        path = ".".join(field_path)

        if self._config is None:
            return

        if not self._config.fields.validation:
            return

        if not value or not field_path:
            return

        for field in field_path:
            if not field.isdigit():
                raise ValueError(f"Field numbers can be digits only. {field} is wrong value")

        if not (field_spec := self.spec.get_field_spec(list(field_path))):
            raise ValueError(f"Lost spec for field {path}")

        if isinstance(value, dict):
            self.validate_fields(value, field_path)
            return

        for letter in value:
            if letter not in valid_values:
                raise ValueError(f"Incorrect letters in field {path}. Seems like problem with encoding")

            if letter in ascii_letters and not field_spec.alpha:
                raise ValueError(f"Alphabetic values not allowed in field {path} - {field_spec.description}")

            if letter in digits and not field_spec.numeric:
                raise ValueError(f"Numeric values not allowed in field {path} - {field_spec.description}")

            if letter in specials and not field_spec.special:
                raise ValueError(f"Special values not allowed in field {path} - {field_spec.description}")

        length = len(value)

        if length > field_spec.max_length:
            raise ValueError(f"Field {path} over MaxLength. Max length: {field_spec.max_length} got: {length}")

        if length < field_spec.min_length:
            raise ValueError(f"Field {path} less MinLength. Min length: {field_spec.min_length} got: {length}")
