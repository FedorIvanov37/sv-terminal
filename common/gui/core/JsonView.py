from typing import Callable
from logging import warning
from collections import OrderedDict
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTreeWidgetItem, QTreeWidget, QItemDelegate
from common.gui.constants.MainFieldSpec import MainFieldSpec as FieldsSpec
from common.gui.core.FIeldItem import Item
from common.gui.core.ItemsValidator import ItemsValidator
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.Transaction import Transaction, TypeFields
from common.lib.data_models.Config import Config
from common.lib.core.FieldsGenerator import FieldsGenerator
from PyQt6.QtCore import pyqtSignal


class JsonView(QTreeWidget):
    field_removed: pyqtSignal = pyqtSignal()
    field_changed: pyqtSignal = pyqtSignal()
    field_added: pyqtSignal = pyqtSignal()

    root: Item = Item(["Message"])
    spec: EpaySpecification = EpaySpecification()

    def void_qt_signals(function: Callable):
        #  The decorator switches off field data validation and helps to avoid the recursive effects
        #  while the field data changes automatically

        def wrapper(self, *args):
            self.blockSignals(True)
            function(self, *args)
            self.blockSignals(False)

        return wrapper

    def __init__(self, config: Config):
        super(JsonView, self).__init__()
        self.config: Config = config
        self._setup()
        self.delegate = QItemDelegate()
        self.delegate.closeEditor.connect(self.hide_pan_after_edit)
        self.setItemDelegate(self.delegate)

    def hide_pan_after_edit(self):  # TODO
        child: Item

        for child in self.root.get_children():
            if not child.field_number == self.spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
                continue

            child.hide_pan(True)

    def _setup(self):
        self.setTabKeyNavigation(True)

        for action in (self.itemCollapsed, self.itemExpanded, self.itemChanged):
            action.connect(self.resize_all)

        self.validator = ItemsValidator(self.config)
        self.itemDoubleClicked.connect(self.edit_item)
        self.itemChanged.connect(self.process_change_item)
        self.setFont(QFont("Calibri", 12))
        self.setAllColumnsShowFocus(True)
        self.setAlternatingRowColors(True)
        self.setHeaderLabels(FieldsSpec.columns)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.addTopLevelItem(self.root)
        self.make_order()

    @void_qt_signals
    def process_change_item(self, item: Item, column=None):
        if item is self.root:
            return

        if column is None:
            item.hide_pan()
            return

        if column in (FieldsSpec.ColumnsOrder.PROPERTY, FieldsSpec.ColumnsOrder.VALUE):
            if item.generate_checkbox_checked():
                item.field_data = FieldsGenerator.generate_field(item.field_number, self.config.fields.max_amount)

        try:
            item.process_change_item()
        except LookupError as spec_error:
            item.set_item_color(red=True)
            warning(spec_error)
            return

        if column == FieldsSpec.ColumnsOrder.FIELD:
            item.set_checkbox()

        if column in (FieldsSpec.ColumnsOrder.VALUE, FieldsSpec.ColumnsOrder.FIELD):
            item.hide_pan(True)

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

        item: Item | QTreeWidgetItem

        if not (item := self.currentItem()):
            return

        self.edit_item(item, column)

    def validate(self, item, column=None):
        if not self.config.fields.validation:
            return

        if self.spec.can_be_generated(item.get_field_path()) and item.generate_checkbox_checked():
            return

        if column == FieldsSpec.ColumnsOrder.FIELD:
            if all((item.field_number, not item.field_data, not item.childCount())):
                self.validator.validate_field_path(item.get_field_path())
                self.validator.validate_duplicates(item)
                return

        self.validator.validate_item(item)

    def plus(self):
        item = Item([])
        parent = None

        if current_item := self.currentItem():
            if not (parent := current_item.parent()):
                parent = self.root

        index = parent.indexOfChild(current_item) + 1
        parent.insertChild(index, item)
        self.set_new_item(item)
        self.field_added.emit()

    @void_qt_signals
    def minus(self, checked=None):
        item: Item | QTreeWidgetItem

        if not (item := self.currentItem()):
            return

        if item is self.root:
            self.setFocus()
            return

        parent: Item = item.parent()
        removed_item_index = parent.indexOfChild(item)
        removed_item: Item = parent.takeChild(removed_item_index)
        cursor_position = removed_item_index if removed_item_index == 0 else removed_item_index - 1
        parent.set_length()

        if not (new_position_item := parent.child(cursor_position)):
            new_position_item = parent

        self.setCurrentItem(new_position_item)
        self.check_duplicates_after_remove(removed_item, parent)
        self.setFocus()
        self.field_removed.emit()

    def next_level(self, checked=None):
        item = Item([])
        current_item: Item | None = self.currentItem()

        if current_item is None:
            return

        self.currentItem().setText(FieldsSpec.ColumnsOrder.VALUE, str())
        self.currentItem().insertChild(int(), item)
        self.set_new_item(item)

    def set_new_item(self, item: Item):
        self.setCurrentItem(item)
        self.scrollToItem(item)
        self.setFocus()
        self.editItem(item, int())

    def check_duplicates_after_remove(self, removed_item: Item, parent_item: Item):
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

    @void_qt_signals
    def clean(self):
        self.root.takeChildren()
        self.root.set_length()

    @void_qt_signals
    def set_field_value(self, field, value):
        for item in self.root.get_children():
            if item.field_number != field:
                continue

            item.setText(FieldsSpec.ColumnsOrder.VALUE, value)
            return

    def edit_item(self, item, column):
        if item is self.root:
            return

        if item.get_children():
            return

        if column not in (FieldsSpec.ColumnsOrder.FIELD, FieldsSpec.ColumnsOrder.VALUE):
            return

        if column == FieldsSpec.ColumnsOrder.VALUE:
            item.hide_pan(False)

        self.editItem(item, column)

    def parse_transaction(self, transaction: Transaction) -> None:
        self.clean()
        self._parse_fields(transaction.data_fields)
        self.set_checkboxes(transaction)
        self.make_order()

    @void_qt_signals
    def set_checkboxes(self, transaction: Transaction):
        for item in self.root.get_children():
            if item.field_number not in FieldsSpec.generated_fields:
                continue

            item.set_checkbox(item.field_number in transaction.generate_fields)

    def _parse_fields(self, input_json: dict, parent: QTreeWidgetItem = None, specification=None):
        if parent is None:
            parent = self.root

        if specification is None:
            specification = self.spec.spec

        for field, field_data in input_json.items():
            field_spec = specification.fields.get(field)
            description = field_spec.description if field_spec else None

            if isinstance(field_data, dict):
                child = Item([field])
                child.setText(3, description)  # TODO
                self._parse_fields(field_data, parent=child, specification=specification.fields.get(field))

            else:
                string_data = [field, str(field_data), None, description]
                child: Item = Item(string_data)

            parent.addChild(child)

    def resize_all(self):
        for column in range(self.columnCount()):
            self.resizeColumnToContents(column)

    def make_order(self):
        self.collapseAll()
        self.expandToDepth(-1)
        self.resize_all()

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
            self.validator.validate_item(row)
            result[row.field_number] = self.generate_fields(row) if row.childCount() else row.field_data

        if parent is self.root:
            fields = OrderedDict({k: result[k] for k in sorted(result.keys(), key=int)})
            self.validator.validate_fields(fields)
            return fields

        return result

    def get_checkboxes(self) -> list:
        column = FieldsSpec.ColumnsOrder.PROPERTY
        return [item.field_number for item in self.root.get_children() if bool(item.checkState(column).value)]

    def get_field_set(self):
        field_set = [field.field_number for field in self.root.get_children() if field.field_data]
        field_set = field_set + self.get_checkboxes()
        return field_set

    def get_field_data(self, field_number):
        for item in self.root.get_children():

            if item.field_number != field_number:
                continue

            if item.field_data:
                return item.field_data

            if self.spec.is_field_complex([field_number]) or item.get_children():
                field_data = "".join([data.field_data for data in item.get_children()])
                field_data = f"{item.field_data}{field_data}"

                return field_data

            return item.field_data
