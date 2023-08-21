# Form implementation generated from reading ui file '.\settings.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(300, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsWindow.sizePolicy().hasHeightForWidth())
        SettingsWindow.setSizePolicy(sizePolicy)
        SettingsWindow.setMinimumSize(QtCore.QSize(300, 500))
        SettingsWindow.setMaximumSize(QtCore.QSize(300, 500))
        SettingsWindow.setWhatsThis("")
        self.gridLayout_2 = QtWidgets.QGridLayout(SettingsWindow)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.ConnectionBox = QtWidgets.QGroupBox(parent=SettingsWindow)
        self.ConnectionBox.setObjectName("ConnectionBox")
        self.gridLayout = QtWidgets.QGridLayout(self.ConnectionBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SvAddress = QtWidgets.QLineEdit(parent=self.ConnectionBox)
        self.SvAddress.setObjectName("SvAddress")
        self.horizontalLayout_2.addWidget(self.SvAddress)
        self.label_2 = QtWidgets.QLabel(parent=self.ConnectionBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.SvPort = QtWidgets.QLineEdit(parent=self.ConnectionBox)
        self.SvPort.setMaximumSize(QtCore.QSize(55, 16777215))
        self.SvPort.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhDigitsOnly|QtCore.Qt.InputMethodHint.ImhPreferNumbers)
        self.SvPort.setMaxLength(5)
        self.SvPort.setObjectName("SvPort")
        self.horizontalLayout_2.addWidget(self.SvPort)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.KeepAliveMode = QtWidgets.QCheckBox(parent=self.ConnectionBox)
        self.KeepAliveMode.setObjectName("KeepAliveMode")
        self.horizontalLayout_3.addWidget(self.KeepAliveMode)
        self.KeepAliveInterval = QtWidgets.QLineEdit(parent=self.ConnectionBox)
        self.KeepAliveInterval.setMaximumSize(QtCore.QSize(55, 16777215))
        self.KeepAliveInterval.setMaxLength(4)
        self.KeepAliveInterval.setObjectName("KeepAliveInterval")
        self.horizontalLayout_3.addWidget(self.KeepAliveInterval)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.ConnectionBox, 0, 0, 1, 1)
        self.OnStartupBox = QtWidgets.QGroupBox(parent=SettingsWindow)
        self.OnStartupBox.setObjectName("OnStartupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.OnStartupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ConnectOnStartup = QtWidgets.QCheckBox(parent=self.OnStartupBox)
        self.ConnectOnStartup.setObjectName("ConnectOnStartup")
        self.verticalLayout_5.addWidget(self.ConnectOnStartup)
        self.ProcessDefaultDump = QtWidgets.QCheckBox(parent=self.OnStartupBox)
        self.ProcessDefaultDump.setObjectName("ProcessDefaultDump")
        self.verticalLayout_5.addWidget(self.ProcessDefaultDump)
        self.gridLayout_2.addWidget(self.OnStartupBox, 1, 0, 1, 1)
        self.LogBox = QtWidgets.QGroupBox(parent=SettingsWindow)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        self.LogBox.setPalette(palette)
        self.LogBox.setObjectName("LogBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.LogBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(parent=self.LogBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.DebugLevel = QtWidgets.QComboBox(parent=self.LogBox)
        self.DebugLevel.setObjectName("DebugLevel")
        self.horizontalLayout_4.addWidget(self.DebugLevel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.ClearLog = QtWidgets.QCheckBox(parent=self.LogBox)
        self.ClearLog.setObjectName("ClearLog")
        self.verticalLayout_3.addWidget(self.ClearLog)
        self.ParseSubfields = QtWidgets.QCheckBox(parent=self.LogBox)
        self.ParseSubfields.setObjectName("ParseSubfields")
        self.verticalLayout_3.addWidget(self.ParseSubfields)
        self.gridLayout_2.addWidget(self.LogBox, 2, 0, 1, 1)
        self.FieldsBox = QtWidgets.QGroupBox(parent=SettingsWindow)
        self.FieldsBox.setObjectName("FieldsBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.FieldsBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.BuildFld90 = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.BuildFld90.setObjectName("BuildFld90")
        self.gridLayout_3.addWidget(self.BuildFld90, 2, 0, 1, 1)
        self.JsonMode = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.JsonMode.setObjectName("JsonMode")
        self.gridLayout_3.addWidget(self.JsonMode, 3, 0, 1, 1)
        self.SendInternalId = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.SendInternalId.setObjectName("SendInternalId")
        self.gridLayout_3.addWidget(self.SendInternalId, 1, 0, 1, 1)
        self.ValidationEnabled = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.ValidationEnabled.setObjectName("ValidationEnabled")
        self.gridLayout_3.addWidget(self.ValidationEnabled, 4, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.FieldsBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.MaxAmount = QtWidgets.QLineEdit(parent=self.FieldsBox)
        self.MaxAmount.setMaxLength(12)
        self.MaxAmount.setObjectName("MaxAmount")
        self.horizontalLayout.addWidget(self.MaxAmount)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.HideSecrets = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.HideSecrets.setObjectName("HideSecrets")
        self.gridLayout_3.addWidget(self.HideSecrets, 5, 0, 1, 1)
        self.gridLayout_2.addWidget(self.FieldsBox, 3, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=SettingsWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_5.addWidget(self.buttonBox)
        spacerItem2 = QtWidgets.QSpacerItem(54, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.ButtonAbout = QtWidgets.QPushButton(parent=SettingsWindow)
        self.ButtonAbout.setMaximumSize(QtCore.QSize(30, 16777215))
        self.ButtonAbout.setText("")
        self.ButtonAbout.setObjectName("ButtonAbout")
        self.horizontalLayout_5.addWidget(self.ButtonAbout)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 4, 0, 1, 1)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Configuration"))
        self.ConnectionBox.setTitle(_translate("SettingsWindow", "Connection"))
        self.SvAddress.setPlaceholderText(_translate("SettingsWindow", "SV address"))
        self.label_2.setText(_translate("SettingsWindow", ":"))
        self.SvPort.setPlaceholderText(_translate("SettingsWindow", "port"))
        self.KeepAliveMode.setText(_translate("SettingsWindow", "Keep Alive message loop (sec)"))
        self.KeepAliveInterval.setPlaceholderText(_translate("SettingsWindow", "seconds"))
        self.OnStartupBox.setTitle(_translate("SettingsWindow", "On startup"))
        self.ConnectOnStartup.setText(_translate("SettingsWindow", "Open SV connection"))
        self.ProcessDefaultDump.setText(_translate("SettingsWindow", "Process default file"))
        self.LogBox.setTitle(_translate("SettingsWindow", "Log"))
        self.label_4.setText(_translate("SettingsWindow", "Debug level"))
        self.ClearLog.setText(_translate("SettingsWindow", "Clear log before sent message"))
        self.ParseSubfields.setText(_translate("SettingsWindow", "Parse subfields"))
        self.FieldsBox.setTitle(_translate("SettingsWindow", "Fields"))
        self.BuildFld90.setText(_translate("SettingsWindow", "Build field 90 in reversal"))
        self.JsonMode.setText(_translate("SettingsWindow", "JSON-like fields representation "))
        self.SendInternalId.setText(_translate("SettingsWindow", "Send internal transaction ID to SV"))
        self.ValidationEnabled.setText(_translate("SettingsWindow", "Fields validation"))
        self.label.setText(_translate("SettingsWindow", "Max amount"))
        self.MaxAmount.setPlaceholderText(_translate("SettingsWindow", "Amount"))
        self.HideSecrets.setText(_translate("SettingsWindow", "Hide secret fields"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QDialog()
    ui = Ui_SettingsWindow()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec())
