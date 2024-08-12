# Form implementation generated from reading ui file '.\common\gui\forms\settings_window.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(400, 525)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsWindow.sizePolicy().hasHeightForWidth())
        SettingsWindow.setSizePolicy(sizePolicy)
        SettingsWindow.setMinimumSize(QtCore.QSize(400, 525))
        SettingsWindow.setMaximumSize(QtCore.QSize(400, 525))
        self.gridLayout_10 = QtWidgets.QGridLayout(SettingsWindow)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.MainTabs = QtWidgets.QTabWidget(parent=SettingsWindow)
        self.MainTabs.setObjectName("MainTabs")
        self.General = QtWidgets.QWidget()
        self.General.setObjectName("General")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.General)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ConnectionBox = QtWidgets.QGroupBox(parent=self.General)
        self.ConnectionBox.setObjectName("ConnectionBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.ConnectionBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.HeaderLengthMode = QtWidgets.QCheckBox(parent=self.ConnectionBox)
        self.HeaderLengthMode.setObjectName("HeaderLengthMode")
        self.horizontalLayout_6.addWidget(self.HeaderLengthMode)
        self.HeaderLength = QtWidgets.QSpinBox(parent=self.ConnectionBox)
        self.HeaderLength.setMinimumSize(QtCore.QSize(80, 0))
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
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.KeepAliveMode = QtWidgets.QCheckBox(parent=self.ConnectionBox)
        self.KeepAliveMode.setObjectName("KeepAliveMode")
        self.horizontalLayout_3.addWidget(self.KeepAliveMode)
        self.KeepAliveInterval = QtWidgets.QSpinBox(parent=self.ConnectionBox)
        self.KeepAliveInterval.setMinimumSize(QtCore.QSize(80, 20))
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
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
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
        self.SvPort.setMinimumSize(QtCore.QSize(80, 0))
        self.SvPort.setMinimum(1)
        self.SvPort.setMaximum(65535)
        self.SvPort.setObjectName("SvPort")
        self.horizontalLayout_2.addWidget(self.SvPort)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.ConnectionBox)
        self.LogBox = QtWidgets.QGroupBox(parent=self.General)
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
        self.ClearLog = QtWidgets.QCheckBox(parent=self.LogBox)
        self.ClearLog.setObjectName("ClearLog")
        self.gridLayout_6.addWidget(self.ClearLog, 4, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(parent=self.LogBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.DebugLevel = QtWidgets.QComboBox(parent=self.LogBox)
        self.DebugLevel.setObjectName("DebugLevel")
        self.horizontalLayout_4.addWidget(self.DebugLevel)
        self.gridLayout_6.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.LogBackupLabel = QtWidgets.QLabel(parent=self.LogBox)
        self.LogBackupLabel.setObjectName("LogBackupLabel")
        self.horizontalLayout_10.addWidget(self.LogBackupLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem1)
        self.LogStorageDepth = QtWidgets.QSpinBox(parent=self.LogBox)
        self.LogStorageDepth.setMaximum(999)
        self.LogStorageDepth.setObjectName("LogStorageDepth")
        self.horizontalLayout_10.addWidget(self.LogStorageDepth)
        self.gridLayout_6.addLayout(self.horizontalLayout_10, 3, 0, 1, 1)
        self.ParseSubfields = QtWidgets.QCheckBox(parent=self.LogBox)
        self.ParseSubfields.setObjectName("ParseSubfields")
        self.gridLayout_6.addWidget(self.ParseSubfields, 2, 0, 1, 1)
        self.ReduceKeepAlive = QtWidgets.QCheckBox(parent=self.LogBox)
        self.ReduceKeepAlive.setObjectName("ReduceKeepAlive")
        self.gridLayout_6.addWidget(self.ReduceKeepAlive, 5, 0, 1, 1)
        self.verticalLayout.addWidget(self.LogBox)
        self.OnStartupBox = QtWidgets.QGroupBox(parent=self.General)
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
        self.verticalLayout.addWidget(self.OnStartupBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.GeneralButtonBox = QtWidgets.QDialogButtonBox(parent=self.General)
        self.GeneralButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok|QtWidgets.QDialogButtonBox.StandardButton.RestoreDefaults)
        self.GeneralButtonBox.setObjectName("GeneralButtonBox")
        self.verticalLayout.addWidget(self.GeneralButtonBox)
        self.MainTabs.addTab(self.General, "")
        self.Fields = QtWidgets.QWidget()
        self.Fields.setObjectName("Fields")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.Fields)
        self.gridLayout_7.setObjectName("gridLayout_7")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_7.addItem(spacerItem3, 2, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(parent=self.Fields)
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
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem4)
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
        self.gridLayout_7.addWidget(self.groupBox, 1, 0, 1, 1)
        self.FieldsBox = QtWidgets.QGroupBox(parent=self.Fields)
        self.FieldsBox.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhDigitsOnly)
        self.FieldsBox.setObjectName("FieldsBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.FieldsBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.ManualInputMode = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.ManualInputMode.setObjectName("ManualInputMode")
        self.gridLayout_5.addWidget(self.ManualInputMode, 5, 0, 1, 1)
        self.JsonMode = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.JsonMode.setObjectName("JsonMode")
        self.gridLayout_5.addWidget(self.JsonMode, 3, 0, 1, 1)
        self.HideSecrets = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.HideSecrets.setObjectName("HideSecrets")
        self.gridLayout_5.addWidget(self.HideSecrets, 4, 0, 1, 1)
        self.SendInternalId = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.SendInternalId.setObjectName("SendInternalId")
        self.gridLayout_5.addWidget(self.SendInternalId, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MaxAmountBox = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.MaxAmountBox.setObjectName("MaxAmountBox")
        self.horizontalLayout.addWidget(self.MaxAmountBox)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
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
        self.BuildFld90 = QtWidgets.QCheckBox(parent=self.FieldsBox)
        self.BuildFld90.setObjectName("BuildFld90")
        self.gridLayout_5.addWidget(self.BuildFld90, 2, 0, 1, 1)
        self.gridLayout_7.addWidget(self.FieldsBox, 0, 0, 1, 1)
        self.FieldsButtonBox = QtWidgets.QDialogButtonBox(parent=self.Fields)
        self.FieldsButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok|QtWidgets.QDialogButtonBox.StandardButton.RestoreDefaults)
        self.FieldsButtonBox.setObjectName("FieldsButtonBox")
        self.gridLayout_7.addWidget(self.FieldsButtonBox, 3, 0, 1, 1)
        self.MainTabs.addTab(self.Fields, "")
        self.API = QtWidgets.QWidget()
        self.API.setObjectName("API")
        self.gridLayout = QtWidgets.QGridLayout(self.API)
        self.gridLayout.setObjectName("gridLayout")
        self.ApiInfoLabel = QtWidgets.QLabel(parent=self.API)
        self.ApiInfoLabel.setWordWrap(True)
        self.ApiInfoLabel.setOpenExternalLinks(False)
        self.ApiInfoLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ApiInfoLabel.setObjectName("ApiInfoLabel")
        self.gridLayout.addWidget(self.ApiInfoLabel, 3, 0, 1, 1)
        self.ApiButtonBox = QtWidgets.QDialogButtonBox(parent=self.API)
        self.ApiButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok|QtWidgets.QDialogButtonBox.StandardButton.RestoreDefaults)
        self.ApiButtonBox.setObjectName("ApiButtonBox")
        self.gridLayout.addWidget(self.ApiButtonBox, 6, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(parent=self.API)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 4, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem6, 2, 0, 1, 1)
        self.ApiBox = QtWidgets.QGroupBox(parent=self.API)
        self.ApiBox.setObjectName("ApiBox")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.ApiBox)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(parent=self.ApiBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.ApiPort = QtWidgets.QSpinBox(parent=self.ApiBox)
        self.ApiPort.setMinimumSize(QtCore.QSize(0, 0))
        self.ApiPort.setMinimum(1)
        self.ApiPort.setMaximum(65535)
        self.ApiPort.setObjectName("ApiPort")
        self.horizontalLayout_5.addWidget(self.ApiPort)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.gridLayout_9.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.WaitForRemoteHost = QtWidgets.QCheckBox(parent=self.ApiBox)
        self.WaitForRemoteHost.setObjectName("WaitForRemoteHost")
        self.gridLayout_9.addWidget(self.WaitForRemoteHost, 2, 0, 1, 1)
        self.ApiRun = QtWidgets.QCheckBox(parent=self.ApiBox)
        self.ApiRun.setObjectName("ApiRun")
        self.gridLayout_9.addWidget(self.ApiRun, 1, 0, 1, 1)
        self.HideSecretsApi = QtWidgets.QCheckBox(parent=self.ApiBox)
        self.HideSecretsApi.setObjectName("HideSecretsApi")
        self.gridLayout_9.addWidget(self.HideSecretsApi, 3, 0, 1, 1)
        self.ParseComplexFields = QtWidgets.QCheckBox(parent=self.ApiBox)
        self.ParseComplexFields.setObjectName("ParseComplexFields")
        self.gridLayout_9.addWidget(self.ParseComplexFields, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.ApiBox, 0, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.ApiAddress = QtWidgets.QLabel(parent=self.API)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setKerning(True)
        self.ApiAddress.setFont(font)
        self.ApiAddress.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ApiAddress.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.ApiAddress.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ApiAddress.setOpenExternalLinks(False)
        self.ApiAddress.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByKeyboard|QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse|QtCore.Qt.TextInteractionFlag.TextBrowserInteraction|QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ApiAddress.setObjectName("ApiAddress")
        self.horizontalLayout_11.addWidget(self.ApiAddress)
        self.gridLayout.addLayout(self.horizontalLayout_11, 1, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem8, 5, 0, 1, 1)
        self.MainTabs.addTab(self.API, "")
        self.Spec = QtWidgets.QWidget()
        self.Spec.setObjectName("Spec")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.Spec)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.SpecBox = QtWidgets.QGroupBox(parent=self.Spec)
        self.SpecBox.setObjectName("SpecBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.SpecBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.UrlLabel = QtWidgets.QLabel(parent=self.SpecBox)
        self.UrlLabel.setObjectName("UrlLabel")
        self.horizontalLayout_8.addWidget(self.UrlLabel)
        self.RemoteSpecUrl = QtWidgets.QLineEdit(parent=self.SpecBox)
        self.RemoteSpecUrl.setObjectName("RemoteSpecUrl")
        self.horizontalLayout_8.addWidget(self.RemoteSpecUrl)
        self.gridLayout_4.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.BackupStorageLabel = QtWidgets.QLabel(parent=self.SpecBox)
        self.BackupStorageLabel.setObjectName("BackupStorageLabel")
        self.horizontalLayout_7.addWidget(self.BackupStorageLabel)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem9)
        self.StorageDepth = QtWidgets.QSpinBox(parent=self.SpecBox)
        self.StorageDepth.setMaximum(999)
        self.StorageDepth.setObjectName("StorageDepth")
        self.horizontalLayout_7.addWidget(self.StorageDepth)
        self.gridLayout_4.addLayout(self.horizontalLayout_7, 4, 0, 1, 1)
        self.RewriteLocalSpec = QtWidgets.QCheckBox(parent=self.SpecBox)
        self.RewriteLocalSpec.setObjectName("RewriteLocalSpec")
        self.gridLayout_4.addWidget(self.RewriteLocalSpec, 2, 0, 1, 1)
        self.LoadSpec2 = QtWidgets.QCheckBox(parent=self.SpecBox)
        self.LoadSpec2.setObjectName("LoadSpec2")
        self.gridLayout_4.addWidget(self.LoadSpec2, 1, 0, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_4.addItem(spacerItem10, 5, 0, 1, 1)
        self.gridLayout_8.addWidget(self.SpecBox, 0, 0, 1, 1)
        self.SpecificationButtonBox = QtWidgets.QDialogButtonBox(parent=self.Spec)
        self.SpecificationButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok|QtWidgets.QDialogButtonBox.StandardButton.RestoreDefaults)
        self.SpecificationButtonBox.setObjectName("SpecificationButtonBox")
        self.gridLayout_8.addWidget(self.SpecificationButtonBox, 1, 0, 1, 1)
        self.MainTabs.addTab(self.Spec, "")
        self.About = QtWidgets.QWidget()
        self.About.setObjectName("About")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.About)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.frame = QtWidgets.QFrame(parent=self.About)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_11.setObjectName("gridLayout_11")
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_11.addItem(spacerItem11, 2, 1, 1, 1)
        self.line = QtWidgets.QFrame(parent=self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_11.addWidget(self.line, 3, 0, 1, 3)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.VersionLabel = QtWidgets.QLabel(parent=self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush)
        self.VersionLabel.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.VersionLabel.setFont(font)
        self.VersionLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.VersionLabel.setObjectName("VersionLabel")
        self.verticalLayout_2.addWidget(self.VersionLabel)
        self.ReleaseLabel = QtWidgets.QLabel(parent=self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush)
        self.ReleaseLabel.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.ReleaseLabel.setFont(font)
        self.ReleaseLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.ReleaseLabel.setObjectName("ReleaseLabel")
        self.verticalLayout_2.addWidget(self.ReleaseLabel)
        self.AuthorLabel = QtWidgets.QLabel(parent=self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush)
        self.AuthorLabel.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.AuthorLabel.setFont(font)
        self.AuthorLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.AuthorLabel.setObjectName("AuthorLabel")
        self.verticalLayout_2.addWidget(self.AuthorLabel)
        self.ContactLabel = QtWidgets.QLabel(parent=self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush)
        self.ContactLabel.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.ContactLabel.setFont(font)
        self.ContactLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.ContactLabel.setObjectName("ContactLabel")
        self.verticalLayout_2.addWidget(self.ContactLabel)
        self.horizontalLayout_13.addLayout(self.verticalLayout_2)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem12)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem13)
        self.MusicOnOfButton = QtWidgets.QPushButton(parent=self.frame)
        self.MusicOnOfButton.setMaximumSize(QtCore.QSize(30, 24))
        self.MusicOnOfButton.setText("")
        self.MusicOnOfButton.setObjectName("MusicOnOfButton")
        self.verticalLayout_4.addWidget(self.MusicOnOfButton)
        self.horizontalLayout_13.addLayout(self.verticalLayout_4)
        self.gridLayout_11.addLayout(self.horizontalLayout_13, 5, 0, 1, 3)
        spacerItem14 = QtWidgets.QSpacerItem(145, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_11.addItem(spacerItem14, 1, 2, 1, 1)
        self.logoLabel = QtWidgets.QLabel(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logoLabel.sizePolicy().hasHeightForWidth())
        self.logoLabel.setSizePolicy(sizePolicy)
        self.logoLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.logoLabel.setMaximumSize(QtCore.QSize(3000, 5000))
        self.logoLabel.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.logoLabel.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logoLabel.setObjectName("logoLabel")
        self.gridLayout_11.addWidget(self.logoLabel, 1, 1, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(146, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_11.addItem(spacerItem15, 1, 0, 1, 1)
        self.spacerLabel = QtWidgets.QLabel(parent=self.frame)
        self.spacerLabel.setText("")
        self.spacerLabel.setObjectName("spacerLabel")
        self.gridLayout_11.addWidget(self.spacerLabel, 4, 0, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_11.addItem(spacerItem16, 0, 1, 1, 1)
        self.gridLayout_12.addWidget(self.frame, 0, 0, 1, 1)
        self.MainTabs.addTab(self.About, "")
        self.gridLayout_10.addWidget(self.MainTabs, 0, 0, 1, 1)

        self.retranslateUi(SettingsWindow)
        self.MainTabs.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Signal | Configuration"))
        self.ConnectionBox.setTitle(_translate("SettingsWindow", "Remote host"))
        self.HeaderLengthMode.setText(_translate("SettingsWindow", "ISO Message header length"))
        self.HeaderLength.setWhatsThis(_translate("SettingsWindow", "Usually 2 or 4"))
        self.HeaderLength.setSuffix(_translate("SettingsWindow", " bytes"))
        self.KeepAliveMode.setText(_translate("SettingsWindow", "Keep-Alive message interval "))
        self.KeepAliveInterval.setSuffix(_translate("SettingsWindow", " sec"))
        self.IpLabel.setText(_translate("SettingsWindow", "IP"))
        self.SvAddress.setPlaceholderText(_translate("SettingsWindow", "Hostname or address"))
        self.PortLabel.setText(_translate("SettingsWindow", ":"))
        self.LogBox.setTitle(_translate("SettingsWindow", "Log"))
        self.ClearLog.setText(_translate("SettingsWindow", "Clear log before sent message"))
        self.label_4.setText(_translate("SettingsWindow", "Debug level"))
        self.LogBackupLabel.setText(_translate("SettingsWindow", "Logfile backup storage depth"))
        self.ParseSubfields.setText(_translate("SettingsWindow", "Parse subfields"))
        self.ReduceKeepAlive.setText(_translate("SettingsWindow", "Do not display Keep-Alive in log"))
        self.OnStartupBox.setTitle(_translate("SettingsWindow", "On startup"))
        self.ConnectOnStartup.setText(_translate("SettingsWindow", "Open connection"))
        self.ProcessDefaultDump.setText(_translate("SettingsWindow", "Process default file"))
        self.LoadSpec.setText(_translate("SettingsWindow", "Load remote specification"))
        self.ShowLicense.setText(_translate("SettingsWindow", "Show license dialog"))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.General), _translate("SettingsWindow", "General"))
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
        self.ManualInputMode.setText(_translate("SettingsWindow", "Fields data manual entry mode"))
        self.JsonMode.setText(_translate("SettingsWindow", "JSON-like fields representation "))
        self.HideSecrets.setText(_translate("SettingsWindow", "Hide secret fields"))
        self.SendInternalId.setText(_translate("SettingsWindow", "Send internal transaction ID to Host"))
        self.MaxAmountBox.setText(_translate("SettingsWindow", "Max generated amount"))
        self.MaxAmount.setItemText(0, _translate("SettingsWindow", "100"))
        self.MaxAmount.setItemText(1, _translate("SettingsWindow", "500"))
        self.MaxAmount.setItemText(2, _translate("SettingsWindow", "1500"))
        self.MaxAmount.setItemText(3, _translate("SettingsWindow", "10000"))
        self.MaxAmount.setItemText(4, _translate("SettingsWindow", "100000"))
        self.BuildFld90.setText(_translate("SettingsWindow", "Build field 90 in reversal"))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.Fields), _translate("SettingsWindow", "Fields"))
        self.ApiInfoLabel.setText(_translate("SettingsWindow", "<html><head/><body><p>Signal provides HTTP API for external integration. It also has a built-in Postman collection, which covers basic needs</p><p>Refer to the <a href=\"www.link.com\"><span style=\" text-decoration: underline; color:#0000ff;\">user reference guide</span></a> for details</p></body></html>"))
        self.ApiBox.setTitle(_translate("SettingsWindow", "API"))
        self.label_2.setText(_translate("SettingsWindow", "Local port"))
        self.WaitForRemoteHost.setText(_translate("SettingsWindow", "Wait for the remote host to respond"))
        self.ApiRun.setText(_translate("SettingsWindow", "Run API on startup (not recommended)"))
        self.HideSecretsApi.setText(_translate("SettingsWindow", "Hide secret fields in the responses"))
        self.ParseComplexFields.setText(_translate("SettingsWindow", "Split complex fields in response"))
        self.ApiAddress.setText(_translate("SettingsWindow", "ApiAddress"))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.API), _translate("SettingsWindow", "API"))
        self.SpecBox.setTitle(_translate("SettingsWindow", "Specification"))
        self.UrlLabel.setText(_translate("SettingsWindow", "URL"))
        self.RemoteSpecUrl.setPlaceholderText(_translate("SettingsWindow", "http://spec.example.url:7002/get_spec"))
        self.BackupStorageLabel.setText(_translate("SettingsWindow", "Specification backup storage depth"))
        self.RewriteLocalSpec.setText(_translate("SettingsWindow", "Overwrite local spec by remote one"))
        self.LoadSpec2.setText(_translate("SettingsWindow", "Load remote specification on startup"))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.Spec), _translate("SettingsWindow", "Specification"))
        self.VersionLabel.setText(_translate("SettingsWindow", "Version"))
        self.ReleaseLabel.setText(_translate("SettingsWindow", "Released in"))
        self.AuthorLabel.setText(_translate("SettingsWindow", "Developed by"))
        self.ContactLabel.setText(_translate("SettingsWindow", "Contact"))
        self.logoLabel.setText(_translate("SettingsWindow", "logo"))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.About), _translate("SettingsWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QDialog()
    ui = Ui_SettingsWindow()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec())
