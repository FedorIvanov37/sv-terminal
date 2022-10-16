from collections import OrderedDict
from logging import error, warning
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.constants.MainFieldSpec import MainFieldSpec as Spec
from common.app.core.tools.field_Item import Item
from common.app.data_models.message import Message
from common.app.data_models.message import TypeFields


class JsonView(QObject):
    root: Item = Item(["Message"])
    item_changed = pyqtSignal()
    _spec = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    def __init__(self, tree: QTreeWidget, spec=None):
        super(JsonView, self).__init__()
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
        self.tree.itemChanged.connect(self.process_change_item)
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
        self.item_changed.emit()

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
        self.item_changed.emit()

    def clean(self):
        self.root.takeChildren()
        self.root.set_length()

    def process_change_item(self, item: Item, column: int):
        if item is self.root:
            self.root.setText(0, "Message")  # TODO
            self.root.setText(1, "")  # TODO
            return

        if item.spec:
            item.set_length()

        self.resize_all()

        if not item.text(column):
            return

        if column == 0:  # TODO
            item.setText(column, item.text(column))
            item.set_description()
            item.set_checkbox()

        if column == 1:  # TODO
            item.setText(column, item.text(column))

        self.item_changed.emit()

    def set_field_value(self, field, value):
        column = 1  # TODO

        for item in self.root.get_children():
            if item.field_number == field:
                item.setText(column, value)
                break

    def parse_message(self, message: Message) -> None:
        self.clean()
        self.parse_fields(message.transaction.fields)

        for item in self.root.get_children():
            field = item.text(int())

            if field not in Spec.generated_fields:
                continue

            item.set_checkbox(checked=field in message.config.generate_fields)

        self.make_order()

    def parse_fields(self, input_json: dict, parent: QTreeWidgetItem = None, specification=None):
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
                child.set_length()

            else:
                child = Item([field])
                child.setText(3, description)  # TODO
                self.parse_fields(field_data, parent=child, specification=specification.fields.get(field))

            parent.addChild(child)

    def edit(self, item: Item, column: int):
        if item is self.root:
            return

        self.tree.setCurrentItem(item)
        item.set_spec()

        if item.childCount():
            if column == 0:  # TODO
                self.tree.editItem(item, column)

            return

        if column in (1, 0):  # TODO
            self.tree.editItem(item, column)

    def resize_all(self):
        for column in range(self.tree.columnCount()):
            self.tree.resizeColumnToContents(column)

    def make_order(self):
        self.tree.collapseAll()
        self.tree.expandToDepth(-1)
        self.resize_all()

    def generate_fields(self, parent=None, validation: bool = False):
        result: TypeFields = dict()
        checked_boxes = self.get_checkboxes()

        if parent is None:
            parent = self.root

        row: Item

        for row in parent.get_children():
            field_number: str = row.field_number
            row.set_spec()

            if not field_number:
                continue

            if field_number in result and validation:
                error("Parsing error: field %s set twice or more" % field_number)
                return

            if row.childCount():
                result[field_number] = self.generate_fields(row, validation=validation)
            else:
                if row.text(1) or row.field_number in checked_boxes:
                    result[field_number] = row.text(1)

            if not row.text(2) and validation:
                warning("Parsing error: No specification for field %s" % row.get_field_path(string=True))
                warning("You have to set the length for the field manually before sending or change the \
                                  specification file: /common/settings/specification.json")

        if parent is self.root:
            return OrderedDict({k: result[k] for k in sorted(result.keys(), key=int)})

        return result

    def get_checkboxes(self) -> list:
        result = set()

        for item in self.root.get_children():
            checked = bool(item.checkState(4))

            if checked:
                result.add(item.field_number)

        return list(result)
