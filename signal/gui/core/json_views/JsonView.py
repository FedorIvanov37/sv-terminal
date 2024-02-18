from copy import deepcopy
from logging import error, warning, debug
from PyQt6.QtCore import pyqtSignal, QModelIndex
from PyQt6.QtWidgets import QTreeWidgetItem, QItemDelegate, QLineEdit
from signal.lib.core.EpaySpecification import EpaySpecification
from signal.lib.core.FieldsGenerator import FieldsGenerator
from signal.lib.core.Parser import Parser
from signal.lib.exceptions.exceptions import DataValidationError, DataValidationWarning
from signal.lib.data_models.Transaction import Transaction, TypeFields
from signal.lib.data_models.Config import Config
from signal.lib.data_models.EpaySpecificationModel import RawFieldSet, Justification, IsoField
from signal.gui.core.json_items.FIeldItem import FieldItem
from signal.gui.core.validators.ItemsValidator import ItemsValidator
from signal.gui.core.json_views.TreeView import TreeView
from signal.gui.core.Undo import UndoAddChildCommand, UndoRemoveChildCommand
from signal.gui.decorators.void_qt_signals import void_qt_signals
from signal.gui.enums.CheckBoxesDefinition import CheckBoxesDefinition
from signal.gui.enums.Colors import Colors
from signal.gui.enums import MainFieldSpec as FieldsSpec
from signal.gui.enums.RootItemNames import RootItemNames


class JsonView(TreeView):
    class Delegate(QItemDelegate):
        _text_edited: pyqtSignal = pyqtSignal(str, int)

        @property
        def text_edited(self):
            return self._text_edited

        def setEditorData(self, editor: QLineEdit, index: QModelIndex):
            editor.textEdited.connect(lambda text: self.text_edited.emit(text, index.column()))
            QItemDelegate.setEditorData(self, editor, index)

    root: FieldItem
    need_disable_next_level: pyqtSignal = pyqtSignal()
    need_enable_next_level: pyqtSignal = pyqtSignal()
    spec: EpaySpecification = EpaySpecification()

    @property
    def len_fill(self):
        return 3 if self.config.validation.validation_enabled else None

    @property
    def hide_secret_fields(self):
        return self.config.fields.hide_secrets

    def __init__(self, config: Config, root_name: str = RootItemNames.TRANSACTION_ROOT_NAME):
        super(JsonView, self).__init__()
        self.root: FieldItem = FieldItem([root_name])
        self.config: Config = config
        self.delegate = JsonView.Delegate()
        self.validator = ItemsValidator(self.config)
        self._setup()

    def _setup(self):
        self.setTabKeyNavigation(True)
        self.setAnimated(True)
        self.itemDoubleClicked.connect(self.editItem)
        self.itemChanged.connect(self.process_change_item)
        self.itemChanged.connect(self.disable_next_level)
        self.delegate.closeEditor.connect(lambda: self.hide_secrets())
        self.delegate.closeEditor.connect(lambda: self.set_all_items_length())
        self.delegate.text_edited.connect(self.set_item_length)
        self.currentItemChanged.connect(self.disable_next_level)
        self.setItemDelegate(self.delegate)
        self.setHeaderLabels(FieldsSpec.Columns)
        self.addTopLevelItem(self.root)
        self.header().setMaximumSectionSize(700)
        self.header().resizeSection(FieldsSpec.ColumnsOrder.DESCRIPTION, 470)
        self.make_order()

    def search(self, text: str, parent: FieldItem | None = None) -> None:
        TreeView.search(self, text, parent)

        if text == str():
            self.resize_all()

    @void_qt_signals
    def set_item_length(self, text, column):
        item: QTreeWidgetItem | FieldItem

        if not (item := self.currentItem()):
            return

        if item.childCount():
            return

        if column not in (FieldsSpec.ColumnsOrder.VALUE, FieldsSpec.ColumnsOrder.LENGTH):
            return

        if column == FieldsSpec.ColumnsOrder.LENGTH and not self.config.validation.validation_enabled:
            return

        item.set_length(len(text), fill_length=self.len_fill)

    def set_all_items_length(self, parent: FieldItem | None = None):
        if parent is None:
            parent = self.root

        child_item: FieldItem

        for child_item in parent.get_children():
            if child_item.childCount():
                self.set_all_items_length(child_item)

            if not child_item.field_length.isdigit():
                continue

            child_item.set_length(fill_length=self.len_fill)

    def refresh_fields(self, parent: FieldItem | None = None):
        if parent is None:
            parent = self.root

        child_item: FieldItem

        for child_item in parent.get_children():
            if child_item.childCount():
                self.refresh_fields(child_item)
                continue

            self.set_item_description(child_item)

        self.set_all_items_length(self.root)

    def hide_secrets(self, parent=None):
        if parent is None:
            parent = self.root

        child: FieldItem

        for child in parent.get_children():
            if child.childCount():
                self.hide_secrets(parent=child)

            child.hide_secret()

    def disable_next_level(self, item: FieldItem):  # Disable button NextLevel in case when flat-mode active
        current_item: FieldItem

        if not (current_item := self.currentItem()):
            current_item: FieldItem = item

        exemptions = [
            item.get_field_depth() != 1,
            not self.spec.is_field_complex(item.get_field_path()),
            item.checkbox_checked(CheckBoxesDefinition.JSON_MODE) and item is current_item,
            current_item.checkbox_checked(CheckBoxesDefinition.JSON_MODE),
            not self.spec.is_field_complex(current_item.get_field_path())
        ]

        signal = self.need_enable_next_level if any(exemptions) else self.need_disable_next_level
        signal.emit()

        if self.currentItem():
            return

        self.setCurrentItem(item)

    def editItem(self, item, column):
        if item is self.root:
            return

        if column not in (FieldsSpec.ColumnsOrder.FIELD, FieldsSpec.ColumnsOrder.VALUE, FieldsSpec.ColumnsOrder.LENGTH):
            return

        if column == FieldsSpec.ColumnsOrder.LENGTH and self.config.validation.validation_enabled:
            return

        if column == FieldsSpec.ColumnsOrder.VALUE:
            if item.childCount():
                return

            item.hide_secret(False)

        if column == FieldsSpec.ColumnsOrder.LENGTH and item.spec:
            return

        TreeView.editItem(self, item, column)

    def generate_item_data(self, item):
        if not item.checkbox_checked(CheckBoxesDefinition.GENERATE):
            return

        item.field_data = FieldsGenerator.generate_field(item.field_number, self.config.fields.max_amount)

    def process_change_property(self, item: FieldItem) -> None:
        try:
            checkbox_type: str = self.itemWidget(item, FieldsSpec.ColumnsOrder.PROPERTY).text()
        except AttributeError | ValueError:
            return

        match checkbox_type:
            case CheckBoxesDefinition.JSON_MODE:
                if item.checkbox_checked(checkbox_type):
                    self.set_json_mode(item)
                    return

                self.set_flat_mode(item)

            case CheckBoxesDefinition.GENERATE:
                item.set_length(fill_length=self.len_fill)

                if not item.checkbox_checked(checkbox_type):
                    return

                item.set_item_color(Colors.BLACK)

    def set_subfields_length(self, item: FieldItem):
        parent: FieldItem
        child_item: FieldItem

        if not (parent := item.parent()):
            return

        if parent is self.root:
            return

        item_length: int = len(item.field_length)

        for child_item in parent.get_children():
            if child_item is item:
                continue

            if child_item.spec:
                continue

            child_length: int = len(child_item.field_length)

            if item_length > child_length:
                child_item.setText(FieldsSpec.ColumnsOrder.LENGTH, child_item.field_length.zfill(item_length))
                continue

            prefix: str = "0" * (child_length - item_length)

            child_item.setText(FieldsSpec.ColumnsOrder.LENGTH, child_item.field_length.removeprefix(prefix))

    @void_qt_signals
    def process_change_item(self, item: FieldItem, column):
        if item is self.root:
            return

        item.set_spec()

        try:
            match column:

                case FieldsSpec.ColumnsOrder.VALUE:
                    self.generate_item_data(item)
                    item.field_data = self.get_justified_field_data(item.spec, item.field_data)
                    self.validate_item(item)
                    item.set_item_color()

                case FieldsSpec.ColumnsOrder.PROPERTY:
                    self.generate_item_data(item)
                    self.process_change_property(item)

                case FieldsSpec.ColumnsOrder.FIELD:
                    self.check_all_items(item)
                    item.set_checkbox()

                case FieldsSpec.ColumnsOrder.LENGTH:
                    self.set_subfields_length(item)

        except (ValueError, DataValidationError) as validation_error:
            item.set_item_color(Colors.RED)
            [warning(err) for err in str(validation_error).splitlines()]
            return

        except DataValidationWarning:
            item.set_item_color(Colors.RED)

        if column != FieldsSpec.ColumnsOrder.PROPERTY:
            self.set_item_description(item)

    @staticmethod
    def get_justified_field_data(field_spec: IsoField, value: str) -> str:
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

    @void_qt_signals
    def set_item_description(self, item: FieldItem):
        try:
            item.set_spec()
        except Exception as set_spec_error:
            debug(set_spec_error)

        specification_found = any((item.spec, self.config.validation.validation_enabled))

        if specification_found:
            item.set_description()

        if not specification_found:
            warn_text = f"⚠ ️No specification for field {item.get_field_path(string=True)}, set field length manually"

            if not item.field_number:
                error(f"Lost field number for field {item.get_field_path(string=True)}")
                return

            item.set_description(warn_text)

        if not item.childCount():
            return

        for child in item.get_children():
            self.set_item_description(child)

    def validate_item(self, item, check_config: bool = True):  # Validate single item, no auto children validate
        if check_config and not self.config.validation.validation_enabled:
            return

        if item is self.root:
            return

        if self.spec.can_be_generated(item.get_field_path()):
            self.validator.validate_duplicates(item)

            if item.checkbox_checked(CheckBoxesDefinition.GENERATE):
                return

        self.validator.validate_item(item)

    def validate_items(self, parent: FieldItem):  # Validate item and child-items when the item has children
        for row in parent.get_children():
            self.validate_item(row)

            if row.childCount():
                self.validate_items(row)

    @void_qt_signals
    def check_all_items(self, parent: FieldItem | None = None, check_config: bool = True):  # Validate and paint item without raising ValueError
        def set_error(item: FieldItem, exception: Exception):
            item.set_item_color(Colors.RED)

            for string in str(exception).splitlines():
                warning(string)

            self.setFocus()

        if parent is None:
            parent = self.root

        try:
            self.validate_item(parent, check_config=check_config)

        except (ValueError, DataValidationError, DataValidationWarning) as validation_error:
            set_error(parent, validation_error)

        else:
            parent.set_item_color()

        for child_item in parent.get_children():
            if child_item.childCount():
                self.check_all_items(parent=child_item, check_config=check_config)
                continue

            try:
                self.validate_item(child_item, check_config=check_config)

            except (ValueError, DataValidationError, DataValidationWarning) as validation_error:
                set_error(child_item, validation_error)
                continue

            child_item.set_item_color(Colors.BLACK)

    def plus(self):
        if not (current_item := self.currentItem()):
            return

        if not (parent := current_item.parent()):
            parent = self.root

        item = FieldItem([])
        index = parent.indexOfChild(current_item)

        if current_item is self.root:
            index = index + 1

        parent.insertChild(index, item)

        self.set_new_item(item)
        self.field_added.emit()
        self.undo_stack.push(UndoAddChildCommand(item, parent))

    @void_qt_signals
    def minus(self, *args):
        item: FieldItem | QTreeWidgetItem

        if not (item := self.currentItem()):
            return

        if item is self.root:
            self.setFocus()
            return

        if not (parent := item.parent()):
            return

        self.undo_stack.push(UndoRemoveChildCommand(item, parent))

        parent.removeChild(item)
        parent.set_length(fill_length=self.len_fill)

        self.check_duplicates_after_remove(item, parent)
        self.setFocus()
        self.field_removed.emit()

    def next_level(self, *args):
        current_item: FieldItem | None = self.currentItem()

        if not current_item:
            return

        if current_item.get_field_depth() == 1:
            is_field_complex = self.spec.is_field_complex(current_item.get_field_path())

            if is_field_complex and not current_item.checkbox_checked(CheckBoxesDefinition.JSON_MODE):
                return

        item = FieldItem([])

        if current_item is None:
            return

        current_item.setText(FieldsSpec.ColumnsOrder.VALUE, str())
        current_item.insertChild(int(), item)
        self.set_new_item(item)
        self.undo_stack.push(UndoAddChildCommand(item, current_item))

    def set_new_item(self, item: FieldItem):
        self.setCurrentItem(item)
        self.scrollToItem(item)
        self.setFocus()
        self.editItem(item, int())

    def check_duplicates_after_remove(self, removed_item: FieldItem, parent_item: FieldItem):
        try:
            self.validator.validate_duplicates(removed_item, parent=parent_item)
        except ValueError:
            return

        for item in parent_item.get_children():
            if not item.field_number == removed_item.field_number:
                continue

            try:
                self.validate_item(item)
            except ValueError:
                item.set_item_color(Colors.RED)
                return

            item.set_item_color()

    def clean(self):
        TreeView.clean(self)
        self.root.set_length()

    @void_qt_signals
    def set_field_value(self, field, value):
        for item in self.root.get_children():
            if item.field_number != field:
                continue

            item.field_data = value

    def parse_transaction(self, transaction: Transaction) -> None:
        for item in self.root.get_children():
            if not item.checkbox_checked(CheckBoxesDefinition.JSON_MODE):
                continue

            transaction.json_fields.append(item.field_number)

        self.clean()

        fields = deepcopy(transaction.data_fields)

        self.parse_fields(fields)
        self.set_checkboxes(transaction)
        self.check_all_items()

        for item in self.root.get_children():
            if item.checkbox_checked(CheckBoxesDefinition.JSON_MODE):
                self.set_json_mode(item)
                continue

            self.set_flat_mode(item)

        self.set_all_items_length()

    def switch_json_mode(self, json_mode):
        for item in self.root.get_children():
            if not self.spec.is_field_complex(item.get_field_path()):
                continue

            item.set_checkbox(json_mode)

            if json_mode:
                self.set_json_mode(item)

            if not json_mode:
                self.set_flat_mode(item)

    def set_json_mode(self, item: FieldItem):
        parsing_error_text: str = "Cannot change JSON mode due to parsing error(s)"

        if item.childCount():
            return

        if not isinstance(item.field_data, str):
            return

        try:
            fields: RawFieldSet = Parser.split_complex_field(item.field_number, item.field_data)
            self.parse_fields(fields, parent=item, specification=self.spec.fields.get(item.field_number))

        except Exception as parsing_error:
            error(f"{parsing_error_text}: {parsing_error}")
            item.set_checkbox(False)
            return

        item.field_data = ""

        if self.config.validation.validation_enabled:
            self.check_all_items(item)

        self.hide_secrets(parent=item)

    def set_flat_mode(self, item):
        parsing_error_text: str = "Cannot change JSON mode due to parsing error(s)"

        if not item.childCount():
            return

        try:
            item.field_data = Parser.join_complex_item(item)
            item.takeChildren()

        except Exception as parsing_error:
            error(parsing_error_text)
            [error(line) for line in str(parsing_error).splitlines()]
            item.set_checkbox()

        self.hide_secrets()

    @void_qt_signals
    def set_checkboxes(self, transaction: Transaction):
        generate_fields = self.spec.get_fields_to_generate()

        for item in self.root.get_children():
            is_checked = False

            if item.field_number in generate_fields:
                is_checked = item.field_number in transaction.generate_fields

            if self.spec.is_field_complex(item.get_field_path()):
                is_checked = self.config.fields.json_mode

                if item.field_number in transaction.json_fields:
                    is_checked = True

            item.set_checkbox(is_checked)

    def parse_fields(self, input_json: dict, parent: QTreeWidgetItem = None, specification=None):
        if parent is None:
            parent = self.root

        if specification is None:
            specification = self.spec.spec

        for field, field_data in input_json.items():
            field_spec = specification.fields.get(field)

            description = field_spec.description if field_spec else None

            if isinstance(field_data, dict):
                child = FieldItem([field])
                child.setText(FieldsSpec.ColumnsOrder.DESCRIPTION, description)
                self.parse_fields(field_data, parent=child, specification=specification.fields.get(field))

            else:
                field_data = self.get_justified_field_data(field_spec, str(field_data))
                string_data = [field, field_data, None, description]
                child: FieldItem = FieldItem(string_data)

            parent.addChild(child, fill_len=self.len_fill)
            child.set_spec(field_spec)
            self.set_item_description(child)

        self.set_all_items_length()
        self.hide_secrets()
        self.make_order()

    def get_top_level_field_numbers(self) -> list[str]:
        field_numbers: list[str] = list()

        for item in self.root.get_children():
            if item.field_data or bool(item.checkState(FieldsSpec.ColumnsOrder.PROPERTY)):
                field_numbers.append(item.field_number)

        return field_numbers

    def generate_fields(self, parent=None, flat: bool = False):
        result: TypeFields = dict()

        if parent is None:
            parent = self.root

        row: FieldItem

        for row in parent.get_children():
            if self.config.validation.validation_enabled:
                self.validate_items(row)

            if row.field_number in result:
                warning(f"Duplicated field number {row.get_field_path(string=True)}")

            if row.childCount():
                if flat:
                    result[row.field_number] = Parser.join_complex_item(row)
                else:
                    result[row.field_number] = self.generate_fields(row, flat=flat)

            if not row.childCount():
                result[row.field_number] = row.field_data

        if parent is self.root:
            fields = {field: result[field] for field in sorted(result, key=int)}

            if not self.config.validation.validation_enabled:
                return fields

            self.validator.validate_fields(fields)

        return result

    def get_checkboxes(self, checkbox_type=CheckBoxesDefinition.GENERATE) -> list[str]:
        checkboxes = list()
        item: FieldItem

        for item in self.root.get_children():
            if not item.checkbox_checked(checkbox_type):
                continue

            checkboxes.append(item.field_number)

        return checkboxes

    def field_has_data(self, field_number: str, parent: FieldItem | None = None):
        if parent is None:
            parent = self.root

        item: FieldItem

        for item in parent.get_children():
            if item.field_number != field_number:
                continue

            return bool(int(item.get_field_length()))

        return False
