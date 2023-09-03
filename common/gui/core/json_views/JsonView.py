from copy import deepcopy
from logging import error, warning
from collections import OrderedDict
from PyQt6.QtCore import pyqtSignal, QModelIndex
from PyQt6.QtWidgets import QTreeWidgetItem, QItemDelegate, QLineEdit
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.Transaction import Transaction, TypeFields
from common.lib.data_models.Config import Config
from common.lib.core.FieldsGenerator import FieldsGenerator
from common.lib.data_models.EpaySpecificationModel import RawFieldSet
from common.lib.core.Parser import Parser
from common.gui.constants.MainFieldSpec import MainFieldSpec as FieldsSpec
from common.gui.core.json_items.FIeldItem import FieldItem
from common.gui.core.validators.ItemsValidator import ItemsValidator
from common.gui.core.Undo import UndoAddChildCommand, UndoRemoveChildCommand
from common.gui.constants.CheckBoxesDefinition import CheckBoxesDefinition
from common.gui.decorators.void_qt_signals import void_qt_signals
from common.gui.core.json_views.TreeView import TreeView


class JsonView(TreeView):
    class Delegate(QItemDelegate):
        _text_edited: pyqtSignal = pyqtSignal(str, int)

        @property
        def text_edited(self):
            return self._text_edited

        def setEditorData(self, editor: QLineEdit, index: QModelIndex):
            editor.textEdited.connect(lambda text: self.text_edited.emit(text, index.column()))
            QItemDelegate.setEditorData(self, editor, index)

    need_disable_next_level: pyqtSignal = pyqtSignal()
    need_enable_next_level: pyqtSignal = pyqtSignal()
    root: FieldItem = FieldItem([FieldsSpec.MESSAGE])
    spec: EpaySpecification = EpaySpecification()

    @property
    def hide_secret_fields(self):
        return self.config.fields.hide_secrets

    def __init__(self, config: Config):
        super(JsonView, self).__init__()
        self.config: Config = config
        self._setup()
        self.delegate = JsonView.Delegate()
        self.delegate.closeEditor.connect(lambda: self.hide_secrets())
        self.delegate.closeEditor.connect(lambda: self.set_all_items_length())
        self.delegate.text_edited.connect(self.set_item_length)
        self.setItemDelegate(self.delegate)

    def _setup(self):
        self.setTabKeyNavigation(True)
        self.setAnimated(True)

        for action in (self.itemCollapsed, self.itemExpanded, self.itemChanged):
            action.connect(self.resize_all)

        self.header().setMaximumSectionSize(700)
        self.validator = ItemsValidator(self.config)
        self.itemDoubleClicked.connect(self.edit_item)
        self.itemChanged.connect(self.process_change_item)
        self.itemChanged.connect(self.disable_next_level)
        self.currentItemChanged.connect(self.disable_next_level)
        self.setHeaderLabels(FieldsSpec.columns)
        self.addTopLevelItem(self.root)
        self.make_order()

    def search(self, text: str, parent = None) -> None:
        TreeView.search(self, text, parent)

        if text == str():
            self.resize_all()

    def set_item_length(self, text, column):
        item: QTreeWidgetItem | FieldItem

        if not (item := self.currentItem()):
            return

        if column != FieldsSpec.ColumnsOrder.VALUE:
            return

        item.set_length(len(text))

    def set_all_items_length(self, parent: FieldItem | None = None):
        if parent is None:
            parent = self.root

        child_item: FieldItem

        for child_item in parent.get_children():
            if child_item.childCount():
                self.set_all_items_length(child_item)

            child_item.set_length()

    def hide_secrets(self, parent=None):
        if parent is None:
            parent = self.root

        child: FieldItem

        for child in parent.get_children():
            if child.childCount():
                self.hide_secrets(parent=child)

            child.hide_secret()

    def disable_next_level(self, item: FieldItem):
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

    @void_qt_signals
    def process_change_item(self, item: FieldItem, column):
        if item is self.root:
            return

        if column in (FieldsSpec.ColumnsOrder.PROPERTY, FieldsSpec.ColumnsOrder.VALUE):
            if item.checkbox_checked(CheckBoxesDefinition.GENERATE):
                item.field_data = FieldsGenerator.generate_field(item.field_number, self.config.fields.max_amount)

        if column == FieldsSpec.ColumnsOrder.PROPERTY:
            try:
                text = self.itemWidget(item, FieldsSpec.ColumnsOrder.PROPERTY).text()
            except AttributeError | ValueError:
                text = ""

            if text  == CheckBoxesDefinition.JSON_MODE:
                if item.checkbox_checked(CheckBoxesDefinition.JSON_MODE):
                    self.set_json_mode(item)
                else:
                    self.set_flat_mode(item)

        try:
            item.process_change_item()

        except LookupError as spec_error:
            item.set_item_color(red=True)
            warning(spec_error)
            return

        if column == FieldsSpec.ColumnsOrder.FIELD:
            item.set_checkbox()

        try:
            self.validate(item, column)

        except ValueError as validation_error:
            item.set_item_color(red=True)
            [warning(err) for err in str(validation_error).splitlines()]

    def edit_column(self, column: int):
        if column not in (FieldsSpec.ColumnsOrder.FIELD, FieldsSpec.ColumnsOrder.VALUE):
            return

        if not self.hasFocus():
            self.setFocus()

        item: FieldItem | QTreeWidgetItem

        if not (item := self.currentItem()):
            return

        self.edit_item(item, column)

    def validate(self, item, column=None):
        if not self.config.fields.validation:
            return

        if self.spec.can_be_generated(item.get_field_path()):
            if item.checkbox_checked(CheckBoxesDefinition.GENERATE):
                return

        if column == FieldsSpec.ColumnsOrder.FIELD:
            if all((item.field_number, not item.field_data, not item.childCount())):
                self.validator.validate_field_path(item.get_field_path())
                self.validator.validate_duplicates(item)
                return

        self.validator.validate_item(item)

    def validate_all(self, parent_item: FieldItem | None = None):
        if parent_item is None:
            parent_item = self.root

        for child_item in parent_item.get_children():
            child_item.set_item_color(red=False)

            try:
                self.validate(child_item)

            except ValueError as validation_error:
                child_item.set_item_color(red=True)
                warning(validation_error)

            self.validate_all(parent_item=child_item)

    def plus(self):
        item = FieldItem([])
        parent = None

        if current_item := self.currentItem():
            if not (parent := current_item.parent()):
                parent = self.root

        index = parent.indexOfChild(current_item) + 1
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

        parent: FieldItem = item.parent()
        removed_item_index = parent.indexOfChild(item)

        self.undo_stack.push(UndoRemoveChildCommand(item, parent))

        parent.removeChild(item)
        cursor_position = removed_item_index if removed_item_index == 0 else removed_item_index - 1
        parent.set_length()

        if not (new_position_item := parent.child(cursor_position)):
            new_position_item = parent

        self.setCurrentItem(new_position_item)
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
                self.validate(item)
            except ValueError:
                item.set_item_color(red=True)
                return

            item.set_item_color(red=False)

    def clean(self):
        TreeView.clean(self)
        self.root.set_length()

    @void_qt_signals
    def set_field_value(self, field, value):
        for item in self.root.get_children():
            if item.field_number != field:
                continue

            item.field_data = value

    def edit_item(self, item, column):
        if item is self.root:
            return

        if item.childCount():
            return

        if column not in (FieldsSpec.ColumnsOrder.FIELD, FieldsSpec.ColumnsOrder.VALUE):
            return

        if column == FieldsSpec.ColumnsOrder.VALUE:
            item.hide_secret(False)

        self.editItem(item, column)

    def parse_transaction(self, transaction: Transaction) -> None:
        self.clean()

        fields = deepcopy(transaction.data_fields)

        for field, field_data in fields.items():
            if self.config.fields.json_mode:
                break

            if not self.spec.is_field_complex([field]):
                continue

            if not isinstance(field_data, dict):
                continue

            try:
                fields[field] = Parser.join_complex_field(field, field_data)
            except Exception as parsing_error:
                error(f"Parsing error: {parsing_error}")
                return

        self._parse_fields(fields)
        self.set_checkboxes(transaction)

        if self.config.fields.validation:
            self.validate_all()

        self.make_order()
        self.hide_secrets()

    def switch_json_mode(self, json_mode):
        for item in self.root.get_children():
            if not self.spec.is_field_complex(item.get_field_path()):
                continue

            item.set_checkbox(json_mode)

            if not json_mode:
                self.set_flat_mode(item)
                continue

            self.set_json_mode(item)

    def set_json_mode(self, item: FieldItem):
        parsing_error_text: str = "Cannot change JSON mode due to parsing error(s)"

        if item.childCount():
            return

        if not isinstance(item.field_data, str):
            return

        try:
            fields: RawFieldSet = Parser.split_complex_field(item.field_number, item.field_data)
            self._parse_fields(fields, parent=item, specification=self.spec.fields.get(item.field_number))

        except Exception as parsing_error:
            error(f"{parsing_error_text}: {parsing_error}")
            item.set_checkbox(False)
            return

        item.field_data = ""
        # item.setExpanded(True)
        self.hide_secrets(parent=item)

    def set_flat_mode(self, item):
        parsing_error_text: str = "Cannot change JSON mode due to parsing error(s)"

        if not item.childCount():
            return

        try:
            fields: RawFieldSet = self.generate_fields(parent=item)
            field_data: str = Parser.join_complex_field(item.field_number, fields)
            item.takeChildren()
            item.field_data = field_data

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

            item.set_checkbox(is_checked)

    def _parse_fields(self, input_json: dict, parent: QTreeWidgetItem = None, specification=None):
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
                self._parse_fields(field_data, parent=child, specification=specification.fields.get(field))

            else:
                string_data = [field, str(field_data), None, description]
                child: FieldItem = FieldItem(string_data)

            parent.addChild(child)

            child.set_spec(field_spec)

    def get_top_level_field_numbers(self) -> list[str]:
        field_numbers: list[str] = list()

        for item in self.root.get_children():
            if item.field_data or bool(item.checkState(FieldsSpec.ColumnsOrder.PROPERTY)):
                field_numbers.append(item.field_number)

        return field_numbers

    def generate_fields(self, parent=None):
        result: TypeFields = dict()

        if parent is None:
            parent = self.root

        for row in parent.get_children():
            result[row.field_number] = self.generate_fields(row) if row.childCount() else row.field_data

            if self.config.fields.validation:
                self.validator.validate_item(row)

        if parent is self.root:
            fields = OrderedDict({k: result[k] for k in sorted(result.keys(), key=int)})

            if not self.config.fields.validation:
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

    def get_field_data(self, field_number):
        for item in self.root.get_children():

            if item.field_number != field_number:
                continue

            if item.field_data:
                return item.field_data

            if self.spec.is_field_complex([field_number]) or item.childCount():
                field_data = "".join([data.field_data for data in item.get_children()])
                field_data = f"{item.field_data}{field_data}"

                return field_data

            return item.field_data
