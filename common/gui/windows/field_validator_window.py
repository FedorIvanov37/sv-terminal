from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QDialog, QListWidgetItem, QCheckBox, QLineEdit, QComboBox, QWidget
from common.gui.core.CheckableComboBox import CheckableComboBox
from common.gui.forms.field_validator_window import Ui_FieldDataSet
from common.gui.decorators.window_settings import set_window_icon, has_close_button_only
from common.gui.constants import FieldTypeParams
from common.lib.data_models.EpaySpecificationModel import IsoField, Justification
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.constants import ValidationParams


class FieldDataSet(Ui_FieldDataSet, QDialog):
    spec: EpaySpecification = EpaySpecification()
    _field_spec: IsoField = None
    _literal_validations_map: dict
    _field_spec_accepted: pyqtSignal = pyqtSignal()

    @property
    def field_spec_accepted(self):
        return self._field_spec_accepted

    @property
    def field_spec(self):
        return self._field_spec

    def __init__(self, field_spec: IsoField):
        super().__init__()
        self._field_spec = field_spec
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
        palette.setColor(palette.ColorRole.AlternateBase, QColor(224, 233, 246))
        self.ValuesList.setPalette(palette)
        self.CheckTypeLayout.addWidget(self.CheckTypeBox)
        self.parse_field_spec(self.field_spec)
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
            self.CancelButton.clicked: self.ok,
            self.PlusButton.clicked: self.plus,
            self.MinusButton.clicked: self.minus,
            self.OkButton.clicked: self.ok,
        }

        for signal, slot in connection_map.items():
            signal.connect(slot)

    def ok(self):
        self.prepare_field_spec(self.field_spec)
        self.field_spec_accepted.emit()
        self.accept()

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

        if self.FillSide.currentText() == "Not set" or self.FillSymbol.text() is str():
            field_spec.validators.justification = None
            return field_spec

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

        self.clear_validation_list()

        if not validation_list:
            return

        for literal in validation_list:
            self.add_validation_value(literal)

    def clear_validation_list(self):
        for row in range(self.ValuesList.count()):
            self.ValuesList.takeItem(int())

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
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsUserCheckable)
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

    def process_field_type_change(self):
        for row in range(self.FieldTypeLayout.count()):
            if not (element := self.FieldTypeLayout.itemAt(row).widget()):
                continue

            element.hide()

        widgets_list = list[QWidget]
        widgets: widgets_list = list()

        match self.FieldType.currentText():
            case FieldTypeParams.CURRENCY:
                widgets: widgets_list = [
                    QCheckBox(code) for code in (
                        FieldTypeParams.CURRENCY_CODE_A3,
                        FieldTypeParams.COUNTRY_CODE_N3,
                    )
                ]

            case FieldTypeParams.COUNTRY:
                widgets: widgets_list = [
                    QCheckBox(code) for code in (
                        FieldTypeParams.COUNTRY_CODE_A3,
                        FieldTypeParams.COUNTRY_CODE_A2,
                        FieldTypeParams.COUNTRY_CODE_N3,
                    )
                ]

            case FieldTypeParams.OTHER:
                widgets: widgets_list = [
                    QCheckBox(validation) for validation in (
                        FieldTypeParams.CHECK_LUHN,
                        FieldTypeParams.UPPERCASE,
                        FieldTypeParams.LOWERCASE,
                        FieldTypeParams.TO_UPPERCASE,
                        FieldTypeParams.TO_LOWERCASE,
                        FieldTypeParams.IGNORE_VALIDATIONS,
                    )
                ]

            case FieldTypeParams.DATE:
                date_format = QLineEdit()
                date_format.setPlaceholderText("Format in Python datetime")
                time_frames = QComboBox()
                time_frames.addItems((FieldTypeParams.ANY_TIME, FieldTypeParams.PAST_TIME, FieldTypeParams.FUTURE_TIME))

                widgets: widgets_list = [date_format, time_frames]

            case FieldTypeParams.MCC:
                widgets: widgets_list = [QCheckBox(FieldTypeParams.MCC_ISO)]

        for widget in widgets:
            self.FieldTypeLayout.addWidget(widget)
