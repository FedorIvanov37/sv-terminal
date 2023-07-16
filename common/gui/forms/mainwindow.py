# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1404, 959)
        MainWindow.setMouseTracking(False)
        MainWindow.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ConnectionScreen = QtWidgets.QTextBrowser(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ConnectionScreen.sizePolicy().hasHeightForWidth())
        self.ConnectionScreen.setSizePolicy(sizePolicy)
        self.ConnectionScreen.setMinimumSize(QtCore.QSize(31, 21))
        self.ConnectionScreen.setMaximumSize(QtCore.QSize(31, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        self.ConnectionScreen.setPalette(palette)
        self.ConnectionScreen.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ConnectionScreen.setAcceptDrops(False)
        self.ConnectionScreen.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ConnectionScreen.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ConnectionScreen.setObjectName("ConnectionScreen")
        self.horizontalLayout_3.addWidget(self.ConnectionScreen)
        self.ConnectionStatus = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ConnectionStatus.setFont(font)
        self.ConnectionStatus.setText("")
        self.ConnectionStatus.setObjectName("ConnectionStatus")
        self.horizontalLayout_3.addWidget(self.ConnectionStatus)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.msgtype = QtWidgets.QComboBox(parent=self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        self.msgtype.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.msgtype.setFont(font)
        self.msgtype.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.msgtype.setEditable(False)
        self.msgtype.setCurrentText("")
        self.msgtype.setObjectName("msgtype")
        self.gridLayout.addWidget(self.msgtype, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Bitmap = QtWidgets.QLineEdit(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.Bitmap.setFont(font)
        self.Bitmap.setMouseTracking(True)
        self.Bitmap.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Bitmap.setReadOnly(True)
        self.Bitmap.setObjectName("Bitmap")
        self.horizontalLayout_4.addWidget(self.Bitmap)
        self.ButtonCopyBitmap = QtWidgets.QPushButton(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonCopyBitmap.setFont(font)
        self.ButtonCopyBitmap.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonCopyBitmap.setObjectName("ButtonCopyBitmap")
        self.horizontalLayout_4.addWidget(self.ButtonCopyBitmap)
        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        self.FieldsTreeLayout = QtWidgets.QVBoxLayout()
        self.FieldsTreeLayout.setObjectName("FieldsTreeLayout")
        self.gridLayout.addLayout(self.FieldsTreeLayout, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.PlusLayout = QtWidgets.QHBoxLayout()
        self.PlusLayout.setObjectName("PlusLayout")
        self.horizontalLayout.addLayout(self.PlusLayout)
        self.MinusLayout = QtWidgets.QHBoxLayout()
        self.MinusLayout.setObjectName("MinusLayout")
        self.horizontalLayout.addLayout(self.MinusLayout)
        self.NextLevelLayout = QtWidgets.QHBoxLayout()
        self.NextLevelLayout.setObjectName("NextLevelLayout")
        self.horizontalLayout.addLayout(self.NextLevelLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.LogArea = QtWidgets.QTextEdit(parent=self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 109))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 109))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        self.LogArea.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(11)
        self.LogArea.setFont(font)
        self.LogArea.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.LogArea.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.LogArea.setReadOnly(True)
        self.LogArea.setAcceptRichText(False)
        self.LogArea.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.LogArea.setObjectName("LogArea")
        self.gridLayout.addWidget(self.LogArea, 5, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ButtonSend = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonSend.sizePolicy().hasHeightForWidth())
        self.ButtonSend.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonSend.setFont(font)
        self.ButtonSend.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonSend.setObjectName("ButtonSend")
        self.horizontalLayout_2.addWidget(self.ButtonSend)
        self.ButtonReverse = QtWidgets.QPushButton(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonReverse.setFont(font)
        self.ButtonReverse.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonReverse.setObjectName("ButtonReverse")
        self.horizontalLayout_2.addWidget(self.ButtonReverse)
        self.ButtonClearLog = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonClearLog.sizePolicy().hasHeightForWidth())
        self.ButtonClearLog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonClearLog.setFont(font)
        self.ButtonClearLog.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonClearLog.setObjectName("ButtonClearLog")
        self.horizontalLayout_2.addWidget(self.ButtonClearLog)
        self.ButtonCopyLog = QtWidgets.QPushButton(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonCopyLog.setFont(font)
        self.ButtonCopyLog.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonCopyLog.setObjectName("ButtonCopyLog")
        self.horizontalLayout_2.addWidget(self.ButtonCopyLog)
        self.ButtonParseDump = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonParseDump.sizePolicy().hasHeightForWidth())
        self.ButtonParseDump.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonParseDump.setFont(font)
        self.ButtonParseDump.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonParseDump.setObjectName("ButtonParseDump")
        self.horizontalLayout_2.addWidget(self.ButtonParseDump)
        self.ButtonSave = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonSave.sizePolicy().hasHeightForWidth())
        self.ButtonSave.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonSave.setFont(font)
        self.ButtonSave.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonSave.setObjectName("ButtonSave")
        self.horizontalLayout_2.addWidget(self.ButtonSave)
        self.ButtonClearMessage = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonClearMessage.sizePolicy().hasHeightForWidth())
        self.ButtonClearMessage.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonClearMessage.setFont(font)
        self.ButtonClearMessage.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonClearMessage.setObjectName("ButtonClearMessage")
        self.horizontalLayout_2.addWidget(self.ButtonClearMessage)
        self.ButtonDefault = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonDefault.sizePolicy().hasHeightForWidth())
        self.ButtonDefault.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonDefault.setFont(font)
        self.ButtonDefault.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonDefault.setObjectName("ButtonDefault")
        self.horizontalLayout_2.addWidget(self.ButtonDefault)
        self.ButtonPrintData = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonPrintData.sizePolicy().hasHeightForWidth())
        self.ButtonPrintData.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonPrintData.setFont(font)
        self.ButtonPrintData.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonPrintData.setObjectName("ButtonPrintData")
        self.horizontalLayout_2.addWidget(self.ButtonPrintData)
        self.ButtonEchoTest = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonEchoTest.sizePolicy().hasHeightForWidth())
        self.ButtonEchoTest.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonEchoTest.setFont(font)
        self.ButtonEchoTest.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonEchoTest.setObjectName("ButtonEchoTest")
        self.horizontalLayout_2.addWidget(self.ButtonEchoTest)
        self.ButtonReconnect = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonReconnect.sizePolicy().hasHeightForWidth())
        self.ButtonReconnect.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonReconnect.setFont(font)
        self.ButtonReconnect.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonReconnect.setObjectName("ButtonReconnect")
        self.horizontalLayout_2.addWidget(self.ButtonReconnect)
        self.ButtonSpecification = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonSpecification.sizePolicy().hasHeightForWidth())
        self.ButtonSpecification.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonSpecification.setFont(font)
        self.ButtonSpecification.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonSpecification.setObjectName("ButtonSpecification")
        self.horizontalLayout_2.addWidget(self.ButtonSpecification)
        self.ButtonHotkeys = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonHotkeys.sizePolicy().hasHeightForWidth())
        self.ButtonHotkeys.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonHotkeys.setFont(font)
        self.ButtonHotkeys.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonHotkeys.setObjectName("ButtonHotkeys")
        self.horizontalLayout_2.addWidget(self.ButtonHotkeys)
        self.ButtonSettings = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonSettings.sizePolicy().hasHeightForWidth())
        self.ButtonSettings.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonSettings.setFont(font)
        self.ButtonSettings.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonSettings.setObjectName("ButtonSettings")
        self.horizontalLayout_2.addWidget(self.ButtonSettings)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1404, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.msgtype, self.Bitmap)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SmartVista Terminal"))
        self.ButtonCopyBitmap.setText(_translate("MainWindow", "Copy"))
        self.ButtonSend.setText(_translate("MainWindow", "Send"))
        self.ButtonReverse.setText(_translate("MainWindow", "Reverse"))
        self.ButtonClearLog.setText(_translate("MainWindow", "Clear log"))
        self.ButtonCopyLog.setText(_translate("MainWindow", "Copy log"))
        self.ButtonParseDump.setText(_translate("MainWindow", "Parse file"))
        self.ButtonSave.setText(_translate("MainWindow", "Save to file"))
        self.ButtonClearMessage.setText(_translate("MainWindow", "Clear message"))
        self.ButtonDefault.setText(_translate("MainWindow", "Reset message"))
        self.ButtonPrintData.setText(_translate("MainWindow", "Print"))
        self.ButtonEchoTest.setText(_translate("MainWindow", "Echo-Test"))
        self.ButtonReconnect.setText(_translate("MainWindow", "[Re]connect"))
        self.ButtonSpecification.setText(_translate("MainWindow", "Specification"))
        self.ButtonHotkeys.setText(_translate("MainWindow", "Hotkeys"))
        self.ButtonSettings.setText(_translate("MainWindow", "Configuration"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
