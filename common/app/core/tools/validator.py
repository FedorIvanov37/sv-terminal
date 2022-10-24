from common.app.core.tools.epay_specification import EpaySpecification
from string import digits, ascii_letters, punctuation
from common.app.data_models.config import Config
from common.app.decorators.singleton import singleton


TypeFields = dict[str, str | dict]
specials = punctuation + " "

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

    def validate_message(self, message):
        if not message:
            raise ValueError("Validation error: empty transaction message")

        self.validate_mti(message.transaction.message_type)
        self.validate_fields(message.transaction.fields)

    def validate_mti(self, mti):
        if mti not in self.spec.get_mti_codes():
            raise ValueError(f"unknown MTI: {mti}")

    def validate_fields(self, fields: TypeFields, field_path: list[str] | None = None):
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

            self.validate_field(field_path, value)

            field_path.pop()

        return fields

    def validate_field(self, field_path: list[str], value: TypeFields | str):
        if not self._config.fields.validation:
            return

        if not value or not field_path:
            return

        for field in field_path:
            if field.isdigit():
                continue

            raise ValueError(f"Field numbers can be digits only. {field} is wrong value")

        if isinstance(value, dict):
            self.validate_fields(value, field_path)
            return

        path = ".".join(field_path)

        if not (field_spec := self.spec.get_field_spec(list(field_path))):
            raise ValueError(f"Lost spec for field {path}")

        for letter in value:
            if letter not in ascii_letters + digits + specials:
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
