# Form implementation generated from reading ui file '.\fields_builder.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FieldsBuilder(object):
    def setupUi(self, FieldsBuilder):
        FieldsBuilder.setObjectName("FieldsBuilder")
        FieldsBuilder.resize(834, 598)
        self.gridLayout = QtWidgets.QGridLayout(FieldsBuilder)
        self.gridLayout.setObjectName("gridLayout")
        self.FieldNumberBox = QtWidgets.QComboBox(parent=FieldsBuilder)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.FieldNumberBox.setFont(font)
        self.FieldNumberBox.setObjectName("FieldNumberBox")
        self.gridLayout.addWidget(self.FieldNumberBox, 0, 0, 1, 1)
        self.JsonViewLayout = QtWidgets.QVBoxLayout()
        self.JsonViewLayout.setObjectName("JsonViewLayout")
        self.gridLayout.addLayout(self.JsonViewLayout, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ButtonPlus = QtWidgets.QPushButton(parent=FieldsBuilder)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.ButtonPlus.setFont(font)
        self.ButtonPlus.setObjectName("ButtonPlus")
        self.horizontalLayout.addWidget(self.ButtonPlus)
        self.ButtonMinus = QtWidgets.QPushButton(parent=FieldsBuilder)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.ButtonMinus.setFont(font)
        self.ButtonMinus.setObjectName("ButtonMinus")
        self.horizontalLayout.addWidget(self.ButtonMinus)
        self.ButtonNextLevel = QtWidgets.QPushButton(parent=FieldsBuilder)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.ButtonNextLevel.setFont(font)
        self.ButtonNextLevel.setObjectName("ButtonNextLevel")
        self.horizontalLayout.addWidget(self.ButtonNextLevel)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.SearchLine = QtWidgets.QLineEdit(parent=FieldsBuilder)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.SearchLine.setFont(font)
        self.SearchLine.setObjectName("SearchLine")
        self.horizontalLayout_3.addWidget(self.SearchLine)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.FIeldDataText = QtWidgets.QTextEdit(parent=FieldsBuilder)
        self.FIeldDataText.setMinimumSize(QtCore.QSize(0, 100))
        self.FIeldDataText.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.FIeldDataText.setFont(font)
        self.FIeldDataText.setObjectName("FIeldDataText")
        self.gridLayout.addWidget(self.FIeldDataText, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ButtonApply = QtWidgets.QPushButton(parent=FieldsBuilder)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.ButtonApply.setFont(font)
        self.ButtonApply.setObjectName("ButtonApply")
        self.horizontalLayout_2.addWidget(self.ButtonApply)
        self.ButtonDiscard = QtWidgets.QPushButton(parent=FieldsBuilder)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.ButtonDiscard.setFont(font)
        self.ButtonDiscard.setObjectName("ButtonDiscard")
        self.horizontalLayout_2.addWidget(self.ButtonDiscard)
        self.ButtonFromMessage = QtWidgets.QPushButton(parent=FieldsBuilder)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.ButtonFromMessage.setFont(font)
        self.ButtonFromMessage.setObjectName("ButtonFromMessage")
        self.horizontalLayout_2.addWidget(self.ButtonFromMessage)
        self.ButtonJsonToString = QtWidgets.QPushButton(parent=FieldsBuilder)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.ButtonJsonToString.setFont(font)
        self.ButtonJsonToString.setObjectName("ButtonJsonToString")
        self.horizontalLayout_2.addWidget(self.ButtonJsonToString)
        self.ButtonStringToJson = QtWidgets.QPushButton(parent=FieldsBuilder)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.ButtonStringToJson.setFont(font)
        self.ButtonStringToJson.setObjectName("ButtonStringToJson")
        self.horizontalLayout_2.addWidget(self.ButtonStringToJson)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)

        self.retranslateUi(FieldsBuilder)
        QtCore.QMetaObject.connectSlotsByName(FieldsBuilder)

    def retranslateUi(self, FieldsBuilder):
        _translate = QtCore.QCoreApplication.translate
        FieldsBuilder.setWindowTitle(_translate("FieldsBuilder", "Complex fields builder"))
        self.ButtonPlus.setText(_translate("FieldsBuilder", "+"))
        self.ButtonMinus.setText(_translate("FieldsBuilder", "-"))
        self.ButtonNextLevel.setText(_translate("FieldsBuilder", "="))
        self.SearchLine.setPlaceholderText(_translate("FieldsBuilder", "Search: field number | field description"))
        self.ButtonApply.setText(_translate("FieldsBuilder", "Apply"))
        self.ButtonDiscard.setText(_translate("FieldsBuilder", "Discard"))
        self.ButtonFromMessage.setText(_translate("FieldsBuilder", "From message"))
        self.ButtonJsonToString.setText(_translate("FieldsBuilder", "JSON to String"))
        self.ButtonStringToJson.setText(_translate("FieldsBuilder", "String to JSON"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FieldsBuilder = QtWidgets.QDialog()
    ui = Ui_FieldsBuilder()
    ui.setupUi(FieldsBuilder)
    FieldsBuilder.show()
    sys.exit(app.exec())
