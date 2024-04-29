# Form implementation generated from reading ui file '.\settings.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(580, 501)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsWindow.sizePolicy().hasHeightForWidth())
        SettingsWindow.setSizePolicy(sizePolicy)
        SettingsWindow.setMinimumSize(QtCore.QSize(580, 501))
        SettingsWindow.setMaximumSize(QtCore.QSize(580, 501))
        SettingsWindow.setWhatsThis("")
        self.gridLayout_4 = QtWidgets.QGridLayout(SettingsWindow)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.ConnectionBox = QtWidgets.QGroupBox(parent=SettingsWindow)
        self.ConnectionBox.setObjectName("ConnectionBox")
        self.gridLayout = QtWidgets.QGridLayout(self.ConnectionBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.KeepAliveMode = QtWidgets.QCheckBox(parent=self.ConnectionBox)
        self.KeepAliveMode.setObjectName("KeepAliveMode")
        self.horizontalLayout_3.addWidget(self.KeepAliveMode)
        self.KeepAliveInterval = QtWidgets.QSpinBox(parent=self.ConnectionBox)
        self.KeepAliveInterval.setMinimumSize(QtCore.QSize(65, 20))
        self.KeepAliveInterval.setMaximumSize(QtCore.QSize(55, 20))
        self.KeepAliveInterval.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.KeepAliveInterval.setKeyboardTracking(True)
        self.KeepAliveInterval.setProperty("showGroupSeparator", False)
        self.KeepAliveInterval.setMinimum(1)
        self.KeepAliveInterval.setMaximum(1000)
        self.KeepAliveInterval.setProperty("value", 300)
        self.KeepAliveInterval.setDisplayIntegerBase(10)
        self.KeepAliveInterval.setObjectName("KeepAliveInterval")
        self.horizontalLayout_3.addWidget(self.KeepAliveInterval)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.HeaderLengthMode = QtWidgets.QCheckBox(parent=self.ConnectionBox)
        self.HeaderLengthMode.setObjectName("HeaderLengthMode")
        self.horizontalLayout_6.addWidget(self.HeaderLengthMode)
        self.HeaderLength = QtWidgets.QSpinBox(parent=self.ConnectionBox)
        self.HeaderLength.setMinimumSize(QtCore.QSize(65, 0))
        self.HeaderLength.setMaximumSize(QtCore.QSize(55, 16777215))
        self.HeaderLength.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.HeaderLength.setReadOnly(False)
        self.HeaderLength.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.HeaderLength.setKeyboardTracking(False)
        self.HeaderLength.setProperty("showGroupSeparator", False)
        self.HeaderLength.setPrefix("")
        self.HeaderLength.setMinimum(2)
        self.HeaderLength.setMaximum(64)
        self.HeaderLength.setSingleStep(2)
        self.HeaderLength.setProperty("value", 2)
        self.HeaderLength.setObjectName("HeaderLength")
        self.horizontalLayout_6.addWidget(self.HeaderLength)
        self.gridLayout.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.IpLabel = QtWidgets.QLabel(parent=self.ConnectionBox)
        self.IpLabel.setObjectName("IpLabel")
        self.horizontalLayout_2.addWidget(self.IpLabel)
        self.SvAddress = QtWidgets.QLineEdit(parent=self.ConnectionBox)
        self.SvAddress.setObjectName("SvAddress")
        self.horizontalLayout_2.addWidget(self.SvAddress)
        self.PortLabel = QtWidgets.QLabel(parent=self.ConnectionBox)
        self.PortLabel.setObjectName("PortLabel")
        self.horizontalLayout_2.addWidget(self.PortLabel)
        self.SvPort = QtWidgets.QSpinBox(parent=self.ConnectionBox)
        self.SvPort.setMinimumSize(QtCore.QSize(65, 0))
        self.SvPort.setFrame(True)
        self.SvPort.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.SvPort.setKeyboardTracking(False)
        self.SvPort.setMinimum(1024)
        self.SvPort.setMaximum(65535)
        self.SvPort.setProperty("value", 16677)
        self.SvPort.setObjectName("SvPort")
        self.horizontalLayout_2.addWidget(self.SvPort)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.gridLayout_4.addWidget(self.ConnectionBox, 0, 0, 1, 1)
        self.SpecBox = QtWidgets.QGroupBox(parent=SettingsWindow)
        self.SpecBox.setObjectName("SpecBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.SpecBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.BackupStorageLabel = QtWidgets.QLabel(parent=self.SpecBox)
        self.BackupStorageLabel.setObjectName("BackupStorageLabel")
        self.horizontalLayout_7.addWidget(self.BackupStorageLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.StorageDepth = QtWidgets.QSpinBox(parent=self.SpecBox)
        self.StorageDepth.setMaximum(999)
        self.StorageDepth.setObjectName("StorageDepth")
        self.horizontalLayout_7.addWidget(self.StorageDepth)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 5, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.UrlLabel = QtWidgets.QLabel(parent=self.SpecBox)
        self.UrlLabel.setObjectName("UrlLabel")
        self.horizontalLayout_8.addWidget(self.UrlLabel)
        self.RemoteSpecUrl = QtWidgets.QLineEdit(parent=self.SpecBox)
        self.RemoteSpecUrl.setObjectName("RemoteSpecUrl")
        self.horizontalLayout_8.addWidget(self.RemoteSpecUrl)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)
        self.RewriteLocalSpec = QtWidgets.QCheckBox(parent=self.SpecBox)
        self.RewriteLocalSpec.setObjectName("RewriteLocalSpec")
        self.gridLayout_2.addWidget(self.RewriteLocalSpec, 2, 0, 1, 1)
        self.LoadSpec2 = QtWidgets.QCheckBox(parent=self.SpecBox)
        self.LoadSpec2.setObjectName("LoadSpec2")
        self.gridLayout_2.addWidget(self.LoadSpec2, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.SpecBox, 0, 1, 1, 1)
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
        self.LoadSpec = QtWidgets.QCheckBox(parent=self.OnStartupBox)
        self.LoadSpec.setObjectName("LoadSpec")
        self.verticalLayout_5.addWidget(self.LoadSpec)
        self.ShowLicense = QtWidgets.QCheckBox(parent=self.OnStartupBox)
        self.ShowLicense.setObjectName("ShowLicense")
        self.verticalLayout_5.addWidget(self.ShowLicense)
        self.gridLayout_4.addWidget(self.OnStartupBox, 1, 0, 1, 1)
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
        self.gridLayout_6 = QtWidgets.QGridLayout(self.LogBox)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(parent=self.LogBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.DebugLevel = QtWidgets.QComboBox(parent=self.LogBox)
        self.DebugLevel.setObjectName("DebugLevel")
        self.horizontalLayout_4.addWidget(self.DebugLevel)
        self.gridLayout_6.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.ClearLog = QtWidgets.QCheckBox(parent=self.LogBox)
        self.ClearLog.setObjectName("ClearLog")
        self.gridLayout_6.addWidget(self.ClearLog, 4, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.LogBackupLabel = QtWidgets.QLabel(parent=self.LogBox)
        self.LogBackupLabel.setObjectName("LogBackupLabel")
        self.horizontalLayout_10.addWidget(self.LogBackupLabel)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem4)
        self.LogStorageDepth = QtWidgets.QSpinBox(parent=self.LogBox)
        self.LogStorageDepth.setMaximum(999)
        self.LogStorageDepth.setObjectName("LogStorageDepth")
        self.horizontalLayout_10.addWidget(self.LogStorageDepth)
        self.gridLayout_6.addLayout(self.horizontalLayout_10, 3, 0, 1, 1)
        self.ParseSubfields = QtWidgets.QCheckBox(parent=self.LogBox)
        self.ParseSubfields.setObjectName("ParseSubfields")
        self.gridLayout_6.addWidget(self.ParseSubfields, 2, 0, 1, 1)
        self.gridLayout_4.addWidget(self.LogBox, 1, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(parent=SettingsWindow)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.ValidationEnabled = QtWidgets.QCheckBox(parent=self.groupBox)
        self.ValidationEnabled.setObjectName("ValidationEnabled")
        self.gridLayout_3.addWidget(self.ValidationEnabled, 0, 0, 1, 1)
        self.ValidateOutgoing = QtWidgets.QCheckBox(parent=self.groupBox)
        self.ValidateOutgoing.setObjectName("ValidateOutgoing")
        self.gridLayout_3.addWidget(self.ValidateOutgoing, 2, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.ValidationModeLabel = QtWidgets.QLabel(parent=self.groupBox)
        self.ValidationModeLabel.setObjectName("ValidationModeLabel")
        self.horizontalLayout_9.addWidget(self.ValidationModeLabel)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem5)
        self.ValidationReaction = QtWidgets.QComboBox(parent=self.groupBox)
        self.ValidationReaction.setObjectName("ValidationReaction")
        self.ValidationReaction.addItem("")
        self.ValidationReaction.addItem("")
        self.ValidationReaction.addItem("")
        self.horizontalLayout_9.addWidget(self.ValidationReaction)
        self.gridLayout_3.addLayout(self.horizontalLayout_9, 7, 0, 1, 1)
        self.ValidateWindow = QtWidgets.QCheckBox(parent=self.groupBox)
        self.ValidateWindow.setObjectName("ValidateWindow")
        self.gridLayout_3.addWidget(self.ValidateWindow, 1, 0, 1, 1)
        self.ValidateIncoming = QtWidgets.QCheckBox(parent=self.groupBox)
        self.ValidateIncoming.setObjectName("ValidateIncoming")
        self.gridLayout_3.addWidget(self.ValidateIncoming, 3, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 2, 0, 1, 1)
        self.FieldsBox = QtWidgets.QGroupBox(parent=SettingsWindow)
        self.FieldsBox.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhDigitsOnly)
        self.FieldsBox.setObjectName("FieldsBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.FieldsBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.SendInternalId = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.SendInternalId.setObjectName("SendInternalId")
        self.gridLayout_5.addWidget(self.SendInternalId, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MaxAmountBox = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.MaxAmountBox.setObjectName("MaxAmountBox")
        self.horizontalLayout.addWidget(self.MaxAmountBox)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.MaxAmount = QtWidgets.QComboBox(parent=self.FieldsBox)
        self.MaxAmount.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhDigitsOnly)
        self.MaxAmount.setEditable(False)
        self.MaxAmount.setObjectName("MaxAmount")
        self.MaxAmount.addItem("")
        self.MaxAmount.addItem("")
        self.MaxAmount.addItem("")
        self.MaxAmount.addItem("")
        self.MaxAmount.addItem("")
        self.horizontalLayout.addWidget(self.MaxAmount)
        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.HideSecrets = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.HideSecrets.setObjectName("HideSecrets")
        self.gridLayout_5.addWidget(self.HideSecrets, 4, 0, 1, 1)
        self.BuildFld90 = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.BuildFld90.setObjectName("BuildFld90")
        self.gridLayout_5.addWidget(self.BuildFld90, 2, 0, 1, 1)
        self.JsonMode = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.JsonMode.setObjectName("JsonMode")
        self.gridLayout_5.addWidget(self.JsonMode, 3, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_5.addItem(spacerItem7, 6, 0, 1, 1)
        self.ManualInputMode = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.ManualInputMode.setObjectName("ManualInputMode")
        self.gridLayout_5.addWidget(self.ManualInputMode, 5, 0, 1, 1)
        self.gridLayout_4.addWidget(self.FieldsBox, 2, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=SettingsWindow)
        self.buttonBox.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_5.addWidget(self.buttonBox)
        self.ButtonDefault = QtWidgets.QPushButton(parent=SettingsWindow)
        self.ButtonDefault.setObjectName("ButtonDefault")
        self.horizontalLayout_5.addWidget(self.ButtonDefault)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem8)
        spacerItem9 = QtWidgets.QSpacerItem(54, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem9)
        self.ButtonAbout = QtWidgets.QPushButton(parent=SettingsWindow)
        self.ButtonAbout.setMaximumSize(QtCore.QSize(30, 16777215))
        self.ButtonAbout.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)
        self.ButtonAbout.setWhatsThis("")
        self.ButtonAbout.setText("")
        self.ButtonAbout.setObjectName("ButtonAbout")
        self.horizontalLayout_5.addWidget(self.ButtonAbout)
        self.gridLayout_4.addLayout(self.horizontalLayout_5, 3, 0, 1, 2)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)
        SettingsWindow.setTabOrder(self.SvAddress, self.SvPort)
        SettingsWindow.setTabOrder(self.SvPort, self.HeaderLengthMode)
        SettingsWindow.setTabOrder(self.HeaderLengthMode, self.HeaderLength)
        SettingsWindow.setTabOrder(self.HeaderLength, self.KeepAliveMode)
        SettingsWindow.setTabOrder(self.KeepAliveMode, self.KeepAliveInterval)
        SettingsWindow.setTabOrder(self.KeepAliveInterval, self.ConnectOnStartup)
        SettingsWindow.setTabOrder(self.ConnectOnStartup, self.ProcessDefaultDump)
        SettingsWindow.setTabOrder(self.ProcessDefaultDump, self.ParseSubfields)
        SettingsWindow.setTabOrder(self.ParseSubfields, self.SendInternalId)
        SettingsWindow.setTabOrder(self.SendInternalId, self.BuildFld90)
        SettingsWindow.setTabOrder(self.BuildFld90, self.JsonMode)
        SettingsWindow.setTabOrder(self.JsonMode, self.HideSecrets)
        SettingsWindow.setTabOrder(self.HideSecrets, self.buttonBox)
        SettingsWindow.setTabOrder(self.buttonBox, self.ButtonAbout)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Signal | Configuration"))
        self.ConnectionBox.setTitle(_translate("SettingsWindow", "Remote host"))
        self.KeepAliveMode.setText(_translate("SettingsWindow", "Keep Alive message interval "))
        self.KeepAliveInterval.setSuffix(_translate("SettingsWindow", " sec"))
        self.HeaderLengthMode.setText(_translate("SettingsWindow", "ISO Message header length"))
        self.HeaderLength.setWhatsThis(_translate("SettingsWindow", "Usually 2 or 4"))
        self.HeaderLength.setSuffix(_translate("SettingsWindow", " bytes"))
        self.IpLabel.setText(_translate("SettingsWindow", "IP"))
        self.SvAddress.setPlaceholderText(_translate("SettingsWindow", "Hostname or address"))
        self.PortLabel.setText(_translate("SettingsWindow", ":"))
        self.SvPort.setSpecialValueText(_translate("SettingsWindow", "Val"))
        self.SpecBox.setTitle(_translate("SettingsWindow", "Specification"))
        self.BackupStorageLabel.setText(_translate("SettingsWindow", "Specification backup storage depth"))
        self.UrlLabel.setText(_translate("SettingsWindow", "URL"))
        self.RemoteSpecUrl.setPlaceholderText(_translate("SettingsWindow", "http://spec.example.url:7002/get_spec"))
        self.RewriteLocalSpec.setText(_translate("SettingsWindow", "Overwrite local spec by remote one"))
        self.LoadSpec2.setText(_translate("SettingsWindow", "Load remote specification on startup"))
        self.OnStartupBox.setTitle(_translate("SettingsWindow", "On startup"))
        self.ConnectOnStartup.setText(_translate("SettingsWindow", "Open connection"))
        self.ProcessDefaultDump.setText(_translate("SettingsWindow", "Process default file"))
        self.LoadSpec.setText(_translate("SettingsWindow", "Load remote specification"))
        self.ShowLicense.setText(_translate("SettingsWindow", "Show license dialog"))
        self.LogBox.setTitle(_translate("SettingsWindow", "Log"))
        self.label_4.setText(_translate("SettingsWindow", "Debug level"))
        self.ClearLog.setText(_translate("SettingsWindow", "Clear log before sent message"))
        self.LogBackupLabel.setText(_translate("SettingsWindow", "Logfile backup storage depth"))
        self.ParseSubfields.setText(_translate("SettingsWindow", "Parse subfields"))
        self.groupBox.setTitle(_translate("SettingsWindow", "Validation"))
        self.ValidationEnabled.setText(_translate("SettingsWindow", "Data validation enabled "))
        self.ValidateOutgoing.setText(_translate("SettingsWindow", "Outgoing messages validation"))
        self.ValidationModeLabel.setText(_translate("SettingsWindow", "Violation processing mode"))
        self.ValidationReaction.setItemText(0, _translate("SettingsWindow", "ERROR"))
        self.ValidationReaction.setItemText(1, _translate("SettingsWindow", "WARNING"))
        self.ValidationReaction.setItemText(2, _translate("SettingsWindow", "FLEXIBLE"))
        self.ValidateWindow.setText(_translate("SettingsWindow", "Window fields validation"))
        self.ValidateIncoming.setText(_translate("SettingsWindow", "Incoming messages validation"))
        self.FieldsBox.setTitle(_translate("SettingsWindow", "Fields"))
        self.SendInternalId.setText(_translate("SettingsWindow", "Send internal transaction ID to Host"))
        self.MaxAmountBox.setText(_translate("SettingsWindow", "Max generated amount"))
        self.MaxAmount.setItemText(0, _translate("SettingsWindow", "100"))
        self.MaxAmount.setItemText(1, _translate("SettingsWindow", "500"))
        self.MaxAmount.setItemText(2, _translate("SettingsWindow", "1500"))
        self.MaxAmount.setItemText(3, _translate("SettingsWindow", "10000"))
        self.MaxAmount.setItemText(4, _translate("SettingsWindow", "100000"))
        self.HideSecrets.setText(_translate("SettingsWindow", "Hide secret fields"))
        self.BuildFld90.setText(_translate("SettingsWindow", "Build field 90 in reversal"))
        self.JsonMode.setText(_translate("SettingsWindow", "JSON-like fields representation "))
        self.ManualInputMode.setText(_translate("SettingsWindow", "Fields data manual entry mode"))
        self.ButtonDefault.setText(_translate("SettingsWindow", "Set default"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QDialog()
    ui = Ui_SettingsWindow()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec())
