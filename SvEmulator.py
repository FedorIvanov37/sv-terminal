from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from common.gui.decorators.window_settings import set_window_icon, has_close_button_only, frameless_window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # create a QWebEngineView widget
        self.web_view = QWebEngineView(self)
        # load HTML content

        with open('common/doc/Signal_v0.18.html', 'r', encoding="utf8") as filedata:
            html_content = filedata.read()

        # html_content = "<html><body><h1>Hello, PyQt5!</h1></body></html>"
        self.web_view.setHtml(html_content)
        # set the widget as the main window's central widget
        self.setCentralWidget(self.web_view)
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.resize(720, 1080)
        self.setWindowTitle("Signal | User reference guide")
        self.setWindowIcon(QIcon(r'common\data\style\logo_triangle.ico'))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
