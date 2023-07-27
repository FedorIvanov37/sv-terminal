from PyQt6 import QtGui
from PyQt6.QtWidgets import QTreeWidgetItem
from common.gui.constants.MainFieldSpec import MainFieldSpec as FieldsSpec
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.gui.core.AbstractItem import AbstractItem
from common.gui.constants.CheckBoxesDefinition import CheckBoxesDefinition
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.toolkit.toolkit import mask_pan
from typing import Callable


class Item(AbstractItem):
    epay_spec: EpaySpecification = EpaySpecification()
    spec: IsoField = None
    pan = ""

    def void_tree_signals(function: Callable):
        def wrapper(self, *args, **kwargs):
            try:
                self.treeWidget().blockSignals(True)
            except AttributeError:
                pass

            function(self, *args, **kwargs)

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
            self.pan = self.field_data
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

        if not (pan := self.field_data):
            return

        mask = mask_pan(pan)
        self.setText(FieldsSpec.ColumnsOrder.VALUE, mask)
        self.pan = pan

    def generate_checkbox_checked(self):
        if self.field_number not in FieldsSpec.generated_fields:
            return False

        return bool(self.checkState(FieldsSpec.ColumnsOrder.PROPERTY).value)

    def flat_mode_checkbox_checked(self):
        if not self.epay_spec.is_field_complex(self.get_field_path()):
            return False

        return bool(self.checkState(FieldsSpec.ColumnsOrder.PROPERTY).value)

    @void_tree_signals
    def set_checkbox(self, checked=True):
        if self.get_field_depth() != 1:
            return

        column_number = FieldsSpec.ColumnsOrder.PROPERTY
        state = CheckBoxesDefinition.CHECKED if checked else CheckBoxesDefinition.UNCHECKED

        if self.field_number in FieldsSpec.generated_fields:
            self.setCheckState(column_number, state)
            self.setText(column_number, CheckBoxesDefinition.GENERATE)

        if self.epay_spec.is_field_complex(self.get_field_path()):
            self.setCheckState(column_number, state)
            self.setText(column_number, CheckBoxesDefinition.FLAT_MODE)

    def process_change_item(self):
        self.set_spec()
        self.set_item_color()
        self.set_length()
        self.set_description()

    @void_tree_signals
    def set_description(self):
        if not self.spec:
            return

        self.setText(FieldsSpec.ColumnsOrder.DESCRIPTION, self.spec.description)

    @void_tree_signals
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

    @void_tree_signals
    def set_item_color(self, red=False):
        color = "#ff0000" if red else "#000000"

        for column in range(self.columnCount()):
            self.setForeground(column, QtGui.QBrush(QtGui.QColor(color)))
