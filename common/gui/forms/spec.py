# Form implementation generated from reading ui file '.\common\gui\forms\spec.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SpecificationWindow(object):
    def setupUi(self, SpecificationWindow):
        SpecificationWindow.setObjectName("SpecificationWindow")
        SpecificationWindow.resize(1150, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SpecificationWindow.sizePolicy().hasHeightForWidth())
        SpecificationWindow.setSizePolicy(sizePolicy)
        SpecificationWindow.setMinimumSize(QtCore.QSize(1150, 700))
        SpecificationWindow.setMaximumSize(QtCore.QSize(1150, 700))
        self.gridLayout = QtWidgets.QGridLayout(SpecificationWindow)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(1164, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
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
        self.CheckBoxHideReverved = QtWidgets.QCheckBox(parent=SpecificationWindow)
        self.CheckBoxHideReverved.setChecked(False)
        self.CheckBoxHideReverved.setTristate(False)
        self.CheckBoxHideReverved.setObjectName("CheckBoxHideReverved")
        self.gridLayout.addWidget(self.CheckBoxHideReverved, 2, 0, 1, 1)
        self.SpecTree = QtWidgets.QTreeWidget(parent=SpecificationWindow)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 59))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 59))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush)
        self.SpecTree.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        self.SpecTree.setFont(font)
        self.SpecTree.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.SpecTree.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.SpecTree.setStyleSheet("QTreeWidget:item:selected:active {background-color: rgb(190, 235, 255)}\n"
"QTextEdit { selection-color: rgb(155, 155, 255) }\n"
"")
        self.SpecTree.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.SpecTree.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.SpecTree.setTabKeyNavigation(True)
        self.SpecTree.setDragEnabled(True)
        self.SpecTree.setDragDropOverwriteMode(True)
        self.SpecTree.setAlternatingRowColors(True)
        self.SpecTree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.SpecTree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.SpecTree.setRootIsDecorated(True)
        self.SpecTree.setUniformRowHeights(True)
        self.SpecTree.setAnimated(True)
        self.SpecTree.setAllColumnsShowFocus(True)
        self.SpecTree.setHeaderHidden(False)
        self.SpecTree.setColumnCount(0)
        self.SpecTree.setObjectName("SpecTree")
        self.SpecTree.header().setHighlightSections(True)
        self.gridLayout.addWidget(self.SpecTree, 4, 0, 1, 2)
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
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.ButtonSetMti = QtWidgets.QPushButton(parent=SpecificationWindow)
        self.ButtonSetMti.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonSetMti.setObjectName("ButtonSetMti")
        self.horizontalLayout_2.addWidget(self.ButtonSetMti)
        self.ButtonApply = QtWidgets.QPushButton(parent=SpecificationWindow)
        self.ButtonApply.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonApply.setObjectName("ButtonApply")
        self.horizontalLayout_2.addWidget(self.ButtonApply)
        self.ButtonReset = QtWidgets.QPushButton(parent=SpecificationWindow)
        self.ButtonReset.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonReset.setObjectName("ButtonReset")
        self.horizontalLayout_2.addWidget(self.ButtonReset)
        self.ButtonBackup = QtWidgets.QPushButton(parent=SpecificationWindow)
        self.ButtonBackup.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonBackup.setObjectName("ButtonBackup")
        self.horizontalLayout_2.addWidget(self.ButtonBackup)
        self.ParseFile = QtWidgets.QPushButton(parent=SpecificationWindow)
        self.ParseFile.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ParseFile.setObjectName("ParseFile")
        self.horizontalLayout_2.addWidget(self.ParseFile)
        self.ButtonClean = QtWidgets.QPushButton(parent=SpecificationWindow)
        self.ButtonClean.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonClean.setObjectName("ButtonClean")
        self.horizontalLayout_2.addWidget(self.ButtonClean)
        self.ButtonClose = QtWidgets.QPushButton(parent=SpecificationWindow)
        self.ButtonClose.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ButtonClose.setObjectName("ButtonClose")
        self.horizontalLayout_2.addWidget(self.ButtonClose)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 0, 1, 2)
        self.CheckBoxReadOnly = QtWidgets.QCheckBox(parent=SpecificationWindow)
        self.CheckBoxReadOnly.setObjectName("CheckBoxReadOnly")
        self.gridLayout.addWidget(self.CheckBoxReadOnly, 1, 0, 1, 1)

        self.retranslateUi(SpecificationWindow)
        QtCore.QMetaObject.connectSlotsByName(SpecificationWindow)

    def retranslateUi(self, SpecificationWindow):
        _translate = QtCore.QCoreApplication.translate
        SpecificationWindow.setWindowTitle(_translate("SpecificationWindow", "Specification"))
        self.label.setText(_translate("SpecificationWindow", "Status:"))
        self.StatusLabel.setText(_translate("SpecificationWindow", ">"))
        self.CheckBoxHideReverved.setText(_translate("SpecificationWindow", "Hide reserved for future"))
        self.SpecTree.setSortingEnabled(True)
        self.ButtonSetMti.setText(_translate("SpecificationWindow", "Set MTI"))
        self.ButtonApply.setText(_translate("SpecificationWindow", "Apply"))
        self.ButtonReset.setText(_translate("SpecificationWindow", "Reset"))
        self.ButtonBackup.setText(_translate("SpecificationWindow", "Backup"))
        self.ParseFile.setText(_translate("SpecificationWindow", "Parse file"))
        self.ButtonClean.setText(_translate("SpecificationWindow", "Clean"))
        self.ButtonClose.setText(_translate("SpecificationWindow", "Close"))
        self.CheckBoxReadOnly.setText(_translate("SpecificationWindow", "Read only mode"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SpecificationWindow = QtWidgets.QDialog()
    ui = Ui_SpecificationWindow()
    ui.setupUi(SpecificationWindow)
    SpecificationWindow.show()
    sys.exit(app.exec())
