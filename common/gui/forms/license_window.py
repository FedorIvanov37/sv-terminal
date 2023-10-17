# Form implementation generated from reading ui file '.\license_window.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_LicenseWindow(object):
    def setupUi(self, LicenseWindow):
        LicenseWindow.setObjectName("LicenseWindow")
        LicenseWindow.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        LicenseWindow.resize(760, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LicenseWindow.sizePolicy().hasHeightForWidth())
        LicenseWindow.setSizePolicy(sizePolicy)
        LicenseWindow.setMinimumSize(QtCore.QSize(760, 900))
        LicenseWindow.setMaximumSize(QtCore.QSize(760, 900))
        LicenseWindow.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(LicenseWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ButtonAccept = QtWidgets.QPushButton(parent=LicenseWindow)
        self.ButtonAccept.setObjectName("ButtonAccept")
        self.horizontalLayout.addWidget(self.ButtonAccept)
        self.ButtonReject = QtWidgets.QPushButton(parent=LicenseWindow)
        self.ButtonReject.setObjectName("ButtonReject")
        self.horizontalLayout.addWidget(self.ButtonReject)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.CheckBoxAgreement = QtWidgets.QCheckBox(parent=LicenseWindow)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxAgreement.setFont(font)
        self.CheckBoxAgreement.setObjectName("CheckBoxAgreement")
        self.verticalLayout.addWidget(self.CheckBoxAgreement)
        self.CheckBoxDontShowAgain = QtWidgets.QCheckBox(parent=LicenseWindow)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxDontShowAgain.setFont(font)
        self.CheckBoxDontShowAgain.setObjectName("CheckBoxDontShowAgain")
        self.verticalLayout.addWidget(self.CheckBoxDontShowAgain)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.InfoBoard = QtWidgets.QTextEdit(parent=LicenseWindow)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        self.InfoBoard.setFont(font)
        self.InfoBoard.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.InfoBoard.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.InfoBoard.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.InfoBoard.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.InfoBoard.setDocumentTitle("")
        self.InfoBoard.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.WidgetWidth)
        self.InfoBoard.setReadOnly(True)
        self.InfoBoard.setAcceptRichText(False)
        self.InfoBoard.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.InfoBoard.setObjectName("InfoBoard")
        self.gridLayout.addWidget(self.InfoBoard, 1, 0, 1, 1)

        self.retranslateUi(LicenseWindow)
        self.ButtonAccept.clicked.connect(LicenseWindow.accept) # type: ignore
        self.ButtonReject.clicked.connect(LicenseWindow.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(LicenseWindow)
        LicenseWindow.setTabOrder(self.CheckBoxAgreement, self.CheckBoxDontShowAgain)
        LicenseWindow.setTabOrder(self.CheckBoxDontShowAgain, self.ButtonAccept)
        LicenseWindow.setTabOrder(self.ButtonAccept, self.ButtonReject)

    def retranslateUi(self, LicenseWindow):
        _translate = QtCore.QCoreApplication.translate
        LicenseWindow.setWindowTitle(_translate("LicenseWindow", "SIGNAL terms and conditions"))
        self.ButtonAccept.setText(_translate("LicenseWindow", "Accept"))
        self.ButtonReject.setText(_translate("LicenseWindow", "Reject"))
        self.CheckBoxAgreement.setText(_translate("LicenseWindow", "I am agree with the terms and conditions"))
        self.CheckBoxDontShowAgain.setText(_translate("LicenseWindow", "Don\'t show this message anymore"))
        self.InfoBoard.setHtml(_translate("LicenseWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Courier New\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LicenseWindow = QtWidgets.QDialog()
    ui = Ui_LicenseWindow()
    ui.setupUi(LicenseWindow)
    LicenseWindow.show()
    sys.exit(app.exec())
