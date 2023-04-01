from PyQt6.QtCore import QObject
from abc import ABCMeta


class QobjecAbcMeta(type(QObject), ABCMeta):
    ...
