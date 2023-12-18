from logging import warning
from common.lib.core.Validator import Validator
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.Config import Config
from common.gui.core.json_items.FIeldItem import FieldItem
from common.lib.data_models.Types import FieldPath
from common.lib.constants import TermFilesPath
from common.lib.data_models.Currencies import Currencies
from common.lib.data_models.Countries import Countries


class ItemsValidator(Validator):
    spec: EpaySpecification = EpaySpecification()

    try:
        with open(TermFilesPath.CURRENCY_DICT) as json_file:
            currencies_dictionary = Currencies.model_validate_json(json_file.read())

        with open(TermFilesPath.COUNTRY_DICT) as json_file:
            countries_dictionary = Countries.model_validate_json(json_file.read())

    except Exception as dictionary_parsing_error:
        warning(f"Cannot load dictionary: {dictionary_parsing_error}")

    def __init__(self, config: Config):
        super(ItemsValidator, self).__init__(self.countries_dictionary, self.currencies_dictionary)

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
