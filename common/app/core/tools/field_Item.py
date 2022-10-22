from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import Qt, QVariant, pyqtSignal
from PyQt5 import QtGui
from common.app.constants.MainFieldSpec import MainFieldSpec as Spec
from common.app.data_models.epay_specification import IsoField
from common.app.core.tools.abstract_item import AbstractItem
from common.app.core.tools.validator import Validator
from logging import warning


class Item(AbstractItem):
    _spec: IsoField = None
    _length: int = int()
    _field_data: str = str()
    _field_number: str = str()
    _is_field_complex: bool = False
    _validator: Validator = None
    _data_was_set: pyqtSignal = pyqtSignal()

    @property
    def data_was_set(self):
        return self._data_was_set

    @property
    def is_field_complex(self):
        return self._is_field_complex

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

    @is_field_complex.setter
    def is_field_complex(self, is_field_complex: bool):
        self._is_field_complex: bool = is_field_complex

    def __init__(self, item_data: list[str]):
        super(Item, self).__init__(item_data)
        field_path = self.get_field_path()
        self.spec: IsoField = self.epay_spec.get_field_spec(field_path)
        self._validator = Validator()

    def validate(self):
        self._validator.validate_field(self.get_field_path(), self.field_data)

    def addChild(self, item):
        item.spec = self.epay_spec.get_field_spec(item.get_field_path())
        QTreeWidgetItem.addChild(self, item)
        item.set_length()

    def set_spec(self):
        self.spec: IsoField = self.epay_spec.get_field_spec(self.get_field_path())

    def set_checkbox(self, checked=True):
        column_number = Spec.columns_order.get(Spec.PROPERTY)

        if self.field_number not in Spec.generated_fields:
            self.setData(column_number, Qt.ItemDataRole.CheckStateRole, QVariant())
            self.setText(column_number, str())
            return

        if self.get_field_depth() != 1:
            return

        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        self.setCheckState(column_number, state)
        self.setText(column_number, Spec.GENERATE)

    def set_description(self):
        if not self.spec:
            return

        self.setText(Spec.columns_order.get(Spec.DESCRIPTION), self.spec.description)

    def setData(self, column: int, role: int, value) -> None:
        QTreeWidgetItem.setData(self, column, role, value)

        if column not in (Spec.columns_order.get(Spec.FIELD), Spec.columns_order.get(Spec.VALUE)):
            return

        if role == Qt.ForegroundRole:
            return

        text_color_red = False

        try:
            self.validate()
        except (TypeError, ValueError) as validation_error:
            warning(validation_error)
            text_color_red = True

        self.set_item_color(red=text_color_red)
        self.process_change_item()

    def process_change_item(self):
        self.set_spec()
        self.set_length()
        self.set_description()

    def set_length(self) -> None:
        column = Spec.columns_order.get(Spec.LENGTH)
        length = str(self.length).zfill(3)
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
