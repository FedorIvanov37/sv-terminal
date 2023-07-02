from PyQt6 import QtGui
from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtCore import Qt, QVariant, pyqtSignal
from common.gui.constants.MainFieldSpec import MainFieldSpec as Spec
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.gui.core.AbstractItem import AbstractItem


class Item(AbstractItem):
    spec: IsoField = None
    _field_data: str = str()

    @property
    def field_data(self):
        return self.text(Spec.columns_order.get(Spec.VALUE))

    @property
    def field_number(self):
        return self.text(Spec.columns_order.get(Spec.FIELD))

    def __init__(self, item_data: list[str]):
        super(Item, self).__init__(item_data)
        field_path = self.get_field_path()
        self.spec: IsoField = self.epay_spec.get_field_spec(field_path)

    def addChild(self, item):
        item.spec = self.epay_spec.get_field_spec(item.get_field_path())
        QTreeWidgetItem.addChild(self, item)
        item.set_length()

    def set_spec(self):
        self.spec: IsoField = self.epay_spec.get_field_spec(self.get_field_path())

    def generate_checkbox_checked(self):
        return bool(self.checkState(Spec.columns_order.get(Spec.PROPERTY)).value)

    def set_checkbox(self, checked=True):
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

    def process_change_item(self):
        self.set_item_color()
        self.set_spec()
        self.set_length()
        self.set_description()

    def set_length(self) -> None:
        column = Spec.columns_order.get(Spec.LENGTH)
        length = f"{self.get_field_length():03}"
        self.setText(column, length)

        if self.parent() is not None:
            self.parent().set_length()

    def get_field_length(self):
        column = Spec.columns_order.get(Spec.VALUE, 1)

        if self.childCount():
            length = sum([item.get_field_length() for item in self.get_children()])
        else:
            length = len(self.text(column))

        return length

    def set_item_color(self, red=False):
        color = "#ff0000" if red else "#000000"

        for column in range(self.columnCount()):
            self.setForeground(column, QtGui.QBrush(QtGui.QColor(color)))
