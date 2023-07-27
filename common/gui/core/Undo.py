from PyQt6.QtGui import QUndoCommand
from common.gui.core.FIeldItem import Item


class UndoAddChildCommand(QUndoCommand):
    def __init__(self, item: Item, parent: Item):
        super(UndoAddChildCommand, self).__init__()
        self.item: Item = item
        self.parent: Item = parent
        self.index: int = self.parent.indexOfChild(self.item)

    def undo(self) -> None:
        self.parent.takeChild(self.index)

    def redo(self) -> None:
        self.parent.insertChild(self.index, self.item)


class UndoRemoveChildCommand(QUndoCommand):
    def __init__(self, item: Item, parent: Item):
        super(UndoRemoveChildCommand, self).__init__()
        self.item: Item = item
        self.parent: Item = parent
        self.index: int = self.parent.indexOfChild(self.item)

    def undo(self) -> None:
        self.parent.insertChild(self.index, self.item)

    def redo(self) -> None:
        self.parent.takeChild(self.index)
