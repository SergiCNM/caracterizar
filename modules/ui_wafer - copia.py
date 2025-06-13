# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'waferjDDRZO.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QVBoxLayout,
    QWidget)
import resources_wafer_rc

class Ui_WaferWindow(object):
    def setupUi(self, WaferWindow):
        if not WaferWindow.objectName():
            WaferWindow.setObjectName(u"WaferWindow")
        WaferWindow.setEnabled(True)
        WaferWindow.resize(1100, 862)
        WaferWindow.setMinimumSize(QSize(1100, 800))
        WaferWindow.setMaximumSize(QSize(1100, 862))
        self.action4 = QAction(WaferWindow)
        self.action4.setObjectName(u"action4")
        self.action6 = QAction(WaferWindow)
        self.action6.setObjectName(u"action6")
        self.action8 = QAction(WaferWindow)
        self.action8.setObjectName(u"action8")
        self.actionXSize = QAction(WaferWindow)
        self.actionXSize.setObjectName(u"actionXSize")
        self.actionView_Module_1 = QAction(WaferWindow)
        self.actionView_Module_1.setObjectName(u"actionView_Module_1")
        self.centralwidget = QWidget(WaferWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(1100, 800))
        self.centralwidget.setMaximumSize(QSize(1100, 800))
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 0, 1081, 791))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.gridLayout.setVerticalSpacing(0)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(80, 0))
        self.label.setMaximumSize(QSize(80, 16777215))
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout_3.addWidget(self.label)

        self.label_10 = QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(80, 0))
        self.label_10.setMaximumSize(QSize(80, 16777215))
        self.label_10.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_10)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(92, 0))
        self.label_2.setMaximumSize(QSize(92, 16777215))
        self.label_2.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 0))
        self.label_4.setMaximumSize(QSize(80, 16777215))
        self.label_4.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(80, 0))
        self.label_3.setMaximumSize(QSize(80, 16777215))
        self.label_3.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.label_12 = QLabel(self.verticalLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(32, 0))
        self.label_12.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayout_3.addWidget(self.label_12)

        self.label_6 = QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(60, 0))
        self.label_6.setMaximumSize(QSize(60, 16777215))
        self.label_6.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_6)

        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(88, 0))
        self.label_5.setMaximumSize(QSize(88, 16777215))
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_5)

        self.label_9 = QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(332, 0))
        self.label_9.setMaximumSize(QSize(332, 16777215))
        font1 = QFont()
        font1.setBold(True)
        font1.setUnderline(False)
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_9)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.cmbWaferSize = QComboBox(self.verticalLayoutWidget)
        self.cmbWaferSize.setObjectName(u"cmbWaferSize")
        self.cmbWaferSize.setEnabled(False)
        self.cmbWaferSize.setMinimumSize(QSize(80, 0))
        self.cmbWaferSize.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.cmbWaferSize)

        self.cmbWaferOrientation = QComboBox(self.verticalLayoutWidget)
        self.cmbWaferOrientation.setObjectName(u"cmbWaferOrientation")
        self.cmbWaferOrientation.setEnabled(False)
        self.cmbWaferOrientation.setMinimumSize(QSize(80, 0))
        self.cmbWaferOrientation.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.cmbWaferOrientation)

        self.txtWaferName = QLineEdit(self.verticalLayoutWidget)
        self.txtWaferName.setObjectName(u"txtWaferName")
        self.txtWaferName.setEnabled(False)
        self.txtWaferName.setMinimumSize(QSize(92, 0))
        self.txtWaferName.setMaximumSize(QSize(92, 16777215))

        self.horizontalLayout.addWidget(self.txtWaferName)

        self.txtXSize = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtXSize.setObjectName(u"txtXSize")
        self.txtXSize.setEnabled(False)
        self.txtXSize.setMinimumSize(QSize(80, 0))
        self.txtXSize.setMaximumSize(QSize(80, 16777215))
        self.txtXSize.setMaximum(999999.989999999990687)

        self.horizontalLayout.addWidget(self.txtXSize)

        self.txtYSize = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtYSize.setObjectName(u"txtYSize")
        self.txtYSize.setEnabled(False)
        self.txtYSize.setMinimumSize(QSize(80, 0))
        self.txtYSize.setMaximumSize(QSize(80, 16777215))
        self.txtYSize.setMaximum(999999.989999999990687)

        self.horizontalLayout.addWidget(self.txtYSize)

        self.btnDraw = QPushButton(self.verticalLayoutWidget)
        self.btnDraw.setObjectName(u"btnDraw")
        self.btnDraw.setEnabled(False)
        self.btnDraw.setMinimumSize(QSize(32, 32))
        self.btnDraw.setMaximumSize(QSize(32, 32))
        icon = QIcon()
        icon.addFile(u":/images/images/buttons/draw.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnDraw.setIcon(icon)
        self.btnDraw.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btnDraw)

        self.txtNumberDies = QSpinBox(self.verticalLayoutWidget)
        self.txtNumberDies.setObjectName(u"txtNumberDies")
        self.txtNumberDies.setEnabled(False)
        self.txtNumberDies.setMinimumSize(QSize(60, 0))
        self.txtNumberDies.setMaximumSize(QSize(60, 16777215))
        self.txtNumberDies.setMinimum(0)
        self.txtNumberDies.setMaximum(999999)

        self.horizontalLayout.addWidget(self.txtNumberDies)

        self.txtNumberModules = QSpinBox(self.verticalLayoutWidget)
        self.txtNumberModules.setObjectName(u"txtNumberModules")
        self.txtNumberModules.setEnabled(False)
        self.txtNumberModules.setMinimumSize(QSize(50, 0))
        self.txtNumberModules.setMaximumSize(QSize(50, 16777215))
        self.txtNumberModules.setMinimum(1)
        self.txtNumberModules.setMaximum(30)

        self.horizontalLayout.addWidget(self.txtNumberModules)

        self.btnModules = QPushButton(self.verticalLayoutWidget)
        self.btnModules.setObjectName(u"btnModules")
        self.btnModules.setEnabled(False)
        self.btnModules.setMinimumSize(QSize(32, 32))
        self.btnModules.setMaximumSize(QSize(32, 32))
        icon1 = QIcon()
        icon1.addFile(u":/images/images/buttons/modules.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnModules.setIcon(icon1)
        self.btnModules.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btnModules)

        self.cmbStartingLocation = QComboBox(self.verticalLayoutWidget)
        self.cmbStartingLocation.setObjectName(u"cmbStartingLocation")
        self.cmbStartingLocation.setEnabled(False)
        self.cmbStartingLocation.setMinimumSize(QSize(100, 0))
        self.cmbStartingLocation.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.cmbStartingLocation)

        self.cmbDirectionalMovement = QComboBox(self.verticalLayoutWidget)
        self.cmbDirectionalMovement.setObjectName(u"cmbDirectionalMovement")
        self.cmbDirectionalMovement.setEnabled(False)
        self.cmbDirectionalMovement.setMinimumSize(QSize(120, 0))
        self.cmbDirectionalMovement.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout.addWidget(self.cmbDirectionalMovement)

        self.cmbMoveBy = QComboBox(self.verticalLayoutWidget)
        self.cmbMoveBy.setObjectName(u"cmbMoveBy")
        self.cmbMoveBy.setEnabled(False)
        self.cmbMoveBy.setMinimumSize(QSize(100, 0))
        self.cmbMoveBy.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.cmbMoveBy)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.btnPrint = QPushButton(self.verticalLayoutWidget)
        self.btnPrint.setObjectName(u"btnPrint")
        self.btnPrint.setEnabled(False)
        self.btnPrint.setMinimumSize(QSize(32, 32))
        self.btnPrint.setMaximumSize(QSize(32, 32))
        icon2 = QIcon()
        icon2.addFile(u":/images/images/buttons/print.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnPrint.setIcon(icon2)
        self.btnPrint.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btnPrint)

        self.btnSave = QPushButton(self.verticalLayoutWidget)
        self.btnSave.setObjectName(u"btnSave")
        self.btnSave.setEnabled(False)
        self.btnSave.setMinimumSize(QSize(32, 32))
        self.btnSave.setMaximumSize(QSize(32, 32))
        icon3 = QIcon()
        icon3.addFile(u":/images/images/buttons/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnSave.setIcon(icon3)
        self.btnSave.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btnSave)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.txtOriginChip = QLineEdit(self.verticalLayoutWidget)
        self.txtOriginChip.setObjectName(u"txtOriginChip")
        self.txtOriginChip.setEnabled(False)
        self.txtOriginChip.setMinimumSize(QSize(60, 0))
        self.txtOriginChip.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_2.addWidget(self.txtOriginChip)

        self.btnOriginPosition = QPushButton(self.verticalLayoutWidget)
        self.btnOriginPosition.setObjectName(u"btnOriginPosition")
        self.btnOriginPosition.setEnabled(True)
        self.btnOriginPosition.setMinimumSize(QSize(40, 40))
        self.btnOriginPosition.setMaximumSize(QSize(40, 40))
        icon4 = QIcon()
        icon4.addFile(u":/images/images/buttons/set_origin.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnOriginPosition.setIcon(icon4)
        self.btnOriginPosition.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.btnOriginPosition)

        self.txtHomeChip = QLineEdit(self.verticalLayoutWidget)
        self.txtHomeChip.setObjectName(u"txtHomeChip")
        self.txtHomeChip.setEnabled(False)
        self.txtHomeChip.setMinimumSize(QSize(70, 0))
        self.txtHomeChip.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_2.addWidget(self.txtHomeChip)

        self.btnHomePosition = QPushButton(self.verticalLayoutWidget)
        self.btnHomePosition.setObjectName(u"btnHomePosition")
        self.btnHomePosition.setEnabled(True)
        self.btnHomePosition.setMinimumSize(QSize(40, 40))
        self.btnHomePosition.setMaximumSize(QSize(40, 40))
        icon5 = QIcon()
        icon5.addFile(u":/images/images/buttons/set_home.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnHomePosition.setIcon(icon5)
        self.btnHomePosition.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.btnHomePosition)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.btnIDLE = QPushButton(self.verticalLayoutWidget)
        self.btnIDLE.setObjectName(u"btnIDLE")
        self.btnIDLE.setEnabled(True)
        self.btnIDLE.setMinimumSize(QSize(70, 40))
        self.btnIDLE.setMaximumSize(QSize(70, 40))
        font2 = QFont()
        font2.setPointSize(8)
        self.btnIDLE.setFont(font2)
        icon6 = QIcon()
        icon6.addFile(u":/images/images/buttons/set_idle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnIDLE.setIcon(icon6)
        self.btnIDLE.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.btnIDLE)

        self.btnIN = QPushButton(self.verticalLayoutWidget)
        self.btnIN.setObjectName(u"btnIN")
        self.btnIN.setEnabled(True)
        self.btnIN.setMinimumSize(QSize(70, 40))
        self.btnIN.setMaximumSize(QSize(70, 40))
        self.btnIN.setFont(font2)
        icon7 = QIcon()
        icon7.addFile(u":/images/images/buttons/set_in.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnIN.setIcon(icon7)
        self.btnIN.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.btnIN)

        self.btnOUT = QPushButton(self.verticalLayoutWidget)
        self.btnOUT.setObjectName(u"btnOUT")
        self.btnOUT.setEnabled(True)
        self.btnOUT.setMinimumSize(QSize(70, 40))
        self.btnOUT.setMaximumSize(QSize(70, 40))
        self.btnOUT.setFont(font2)
        icon8 = QIcon()
        icon8.addFile(u":/images/images/buttons/set_out.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnOUT.setIcon(icon8)
        self.btnOUT.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.btnOUT)

        self.btnMEAS = QPushButton(self.verticalLayoutWidget)
        self.btnMEAS.setObjectName(u"btnMEAS")
        self.btnMEAS.setEnabled(True)
        self.btnMEAS.setMinimumSize(QSize(70, 40))
        self.btnMEAS.setMaximumSize(QSize(70, 40))
        self.btnMEAS.setFont(font2)
        icon9 = QIcon()
        icon9.addFile(u":/images/images/buttons/set_meas.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnMEAS.setIcon(icon9)
        self.btnMEAS.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.btnMEAS)

        self.btnMEAS_SUCCESS = QPushButton(self.verticalLayoutWidget)
        self.btnMEAS_SUCCESS.setObjectName(u"btnMEAS_SUCCESS")
        self.btnMEAS_SUCCESS.setEnabled(True)
        self.btnMEAS_SUCCESS.setMinimumSize(QSize(70, 40))
        self.btnMEAS_SUCCESS.setMaximumSize(QSize(70, 40))
        font3 = QFont()
        font3.setPointSize(6)
        self.btnMEAS_SUCCESS.setFont(font3)
        icon10 = QIcon()
        icon10.addFile(u":/images/images/buttons/set_meas_success.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnMEAS_SUCCESS.setIcon(icon10)
        self.btnMEAS_SUCCESS.setIconSize(QSize(24, 24))

        self.horizontalLayout_2.addWidget(self.btnMEAS_SUCCESS)

        self.btnMEAS_WARNING = QPushButton(self.verticalLayoutWidget)
        self.btnMEAS_WARNING.setObjectName(u"btnMEAS_WARNING")
        self.btnMEAS_WARNING.setEnabled(True)
        self.btnMEAS_WARNING.setMinimumSize(QSize(70, 40))
        self.btnMEAS_WARNING.setMaximumSize(QSize(70, 40))
        self.btnMEAS_WARNING.setFont(font3)
        icon11 = QIcon()
        icon11.addFile(u":/images/images/buttons/set_meas_warning.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnMEAS_WARNING.setIcon(icon11)
        self.btnMEAS_WARNING.setIconSize(QSize(24, 24))

        self.horizontalLayout_2.addWidget(self.btnMEAS_WARNING)

        self.btnMEAS_ERROR = QPushButton(self.verticalLayoutWidget)
        self.btnMEAS_ERROR.setObjectName(u"btnMEAS_ERROR")
        self.btnMEAS_ERROR.setEnabled(True)
        self.btnMEAS_ERROR.setMinimumSize(QSize(70, 40))
        self.btnMEAS_ERROR.setMaximumSize(QSize(70, 40))
        self.btnMEAS_ERROR.setFont(font3)
        icon12 = QIcon()
        icon12.addFile(u":/images/images/buttons/set_meas_error.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnMEAS_ERROR.setIcon(icon12)
        self.btnMEAS_ERROR.setIconSize(QSize(24, 24))

        self.horizontalLayout_2.addWidget(self.btnMEAS_ERROR)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.btnMarkAll = QPushButton(self.verticalLayoutWidget)
        self.btnMarkAll.setObjectName(u"btnMarkAll")
        self.btnMarkAll.setEnabled(True)
        self.btnMarkAll.setMinimumSize(QSize(55, 40))
        self.btnMarkAll.setMaximumSize(QSize(55, 40))
        self.btnMarkAll.setFont(font2)
        self.btnMarkAll.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.btnMarkAll)

        self.btnUnmarkAll = QPushButton(self.verticalLayoutWidget)
        self.btnUnmarkAll.setObjectName(u"btnUnmarkAll")
        self.btnUnmarkAll.setEnabled(True)
        self.btnUnmarkAll.setMinimumSize(QSize(60, 40))
        self.btnUnmarkAll.setMaximumSize(QSize(60, 40))
        self.btnUnmarkAll.setFont(font2)
        self.btnUnmarkAll.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.btnUnmarkAll)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        WaferWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(WaferWindow)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setMinimumSize(QSize(0, 40))
        self.statusBar.setMaximumSize(QSize(16777215, 40))
        self.statusBar.setLayoutDirection(Qt.LeftToRight)
        self.statusBar.setStyleSheet(u"text-align: right;")
        WaferWindow.setStatusBar(self.statusBar)
        self.menuBar = QMenuBar(WaferWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1100, 22))
        WaferWindow.setMenuBar(self.menuBar)

        self.retranslateUi(WaferWindow)

        QMetaObject.connectSlotsByName(WaferWindow)
    # setupUi

    def retranslateUi(self, WaferWindow):
        WaferWindow.setWindowTitle(QCoreApplication.translate("WaferWindow", u"Wafer window", None))
        self.action4.setText(QCoreApplication.translate("WaferWindow", u"4\"", None))
        self.action6.setText(QCoreApplication.translate("WaferWindow", u"6\"", None))
        self.action8.setText(QCoreApplication.translate("WaferWindow", u"8\"", None))
        self.actionXSize.setText(QCoreApplication.translate("WaferWindow", u"XSize", None))
        self.actionView_Module_1.setText(QCoreApplication.translate("WaferWindow", u"View Module 1", None))
        self.label.setText(QCoreApplication.translate("WaferWindow", u"Wafer size", None))
        self.label_10.setText(QCoreApplication.translate("WaferWindow", u"Wafer Flat", None))
        self.label_2.setText(QCoreApplication.translate("WaferWindow", u"Wafer name", None))
        self.label_4.setText(QCoreApplication.translate("WaferWindow", u"XSize (um)", None))
        self.label_3.setText(QCoreApplication.translate("WaferWindow", u"YSize (um)", None))
        self.label_12.setText("")
        self.label_6.setText(QCoreApplication.translate("WaferWindow", u"Dies", None))
        self.label_5.setText(QCoreApplication.translate("WaferWindow", u"Modules", None))
        self.label_9.setText(QCoreApplication.translate("WaferWindow", u"Navigation options", None))
        self.cmbWaferSize.setCurrentText("")
        self.cmbWaferOrientation.setCurrentText("")
        self.txtWaferName.setPlaceholderText(QCoreApplication.translate("WaferWindow", u"Wafer name", None))
#if QT_CONFIG(tooltip)
        self.btnDraw.setToolTip(QCoreApplication.translate("WaferWindow", u"Draw wafer", None))
#endif // QT_CONFIG(tooltip)
        self.btnDraw.setText("")
#if QT_CONFIG(tooltip)
        self.btnModules.setToolTip(QCoreApplication.translate("WaferWindow", u"View Modules", None))
#endif // QT_CONFIG(tooltip)
        self.btnModules.setText("")
#if QT_CONFIG(tooltip)
        self.cmbStartingLocation.setToolTip(QCoreApplication.translate("WaferWindow", u"Starting location", None))
#endif // QT_CONFIG(tooltip)
        self.cmbStartingLocation.setCurrentText("")
#if QT_CONFIG(tooltip)
        self.cmbDirectionalMovement.setToolTip(QCoreApplication.translate("WaferWindow", u"Directional movement", None))
#endif // QT_CONFIG(tooltip)
        self.cmbDirectionalMovement.setCurrentText("")
#if QT_CONFIG(tooltip)
        self.cmbMoveBy.setToolTip(QCoreApplication.translate("WaferWindow", u"Move by", None))
#endif // QT_CONFIG(tooltip)
        self.cmbMoveBy.setCurrentText("")
#if QT_CONFIG(tooltip)
        self.btnPrint.setToolTip(QCoreApplication.translate("WaferWindow", u"Print to PNG", None))
#endif // QT_CONFIG(tooltip)
        self.btnPrint.setText("")
#if QT_CONFIG(tooltip)
        self.btnSave.setToolTip(QCoreApplication.translate("WaferWindow", u"Save as", None))
#endif // QT_CONFIG(tooltip)
        self.btnSave.setText("")
#if QT_CONFIG(tooltip)
        self.txtOriginChip.setToolTip(QCoreApplication.translate("WaferWindow", u"Real Origin position (0,0)", None))
#endif // QT_CONFIG(tooltip)
        self.txtOriginChip.setText("")
#if QT_CONFIG(tooltip)
        self.btnOriginPosition.setToolTip(QCoreApplication.translate("WaferWindow", u"Set Origin", None))
#endif // QT_CONFIG(tooltip)
        self.btnOriginPosition.setText("")
#if QT_CONFIG(tooltip)
        self.txtHomeChip.setToolTip(QCoreApplication.translate("WaferWindow", u"Home position (ref to Origin)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btnHomePosition.setToolTip(QCoreApplication.translate("WaferWindow", u"Set Home", None))
#endif // QT_CONFIG(tooltip)
        self.btnHomePosition.setText("")
#if QT_CONFIG(tooltip)
        self.btnIDLE.setToolTip(QCoreApplication.translate("WaferWindow", u"Set IDLE", None))
#endif // QT_CONFIG(tooltip)
        self.btnIDLE.setText(QCoreApplication.translate("WaferWindow", u"IDLE", None))
#if QT_CONFIG(tooltip)
        self.btnIN.setToolTip(QCoreApplication.translate("WaferWindow", u"Set IN ", None))
#endif // QT_CONFIG(tooltip)
        self.btnIN.setText(QCoreApplication.translate("WaferWindow", u"IN", None))
#if QT_CONFIG(tooltip)
        self.btnOUT.setToolTip(QCoreApplication.translate("WaferWindow", u"Set OUT", None))
#endif // QT_CONFIG(tooltip)
        self.btnOUT.setText(QCoreApplication.translate("WaferWindow", u"OUT", None))
#if QT_CONFIG(tooltip)
        self.btnMEAS.setToolTip(QCoreApplication.translate("WaferWindow", u"Set MEAS", None))
#endif // QT_CONFIG(tooltip)
        self.btnMEAS.setText(QCoreApplication.translate("WaferWindow", u"MEAS", None))
#if QT_CONFIG(tooltip)
        self.btnMEAS_SUCCESS.setToolTip(QCoreApplication.translate("WaferWindow", u"Set MEAS SUCCESS", None))
#endif // QT_CONFIG(tooltip)
        self.btnMEAS_SUCCESS.setText(QCoreApplication.translate("WaferWindow", u"SUCCESS", None))
#if QT_CONFIG(tooltip)
        self.btnMEAS_WARNING.setToolTip(QCoreApplication.translate("WaferWindow", u"Set MEAS WARNING", None))
#endif // QT_CONFIG(tooltip)
        self.btnMEAS_WARNING.setText(QCoreApplication.translate("WaferWindow", u"WARNING", None))
#if QT_CONFIG(tooltip)
        self.btnMEAS_ERROR.setToolTip(QCoreApplication.translate("WaferWindow", u"Set MEAS ERROR", None))
#endif // QT_CONFIG(tooltip)
        self.btnMEAS_ERROR.setText(QCoreApplication.translate("WaferWindow", u"ERROR", None))
#if QT_CONFIG(tooltip)
        self.btnMarkAll.setToolTip(QCoreApplication.translate("WaferWindow", u"Mark all", None))
#endif // QT_CONFIG(tooltip)
        self.btnMarkAll.setText(QCoreApplication.translate("WaferWindow", u"MARK", None))
#if QT_CONFIG(tooltip)
        self.btnUnmarkAll.setToolTip(QCoreApplication.translate("WaferWindow", u"Unmark all", None))
#endif // QT_CONFIG(tooltip)
        self.btnUnmarkAll.setText(QCoreApplication.translate("WaferWindow", u"UNMARK", None))
    # retranslateUi

