from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidgetItem
from common.lib.data_models.Types import FieldPath
from common.lib.core.EpaySpecification import EpaySpecification
from common.gui.decorators.void_qt_signals import void_tree_signals
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.gui.constants.Colors import Colors


class Item(QTreeWidgetItem):
    _field_number: str = None
    _epay_spec = EpaySpecification()

    @property
    def epay_spec(self):
        return self._epay_spec

    @property
    def field_number(self):
        return self._field_number

    def __init__(self, item_data: list[str]):
        super(Item, self).__init__(item_data)

        self.setFlags(
            Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable |
            Qt.ItemFlag.ItemIsSelectable
        )

    def get_field_depth(self):
        return len(self.get_field_path())

    def get_field_path(self, string=False) -> FieldPath | str:
        path: FieldPath = list()
        item = self

        while item.parent() is not None:
            if not (field_number := item.field_number) and string:
                field_number: str = "<empty>"

            path.insert(int(), field_number)
            item = item.parent()

        if string:
            return ".".join(path)

        return path

    def set_spec(self, spec: IsoField | None = None):
        if not spec:
            spec: IsoField = self.epay_spec.get_field_spec(self.get_field_path())

        self.spec = spec

        for child in self.get_children():
            child.set_spec()

    def get_children(self) -> tuple:
        return tuple(self.child(child_id) for child_id in range(self.childCount()))

    @void_tree_signals
    def set_item_color(self, color=Colors.BLACK):
        for column in range(self.columnCount()):
            self.setForeground(column, QtGui.QBrush(QtGui.QColor(color)))
