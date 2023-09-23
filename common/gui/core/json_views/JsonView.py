from copy import deepcopy
from logging import error, warning
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
from common.gui.constants.Colors import Colors


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
    def len_fill(self):
        return 3 if self.config.fields.validation else None

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
        self.validator = ItemsValidator(self.config)
        self.itemDoubleClicked.connect(self.edit_item)
        self.itemChanged.connect(self.process_change_item)
        self.itemChanged.connect(self.disable_next_level)
        self.currentItemChanged.connect(self.disable_next_level)
        self.setHeaderLabels(FieldsSpec.columns)
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

        if column not in (FieldsSpec.ColumnsOrder.VALUE, FieldsSpec.ColumnsOrder.LENGTH):
            return

        if column == FieldsSpec.ColumnsOrder.LENGTH and not self.config.fields.validation:
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

    def edit_item(self, item, column):
        if item is self.root:
            return

        if column not in (FieldsSpec.ColumnsOrder.FIELD, FieldsSpec.ColumnsOrder.VALUE, FieldsSpec.ColumnsOrder.LENGTH):
            return

        if column == FieldsSpec.ColumnsOrder.LENGTH and self.config.fields.validation:
            return

        if column == FieldsSpec.ColumnsOrder.VALUE:
            if item.childCount():
                return

            item.hide_secret(False)

        if column == FieldsSpec.ColumnsOrder.LENGTH and item.spec:
            return

        self.editItem(item, column)

    def generate_item_data(self, item):
        if not item.checkbox_checked(CheckBoxesDefinition.GENERATE):
            return

        item.field_data = FieldsGenerator.generate_field(item.field_number, self.config.fields.max_amount)

    def process_change_property(self, item):
        try:
            text = self.itemWidget(item, FieldsSpec.ColumnsOrder.PROPERTY).text()
        except AttributeError | ValueError:
            text = ""

        if text == CheckBoxesDefinition.JSON_MODE:
            if item.checkbox_checked(CheckBoxesDefinition.JSON_MODE):
                self.set_json_mode(item)
            else:
                self.set_flat_mode(item)

        if text == CheckBoxesDefinition.GENERATE:
            item.set_length(fill_length=self.len_fill)

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

            prefix: str = '0' * (child_length - item_length)

            if child_item.field_length.startswith(prefix):
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
                    self.validate_item(item, column)
                    item.set_item_color()

                case FieldsSpec.ColumnsOrder.PROPERTY:
                    self.generate_item_data(item)
                    self.process_change_property(item)

                case FieldsSpec.ColumnsOrder.FIELD:
                    item.set_checkbox()
                    self.check_all_items(item)

                case FieldsSpec.ColumnsOrder.LENGTH:
                    self.set_subfields_length(item)

        except ValueError as validation_error:
            item.set_item_color(Colors.RED)
            [warning(err) for err in str(validation_error).splitlines()]
            return

        if column == FieldsSpec.ColumnsOrder.PROPERTY:
            return

        self.set_item_description(item)

    @void_qt_signals
    def set_item_description(self, item: FieldItem):
        try:
            item.set_spec()
        except Exception:
            pass

        specification_found = any((item.spec, self.config.fields.validation))

        if specification_found:
            item.set_description()

        if not specification_found:
            warn_text = f"⚠ ️No specification for field {item.get_field_path(string=True)}, set field length manually"

            if not item.field_number:
                error(f"Lost field number for field {item.get_field_path(string=True)}")
                return

            item.set_description(warn_text)
            item.set_item_color(color=Colors.DEEP_RED)

        if not item.childCount():
            return

        for child in item.get_children():
            self.set_item_description(child)

    def edit_column(self, column: int):
        if column not in (FieldsSpec.ColumnsOrder.FIELD, FieldsSpec.ColumnsOrder.VALUE):
            return

        if not self.hasFocus():
            self.setFocus()

        item: FieldItem | QTreeWidgetItem

        if not (item := self.currentItem()):
            return

        self.edit_item(item, column)

    def validate_item(self, item, column=None):  # Validate single item, no auto children validate
        if not self.config.fields.validation:
            return

        if item is self.root:
            return

        if self.spec.can_be_generated(item.get_field_path()):
            if item.checkbox_checked(CheckBoxesDefinition.GENERATE):
                return

        self.validator.validate_item(item)

    def validate_items(self, parent: FieldItem):  # Validate item and child-items when the item has children
        for row in parent.get_children():
            self.validate_item(row)

            if row.childCount():
                self.validate_items(row)

    def check_all_items(self, parent: FieldItem | None = None):  # Validate and paint item without raising ValueError
        def set_error(item: FieldItem, exception: Exception):
            item.set_item_color(Colors.RED)
            warning(exception)

        if parent is None:
            parent = self.root

        try:
            self.validate_item(parent)

        except ValueError as validation_error:
            set_error(parent, validation_error)

        else:
            parent.set_item_color()

        for child_item in parent.get_children():
            if child_item.childCount():
                self.check_all_items(parent=child_item)
                continue

            try:
                self.validate_item(child_item)

            except ValueError as validation_error:
                set_error(child_item, validation_error)

            else:
                child_item.set_item_color(Colors.BLACK)

    def plus(self):
        if not (current_item := self.currentItem()):
            return

        if not (parent := current_item.parent()):
            parent = self.root

        item = FieldItem([])
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
        parent.set_length(fill_length=self.len_fill)

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
        self.clean()

        fields = deepcopy(transaction.data_fields)

        self.parse_fields(fields)
        self.set_checkboxes(transaction)
        self.make_order()
        self.hide_secrets()
        self.check_all_items()

        for item in self.root.get_children():
            if item.checkbox_checked(CheckBoxesDefinition.JSON_MODE):
                self.set_json_mode(item)
                break

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
                string_data = [field, str(field_data), None, description]
                child: FieldItem = FieldItem(string_data)

            parent.addChild(child, fill_len=self.len_fill)
            child.set_spec(field_spec)
            self.set_item_description(child)

        self.set_all_items_length()

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
            if self.config.fields.validation:
                self.validate_items(row)

            if row.childCount():
                if flat:
                    result[row.field_number] = Parser.join_complex_item(row)
                else:
                    result[row.field_number] = self.generate_fields(row, flat=flat)

            if not row.childCount():
                result[row.field_number] = row.field_data

        if parent is self.root:
            fields = {field: result[field] for field in sorted(result, key=int)}

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

    def field_has_data(self, field_number: str, parent: FieldItem | None = None):
        if parent is None:
            parent = self.root

        item: FieldItem

        for item in parent.get_children():
            if item.field_number != field_number:
                continue

            return bool(int(item.get_field_length()))

        return False
