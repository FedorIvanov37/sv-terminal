from PyQt6.QtGui import QUndoCommand
from signal.gui.core.json_items.FIeldItem import FieldItem


class UndoAddChildCommand(QUndoCommand):
    def __init__(self, item: FieldItem, parent: FieldItem):
        super(UndoAddChildCommand, self).__init__()
        self.item: FieldItem = item
        self.parent: FieldItem = parent
        self.index: int = self.parent.indexOfChild(self.item)

    def undo(self) -> None:
        self.parent.takeChild(self.index)

    def redo(self) -> None:
        self.parent.insertChild(self.index, self.item)


class UndoRemoveChildCommand(QUndoCommand):
    def __init__(self, item: FieldItem, parent: FieldItem):
        super(UndoRemoveChildCommand, self).__init__()
        self.item: FieldItem = item
        self.parent: FieldItem = parent
        self.index: int = self.parent.indexOfChild(self.item)

    def undo(self) -> None:
        self.parent.insertChild(self.index, self.item)

    def redo(self) -> None:
        self.parent.takeChild(self.index)
