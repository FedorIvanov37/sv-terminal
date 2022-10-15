# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\spec_unsaved.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SpecUnsaved(object):
    def setupUi(self, SpecUnsaved):
        SpecUnsaved.setObjectName("SpecUnsaved")
        SpecUnsaved.setWindowModality(QtCore.Qt.ApplicationModal)
        SpecUnsaved.setEnabled(True)
        SpecUnsaved.resize(280, 81)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SpecUnsaved.sizePolicy().hasHeightForWidth())
        SpecUnsaved.setSizePolicy(sizePolicy)
        SpecUnsaved.setMinimumSize(QtCore.QSize(280, 81))
        SpecUnsaved.setMaximumSize(QtCore.QSize(280, 81))
        SpecUnsaved.setSizeGripEnabled(False)
        SpecUnsaved.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(SpecUnsaved)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.LogoLabel = QtWidgets.QLabel(SpecUnsaved)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LogoLabel.sizePolicy().hasHeightForWidth())
        self.LogoLabel.setSizePolicy(sizePolicy)
        self.LogoLabel.setMaximumSize(QtCore.QSize(30, 30))
        self.LogoLabel.setText("")
        self.LogoLabel.setPixmap(QtGui.QPixmap("../style/logo_triangle.png"))
        self.LogoLabel.setScaledContents(True)
        self.LogoLabel.setObjectName("LogoLabel")
        self.horizontalLayout_3.addWidget(self.LogoLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(SpecUnsaved)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ButtonSave = QtWidgets.QPushButton(SpecUnsaved)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonSave.sizePolicy().hasHeightForWidth())
        self.ButtonSave.setSizePolicy(sizePolicy)
        self.ButtonSave.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ButtonSave.setObjectName("ButtonSave")
        self.horizontalLayout.addWidget(self.ButtonSave)
        self.ButtonClose = QtWidgets.QPushButton(SpecUnsaved)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonClose.sizePolicy().hasHeightForWidth())
        self.ButtonClose.setSizePolicy(sizePolicy)
        self.ButtonClose.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ButtonClose.setObjectName("ButtonClose")
        self.horizontalLayout.addWidget(self.ButtonClose)
        self.ButtonReturn = QtWidgets.QPushButton(SpecUnsaved)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonReturn.sizePolicy().hasHeightForWidth())
        self.ButtonReturn.setSizePolicy(sizePolicy)
        self.ButtonReturn.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ButtonReturn.setObjectName("ButtonReturn")
        self.horizontalLayout.addWidget(self.ButtonReturn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SpecUnsaved)
        self.ButtonClose.clicked.connect(SpecUnsaved.reject)
        QtCore.QMetaObject.connectSlotsByName(SpecUnsaved)

    def retranslateUi(self, SpecUnsaved):
        _translate = QtCore.QCoreApplication.translate
        SpecUnsaved.setWindowTitle(_translate("SpecUnsaved", "Specification unsaved changes"))
        self.label_2.setText(_translate("SpecUnsaved", "Specification has unsaved changes"))
        self.ButtonSave.setText(_translate("SpecUnsaved", "Save"))
        self.ButtonClose.setText(_translate("SpecUnsaved", "Don't Save"))
        self.ButtonReturn.setText(_translate("SpecUnsaved", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SpecUnsaved = QtWidgets.QDialog()
    ui = Ui_SpecUnsaved()
    ui.setupUi(SpecUnsaved)
    SpecUnsaved.show()
    sys.exit(app.exec_())
