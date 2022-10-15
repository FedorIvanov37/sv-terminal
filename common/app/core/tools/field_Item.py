from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import Qt, QVariant
from common.app.constants.MainFieldSpec import MainFieldSpec as Spec
from common.app.data_models.epay_specification import IsoField
from common.app.core.tools.item_ import AbstractItem
from logging import error


class Item(AbstractItem):
    _spec: IsoField = None
    _length: int = int()
    _field_data: str = str()
    _field_number: str = str()
    _is_field_complex: bool = False

    @property
    def is_field_complex(self):
        return self._is_field_complex

    @property
    def spec(self):
        return self._spec

    @property
    def length(self):
        return self._length

    @property
    def field_data(self):
        return self._field_data

    @property
    def field_number(self):
        return self._field_number

    @spec.setter
    def spec(self, spec: IsoField):
        self._spec: IsoField = spec

    @field_number.setter
    def field_number(self, field_number: str):
        if not field_number.isdigit():
            return

        self._field_number = str(field_number)
        path: list[str] = self.get_field_path()
        self.spec: Spec = self.epay_spec.get_field_spec(path=path)

        if self.spec is None and self.parent():
            error("No specification for field %s. Set the field length manually" % self.get_field_path(string=True))
            return

        if self.spec is not None:
            self.is_field_complex = bool(self.spec.fields)

    @field_data.setter
    def field_data(self, field_data: str):
        self._field_data: str = field_data
        self.spec: IsoField = self.epay_spec.get_field_spec(self.get_field_path())
        self.set_length()

    @length.setter
    def length(self, length):
        self._length = length

    @is_field_complex.setter
    def is_field_complex(self, is_field_complex: bool):
        self._is_field_complex: bool = is_field_complex

    def __init__(self, item_data: list[str]):
        super(Item, self).__init__(item_data)

        try:
            self.field_number = item_data[Spec.columns_order.get(Spec.FIELD)]
            self.field_data = item_data[Spec.columns_order.get(Spec.VALUE)]
        except IndexError:
            pass

        field_path = self.get_field_path()

        self.spec: IsoField = self.epay_spec.get_field_spec(field_path)

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
        column_number = Spec.columns_order.get(Spec.DESCRIPTION)
        description = self.epay_spec.get_field_description(self.get_field_path())
        self.setText(column_number, description)

    def setText(self, column: int, atext: str) -> None:
        if column == Spec.columns_order.get(Spec.FIELD):
            parent = self.parent()

            if parent and parent.spec:
                atext = atext.zfill(parent.spec.tag_length)

            self.field_number = atext

        if column == Spec.columns_order.get(Spec.VALUE):
            self.field_data = atext

        QTreeWidgetItem.setText(self, column, atext)

    def set_length(self, clear: bool = False) -> None:
        if clear:
            self.setText(2, "")
            return

        column = Spec.columns_order.get(Spec.LENGTH)
        self.length = self.get_field_length()
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
