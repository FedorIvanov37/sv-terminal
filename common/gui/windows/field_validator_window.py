from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QDialog, QListWidgetItem, QCheckBox, QLineEdit, QComboBox
from common.gui.core.CheckableComboBox import CheckableComboBox
from common.gui.forms.field_validator_window import Ui_FieldDataSet
from common.gui.decorators.window_settings import set_window_icon, has_close_button_only
from common.lib.data_models.EpaySpecificationModel import IsoField, Validators
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.constants import ValidationParams


class FieldDataSet(Ui_FieldDataSet, QDialog):
    spec: EpaySpecification = EpaySpecification()
    _field_spec: IsoField = None
    _literal_validations_map: dict
    _field_spec_accepted: pyqtSignal = pyqtSignal(IsoField)

    @property
    def field_spec_accepted(self):
        return self._field_spec_accepted

    @property
    def field_spec(self):
        return self._field_spec

    def __init__(self, field_spec: IsoField):
        super(FieldDataSet, self).__init__()
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

        self.CheckTypeLayout.addWidget(self.CheckTypeBox)
        self.parse_field_spec(self.field_spec)
        self.process_changes()
        self.process_field_type_change()
        self.connect_all()

    def connect_all(self):
        self.CheckBoxComplex.stateChanged.connect(self.process_changes)
        self.FillSide.currentIndexChanged.connect(self.process_changes)
        self.FieldType.currentIndexChanged.connect(self.process_field_type_change)
        self.CancelButton.clicked.connect(self.close)
        self.PlusButton.clicked.connect(self.plus)
        self.MinusButton.clicked.connect(self.remove_validation_value)
        self.CheckTypeBox.currentIndexChanged.connect(self.process_check_type_change)
        self.OkButton.clicked.connect(self.ok)
        self.FillSide.currentIndexChanged.connect(self.process_justification_change)
        self.FillUpTo.currentIndexChanged.connect(self.process_justification_length_change)
        self.FillSymbol.textChanged.connect(self.set_justification_simbols)

        checkboxes = (
            self.CheckBoxAlpha,
            self.CheckBoxNumeric,
            self.CheckBoxSpecial,
            self.CheckBoxMatching,
            self.CheckBoxReversal,
            self.CheckBoxGeneratible,
            self.CheckBoxSecret,
        )

        for checkbox in checkboxes:
            checkbox.stateChanged.connect(lambda: self.process_checkbox_change(checkbox))

    def ok(self):
        self.save_validations()
        self.field_spec_accepted.emit(self.field_spec)
        self.accept()

    def set_justification_simbols(self):
        self.field_spec.validators.justification_element = self.FillSymbol.text()

    def process_justification_length_change(self):
        just_len_map = {
            "Min Length": self.MinLength.value(),
            "Max Length": self.MaxLength.value()
        }

        just_len = self.FillUpTo.currentText()

        if just_len in just_len_map:
            self.field_spec.validators.justification_length = just_len_map.get(just_len)
            return

        if not str(just_len).isdigit():
            return

        self.field_spec.validators.justification_length = just_len

    def process_justification_change(self):
        just_map = {
            "No Pad": None,
            "Left Pad": "LEFT",
            "Rigth Pad": "RIGHT"
        }

        self.field_spec.validators.justification = just_map.get(self.FillSide.currentText())

    def process_checkbox_change(self, checkbox: QCheckBox):
        match checkbox:
            case self.CheckBoxAlpha:
                self.field_spec.alpha = checkbox.isChecked()
            case self.CheckBoxNumeric:
                self.field_spec.numeric = checkbox.isChecked()
            case self.CheckBoxSpecial:
                self.field_spec.special = checkbox.isChecked()
            case self.CheckBoxMatching:
                self.field_spec.matching = checkbox.isChecked()
            case self.CheckBoxReversal:
                self.field_spec.reversal = checkbox.isChecked()
            case self.CheckBoxGeneratible:
                self.field_spec.generate = checkbox.isChecked()
            case self.CheckBoxSecret:
                self.field_spec.is_secret = checkbox.isChecked()

    def process_check_type_change(self):
        if previous_check_type := self.CheckTypeBox.get_previous_text():
            self.save_validations(previous_check_type)

        current_check_type: str = self.CheckTypeBox.currentText()

        self.set_validation_items(current_check_type)

    def save_validations(self, check_type: str | None = None):
        if check_type is None:
            check_type = self.CheckTypeBox.currentText()

        literal_list: list[str] = []

        for row in range(self.ValuesList.count()):
            item = self.ValuesList.item(row)
            literal_list.append(item.text())

        literal_list: list[str] = list(set(literal_list))

        if str() in literal_list:
            literal_list.remove(str())

        self._literal_validations_map[check_type] = literal_list

        self.update_validators()

    def update_validators(self):
        self.field_spec.validators.must_contain=self._literal_validations_map.get(ValidationParams.MUST_CONTAIN)
        self.field_spec.validators.must_contain_only=self._literal_validations_map.get(ValidationParams.MUST_CONTAIN_ONLY)
        self.field_spec.validators.must_not_contain=self._literal_validations_map.get(ValidationParams.MUST_NOT_CONTAIN)
        self.field_spec.validators.must_not_contain_only=self._literal_validations_map.get(ValidationParams.MUST_NOT_CONTAIN_ONLY)
        self.field_spec.validators.must_start_with=self._literal_validations_map.get(ValidationParams.MUST_START_WITH)
        self.field_spec.validators.must_not_start_with=self._literal_validations_map.get(ValidationParams.MUST_NOT_START_WITH)
        self.field_spec.validators.must_end_with=self._literal_validations_map.get(ValidationParams.MUST_END_WITH)
        self.field_spec.validators.must_not_end_with=self._literal_validations_map.get(ValidationParams.MUST_NOT_END_WITH)
        self.field_spec.validators.valid_values=self._literal_validations_map.get(ValidationParams.VALID_VALUES)
        self.field_spec.validators.invalid_values=self._literal_validations_map.get(ValidationParams.INVALID_VALUES)

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

    def remove_validation_value(self):
        self.ValuesList.setFocus()

        if not (item := self.ValuesList.currentItem()):
            return

        self.ValuesList.takeItem(self.ValuesList.row(item))
        self.set_validator_mark()

    def plus(self):
        item: QListWidgetItem = self.add_validation_value()
        self.set_validator_mark()
        self.ValuesList.editItem(item)

    def set_validator_mark(self):
        self.CheckTypeBox.set_validation_mark(mark=self.ValuesList.count() > int())

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
            self.FillSide.setCurrentText("No Pad")

        self.FieldDescription.setText(f"Field {field_path} - {field_desc}")
        self.CheckBoxComplex.setChecked(not iso_field.fields is None)

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
            state: Qt.CheckState = Qt.CheckState.Checked if values else Qt.CheckState.Unchecked
            self.CheckTypeBox.addItem(check_type, state)

        self.set_validation_items(self.CheckTypeBox.currentText())

    def process_changes(self):
        self.TagLengthLabel.setEnabled(self.CheckBoxComplex.isChecked())
        self.TagLength.setEnabled(self.CheckBoxComplex.isChecked())

        justification_enabled = self.FillSide.currentText().upper() != "NO PAD"
        
        for element in self.FillUpTo, self.FillSymbolLabel, self.FillUpToLabel, self.FillSymbol.setEnabled:
            element.setEnabled(justification_enabled)

    def process_field_type_change(self):
        for row in range(self.FieldTypeLayout.count()):
            if not (widget := self.FieldTypeLayout.itemAt(row).widget()):
                continue

            widget.hide()

        match self.FieldType.currentText():
            case "Currency":
                code_a3 = QCheckBox("Currency Code Alpha 3")
                code_n3 = QCheckBox("Currency Code Numeric 3")

                for widget in code_a3, code_n3:
                    self.FieldTypeLayout.addWidget(widget)

            case "Country":
                code_a3 = QCheckBox("Country Code Alpha 3")
                code_a2 = QCheckBox("Country Code Alpha 2")
                code_n3 = QCheckBox("Country Code Numeric 3")

                for widget in code_a2, code_a3, code_n3:
                    self.FieldTypeLayout.addWidget(widget)

            case "MCC":
                self.FieldTypeLayout.addWidget(QCheckBox("ISO 18245 MCC"))

            case "Date":
                date_format = QLineEdit()
                date_format.setPlaceholderText("Date format Python datetime")
                current_date = QComboBox()
                current_date.addItems(["Past time", "Future time", "Not check"])

                for widget in date_format, current_date:
                    self.FieldTypeLayout.addWidget(widget)

            case "Other":
                check_luhn = QCheckBox("Check Luhn algorithm")
                uppercase = QCheckBox("Upper case only")
                lowercase = QCheckBox("Lower case only")
                to_uppercase = QCheckBox("Translate to upper case")
                to_lowercase = QCheckBox("Translate to lower case")
                ignore = QCheckBox("Ignore all validations")

                for widget in check_luhn, uppercase, lowercase, to_uppercase, to_lowercase, ignore:
                    self.FieldTypeLayout.addWidget(widget)
