from traceback import format_exc
from PyQt6.QtWidgets import QDialog
from common.gui.forms.error import Ui_Error
from common.gui.decorators.window_settings import set_window_icon, has_close_button_only


class ErrorWindow(Ui_Error, QDialog):
    def __init__(self, exc):
        super().__init__()

        self.exception = exc

        try:
            self.setupUi(self)
            self.setup()

        except Exception as exc:
            self.exit(exc)

    @set_window_icon
    @has_close_button_only
    def setup(self):
        self.accepted.connect(self.exit)
        self.rejected.connect(self.exit)
        self.TextField.append(format_exc())

    def exit(self, exception=None, error_code=100):
        print(f"Finished with error: {exception if exception else self.exception}")
        exit(error_code)
