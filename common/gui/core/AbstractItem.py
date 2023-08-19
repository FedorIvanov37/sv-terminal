from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidgetItem
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.Types import FieldPath
from common.gui.decorators.void_qt_signals import void_tree_signals


class AbstractItem(QTreeWidgetItem):
    _field_number: str = None
    _epay_spec = EpaySpecification()

    @property
    def epay_spec(self):
        return self._epay_spec

    @property
    def field_number(self):
        return self._field_number

    def __init__(self, item_data: list[str]):
        super(AbstractItem, self).__init__(item_data)

        self.setFlags(
             Qt.ItemFlag.ItemIsEditable |
             Qt.ItemFlag.ItemIsEnabled |
             Qt.ItemFlag.ItemIsUserCheckable |
             Qt.ItemFlag.ItemIsSelectable
        )

    def get_field_depth(self):
        return len(self.get_field_path())

    def get_field_path(self, string=False) -> FieldPath | str:
        path: FieldPath = list()
        item = self

        while item.parent() is not None:
            path.insert(int(), item.field_number)
            item = item.parent()

        if string:
            return ".".join(path)

        return path

    def get_children(self) -> tuple:
        return tuple(self.child(child_id) for child_id in range(self.childCount()))

    @void_tree_signals
    def set_item_color(self, red=False):
        color = "#ff0000" if red else "#000000"

        for column in range(self.columnCount()):
            self.setForeground(column, QtGui.QBrush(QtGui.QColor(color)))
