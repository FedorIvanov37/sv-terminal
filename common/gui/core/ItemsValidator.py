from common.lib.core.Validator import Validator
from common.gui.core.FIeldItem import Item
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.Config import Config


class ItemsValidator(Validator):
    spec: EpaySpecification = EpaySpecification()

    def __init__(self, config: Config):
        self.config: Config = config

    def validate_item(self, item: Item):
        if not any((item.field_number, item.field_data)):
            return

        field_path: list[str] = item.get_field_path()

        self.validate_field_path(field_path)
        self.validate_duplicates(item)

        if self.spec.is_field_complex(field_path) and not item.field_data:
            return

        self.validate_field_data(field_path, item.field_data)

    def validate_duplicates(self, item: Item, parent: Item = None):
        if parent is None:
            if not (parent := item.parent()):
                return

        for child in item.get_children():
            self.validate_duplicates(child)

        if [child_item.field_number for child_item in parent.get_children()].count(item.field_number) > 1:
            raise ValueError(f"Duplicated field number {item.get_field_path(string=True)}")
