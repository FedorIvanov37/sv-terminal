# Form implementation generated from reading ui file '.\spec.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SpecificationWindow(object):
    def setupUi(self, SpecificationWindow):
        SpecificationWindow.setObjectName("SpecificationWindow")
        SpecificationWindow.resize(1200, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SpecificationWindow.sizePolicy().hasHeightForWidth())
        SpecificationWindow.setSizePolicy(sizePolicy)
        SpecificationWindow.setMinimumSize(QtCore.QSize(1200, 700))
        SpecificationWindow.setMaximumSize(QtCore.QSize(1200, 700))
        self.gridLayout = QtWidgets.QGridLayout(SpecificationWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(parent=SpecificationWindow)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.StatusLabel = QtWidgets.QLabel(parent=SpecificationWindow)
        self.StatusLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse|QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.StatusLabel.setObjectName("StatusLabel")
        self.horizontalLayout_3.addWidget(self.StatusLabel)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(1164, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.CheckBoxReadOnly = QtWidgets.QCheckBox(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxReadOnly.setFont(font)
        self.CheckBoxReadOnly.setObjectName("CheckBoxReadOnly")
        self.gridLayout.addWidget(self.CheckBoxReadOnly, 1, 0, 1, 1)
        self.CheckBoxHideReverved = QtWidgets.QCheckBox(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.CheckBoxHideReverved.setFont(font)
        self.CheckBoxHideReverved.setChecked(False)
        self.CheckBoxHideReverved.setTristate(False)
        self.CheckBoxHideReverved.setObjectName("CheckBoxHideReverved")
        self.gridLayout.addWidget(self.CheckBoxHideReverved, 2, 0, 1, 1)
        self.SpecTree = QtWidgets.QTreeWidget(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.SpecTree.setFont(font)
        self.SpecTree.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.SpecTree.setDragEnabled(True)
        self.SpecTree.setDragDropOverwriteMode(True)
        self.SpecTree.setAlternatingRowColors(True)
        self.SpecTree.setAnimated(True)
        self.SpecTree.setAllColumnsShowFocus(True)
        self.SpecTree.setObjectName("SpecTree")
        self.SpecTree.headerItem().setText(0, "1")
        self.gridLayout.addWidget(self.SpecTree, 3, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
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
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.SearchLine = QtWidgets.QLineEdit(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.SearchLine.setFont(font)
        self.SearchLine.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhLatinOnly)
        self.SearchLine.setMaxLength(128)
        self.SearchLine.setReadOnly(False)
        self.SearchLine.setClearButtonEnabled(True)
        self.SearchLine.setObjectName("SearchLine")
        self.horizontalLayout_2.addWidget(self.SearchLine)
        self.ButtonSetMti = QtWidgets.QPushButton(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonSetMti.setFont(font)
        self.ButtonSetMti.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonSetMti.setObjectName("ButtonSetMti")
        self.horizontalLayout_2.addWidget(self.ButtonSetMti)
        self.ButtonApply = QtWidgets.QPushButton(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonApply.setFont(font)
        self.ButtonApply.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonApply.setObjectName("ButtonApply")
        self.horizontalLayout_2.addWidget(self.ButtonApply)
        self.ButtonReset = QtWidgets.QPushButton(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonReset.setFont(font)
        self.ButtonReset.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonReset.setObjectName("ButtonReset")
        self.horizontalLayout_2.addWidget(self.ButtonReset)
        self.ButtonBackup = QtWidgets.QPushButton(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonBackup.setFont(font)
        self.ButtonBackup.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonBackup.setObjectName("ButtonBackup")
        self.horizontalLayout_2.addWidget(self.ButtonBackup)
        self.ParseFile = QtWidgets.QPushButton(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ParseFile.setFont(font)
        self.ParseFile.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ParseFile.setObjectName("ParseFile")
        self.horizontalLayout_2.addWidget(self.ParseFile)
        self.ButtonClean = QtWidgets.QPushButton(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonClean.setFont(font)
        self.ButtonClean.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonClean.setObjectName("ButtonClean")
        self.horizontalLayout_2.addWidget(self.ButtonClean)
        self.ButtonClose = QtWidgets.QPushButton(parent=SpecificationWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonClose.setFont(font)
        self.ButtonClose.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonClose.setObjectName("ButtonClose")
        self.horizontalLayout_2.addWidget(self.ButtonClose)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 2)

        self.retranslateUi(SpecificationWindow)
        QtCore.QMetaObject.connectSlotsByName(SpecificationWindow)

    def retranslateUi(self, SpecificationWindow):
        _translate = QtCore.QCoreApplication.translate
        SpecificationWindow.setWindowTitle(_translate("SpecificationWindow", "Specification"))
        self.label.setText(_translate("SpecificationWindow", "Status:"))
        self.StatusLabel.setText(_translate("SpecificationWindow", ">"))
        self.CheckBoxReadOnly.setText(_translate("SpecificationWindow", "Read only mode"))
        self.CheckBoxHideReverved.setText(_translate("SpecificationWindow", "Hide reserved for future"))
        self.SearchLine.setPlaceholderText(_translate("SpecificationWindow", "Search: text | Goto: field path"))
        self.ButtonSetMti.setText(_translate("SpecificationWindow", "Set MTI"))
        self.ButtonApply.setText(_translate("SpecificationWindow", "Apply"))
        self.ButtonReset.setText(_translate("SpecificationWindow", "Reset"))
        self.ButtonBackup.setText(_translate("SpecificationWindow", "Backup"))
        self.ParseFile.setText(_translate("SpecificationWindow", "Parse file"))
        self.ButtonClean.setText(_translate("SpecificationWindow", "Clean"))
        self.ButtonClose.setText(_translate("SpecificationWindow", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SpecificationWindow = QtWidgets.QDialog()
    ui = Ui_SpecificationWindow()
    ui.setupUi(SpecificationWindow)
    SpecificationWindow.show()
    sys.exit(app.exec())
