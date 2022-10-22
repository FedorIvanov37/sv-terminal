from collections import OrderedDict
from logging import error, warning
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.constants.MainFieldSpec import MainFieldSpec as Spec
from common.app.core.tools.field_Item import Item
from common.app.data_models.message import Message
from common.app.data_models.message import TypeFields
from common.app.data_models.config import Config


class JsonView(QObject):
    _spec: EpaySpecification = EpaySpecification()
    root: Item = Item(["Message"])

    @property
    def spec(self):
        return self._spec

    def __init__(self, config: Config, tree: QTreeWidget, spec=None):
        super(JsonView, self).__init__()
        self.config = config
        self.tree: QTreeWidget = tree
        self.setup(spec)

    def setup(self, spec):
        if spec is None:
            spec = Spec

        self.tree.setHeaderLabels(spec.columns)
        self.tree.addTopLevelItem(self.root)
        self.tree.itemCollapsed.connect(lambda _: self.resize_all())
        self.tree.itemExpanded.connect(lambda _: self.resize_all())
        self.tree.itemDoubleClicked.connect(lambda item, column: self.edit(item, column))
        self.tree.itemChanged.connect(self.resize_all)
        self.tree.setFocusPolicy(Qt.StrongFocus)
        self.make_order()

    def plus(self):
        item = Item([])
        current_item = self.tree.currentItem()

        if current_item is None:
            current_item = self.root

        if current_item.parent() is not None:
            current_item = current_item.parent()

        current_item.insertChild(self.tree.currentIndex().row() + 1, item)
        self.tree.scrollToItem(item)
        self.edit(item, 0)  # TODO

    def minus(self):
        item = self.tree.currentItem()

        if item is None:
            return

        if item is self.root:
            self.tree.setCurrentItem(self.root)
            self.tree.setFocus()
            return

        self.tree.previousInFocusChain()
        self.tree.setFocus()
        parent: Item | QTreeWidgetItem = item.parent()
        parent.takeChild(parent.indexOfChild(item))
        parent.set_length()

    def next_level(self):
        item = Item([])
        current_item: Item = self.tree.currentItem()

        if current_item is None:
            return

        if current_item.parent() is self.root:
            try:
                if current_item.spec.fields is None:
                    error("Field has no sub-fields")
                    self.tree.setCurrentItem(current_item)
                    self.tree.setFocus()
                    return
            except AttributeError:
                pass

        self.tree.currentItem().setText(1, str())
        self.tree.currentItem().addChild(item)
        self.tree.setCurrentItem(item)
        self.edit(item, int())

    def clean(self):
        self.root.takeChildren()
        self.root.set_length()

    def set_field_value(self, field, value):
        column = 1  # TODO

        for item in self.root.get_children():
            if item.field_number == field:
                item.setText(column, value)
                break

    def parse_message(self, message: Message) -> None:
        self.clean()
        self._parse_fields(message.transaction.fields)
        self.set_checkboxes(message)
        self.make_order()

    def set_checkboxes(self, message):
        for item in self.root.get_children():
            if item.field_number not in Spec.generated_fields:
                continue

            item.set_checkbox(item.field_number in message.config.generate_fields)

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
                self.tree.itemChanged.connect(child.process_change_item)
                child.set_length()

            else:
                child = Item([field])
                child.setText(3, description)  # TODO
                self._parse_fields(field_data, parent=child, specification=specification.fields.get(field))

            parent.addChild(child)

    def edit(self, item: Item, column: int):
        if item is self.root:
            return

        self.tree.setCurrentItem(item)

        if column in (1, 0):  # TODO
            self.tree.editItem(item, column)

    def resize_all(self):
        for column in range(self.tree.columnCount()):
            self.tree.resizeColumnToContents(column)

    def make_order(self):
        self.tree.collapseAll()
        self.tree.expandToDepth(-1)
        self.resize_all()

    def generate_fields(self, parent=None):
        result: TypeFields = dict()

        if parent is None:
            parent = self.root

        row: Item

        for row in parent.get_children():
            field_number: str = row.field_number
            field_data: str = row.field_data

            if not field_number:
                warning(f"Lost field number. The field will not be sent")
                continue

            if not field_number.isdigit():
                raise ValueError(f"Error: non-numeric field number found: {row.get_field_path(string=True)}")

            if field_number in result:
                raise ValueError(f"Error: duplicated field number {row.get_field_path(string=True)} found")

            if not field_data and field_number not in self.get_checkboxes() and not row.get_children():
                warning(f"No value for field {field_number}. The field will not be sent")
                continue

            result[field_number] = self.generate_fields(row) if row.childCount() else field_data

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
