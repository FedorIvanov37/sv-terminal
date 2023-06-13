from PyQt6 import QtGui
from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtCore import Qt, QVariant, pyqtSignal
from common.gui.constants.MainFieldSpec import MainFieldSpec as Spec
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.gui.core.AbstractItem import AbstractItem


class Item(AbstractItem):
    _spec: IsoField = None
    _length: int = int()
    _field_data: str = str()
    _field_number: str = str()
    _is_field_complex: bool = False
    _data_was_set: pyqtSignal = pyqtSignal()
    _value: str = ""

    @property
    def is_secret(self):
        if not self.spec:
            return False

        return self.spec.is_secret

    @property
    def data_was_set(self):
        return self._data_was_set

    @property
    def is_field_complex(self):
        if not self.spec:
            return False

        return bool(self.spec.fields)

    @property
    def spec(self):
        return self._spec

    @property
    def length(self):
        return self.get_field_length()

    @property
    def field_data(self):
        return self.text(Spec.columns_order.get(Spec.VALUE))

    @property
    def field_number(self):
        return self.text(Spec.columns_order.get(Spec.FIELD))

    @spec.setter
    def spec(self, spec: IsoField):
        self._spec: IsoField = spec

    # @is_field_complex.setter
    # def is_field_complex(self, is_field_complex: bool):
    #     self._is_field_complex: bool = is_field_complex

    def __init__(self, item_data: list[str]):
        super(Item, self).__init__(item_data)
        field_path = self.get_field_path()
        self.spec: IsoField = self.epay_spec.get_field_spec(field_path)

    def is_duplicated(self):
        root = self.treeWidget().root
        path = self.get_field_path()

        for field in path:
            if [item.field_number for item in root.get_children()].count(field) > 1:
                return True

            root = [item for item in root.get_children() if item.field_number == field][0]

        return False

    def addChild(self, item):
        item.spec = self.epay_spec.get_field_spec(item.get_field_path())
        QTreeWidgetItem.addChild(self, item)
        item.set_length()

    def set_spec(self):
        self.spec: IsoField = self.epay_spec.get_field_spec(self.get_field_path())

    def generate_checkbox_checked(self):
        return bool(self.checkState(Spec.columns_order.get(Spec.PROPERTY)).value)

    def set_checkbox(self, checked):
        column_number = Spec.columns_order.get(Spec.PROPERTY)

        if self.field_number not in Spec.generated_fields:
            self.setData(column_number, Qt.ItemDataRole.CheckStateRole, QVariant())
            self.setText(column_number, str())
            return

        if self.get_field_depth() != 1:
            return

        self.setCheckState(column_number, Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)
        self.setText(column_number, Spec.GENERATE)

    def set_description(self):
        if not self.spec:
            return

        self.setText(Spec.columns_order.get(Spec.DESCRIPTION), self.spec.description)

    def setData(self, column: int, role: int, value) -> None:
        QTreeWidgetItem.setData(self, column, role, value)

        if column not in (Spec.columns_order.get(Spec.FIELD), Spec.columns_order.get(Spec.VALUE)):
            return

        if role == Qt.ItemDataRole.ForegroundRole:
            return

        self.treeWidget().validate(self)
        self.process_change_item(column)

    def process_change_item(self, column: int | None = None):
        self.set_spec()
        self.set_length()
        self.set_description()

        if column == Spec.columns_order.get(Spec.FIELD):
            self.set_checkbox(self.field_number in Spec.generated_fields)

    def set_length(self) -> None:
        column = Spec.columns_order.get(Spec.LENGTH)
        length = f"{self.length:03}"
        self.setText(column, length)

        if self.parent() is not None:
            self.parent().set_length()

    def get_field_length(self):
        column = Spec.columns_order.get(Spec.VALUE, 1)

        if self.childCount():
            length = sum([item.length for item in self.get_children()])
        else:
            length = len(self.text(column))

        return length

    def set_item_color(self, red=True):
        color = "#ff0000" if red else "#000000"

        for column in range(self.columnCount()):
            self.setForeground(column, QtGui.QBrush(QtGui.QColor(color)))
