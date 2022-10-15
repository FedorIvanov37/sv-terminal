# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mti_spec.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MtiSpecWindow(object):
    def setupUi(self, MtiSpecWindow):
        MtiSpecWindow.setObjectName("MtiSpecWindow")
        MtiSpecWindow.setWindowModality(QtCore.Qt.NonModal)
        MtiSpecWindow.resize(620, 410)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MtiSpecWindow.sizePolicy().hasHeightForWidth())
        MtiSpecWindow.setSizePolicy(sizePolicy)
        MtiSpecWindow.setMinimumSize(QtCore.QSize(620, 410))
        MtiSpecWindow.setMaximumSize(QtCore.QSize(620, 410))
        MtiSpecWindow.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(MtiSpecWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.MtiTable = QtWidgets.QTableWidget(MtiSpecWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.MtiTable.setFont(font)
        self.MtiTable.setFocusPolicy(QtCore.Qt.NoFocus)
        self.MtiTable.setAutoFillBackground(False)
        self.MtiTable.setGridStyle(QtCore.Qt.SolidLine)
        self.MtiTable.setCornerButtonEnabled(True)
        self.MtiTable.setObjectName("MtiTable")
        self.MtiTable.setColumnCount(5)
        self.MtiTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.MtiTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.MtiTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.MtiTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.MtiTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.MtiTable.setHorizontalHeaderItem(4, item)
        self.MtiTable.horizontalHeader().setCascadingSectionResizes(True)
        self.MtiTable.horizontalHeader().setHighlightSections(False)
        self.MtiTable.verticalHeader().setVisible(True)
        self.MtiTable.verticalHeader().setCascadingSectionResizes(True)
        self.MtiTable.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.MtiTable, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ButtonPlus = QtWidgets.QPushButton(MtiSpecWindow)
        self.ButtonPlus.setObjectName("ButtonPlus")
        self.horizontalLayout.addWidget(self.ButtonPlus)
        self.ButtonMinus = QtWidgets.QPushButton(MtiSpecWindow)
        self.ButtonMinus.setObjectName("ButtonMinus")
        self.horizontalLayout.addWidget(self.ButtonMinus)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.ButtonSave = QtWidgets.QPushButton(MtiSpecWindow)
        self.ButtonSave.setObjectName("ButtonSave")
        self.horizontalLayout.addWidget(self.ButtonSave)
        self.ButtonCancel = QtWidgets.QPushButton(MtiSpecWindow)
        self.ButtonCancel.setObjectName("ButtonCancel")
        self.horizontalLayout.addWidget(self.ButtonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MtiSpecWindow)
        QtCore.QMetaObject.connectSlotsByName(MtiSpecWindow)

    def retranslateUi(self, MtiSpecWindow):
        _translate = QtCore.QCoreApplication.translate
        MtiSpecWindow.setWindowTitle(_translate("MtiSpecWindow", "Message Type Indicator"))
        item = self.MtiTable.horizontalHeaderItem(0)
        item.setText(_translate("MtiSpecWindow", "Description"))
        item = self.MtiTable.horizontalHeaderItem(1)
        item.setText(_translate("MtiSpecWindow", "Request"))
        item = self.MtiTable.horizontalHeaderItem(2)
        item.setText(_translate("MtiSpecWindow", "Response"))
        item = self.MtiTable.horizontalHeaderItem(3)
        item.setText(_translate("MtiSpecWindow", "Reversible"))
        item = self.MtiTable.horizontalHeaderItem(4)
        item.setText(_translate("MtiSpecWindow", "Reversal MTI"))
        self.ButtonPlus.setText(_translate("MtiSpecWindow", "+"))
        self.ButtonMinus.setText(_translate("MtiSpecWindow", "-"))
        self.ButtonSave.setText(_translate("MtiSpecWindow", "Save"))
        self.ButtonCancel.setText(_translate("MtiSpecWindow", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MtiSpecWindow = QtWidgets.QDialog()
    ui = Ui_MtiSpecWindow()
    ui.setupUi(MtiSpecWindow)
    MtiSpecWindow.show()
    sys.exit(app.exec_())
