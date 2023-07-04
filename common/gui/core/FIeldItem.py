from PyQt6 import QtGui
from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtCore import Qt, QVariant
from common.gui.constants.MainFieldSpec import MainFieldSpec as FieldsSpec
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.gui.core.AbstractItem import AbstractItem
from common.lib.core.EpaySpecification import EpaySpecification
from typing import Callable


class Item(AbstractItem):
    epay_spec: EpaySpecification = EpaySpecification()
    spec: IsoField = None
    pan = ""

    def void_tree_signals(function: Callable):
        def wrapper(self, *args):
            try:
                self.treeWidget().blockSignals(True)
            except AttributeError:
                pass

            function(self, *args)

            try:
                self.treeWidget().blockSignals(False)
            except AttributeError:
                pass

        return wrapper

    @property
    def field_data(self):
        if self.field_number == self.epay_spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
            return self.pan if self.pan else self.text(FieldsSpec.ColumnsOrder.VALUE)

        return self.text(FieldsSpec.ColumnsOrder.VALUE)

    @field_data.setter
    def field_data(self, field_data):
        self.setText(FieldsSpec.ColumnsOrder.VALUE, field_data)

    @property
    def field_number(self):
        return self.text(FieldsSpec.ColumnsOrder.FIELD)

    def __init__(self, item_data: list[str]):
        super(Item, self).__init__(item_data)
        field_path = self.get_field_path()
        self.spec: IsoField = self.epay_spec.get_field_spec(field_path)

        if self.field_number == self.epay_spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
            self.hide_pan(True)

    def addChild(self, item):
        item.spec = self.epay_spec.get_field_spec(item.get_field_path())
        QTreeWidgetItem.addChild(self, item)
        item.set_length()

    def set_spec(self):
        self.spec: IsoField = self.epay_spec.get_field_spec(self.get_field_path())

    @void_tree_signals
    def hide_pan(self, hide=True):
        if not self.field_number == self.epay_spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
            return

        if not hide:
            self.setText(FieldsSpec.ColumnsOrder.VALUE, self.pan)
            self.pan = ""
            return

        pan = self.field_data
        mask = self.mask_pan(pan)
        self.setText(FieldsSpec.ColumnsOrder.VALUE, mask)
        self.pan = pan

    def generate_checkbox_checked(self):
        return bool(self.checkState(FieldsSpec.ColumnsOrder.PROPERTY).value)

    def mask_pan(self, pan: str):
        if len(pan) < 10:
            return pan

        return f"{pan[:6]}******{pan[-4:]}"

    def set_checkbox(self, checked=True):
        column_number = FieldsSpec.ColumnsOrder.PROPERTY

        if self.field_number not in FieldsSpec.generated_fields:
            self.setData(column_number, Qt.ItemDataRole.CheckStateRole, QVariant())
            self.setText(column_number, str())
            return

        if self.get_field_depth() != 1:
            return

        self.setCheckState(column_number, Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)
        self.setText(column_number, "Generate")

    def set_description(self):
        if not self.spec:
            return

        self.setText(FieldsSpec.ColumnsOrder.DESCRIPTION, self.spec.description)

    def process_change_item(self):
        self.set_spec()
        self.set_item_color()
        self.set_length()
        self.set_description()

    def set_length(self) -> None:
        column = FieldsSpec.ColumnsOrder.LENGTH
        length = f"{self.get_field_length():03}"
        self.setText(column, length)

        if self.parent() is not None:
            self.parent().set_length()

    def get_field_length(self):
        if self.childCount():
            length = sum([item.get_field_length() for item in self.get_children()])
        else:
            length = len(self.field_data)

        return length

    def set_item_color(self, red=False):
        color = "#ff0000" if red else "#000000"

        for column in range(self.columnCount()):
            self.setForeground(column, QtGui.QBrush(QtGui.QColor(color)))
