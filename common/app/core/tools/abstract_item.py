from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import Qt
from common.lib.EpaySpecification import EpaySpecification


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
        self.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)

    def get_field_depth(self):
        return len(self.get_field_path())

    def get_field_path(self, string=False) -> list[str] | str:
        path = list()
        item = self

        while item.parent() is not None:
            if not item.field_number:
                return list()

            path.insert(int(), item.field_number)
            item = item.parent()

        if string:
            return ".".join(path)

        return path

    def get_children(self) -> tuple:
        return tuple(self.child(child_id) for child_id in range(self.childCount()))
