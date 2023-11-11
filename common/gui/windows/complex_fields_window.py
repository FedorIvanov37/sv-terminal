from re import search
from json import dumps, loads
from json.decoder import JSONDecodeError
from logging import error
from dataclasses import asdict
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMenu, QDialog, QPushButton, QApplication
from common.lib.data_models.Config import Config
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.core.Parser import Parser
from common.gui.forms.complex_fields_parser import Ui_ComplexFieldsParser
from common.gui.decorators.window_settings import set_window_icon, has_close_button_only
from common.gui.core.json_views.JsonView import JsonView
from common.gui.constants import MainFieldSpec, ButtonActions
from common.lib.data_models.Transaction import Transaction


class ComplexFieldsParser(Ui_ComplexFieldsParser, QDialog):
    spec: EpaySpecification = EpaySpecification()

    def __init__(self, config: Config, terminal):
        super(ComplexFieldsParser, self).__init__()
        self.config: Config = config
        self.terminal = terminal
        self.setupUi(self)
        self._setup()

    @has_close_button_only
    @set_window_icon
    def _setup(self):
        self.PlusButton: QPushButton = QPushButton(ButtonActions.BUTTON_PLUS_SIGN)
        self.MinusButton: QPushButton = QPushButton(ButtonActions.BUTTON_MINUS_SIGN)
        self.NextLevelButton: QPushButton = QPushButton(ButtonActions.BUTTON_NEXT_LEVEL_SIGN)
        self.UpButton: QPushButton = QPushButton(f"{ButtonActions.BUTTON_UP_SIGN} To JSON ")
        self.DownButton: QPushButton = QPushButton(f"{ButtonActions.BUTTON_DOWN_SIGN} To String ")
        self.JsonView: JsonView = JsonView(self.config, "Field Data")

        widgets_layouts_map = {
            self.PlusLayout: self.PlusButton,
            self.MinusLayout: self.MinusButton,
            self.NextLevelLayout: self.NextLevelButton,
            self.UpLayout: self.UpButton,
            self.DownLayout: self.DownButton,
            self.JsonLayout: self.JsonView,
        }

        for button in self.UpButton, self.DownButton:
            button.setFont(QFont("MS Shell Dlg 2", 10))

        for layout, widget in  widgets_layouts_map.items():
            layout.addWidget(widget)

        for field in asdict(self.spec.FIELD_SET).values():
            if not self.spec.is_field_complex([field]):
                continue

            description: str = self.spec.get_field_description([field], string=True)

            self.FieldNumber.addItem(f"{field} - {description}")

        button_menu_structure = {
            self.ButtonClearString: {
                ButtonActions.ALL: self.clear_all,
                ButtonActions.JSON: self.JsonView.clean,
                ButtonActions.STRING: self.clear_string,
            },

            self.ButtonCopy: {
                ButtonActions.JSON: self.copy_json,
                ButtonActions.STRING: self.copy_string,
            },
        }

        for button, actions in button_menu_structure.items():
            button.setMenu(QMenu())

            for action, function in actions.items():
                button.menu().addAction(action, function)
                button.menu().addSeparator()

        self.JsonView.hideColumn(MainFieldSpec.ColumnsOrder.PROPERTY)
        self.JsonView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.connect_all()
        self.set_field_data()

    def connect_all(self):
        button_connection_map = {
            self.ButtonClose: self.close,
            self.ButtonGetFromMessage: self.get_from_main_window,
            self.ButtonClearString: self.clear_string,
            self.UpButton: self.parse_string,
            self.DownButton: self.parse_json,
            self.PlusButton: self.JsonView.plus,
            self.MinusButton: self.JsonView.minus,
            self.NextLevelButton: self.JsonView.next_level,
            self.ButtonSetToMessage: self.set_to_message,
        }

        for button, action in button_connection_map.items():
            button.clicked.connect(action)

        self.FieldNumber.currentIndexChanged.connect(self.set_field_data)

    def copy_json(self):
        json_data: dict = self.get_json_data()
        json_data: str = dumps(json_data, indent=4)
        self.set_clipboard_text(json_data)

    def copy_string(self):
        self.set_clipboard_text(self.TextData.toPlainText())

    @staticmethod
    def set_clipboard_text(data: str = str()) -> None:
        QApplication.clipboard().setText(data)

    def set_to_message(self):
        try:
            field_number = self.get_field_number()
        except LookupError as lookup_error:
            error(lookup_error)
            return

        if not (json_data := self.get_json_data()):
            return

        if not (field_data := json_data.get(field_number)):
            return

        transaction: Transaction = self.terminal.parse_main_window()
        transaction.data_fields[field_number] = field_data

        self.terminal.parse_transaction(transaction)

    def get_json_data(self):
        try:
            field_number = self.get_field_number()
        except LookupError as lookup_error:
            error(lookup_error)
            return

        try:
            json_data = self.JsonView.generate_fields()
        except ValueError as validation_error:
            self.clear_string()
            error(validation_error)
            return

        if not (json_data.get(field_number)):
            return

        return json_data

    def clear_all(self):
        self.JsonView.clean()
        self.clear_string()

    def parse_json(self):
        string_data = str()

        for item in self.JsonView.root.get_children():
            if not item.childCount():
                continue

            try:
                string_data = string_data + Parser.join_complex_item(item)
            except Exception as parsing_error:
                error(f"JSON parsing error: {parsing_error}")
                return

        self.TextData.setText(string_data)

    def get_from_main_window(self):
        try:
            field_number = self.get_field_number()
        except LookupError as lookup_error:
            error(lookup_error)
            return

        try:
            transaction: Transaction = self.terminal.parse_main_window()
        except Exception as window_parsing_error:
            error(window_parsing_error)
            return

        if not (field_data := transaction.data_fields.get(field_number)):
            return

        self.TextData.setText(field_data)
        self.parse_string()

    def parse_string(self):
        try:
            field_number = self.get_field_number()
        except LookupError as lookup_error:
            error(lookup_error)
            return

        if not (field_data := self.TextData.toPlainText()):
            return

        try:
            field_data = self.parse_json_data(field_data)
        except Exception as parsing_error:
            error(parsing_error)
            return

        field_data = field_data.replace("\n", "")

        try:
            json_data = Parser.split_complex_field(field_number, field_data)
        except Exception as parsing_error:
            error(f"String parsing error: {parsing_error}")
            self.JsonView.clean()
            return

        json_data = {field_number: json_data}

        self.JsonView.clean()
        self.JsonView.parse_fields(json_data)

    def parse_json_data(self, data: str):
        try:
            json_data: dict = loads(data)
        except JSONDecodeError:
            return data

        if not isinstance(json_data, dict):
            return str(data)

        field_number = self.get_field_number()

        if not (json_body := json_data.get(field_number)):
            return data

        field_data: str = Parser.join_complex_field(field_number, json_body)

        return field_data

    def set_field_data(self):
        self.JsonView.clean()
        self.get_from_main_window()

    def clear_string(self):
        self.TextData.setText(str())

    def get_field_number(self):
        field_number = self.FieldNumber.currentText()

        if not (field_number := search(r"^\d{1,3}", field_number)):
            raise LookupError("Cannot get field number")

        field_number = field_number.group()

        return field_number
