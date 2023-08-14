from PyQt6 import QtGui
from PyQt6.QtWidgets import QTreeWidgetItem
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.lib.toolkit.toolkit import mask_pan, mask_secret
from common.lib.core.EpaySpecification import EpaySpecification
from common.gui.constants.MainFieldSpec import MainFieldSpec as FieldsSpec
from common.gui.core.AbstractItem import AbstractItem
from common.gui.constants.CheckBoxesDefinition import CheckBoxesDefinition
from common.gui.decorators.void_qt_signals import void_tree_signals


class Item(AbstractItem):
    epay_spec: EpaySpecification = EpaySpecification()
    spec: IsoField = None
    _secret: str = ""
    _masked: bool = False

    @property
    def masked(self):
        return self._masked

    @masked.setter
    def masked(self, masked):
        self._masked = masked

    @property
    def field_data(self):
        if self.is_secret and self._secret:
            return self._secret

        return self.text(FieldsSpec.ColumnsOrder.VALUE)

    @field_data.setter
    def field_data(self, field_data):
        self.setText(FieldsSpec.ColumnsOrder.VALUE, field_data)
        self._secret = ""
        self.hide_secret()

    @property
    def field_number(self):
        return self.text(FieldsSpec.ColumnsOrder.FIELD)

    @property
    def is_secret(self):
        if not (spec := self.epay_spec.get_field_spec(self.get_field_path())):
            spec = self.spec

        return spec and spec.is_secret

    def __init__(self, item_data: list[str], spec=None):
        super(Item, self).__init__(item_data)
        self.spec = spec if spec else self.spec

    def addChild(self, item):
        item.spec = self.epay_spec.get_field_spec(item.get_field_path())
        QTreeWidgetItem.addChild(self, item)
        item.set_length()

    def set_spec(self, spec: IsoField | None = None):
        if not spec:
            self.spec: IsoField = self.epay_spec.get_field_spec(self.get_field_path())

        self.spec = spec

    def hide_secret(self, hide_the_secret: bool | None = None):
        if self.treeWidget() and not self.treeWidget().hide_secret_fields:
            if self.field_number != self.epay_spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
                hide_the_secret = False

        if hide_the_secret is None:
            hide_the_secret = self.is_secret

        if hide_the_secret:
            self.mask_secret_value()

        if not hide_the_secret:
            self.show_secret_value()

    @void_tree_signals
    def mask_secret_value(self):
        secret = self.field_data

        if self.field_number == self.epay_spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
            mask = mask_pan(secret)
        else:
            mask = mask_secret(secret)

        self.setText(FieldsSpec.ColumnsOrder.VALUE, mask)
        self._secret = secret
        self.masked = True

    @void_tree_signals
    def show_secret_value(self):
        if not self.masked:
            return

        self.setText(FieldsSpec.ColumnsOrder.VALUE, self._secret)
        self._secret = ""
        self.masked = False

    def generate_checkbox_checked(self):
        if self.field_number not in FieldsSpec.generated_fields:
            return False

        return bool(self.checkState(FieldsSpec.ColumnsOrder.PROPERTY).value)

    def json_mode_checkbox_checked(self):
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
            self.setText(column_number, CheckBoxesDefinition.JSON_MODE)

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
