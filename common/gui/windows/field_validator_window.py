from copy import deepcopy
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QDialog, QListWidgetItem, QCheckBox, QLineEdit, QComboBox, QWidget
from common.gui.core.CheckableComboBox import CheckableComboBox
from common.gui.forms.field_validator_window import Ui_FieldDataSet
from common.gui.decorators.window_settings import set_window_icon, has_close_button_only
from common.gui.constants import FieldTypeParams, Colors
from common.lib.data_models.EpaySpecificationModel import IsoField, Justification, LogicalValidators
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.constants import ValidationParams


class FieldDataSet(Ui_FieldDataSet, QDialog):
    spec: EpaySpecification = EpaySpecification()
    _field_spec: IsoField = None
    _literal_validations_map: dict
    _field_spec_accepted: pyqtSignal = pyqtSignal(IsoField)
    _field_type_checkboxes: dict[str, dict[str, QLineEdit | QCheckBox]] = {}

    @property
    def field_spec_accepted(self):
        return self._field_spec_accepted

    @property
    def field_spec(self):
        return self._field_spec

    def __init__(self, field_spec: IsoField):
        super(FieldDataSet, self).__init__()
        self._field_spec = deepcopy(field_spec)
        self.CheckTypeBox = CheckableComboBox()
        self.setupUi(self)
        self.setup()

    @set_window_icon
    @has_close_button_only
    def setup(self):
        self._literal_validations_map = {
            ValidationParams.MUST_CONTAIN: self.field_spec.validators.must_contain,
            ValidationParams.MUST_CONTAIN_ONLY: self.field_spec.validators.must_contain_only,
            ValidationParams.MUST_NOT_CONTAIN: self.field_spec.validators.must_not_contain,
            ValidationParams.MUST_NOT_CONTAIN_ONLY: self.field_spec.validators.must_not_contain_only,
            ValidationParams.MUST_START_WITH: self.field_spec.validators.must_start_with,
            ValidationParams.MUST_NOT_START_WITH: self.field_spec.validators.must_not_start_with,
            ValidationParams.MUST_END_WITH: self.field_spec.validators.must_end_with,
            ValidationParams.MUST_NOT_END_WITH: self.field_spec.validators.must_not_end_with,
            ValidationParams.VALID_VALUES: self.field_spec.validators.valid_values,
            ValidationParams.INVALID_VALUES: self.field_spec.validators.invalid_values,
        }

        palette = QPalette()
        palette.setColor(palette.ColorRole.AlternateBase, QColor(*Colors.ALTERNATE_CELLS))
        self.ValuesList.setPalette(palette)
        self.CheckTypeLayout.addWidget(self.CheckTypeBox)
        self.parse_field_spec(self.field_spec)
        self.create_field_type_checkboxes()
        self.process_changes()
        self.process_field_type_change()
        self.process_check_type_change()
        self.connect_all()

    def connect_all(self):
        connection_map = {
            self.FillSide.currentIndexChanged: self.process_changes,
            self.FieldType.currentIndexChanged: self.process_field_type_change,
            self.CheckTypeBox.currentIndexChanged: self.process_check_type_change,
            self.ValuesList.itemChanged: self.mark_all_check_types,
            self.CancelButton.clicked: self.reject,
            self.PlusButton.clicked: self.plus,
            self.MinusButton.clicked: self.minus,
            self.ButtonClear.clicked: self.clear_validation,
            self.ButtonClearAll.clicked: self.clear_all_validations,
            self.OkButton.clicked: self.ok,
        }

        for signal, slot in connection_map.items():
            signal.connect(slot)

    def ok(self):
        self.prepare_field_spec(self.field_spec)
        self.field_spec_accepted.emit(self.field_spec)
        self.accept()

    def clear_all_validations(self):
        self.clear_validation()

        for check_type in self._literal_validations_map:
            self._literal_validations_map[check_type] = list()

        self.mark_all_check_types()

    def clear_validation(self):
        for index in range(self.ValuesList.count()):
            self.ValuesList.takeItem(int())

        self.CheckTypeBox.set_validation_mark(mark=False, item=self.CheckTypeBox.currentIndex())

    def create_field_type_checkboxes(self):
        self._field_type_checkboxes = {
            FieldTypeParams.COUNTRY: {
                FieldTypeParams.COUNTRY_CODE_N3: QCheckBox(FieldTypeParams.COUNTRY_CODE_N3),
                FieldTypeParams.COUNTRY_CODE_A3: QCheckBox(FieldTypeParams.COUNTRY_CODE_A3),
                FieldTypeParams.COUNTRY_CODE_A2: QCheckBox(FieldTypeParams.COUNTRY_CODE_A2),
            },

            FieldTypeParams.CURRENCY: {
                FieldTypeParams.CURRENCY_CODE_A3: QCheckBox(FieldTypeParams.CURRENCY_CODE_A3),
                FieldTypeParams.CURRENCY_CODE_N3: QCheckBox(FieldTypeParams.CURRENCY_CODE_N3),
            },

            FieldTypeParams.MERCHANT_CATEGORY_CODE: {
                FieldTypeParams.MCC_ISO: QCheckBox(FieldTypeParams.MCC_ISO),
            },

            FieldTypeParams.DATE: {
                FieldTypeParams.DATE_FORMAT: QLineEdit(),
                FieldTypeParams.PAST_TIME: QCheckBox(FieldTypeParams.PAST_TIME),
                FieldTypeParams.FUTURE_TIME: QCheckBox(FieldTypeParams.FUTURE_TIME),
            },

            FieldTypeParams.OTHER: {
                FieldTypeParams.CHECK_LUHN: QCheckBox(FieldTypeParams.CHECK_LUHN),
                FieldTypeParams.UPPERCASE: QCheckBox(FieldTypeParams.UPPERCASE),
                FieldTypeParams.LOWERCASE: QCheckBox(FieldTypeParams.LOWERCASE),
                FieldTypeParams.TO_UPPERCASE: QCheckBox(FieldTypeParams.TO_UPPERCASE),
                FieldTypeParams.TO_LOWERCASE: QCheckBox(FieldTypeParams.TO_LOWERCASE),
                FieldTypeParams.IGNORE_VALIDATIONS: QCheckBox(FieldTypeParams.IGNORE_VALIDATIONS),
            }
        }

        try:
            field_date: dict = self._field_type_checkboxes[FieldTypeParams.DATE]
            line_date: QLineEdit = field_date[FieldTypeParams.DATE_FORMAT]
            line_date.setPlaceholderText(FieldTypeParams.DATE_FORMAT)
        except KeyError:
            pass

        for field_type, widgets in self._field_type_checkboxes.items():
            self.FieldType.addItem(field_type)

            for widget in widgets.values():
                self.FieldTypeLayout.addWidget(widget)

        self.hide_field_type_widgets()

    def process_field_type_change(self):
        self.hide_field_type_widgets()

        if not (field_type := self.FieldType.currentText()):
            return

        if not (widgets := self._field_type_checkboxes.get(field_type)):
            return

        for widget in widgets.values():
            widget.show()

    def hide_field_type_widgets(self):
        for widgets in self._field_type_checkboxes.values():
            for widget in widgets.values():
                widget.hide()

    def prepare_field_spec(self, field_spec: IsoField | None = None) -> IsoField:
        if field_spec is None:
            field_spec = self.field_spec

        self.save_validations()

        field_spec.min_length = self.MinLength.value()
        field_spec.max_length = self.MaxLength.value()
        field_spec.tag_length = self.TagLength.value()
        field_spec.var_length = self.DataLength.value()

        field_spec.alpha = self.CheckBoxAlpha.isChecked()
        field_spec.numeric = self.CheckBoxNumeric.isChecked()
        field_spec.special = self.CheckBoxSpecial.isChecked()
        field_spec.matching = self.CheckBoxMatching.isChecked()
        field_spec.reversal = self.CheckBoxReversal.isChecked()
        field_spec.generate = self.CheckBoxGeneratible.isChecked()
        field_spec.is_secret = self.CheckBoxSecret.isChecked()

        if self.FillSide.currentText() == "Left Pad":
            field_spec.validators.justification = Justification.LEFT

        if self.FillSide.currentText() == "Right Pad":
            field_spec.validators.justification = Justification.RIGHT

        if self.FillUpTo.currentText() == "Min Length":
            field_spec.validators.justification_length = field_spec.min_length

        if self.FillUpTo.currentText() == "Max Length":
            field_spec.validators.justification_length = field_spec.max_length

        if self.FillUpTo.currentText().isdigit():
            field_spec.validators.justification_length = int(self.FillUpTo.currentText())

        if self.FillSymbol.text():
            field_spec.validators.justification_element = self.FillSymbol.text()

        logical_validators = LogicalValidators()

        if currency := self._field_type_checkboxes.get(FieldTypeParams.CURRENCY):
            logical_validators.currency_n3 = currency.get(FieldTypeParams.CURRENCY_CODE_N3).isChecked()
            logical_validators.currency_a3 = currency.get(FieldTypeParams.CURRENCY_CODE_A3).isChecked()

        if country := self._field_type_checkboxes.get(FieldTypeParams.COUNTRY):
            logical_validators.country_a2 = country.get(FieldTypeParams.COUNTRY_CODE_A2).isChecked()
            logical_validators.country_a3 = country.get(FieldTypeParams.COUNTRY_CODE_A3).isChecked()
            logical_validators.country_n3 = country.get(FieldTypeParams.COUNTRY_CODE_N3).isChecked()

        if merch_cat := self._field_type_checkboxes.get(FieldTypeParams.MCC):
            logical_validators.mcc = merch_cat.get(FieldTypeParams.MCC_ISO).isChecked()

        if date := self._field_type_checkboxes.get(FieldTypeParams.DATE):
            logical_validators.date_format = date.get(FieldTypeParams.DATE_FORMAT).text()
            logical_validators.future = date.get(FieldTypeParams.FUTURE_TIME).isChecked()
            logical_validators.past = date.get(FieldTypeParams.PAST_TIME).isChecked()

        if other := self._field_type_checkboxes.get(FieldTypeParams.OTHER):
            logical_validators.check_luhn = other.get(FieldTypeParams.CHECK_LUHN).isChecked()
            logical_validators.only_upper = other.get(FieldTypeParams.UPPERCASE).isChecked()
            logical_validators.only_lower = other.get(FieldTypeParams.LOWERCASE).isChecked()
            logical_validators.change_to_upper = other.get(FieldTypeParams.TO_UPPERCASE).isChecked()
            logical_validators.change_to_lower = other.get(FieldTypeParams.TO_LOWERCASE).isChecked()
            logical_validators.do_not_validate = other.get(FieldTypeParams.IGNORE_VALIDATIONS).isChecked()

        field_spec.validators.field_type_validators = logical_validators

        return field_spec

    def set_justification_simbols(self):
        self.field_spec.validators.justification_element = self.FillSymbol.text()

    def mark_all_check_types(self):
        self.save_validations()

        for item_index in range(self.CheckTypeBox.count()):
            if not self._literal_validations_map.get(self.CheckTypeBox.itemText(item_index)):
                self.CheckTypeBox.set_validation_mark(mark=False, item=item_index)
                continue

            self.CheckTypeBox.set_validation_mark(mark=True, item=item_index)

    def process_check_type_change(self):
        if previous_check_type := self.CheckTypeBox.get_previous_text():
            self.save_validations(previous_check_type)

        current_check_type: str = self.CheckTypeBox.currentText()

        self.set_validation_items(current_check_type)
        self.mark_all_check_types()
        self.ValuesList.setFocus()

    def save_validations(self, check_type: str | None = None):
        if check_type is None:
            check_type = self.CheckTypeBox.currentText()

        check_list = list[str]
        validations_map: dict[str, check_list] = self._literal_validations_map

        literal_list: check_list = [self.ValuesList.item(row).text() for row in range(self.ValuesList.count())]
        literal_list: check_list = list(set(literal_list))

        try:
            literal_list.remove(str())
        except ValueError:
            pass  # When no empty strings in literal_list

        validations_map[check_type] = literal_list

        self.field_spec.validators.must_contain = validations_map.get(ValidationParams.MUST_CONTAIN)
        self.field_spec.validators.must_contain_only = validations_map.get(ValidationParams.MUST_CONTAIN_ONLY)
        self.field_spec.validators.must_not_contain = validations_map.get(ValidationParams.MUST_NOT_CONTAIN)
        self.field_spec.validators.must_not_contain_only = validations_map.get(ValidationParams.MUST_NOT_CONTAIN_ONLY)
        self.field_spec.validators.must_start_with = validations_map.get(ValidationParams.MUST_START_WITH)
        self.field_spec.validators.must_not_start_with = validations_map.get(ValidationParams.MUST_NOT_START_WITH)
        self.field_spec.validators.must_end_with = validations_map.get(ValidationParams.MUST_END_WITH)
        self.field_spec.validators.must_not_end_with = validations_map.get(ValidationParams.MUST_NOT_END_WITH)
        self.field_spec.validators.valid_values = validations_map.get(ValidationParams.VALID_VALUES)
        self.field_spec.validators.invalid_values = validations_map.get(ValidationParams.INVALID_VALUES)

    def set_validation_items(self, check_type):
        if (validation_list := self._literal_validations_map.get(check_type)) is None:
            return

        self.clear_validation()

        if not validation_list:
            return

        for literal in validation_list:
            self.add_validation_value(literal)

    def minus(self):
        self.ValuesList.setFocus()

        if not (item := self.ValuesList.currentItem()):
            return

        self.ValuesList.takeItem(self.ValuesList.row(item))
        self.save_validations()
        self.mark_all_check_types()

    def plus(self):
        item: QListWidgetItem = self.add_validation_value()
        self.ValuesList.editItem(item)

    def set_validator_mark(self):
        values_count = len([row for row in range(self.ValuesList.count()) if self.ValuesList.item(row).text() != str()])
        validation_mark: bool = bool(values_count)
        self.CheckTypeBox.set_validation_mark(mark=validation_mark)

    def add_validation_value(self, value_data: str | None = None) -> QListWidgetItem:
        value_data: str = str() if value_data is None else value_data
        item: QListWidgetItem = QListWidgetItem(value_data)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable)
        self.ValuesList.addItem(item)
        return item

    def parse_field_spec(self, iso_field: IsoField):
        field_desc: str = self.spec.get_field_description(iso_field.field_path, string=True)
        field_path: str = ".".join(iso_field.field_path)

        self.FillSide.setCurrentText(iso_field.validators.justification)

        if not iso_field.validators.justification:
            self.FillSide.setCurrentText("Not set")

        self.FieldDescription.setText(f"Field {field_path}  - {field_desc}")

        checkbox_property_map = {
            self.CheckBoxAlpha: iso_field.alpha,
            self.CheckBoxNumeric: iso_field.numeric,
            self.CheckBoxSpecial: iso_field.special,
            self.CheckBoxMatching: iso_field.matching,
            self.CheckBoxReversal: iso_field.reversal,
            self.CheckBoxGeneratible: iso_field.generate,
            self.CheckBoxSecret: iso_field.is_secret,
        }

        length_property_map = {
            self.MinLength: iso_field.min_length,
            self.MaxLength: iso_field.max_length,
            self.DataLength: iso_field.var_length,
            self.TagLength: iso_field.tag_length,
        }

        for length, field_property in length_property_map.items():
            length.setValue(field_property)

        for checkbox, field_property in checkbox_property_map.items():
            checkbox.setChecked(field_property)

        for check_type, values in self._literal_validations_map.items():
            self.CheckTypeBox.addItem(check_type)

        if self.field_spec.field_number == self.spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
            self.CheckBoxSecret.setChecked(True)
            self.CheckBoxSecret.setDisabled(True)

        self.set_validation_items(self.CheckTypeBox.currentText())

        if iso_field.validators.justification is None:
            self.FillSide.setCurrentText("Not set")
            return

        if iso_field.validators.justification == Justification.RIGHT:
            self.FillSide.setCurrentText("Right Pad")

        if iso_field.validators.justification == Justification.LEFT:
            self.FillSide.setCurrentText("Left Pad")

        self.FillUpTo.setCurrentText(str(iso_field.validators.justification_length))
        self.FillSymbol.setText(iso_field.validators.justification_element)

        if iso_field.validators.justification_length == iso_field.max_length:
            self.FillUpTo.setCurrentText("Max Length")
            return

        if iso_field.validators.justification_length == iso_field.min_length:
            self.FillUpTo.setCurrentText("Min Length")

    def process_changes(self):
        justification_enabled = self.FillSide.currentText().lower() != "not set".lower()
        
        for element in self.FillUpTo, self.FillSymbolLabel, self.FillUpToLabel, self.FillSymbol:
            element.setEnabled(justification_enabled)
