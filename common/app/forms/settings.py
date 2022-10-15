# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(300, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsWindow.sizePolicy().hasHeightForWidth())
        SettingsWindow.setSizePolicy(sizePolicy)
        SettingsWindow.setMinimumSize(QtCore.QSize(300, 450))
        SettingsWindow.setMaximumSize(QtCore.QSize(300, 450))
        SettingsWindow.setWhatsThis("")
        self.gridLayout_2 = QtWidgets.QGridLayout(SettingsWindow)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(SettingsWindow)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.SvAddress = QtWidgets.QLineEdit(self.groupBox)
        self.SvAddress.setObjectName("SvAddress")
        self.horizontalLayout_2.addWidget(self.SvAddress)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.SvPort = QtWidgets.QLineEdit(self.groupBox)
        self.SvPort.setMaximumSize(QtCore.QSize(55, 16777215))
        self.SvPort.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.SvPort.setMaxLength(5)
        self.SvPort.setObjectName("SvPort")
        self.horizontalLayout_2.addWidget(self.SvPort)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.ApiUrl = QtWidgets.QLineEdit(self.groupBox)
        self.ApiUrl.setEnabled(False)
        self.ApiUrl.setReadOnly(True)
        self.ApiUrl.setObjectName("ApiUrl")
        self.horizontalLayout_3.addWidget(self.ApiUrl)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.ApiPort = QtWidgets.QLineEdit(self.groupBox)
        self.ApiPort.setMaximumSize(QtCore.QSize(55, 16777215))
        self.ApiPort.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.ApiPort.setMaxLength(5)
        self.ApiPort.setObjectName("ApiPort")
        self.horizontalLayout_3.addWidget(self.ApiPort)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(SettingsWindow)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.RunApi = QtWidgets.QCheckBox(self.groupBox_3)
        self.RunApi.setObjectName("RunApi")
        self.verticalLayout_5.addWidget(self.RunApi)
        self.ConnectOnStartup = QtWidgets.QCheckBox(self.groupBox_3)
        self.ConnectOnStartup.setObjectName("ConnectOnStartup")
        self.verticalLayout_5.addWidget(self.ConnectOnStartup)
        self.ProcessDefaultDump = QtWidgets.QCheckBox(self.groupBox_3)
        self.ProcessDefaultDump.setObjectName("ProcessDefaultDump")
        self.verticalLayout_5.addWidget(self.ProcessDefaultDump)
        self.gridLayout_2.addWidget(self.groupBox_3, 1, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(SettingsWindow)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.groupBox_2.setPalette(palette)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.DebugLevel = QtWidgets.QComboBox(self.groupBox_2)
        self.DebugLevel.setObjectName("DebugLevel")
        self.horizontalLayout_4.addWidget(self.DebugLevel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.ClearLog = QtWidgets.QCheckBox(self.groupBox_2)
        self.ClearLog.setObjectName("ClearLog")
        self.verticalLayout_3.addWidget(self.ClearLog)
        self.ParseSubfields = QtWidgets.QCheckBox(self.groupBox_2)
        self.ParseSubfields.setObjectName("ParseSubfields")
        self.verticalLayout_3.addWidget(self.ParseSubfields)
        self.gridLayout_2.addWidget(self.groupBox_2, 2, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(SettingsWindow)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.MaxAmount = QtWidgets.QLineEdit(self.groupBox_4)
        self.MaxAmount.setMaxLength(12)
        self.MaxAmount.setObjectName("MaxAmount")
        self.horizontalLayout.addWidget(self.MaxAmount)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.BuildFld90 = QtWidgets.QCheckBox(self.groupBox_4)
        self.BuildFld90.setObjectName("BuildFld90")
        self.gridLayout_3.addWidget(self.BuildFld90, 2, 0, 1, 1)
        self.SendInternalId = QtWidgets.QCheckBox(self.groupBox_4)
        self.SendInternalId.setObjectName("SendInternalId")
        self.gridLayout_3.addWidget(self.SendInternalId, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_4, 3, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_5.addWidget(self.buttonBox)
        spacerItem2 = QtWidgets.QSpacerItem(54, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.ButtonAbout = QtWidgets.QPushButton(SettingsWindow)
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
        self.groupBox.setTitle(_translate("SettingsWindow", "Connection"))
        self.label_3.setText(_translate("SettingsWindow", "SmartVista"))
        self.SvAddress.setPlaceholderText(_translate("SettingsWindow", "SV address"))
        self.label_2.setText(_translate("SettingsWindow", ":"))
        self.SvPort.setPlaceholderText(_translate("SettingsWindow", "port"))
        self.label_5.setText(_translate("SettingsWindow", "API URL    "))
        self.ApiUrl.setText(_translate("SettingsWindow", "http://127.0.0.1"))
        self.ApiUrl.setPlaceholderText(_translate("SettingsWindow", "API URL"))
        self.label_6.setText(_translate("SettingsWindow", ":"))
        self.ApiPort.setPlaceholderText(_translate("SettingsWindow", "port"))
        self.groupBox_3.setTitle(_translate("SettingsWindow", "On startup"))
        self.RunApi.setText(_translate("SettingsWindow", "Run API"))
        self.ConnectOnStartup.setText(_translate("SettingsWindow", "Open SV connection"))
        self.ProcessDefaultDump.setText(_translate("SettingsWindow", "Process default file"))
        self.groupBox_2.setTitle(_translate("SettingsWindow", "Log"))
        self.label_4.setText(_translate("SettingsWindow", "Debug level"))
        self.ClearLog.setText(_translate("SettingsWindow", "Clear log before sent message"))
        self.ParseSubfields.setText(_translate("SettingsWindow", "Parse subfields"))
        self.groupBox_4.setTitle(_translate("SettingsWindow", "Fields"))
        self.label.setText(_translate("SettingsWindow", "Max amount"))
        self.MaxAmount.setPlaceholderText(_translate("SettingsWindow", "Amount"))
        self.BuildFld90.setText(_translate("SettingsWindow", "Build Original Data Elements (Field 90) in Reversal"))
        self.SendInternalId.setText(_translate("SettingsWindow", "Send internal transaction ID to SV"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QDialog()
    ui = Ui_SettingsWindow()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec_())
