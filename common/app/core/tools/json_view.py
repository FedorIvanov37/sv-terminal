from collections import OrderedDict
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.constants.MainFieldSpec import MainFieldSpec as Spec
from common.app.core.tools.field_Item import Item
from common.app.data_models.message import TypeFields
from common.app.data_models.transaction import Transaction
from common.app.core.tools.validator import Validator


class JsonView(QTreeWidget):
    _spec: EpaySpecification = EpaySpecification()
    _root: Item = Item(["Message"])

    @property
    def spec(self):
        return self._spec

    @property
    def root(self):
        return self._root

    def __init__(self):
        super(JsonView, self).__init__()
        self.setup()

    def setup(self):
        for action in (self.itemCollapsed, self.itemExpanded, self.itemChanged):
            action.connect(self.resize_all)

        self.itemDoubleClicked.connect(self.edit_item)
        self.setFont(QFont("Calibri", 12))
        self.setAllColumnsShowFocus(True)
        self.setAlternatingRowColors(True)
        self.setHeaderLabels(Spec.columns)
        self.setEditTriggers(self.NoEditTriggers)
        self.addTopLevelItem(self.root)
        self.make_order()

    def plus(self):
        item = Item([])
        current_item = self.currentItem()
        parent = self.currentItem().parent()

        if parent is None:
            parent = self.root

        index = parent.indexOfChild(current_item) + 1
        parent.insertChild(index, item)
        self.setCurrentItem(item)
        self.scrollToItem(item)
        self.setFocus()
        self.editItem(item, int())  # TODO

    def minus(self):
        item: Item | QTreeWidgetItem = self.currentItem()

        if item is self.root:
            self.setCurrentItem(self.root)
            self.setFocus()
            return

        parent: Item = item.parent()
        parent.takeChild(parent.indexOfChild(item))
        parent.set_length()
        self.setFocus()

    def next_level(self):
        item = Item([])
        current_item: Item | None = self.currentItem()

        if current_item is None:
            return

        self.currentItem().setText(1, str())
        self.currentItem().insertChild(0, item)
        self.setCurrentItem(item)
        self.scrollToItem(item)
        self.setFocus()
        self.editItem(item, int())

    def clean(self):
        self.root.takeChildren()
        self.root.set_length()

    def set_field_value(self, field, value):
        column = 1  # TODO

        for item in self.root.get_children():
            if item.field_number == field:
                item.setText(column, value)
                break

    def edit_item(self, item, column):
        if item is self.root:
            return

        if item.get_children():
            return

        if column not in (Spec.columns_order.get(Spec.FIELD), Spec.columns_order.get(Spec.VALUE)):
            return
        
        self.editItem(item, column)

    def parse_transaction(self, transaction: Transaction) -> None:
        self.clean()
        self._parse_fields(transaction.data_fields)
        self.set_checkboxes(transaction)
        self.make_order()

    def set_checkboxes(self, transaction: Transaction):
        for item in self.root.get_children():
            if item.field_number not in Spec.generated_fields:
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

            if isinstance(field_data, str):
                string_data = [field, field_data, None, description]
                child: Item = Item(string_data)
                self.itemChanged.connect(child.process_change_item)

            else:
                child = Item([field])
                child.setText(3, description)  # TODO
                self._parse_fields(field_data, parent=child, specification=specification.fields.get(field))

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
            if item.field_data or item.checkState(Spec.columns_order.get(Spec.PROPERTY)):
                field_numbers.append(item.field_number)

        return field_numbers

    def generate_fields(self, parent=None):
        result: TypeFields = dict()
        validator = Validator()

        if parent is None:
            parent = self.root

        for row in parent.get_children():
            validator.validate_field_item(row)
            result[row.field_number] = self.generate_fields(row) if row.childCount() else row.field_data

        if parent is self.root:
            return OrderedDict({k: result[k] for k in sorted(result.keys(), key=int)})

        return result

    def get_checkboxes(self) -> list:
        column = Spec.columns_order.get(Spec.PROPERTY)
        return [item.field_number for item in self.root.get_children() if item.checkState(column)]

    def get_field_set(self):
        field_set = [field.field_number for field in self.root.get_children() if field.field_data]
        field_set = field_set + self.get_checkboxes()
        return field_set
