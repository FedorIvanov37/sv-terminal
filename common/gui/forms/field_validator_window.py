# Form implementation generated from reading ui file '.\field_validator_window.ui'
#
# Created by: PyQt6 UI code generator 6.5.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FieldDataSet(object):
    def setupUi(self, FieldDataSet):
        FieldDataSet.setObjectName("FieldDataSet")
        FieldDataSet.resize(470, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FieldDataSet.sizePolicy().hasHeightForWidth())
        FieldDataSet.setSizePolicy(sizePolicy)
        FieldDataSet.setMinimumSize(QtCore.QSize(470, 700))
        FieldDataSet.setMaximumSize(QtCore.QSize(470, 700))
        FieldDataSet.setModal(False)
        self.gridLayout_3 = QtWidgets.QGridLayout(FieldDataSet)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(parent=FieldDataSet)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.CheckBoxAlpha = QtWidgets.QCheckBox(parent=self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxAlpha.setFont(font)
        self.CheckBoxAlpha.setObjectName("CheckBoxAlpha")
        self.gridLayout_2.addWidget(self.CheckBoxAlpha, 0, 0, 1, 1)
        self.CheckBoxSpecial = QtWidgets.QCheckBox(parent=self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxSpecial.setFont(font)
        self.CheckBoxSpecial.setObjectName("CheckBoxSpecial")
        self.gridLayout_2.addWidget(self.CheckBoxSpecial, 2, 0, 1, 1)
        self.CheckBoxNumeric = QtWidgets.QCheckBox(parent=self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxNumeric.setFont(font)
        self.CheckBoxNumeric.setObjectName("CheckBoxNumeric")
        self.gridLayout_2.addWidget(self.CheckBoxNumeric, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(parent=FieldDataSet)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setAutoFillBackground(True)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.MinLengthLabel = QtWidgets.QLabel(parent=self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.MinLengthLabel.setFont(font)
        self.MinLengthLabel.setObjectName("MinLengthLabel")
        self.horizontalLayout_5.addWidget(self.MinLengthLabel)
        self.MinLength = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.MinLength.setObjectName("MinLength")
        self.horizontalLayout_5.addWidget(self.MinLength)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.MaxLengthLabel = QtWidgets.QLabel(parent=self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.MaxLengthLabel.setFont(font)
        self.MaxLengthLabel.setObjectName("MaxLengthLabel")
        self.horizontalLayout_2.addWidget(self.MaxLengthLabel)
        self.MaxLength = QtWidgets.QSpinBox(parent=self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.MaxLength.setFont(font)
        self.MaxLength.setObjectName("MaxLength")
        self.horizontalLayout_2.addWidget(self.MaxLength)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.DataLengthLabel = QtWidgets.QLabel(parent=self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.DataLengthLabel.setFont(font)
        self.DataLengthLabel.setObjectName("DataLengthLabel")
        self.horizontalLayout_3.addWidget(self.DataLengthLabel)
        self.DataLength = QtWidgets.QSpinBox(parent=self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.DataLength.setFont(font)
        self.DataLength.setObjectName("DataLength")
        self.horizontalLayout_3.addWidget(self.DataLength)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.TagLengthLabel = QtWidgets.QLabel(parent=self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.TagLengthLabel.setFont(font)
        self.TagLengthLabel.setObjectName("TagLengthLabel")
        self.horizontalLayout_4.addWidget(self.TagLengthLabel)
        self.TagLength = QtWidgets.QSpinBox(parent=self.groupBox_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.TagLength.setFont(font)
        self.TagLength.setObjectName("TagLength")
        self.horizontalLayout_4.addWidget(self.TagLength)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.gridLayout_3.addWidget(self.groupBox_4, 1, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=FieldDataSet)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAutoFillBackground(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.CheckBoxReversal = QtWidgets.QCheckBox(parent=self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxReversal.setFont(font)
        self.CheckBoxReversal.setObjectName("CheckBoxReversal")
        self.gridLayout_4.addWidget(self.CheckBoxReversal, 2, 0, 1, 1)
        self.CheckBoxMatching = QtWidgets.QCheckBox(parent=self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxMatching.setFont(font)
        self.CheckBoxMatching.setObjectName("CheckBoxMatching")
        self.gridLayout_4.addWidget(self.CheckBoxMatching, 1, 0, 1, 1)
        self.CheckBoxSecret = QtWidgets.QCheckBox(parent=self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxSecret.setFont(font)
        self.CheckBoxSecret.setObjectName("CheckBoxSecret")
        self.gridLayout_4.addWidget(self.CheckBoxSecret, 4, 0, 1, 1)
        self.CheckBoxGeneratible = QtWidgets.QCheckBox(parent=self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxGeneratible.setFont(font)
        self.CheckBoxGeneratible.setObjectName("CheckBoxGeneratible")
        self.gridLayout_4.addWidget(self.CheckBoxGeneratible, 3, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 2, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(parent=FieldDataSet)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setAutoFillBackground(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_8.addWidget(self.label_2)
        self.FillSide = QtWidgets.QComboBox(parent=self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FillSide.sizePolicy().hasHeightForWidth())
        self.FillSide.setSizePolicy(sizePolicy)
        self.FillSide.setMinimumSize(QtCore.QSize(120, 0))
        self.FillSide.setMaximumSize(QtCore.QSize(120, 50))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.FillSide.setFont(font)
        self.FillSide.setObjectName("FillSide")
        self.FillSide.addItem("")
        self.FillSide.addItem("")
        self.FillSide.addItem("")
        self.horizontalLayout_8.addWidget(self.FillSide)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.FillUpToLabel = QtWidgets.QLabel(parent=self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.FillUpToLabel.setFont(font)
        self.FillUpToLabel.setObjectName("FillUpToLabel")
        self.horizontalLayout_9.addWidget(self.FillUpToLabel)
        self.FillUpTo = QtWidgets.QComboBox(parent=self.groupBox_3)
        self.FillUpTo.setMinimumSize(QtCore.QSize(120, 0))
        self.FillUpTo.setMaximumSize(QtCore.QSize(120, 50))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.FillUpTo.setFont(font)
        self.FillUpTo.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhDigitsOnly)
        self.FillUpTo.setEditable(True)
        self.FillUpTo.setObjectName("FillUpTo")
        self.FillUpTo.addItem("")
        self.FillUpTo.addItem("")
        self.FillUpTo.addItem("")
        self.horizontalLayout_9.addWidget(self.FillUpTo)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.FillSymbolLabel = QtWidgets.QLabel(parent=self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.FillSymbolLabel.setFont(font)
        self.FillSymbolLabel.setObjectName("FillSymbolLabel")
        self.horizontalLayout_10.addWidget(self.FillSymbolLabel)
        self.FillSymbol = QtWidgets.QLineEdit(parent=self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FillSymbol.sizePolicy().hasHeightForWidth())
        self.FillSymbol.setSizePolicy(sizePolicy)
        self.FillSymbol.setMinimumSize(QtCore.QSize(120, 0))
        self.FillSymbol.setMaximumSize(QtCore.QSize(120, 50))
        self.FillSymbol.setMaxLength(1)
        self.FillSymbol.setObjectName("FillSymbol")
        self.horizontalLayout_10.addWidget(self.FillSymbol)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.gridLayout_3.addWidget(self.groupBox_3, 2, 1, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(parent=FieldDataSet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setAutoFillBackground(True)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout.setObjectName("gridLayout")
        self.CheckTypeLayout = QtWidgets.QHBoxLayout()
        self.CheckTypeLayout.setObjectName("CheckTypeLayout")
        self.gridLayout.addLayout(self.CheckTypeLayout, 0, 0, 1, 1)
        self.ValuesList = QtWidgets.QListWidget(parent=self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ValuesList.sizePolicy().hasHeightForWidth())
        self.ValuesList.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.ValuesList.setFont(font)
        self.ValuesList.setAlternatingRowColors(True)
        self.ValuesList.setViewMode(QtWidgets.QListView.ViewMode.ListMode)
        self.ValuesList.setObjectName("ValuesList")
        self.gridLayout.addWidget(self.ValuesList, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.PlusButton = QtWidgets.QPushButton(parent=self.groupBox_6)
        self.PlusButton.setMaximumSize(QtCore.QSize(40, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlusButton.setFont(font)
        self.PlusButton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.PlusButton.setObjectName("PlusButton")
        self.horizontalLayout.addWidget(self.PlusButton)
        self.MinusButton = QtWidgets.QPushButton(parent=self.groupBox_6)
        self.MinusButton.setMaximumSize(QtCore.QSize(55, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.MinusButton.setFont(font)
        self.MinusButton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.MinusButton.setObjectName("MinusButton")
        self.horizontalLayout.addWidget(self.MinusButton)
        self.ButtonClear = QtWidgets.QPushButton(parent=self.groupBox_6)
        self.ButtonClear.setMaximumSize(QtCore.QSize(45, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ButtonClear.setFont(font)
        self.ButtonClear.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonClear.setObjectName("ButtonClear")
        self.horizontalLayout.addWidget(self.ButtonClear)
        self.ButtonClearAll = QtWidgets.QPushButton(parent=self.groupBox_6)
        self.ButtonClearAll.setMaximumSize(QtCore.QSize(55, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ButtonClearAll.setFont(font)
        self.ButtonClearAll.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonClearAll.setObjectName("ButtonClearAll")
        self.horizontalLayout.addWidget(self.ButtonClearAll)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_6, 3, 0, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(parent=FieldDataSet)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setAutoFillBackground(True)
        self.groupBox_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.FieldTypeBoxLayout = QtWidgets.QHBoxLayout()
        self.FieldTypeBoxLayout.setObjectName("FieldTypeBoxLayout")
        self.verticalLayout.addLayout(self.FieldTypeBoxLayout)
        self.FieldTypeLayout = QtWidgets.QGridLayout()
        self.FieldTypeLayout.setObjectName("FieldTypeLayout")
        self.verticalLayout.addLayout(self.FieldTypeLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.gridLayout_3.addWidget(self.groupBox_5, 3, 1, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.OkButton = QtWidgets.QPushButton(parent=FieldDataSet)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.OkButton.setFont(font)
        self.OkButton.setObjectName("OkButton")
        self.horizontalLayout_11.addWidget(self.OkButton)
        self.CancelButton = QtWidgets.QPushButton(parent=FieldDataSet)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CancelButton.setFont(font)
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout_11.addWidget(self.CancelButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem3)
        self.gridLayout_3.addLayout(self.horizontalLayout_11, 4, 0, 1, 2)
        self.FieldDescription = QtWidgets.QLabel(parent=FieldDataSet)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.FieldDescription.setFont(font)
        self.FieldDescription.setWordWrap(True)
        self.FieldDescription.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.FieldDescription.setObjectName("FieldDescription")
        self.gridLayout_3.addWidget(self.FieldDescription, 0, 0, 1, 2)

        self.retranslateUi(FieldDataSet)
        QtCore.QMetaObject.connectSlotsByName(FieldDataSet)

    def retranslateUi(self, FieldDataSet):
        _translate = QtCore.QCoreApplication.translate
        FieldDataSet.setWindowTitle(_translate("FieldDataSet", "Field Settings"))
        self.groupBox.setTitle(_translate("FieldDataSet", "Field Charset"))
        self.CheckBoxAlpha.setText(_translate("FieldDataSet", "Alphabetic"))
        self.CheckBoxSpecial.setText(_translate("FieldDataSet", "Special"))
        self.CheckBoxNumeric.setText(_translate("FieldDataSet", "Numeric"))
        self.groupBox_4.setTitle(_translate("FieldDataSet", "Field Length"))
        self.MinLengthLabel.setText(_translate("FieldDataSet", "Min Lenght"))
        self.MaxLengthLabel.setText(_translate("FieldDataSet", "Max Lenght"))
        self.DataLengthLabel.setText(_translate("FieldDataSet", "Data length"))
        self.TagLengthLabel.setText(_translate("FieldDataSet", "Tag length"))
        self.groupBox_2.setTitle(_translate("FieldDataSet", "Field Usage"))
        self.CheckBoxReversal.setText(_translate("FieldDataSet", "Use field for reversal"))
        self.CheckBoxMatching.setText(_translate("FieldDataSet", "Use field for matching"))
        self.CheckBoxSecret.setText(_translate("FieldDataSet", "Hide field value"))
        self.CheckBoxGeneratible.setText(_translate("FieldDataSet", "Field can be generated"))
        self.groupBox_3.setTitle(_translate("FieldDataSet", "Field Data Padding"))
        self.label_2.setText(_translate("FieldDataSet", "Pad side"))
        self.FillSide.setItemText(0, _translate("FieldDataSet", "Not set"))
        self.FillSide.setItemText(1, _translate("FieldDataSet", "Left Pad"))
        self.FillSide.setItemText(2, _translate("FieldDataSet", "Right Pad"))
        self.FillUpToLabel.setText(_translate("FieldDataSet", "Pad to"))
        self.FillUpTo.setItemText(0, _translate("FieldDataSet", "Min Length"))
        self.FillUpTo.setItemText(1, _translate("FieldDataSet", "Max Length"))
        self.FillUpTo.setItemText(2, _translate("FieldDataSet", "Custom"))
        self.FillSymbolLabel.setText(_translate("FieldDataSet", "Pad by"))
        self.FillSymbol.setPlaceholderText(_translate("FieldDataSet", "Any letter"))
        self.groupBox_6.setTitle(_translate("FieldDataSet", "Field Custom Validation"))
        self.ValuesList.setSortingEnabled(True)
        self.PlusButton.setText(_translate("FieldDataSet", "Add"))
        self.MinusButton.setText(_translate("FieldDataSet", "Remove"))
        self.ButtonClear.setText(_translate("FieldDataSet", "Clear"))
        self.ButtonClearAll.setText(_translate("FieldDataSet", "Clear all"))
        self.groupBox_5.setTitle(_translate("FieldDataSet", "Field Type"))
        self.OkButton.setText(_translate("FieldDataSet", "OK"))
        self.CancelButton.setText(_translate("FieldDataSet", "Cancel"))
        self.FieldDescription.setText(_translate("FieldDataSet", "Field Description"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FieldDataSet = QtWidgets.QDialog()
    ui = Ui_FieldDataSet()
    ui.setupUi(FieldDataSet)
    FieldDataSet.show()
    sys.exit(app.exec())
