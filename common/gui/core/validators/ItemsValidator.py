from common.lib.core.Validator import Validator
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.Config import Config
from common.gui.core.json_items.FIeldItem import FieldItem
from common.lib.data_models.Types import FieldPath


class ItemsValidator(Validator):
    spec: EpaySpecification = EpaySpecification()

    def __init__(self, config: Config):
        self.config: Config = config

    def validate_item(self, item: FieldItem):
        field_path: FieldPath = item.get_field_path()

        if not item.spec:
            raise ValueError(f"Lost spec for field {item.get_field_path(string=True)}")

        self.validate_field_path(field_path)
        self.validate_duplicates(item)

        if not self.spec.is_field_complex(field_path):
            self.validate_field_data(field_path, item.field_data)

    def validate_complex_field(self, parent: FieldItem):
        child_item: FieldItem

        for child_item in parent.get_children():
            if child_item.childCount():
                self.validate_complex_field(child_item)

            else:
                self.validate_item(child_item)

    def validate_duplicates(self, item: FieldItem, parent: FieldItem = None):
        if item is None:
            return

        if parent is None and not (parent := item.parent()):
            return

        for child in item.get_children():
            self.validate_duplicates(child)

        if [child_item.field_number for child_item in parent.get_children()].count(item.field_number) > 1:
            raise ValueError(f"Duplicated field number {item.get_field_path(string=True)}")
