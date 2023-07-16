from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from common.gui.constants.TermFilesPath import TermFilesPath


# Set default window icon before show window
def set_window_icon(setup_function: callable):

    def wrapper(window: QDialog, *args, **kwargs):
        window.setWindowIcon(QIcon(TermFilesPath.MAIN_LOGO))
        setup_function(window, *args, **kwargs)

    return wrapper


# Frameless modal window, no close menu, window title, etc
def frameless_window(setup_function: callable):

    def wrapper(window: QDialog, *args, **kwargs):
        window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        setup_function(window, *args, **kwargs)

    return wrapper


# The window has a close button only, buttons that resize and collapse are absent
def has_close_button_only(setup_function: callable):

    def wrapper(window: QDialog, *args, **kwargs):
        window.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        setup_function(window, *args, **kwargs)

    return wrapper
