# Form implementation generated from reading ui file '.\common\app\forms\reversal.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ReversalWindow(object):
    def setupUi(self, ReversalWindow):
        ReversalWindow.setObjectName("ReversalWindow")
        ReversalWindow.resize(350, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ReversalWindow.sizePolicy().hasHeightForWidth())
        ReversalWindow.setSizePolicy(sizePolicy)
        ReversalWindow.setMinimumSize(QtCore.QSize(350, 100))
        ReversalWindow.setMaximumSize(QtCore.QSize(350, 100))
        ReversalWindow.setModal(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ReversalWindow)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.TransactionIdField = QtWidgets.QLineEdit(parent=ReversalWindow)
        self.TransactionIdField.setObjectName("TransactionIdField")
        self.verticalLayout.addWidget(self.TransactionIdField)
        self.ComboBoxId = QtWidgets.QComboBox(parent=ReversalWindow)
        self.ComboBoxId.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ComboBoxId.setObjectName("ComboBoxId")
        self.verticalLayout.addWidget(self.ComboBoxId)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=ReversalWindow)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(ReversalWindow)
        self.buttonBox.accepted.connect(ReversalWindow.accept) # type: ignore
        self.buttonBox.rejected.connect(ReversalWindow.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ReversalWindow)

    def retranslateUi(self, ReversalWindow):
        _translate = QtCore.QCoreApplication.translate
        ReversalWindow.setWindowTitle(_translate("ReversalWindow", "Reversal"))
        self.TransactionIdField.setPlaceholderText(_translate("ReversalWindow", "ID of original transaction"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ReversalWindow = QtWidgets.QDialog()
    ui = Ui_ReversalWindow()
    ui.setupUi(ReversalWindow)
    ReversalWindow.show()
    sys.exit(app.exec())
