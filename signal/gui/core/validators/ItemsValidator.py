from signal.lib.core.validators.Validator import Validator
from signal.lib.core.EpaySpecification import EpaySpecification
from signal.lib.data_models.Config import Config
from signal.gui.core.json_items.FIeldItem import FieldItem
from signal.lib.data_models.Validation import ValidationResult
from signal.lib.exceptions.exceptions import DataValidationError
from signal.lib.data_models.EpaySpecificationModel import IsoField, Justification


class ItemsValidator(Validator):
    spec: EpaySpecification = EpaySpecification()

    def __init__(self, config: Config):
        super(ItemsValidator, self).__init__(config)
        self.config: Config = config

    def validate_item(self, item: FieldItem):
        if not item.field_number:
            raise DataValidationError("Lost field number")

        if not (field_path := item.get_field_path()):
            raise DataValidationError(f"Cannot get field path for field {item.field_number}")

        if not item.spec:
            raise DataValidationError(f"Lost spec for field {item.get_field_path(string=True)}")

        if all([not item.field_data and not self.spec.is_field_complex(field_path)]):
            raise DataValidationError(f"Lost field value for field {item.get_field_path(string=True)}")

        self.validate_field_path(field_path)

        self.validate_duplicates(item)

        if self.spec.is_field_complex(field_path):
            return

        validation_result: ValidationResult = self.validate_field_data(field_path, item.field_data, ValidationResult())

        self.process_validation_result(validation_result)

    def validate_complex_field(self, parent: FieldItem):
        child_item: FieldItem

        for child_item in parent.get_children():
            if not child_item.childCount():
                self.validate_item(child_item)
                continue

            self.validate_complex_field(child_item)

    def validate_duplicates(self, item: FieldItem, parent: FieldItem = None):
        if item is None:
            return

        if not item.field_number:
            return

        if parent is None and not (parent := item.parent()):
            return

        for child in item.get_children():
            self.validate_duplicates(child)

        field_numbers = [child_item.field_number for child_item in parent.get_children()]

        if field_numbers.count(item.field_number) > 1:
            raise DataValidationError(f"Duplicated field number {item.get_field_path(string=True)}")

    def modify_all_fields_data(self, parent: FieldItem):
        for child_item in parent.get_children():
            if child_item.childCount():
                self.modify_all_fields_data(parent=child_item)
                continue

            self.modify_field_data(child_item)

    def modify_field_data(self, item: FieldItem) -> None:
        if not self.config.validation.validation_enabled:
            return

        if not (validations := self.spec.get_field_validations(item.get_field_path())):
            return

        if validations.justification:
            item.field_data = self.get_justified_field_data(item.spec, item.field_data)

        if validations.field_type_validators.change_to_lower and validations.field_type_validators.change_to_upper:
            item.field_data = item.field_data.upper()
            return

        if validations.field_type_validators.change_to_lower:
            item.field_data = item.field_data.lower()

        if validations.field_type_validators.change_to_upper:
            item.field_data = item.field_data.upper()

    @staticmethod
    def get_justified_field_data(field_spec: IsoField, value: str) -> str:
        if not field_spec:
            return value

        if field_spec.validators.justification is None:
            return value

        if not (just_letter := field_spec.validators.justification_element):
            return value

        if not (just_length := field_spec.validators.justification_length):
            return value

        if field_spec.validators.justification == Justification.RIGHT:
            return value.ljust(just_length, just_letter)

        if field_spec.validators.justification == Justification.LEFT:
            return value.rjust(just_length, just_letter)

        return value
