# Form implementation generated from reading ui file '.\license_window.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_LicenseWindow(object):
    def setupUi(self, LicenseWindow):
        LicenseWindow.setObjectName("LicenseWindow")
        LicenseWindow.setWindowModality(QtCore.Qt.WindowModality.NonModal)
        LicenseWindow.resize(850, 950)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LicenseWindow.sizePolicy().hasHeightForWidth())
        LicenseWindow.setSizePolicy(sizePolicy)
        LicenseWindow.setMinimumSize(QtCore.QSize(850, 950))
        LicenseWindow.setMaximumSize(QtCore.QSize(850, 950))
        LicenseWindow.setModal(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(LicenseWindow)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(parent=LicenseWindow)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        self.frame.setPalette(palette)
        self.frame.setStyleSheet("background-color: rgb(214, 214, 214);")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ButtonAccept = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonAccept.setFont(font)
        self.ButtonAccept.setObjectName("ButtonAccept")
        self.horizontalLayout.addWidget(self.ButtonAccept)
        self.ButtonReject = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonReject.setFont(font)
        self.ButtonReject.setObjectName("ButtonReject")
        self.horizontalLayout.addWidget(self.ButtonReject)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.SpacerLabel_1 = QtWidgets.QLabel(parent=self.frame)
        self.SpacerLabel_1.setText("")
        self.SpacerLabel_1.setObjectName("SpacerLabel_1")
        self.verticalLayout.addWidget(self.SpacerLabel_1)
        self.CheckBoxAgreement = QtWidgets.QCheckBox(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxAgreement.setFont(font)
        self.CheckBoxAgreement.setObjectName("CheckBoxAgreement")
        self.verticalLayout.addWidget(self.CheckBoxAgreement)
        self.CheckBoxDontShowAgain = QtWidgets.QCheckBox(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxDontShowAgain.setFont(font)
        self.CheckBoxDontShowAgain.setObjectName("CheckBoxDontShowAgain")
        self.verticalLayout.addWidget(self.CheckBoxDontShowAgain)
        self.SpacerLabel = QtWidgets.QLabel(parent=self.frame)
        self.SpacerLabel.setText("")
        self.SpacerLabel.setObjectName("SpacerLabel")
        self.verticalLayout.addWidget(self.SpacerLabel)
        self.gridLayout.addLayout(self.verticalLayout, 4, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(222, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(222, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        self.InfoBoard = QtWidgets.QTextEdit(parent=self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        self.InfoBoard.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        self.InfoBoard.setFont(font)
        self.InfoBoard.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.InfoBoard.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.InfoBoard.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.InfoBoard.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.InfoBoard.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.InfoBoard.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.InfoBoard.setUndoRedoEnabled(False)
        self.InfoBoard.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.InfoBoard.setReadOnly(True)
        self.InfoBoard.setAcceptRichText(False)
        self.InfoBoard.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByKeyboard|QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse|QtCore.Qt.TextInteractionFlag.TextBrowserInteraction|QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.InfoBoard.setObjectName("InfoBoard")
        self.gridLayout.addWidget(self.InfoBoard, 2, 0, 1, 3)
        self.line = QtWidgets.QFrame(parent=self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 3)
        self.LogoLabel = QtWidgets.QLabel(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LogoLabel.sizePolicy().hasHeightForWidth())
        self.LogoLabel.setSizePolicy(sizePolicy)
        self.LogoLabel.setMinimumSize(QtCore.QSize(300, 300))
        self.LogoLabel.setMaximumSize(QtCore.QSize(300, 300))
        self.LogoLabel.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.LogoLabel.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.LogoLabel.setScaledContents(True)
        self.LogoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LogoLabel.setObjectName("LogoLabel")
        self.gridLayout.addWidget(self.LogoLabel, 0, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(parent=self.frame)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 3)
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(LicenseWindow)
        self.ButtonAccept.clicked.connect(LicenseWindow.accept) # type: ignore
        self.ButtonReject.clicked.connect(LicenseWindow.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(LicenseWindow)
        LicenseWindow.setTabOrder(self.CheckBoxAgreement, self.CheckBoxDontShowAgain)

    def retranslateUi(self, LicenseWindow):
        _translate = QtCore.QCoreApplication.translate
        LicenseWindow.setWindowTitle(_translate("LicenseWindow", "Signal | GNU General Public License"))
        self.ButtonAccept.setText(_translate("LicenseWindow", "Accept"))
        self.ButtonReject.setText(_translate("LicenseWindow", "Reject"))
        self.CheckBoxAgreement.setText(_translate("LicenseWindow", "I am agree with the terms and conditions"))
        self.CheckBoxDontShowAgain.setText(_translate("LicenseWindow", "Don\'t show this message anymore"))
        self.InfoBoard.setDocumentTitle(_translate("LicenseWindow", "GNU/GPL license agreement"))
        self.InfoBoard.setHtml(_translate("LicenseWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><title>GNU/GPL license agreement</title><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Courier New\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.LogoLabel.setText(_translate("LicenseWindow", "logo"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LicenseWindow = QtWidgets.QDialog()
    ui = Ui_LicenseWindow()
    ui.setupUi(LicenseWindow)
    LicenseWindow.show()
    sys.exit(app.exec())
