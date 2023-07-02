from common.lib.core.Validator import Validator
from common.gui.core.FIeldItem import Item


class ItemsValidator(Validator):
    def validate_single_item(self, item: Item):
        if item.generate_checkbox_checked():
            return

        if not item.field_number:
            raise ValueError(f"Lost field number")

        if not item.field_number.isdigit():
            raise ValueError(f"Non-numeric field number found: {item.get_field_path(string=True)}")

        if not all((item.get_field_path(), item.field_data)):
            return

        self.validate_field_data(item.get_field_path(), item.field_data)

    def validate_item(self, parent_item: Item):
        if parent_item.childCount():
            for child in parent_item.get_children():
                self.validate_item(parent_item=child)
        else:
            self.validate_single_item(parent_item)
