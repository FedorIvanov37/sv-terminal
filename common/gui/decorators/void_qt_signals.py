from typing import Callable


#  The decorator switches off field data validation and helps to avoid the recursive effects
#  while the field data changes automatically


def void_qt_signals(function: Callable):

    def wrapper(self, *args, **kwargs):
        self.blockSignals(True)
        function(self, *args, **kwargs)
        self.blockSignals(False)

    return wrapper


def void_tree_signals(function: Callable):

    def wrapper(self, *args, **kwargs):
        if tree := self.treeWidget():
            tree.blockSignals(True)

        function(self, *args, **kwargs)

        if tree := self.treeWidget():
            tree.blockSignals(False)

    return wrapper
