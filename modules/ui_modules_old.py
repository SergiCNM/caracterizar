# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modulesiFiUFL.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_ModulesWindow(object):
    def setupUi(self, ModulesWindow):
        if not ModulesWindow.objectName():
            ModulesWindow.setObjectName(u"ModulesWindow")
        ModulesWindow.resize(300, 400)
        ModulesWindow.setMinimumSize(QSize(300, 400))
        ModulesWindow.setMaximumSize(QSize(300, 400))
        self.centralwidget = QWidget(ModulesWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(9, 10, 281, 51))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.txtNumberModules = QLineEdit(self.horizontalLayoutWidget)
        self.txtNumberModules.setObjectName(u"txtNumberModules")
        self.txtNumberModules.setEnabled(False)
        self.txtNumberModules.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.txtNumberModules)

        self.btnSaveModules = QPushButton(self.horizontalLayoutWidget)
        self.btnSaveModules.setObjectName(u"btnSaveModules")
        self.btnSaveModules.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.btnSaveModules)

        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(100, 70, 91, 301))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 16))
        font = QFont()
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.label_2)

        self.txtX1 = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtX1.setObjectName(u"txtX1")
        self.txtX1.setMaximumSize(QSize(85, 16777215))
        self.txtX1.setDecimals(6)
        self.txtX1.setMinimum(-999999.989999999990687)
        self.txtX1.setMaximum(999999.989999999990687)

        self.verticalLayout.addWidget(self.txtX1)

        self.txtX2 = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtX2.setObjectName(u"txtX2")
        self.txtX2.setMaximumSize(QSize(85, 16777215))
        self.txtX2.setDecimals(6)
        self.txtX2.setMinimum(-999999.989999999990687)
        self.txtX2.setMaximum(999999.989999999990687)

        self.verticalLayout.addWidget(self.txtX2)

        self.txtX3 = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtX3.setObjectName(u"txtX3")
        self.txtX3.setMaximumSize(QSize(85, 16777215))
        self.txtX3.setDecimals(6)
        self.txtX3.setMinimum(-999999.989999999990687)
        self.txtX3.setMaximum(999999.989999999990687)

        self.verticalLayout.addWidget(self.txtX3)

        self.txtX4 = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtX4.setObjectName(u"txtX4")
        self.txtX4.setMaximumSize(QSize(85, 16777215))
        self.txtX4.setDecimals(6)
        self.txtX4.setMinimum(-999999.989999999990687)
        self.txtX4.setMaximum(999999.989999999990687)

        self.verticalLayout.addWidget(self.txtX4)

        self.txtX5 = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtX5.setObjectName(u"txtX5")
        self.txtX5.setMaximumSize(QSize(85, 16777215))
        self.txtX5.setDecimals(6)
        self.txtX5.setMinimum(-999999.989999999990687)
        self.txtX5.setMaximum(999999.989999999990687)

        self.verticalLayout.addWidget(self.txtX5)

        self.txtX6 = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtX6.setObjectName(u"txtX6")
        self.txtX6.setMaximumSize(QSize(85, 16777215))
        self.txtX6.setDecimals(6)
        self.txtX6.setMinimum(-999999.989999999990687)
        self.txtX6.setMaximum(999999.989999999990687)

        self.verticalLayout.addWidget(self.txtX6)

        self.txtX7 = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtX7.setObjectName(u"txtX7")
        self.txtX7.setMaximumSize(QSize(85, 16777215))
        self.txtX7.setDecimals(6)
        self.txtX7.setMinimum(-999999.989999999990687)
        self.txtX7.setMaximum(999999.989999999990687)

        self.verticalLayout.addWidget(self.txtX7)

        self.txtX8 = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtX8.setObjectName(u"txtX8")
        self.txtX8.setMaximumSize(QSize(85, 16777215))
        self.txtX8.setDecimals(6)
        self.txtX8.setMinimum(-999999.989999999990687)
        self.txtX8.setMaximum(999999.989999999990687)

        self.verticalLayout.addWidget(self.txtX8)

        self.txtX9 = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtX9.setObjectName(u"txtX9")
        self.txtX9.setMaximumSize(QSize(85, 16777215))
        self.txtX9.setDecimals(6)
        self.txtX9.setMinimum(-999999.989999999990687)
        self.txtX9.setMaximum(999999.989999999990687)

        self.verticalLayout.addWidget(self.txtX9)

        self.txtX10 = QDoubleSpinBox(self.verticalLayoutWidget)
        self.txtX10.setObjectName(u"txtX10")
        self.txtX10.setMaximumSize(QSize(85, 16777215))
        self.txtX10.setDecimals(6)
        self.txtX10.setMinimum(-999999.989999999990687)
        self.txtX10.setMaximum(999999.989999999990687)

        self.verticalLayout.addWidget(self.txtX10)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(200, 70, 91, 301))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 16))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_2.addWidget(self.label_3)

        self.txtY1 = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.txtY1.setObjectName(u"txtY1")
        self.txtY1.setMaximumSize(QSize(85, 16777215))
        self.txtY1.setDecimals(6)
        self.txtY1.setMinimum(-999999.989999999990687)
        self.txtY1.setMaximum(999999.989999999990687)

        self.verticalLayout_2.addWidget(self.txtY1)

        self.txtY2 = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.txtY2.setObjectName(u"txtY2")
        self.txtY2.setMaximumSize(QSize(85, 16777215))
        self.txtY2.setDecimals(6)
        self.txtY2.setMinimum(-999999.989999999990687)
        self.txtY2.setMaximum(999999.989999999990687)

        self.verticalLayout_2.addWidget(self.txtY2)

        self.txtY3 = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.txtY3.setObjectName(u"txtY3")
        self.txtY3.setMaximumSize(QSize(85, 16777215))
        self.txtY3.setDecimals(6)
        self.txtY3.setMinimum(-999999.989999999990687)
        self.txtY3.setMaximum(999999.989999999990687)

        self.verticalLayout_2.addWidget(self.txtY3)

        self.txtY4 = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.txtY4.setObjectName(u"txtY4")
        self.txtY4.setMaximumSize(QSize(85, 16777215))
        self.txtY4.setDecimals(6)
        self.txtY4.setMinimum(-999999.989999999990687)
        self.txtY4.setMaximum(999999.989999999990687)

        self.verticalLayout_2.addWidget(self.txtY4)

        self.txtY5 = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.txtY5.setObjectName(u"txtY5")
        self.txtY5.setMaximumSize(QSize(85, 16777215))
        self.txtY5.setDecimals(6)
        self.txtY5.setMinimum(-999999.989999999990687)
        self.txtY5.setMaximum(999999.989999999990687)

        self.verticalLayout_2.addWidget(self.txtY5)

        self.txtY6 = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.txtY6.setObjectName(u"txtY6")
        self.txtY6.setMaximumSize(QSize(85, 16777215))
        self.txtY6.setDecimals(6)
        self.txtY6.setMinimum(-999999.989999999990687)
        self.txtY6.setMaximum(999999.989999999990687)

        self.verticalLayout_2.addWidget(self.txtY6)

        self.txtY7 = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.txtY7.setObjectName(u"txtY7")
        self.txtY7.setMaximumSize(QSize(85, 16777215))
        self.txtY7.setDecimals(6)
        self.txtY7.setMinimum(-999999.989999999990687)
        self.txtY7.setMaximum(999999.989999999990687)

        self.verticalLayout_2.addWidget(self.txtY7)

        self.txtY8 = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.txtY8.setObjectName(u"txtY8")
        self.txtY8.setMaximumSize(QSize(85, 16777215))
        self.txtY8.setDecimals(6)
        self.txtY8.setMinimum(-999999.989999999990687)
        self.txtY8.setMaximum(999999.989999999990687)

        self.verticalLayout_2.addWidget(self.txtY8)

        self.txtY9 = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.txtY9.setObjectName(u"txtY9")
        self.txtY9.setMaximumSize(QSize(85, 16777215))
        self.txtY9.setDecimals(6)
        self.txtY9.setMinimum(-999999.989999999990687)
        self.txtY9.setMaximum(999999.989999999990687)

        self.verticalLayout_2.addWidget(self.txtY9)

        self.txtY10 = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.txtY10.setObjectName(u"txtY10")
        self.txtY10.setMaximumSize(QSize(85, 16777215))
        self.txtY10.setDecimals(6)
        self.txtY10.setMinimum(-999999.989999999990687)
        self.txtY10.setMaximum(999999.989999999990687)

        self.verticalLayout_2.addWidget(self.txtY10)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 70, 70, 298))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.verticalLayoutWidget_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_4.addWidget(self.label_5)

        self.label_6 = QLabel(self.verticalLayoutWidget_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 22))

        self.verticalLayout_4.addWidget(self.label_6)

        self.label_7 = QLabel(self.verticalLayoutWidget_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 22))

        self.verticalLayout_4.addWidget(self.label_7)

        self.label_8 = QLabel(self.verticalLayoutWidget_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 22))

        self.verticalLayout_4.addWidget(self.label_8)

        self.label_9 = QLabel(self.verticalLayoutWidget_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 22))

        self.verticalLayout_4.addWidget(self.label_9)

        self.label_10 = QLabel(self.verticalLayoutWidget_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 22))

        self.verticalLayout_4.addWidget(self.label_10)

        self.label_11 = QLabel(self.verticalLayoutWidget_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 22))

        self.verticalLayout_4.addWidget(self.label_11)

        self.label_12 = QLabel(self.verticalLayoutWidget_3)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(0, 22))

        self.verticalLayout_4.addWidget(self.label_12)

        self.label_13 = QLabel(self.verticalLayoutWidget_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 22))

        self.verticalLayout_4.addWidget(self.label_13)

        self.label_14 = QLabel(self.verticalLayoutWidget_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 22))

        self.verticalLayout_4.addWidget(self.label_14)

        self.label_15 = QLabel(self.verticalLayoutWidget_3)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 22))

        self.verticalLayout_4.addWidget(self.label_15)

        ModulesWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(ModulesWindow)
        self.statusbar.setObjectName(u"statusbar")
        ModulesWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ModulesWindow)

        QMetaObject.connectSlotsByName(ModulesWindow)
    # setupUi

    def retranslateUi(self, ModulesWindow):
        ModulesWindow.setWindowTitle(QCoreApplication.translate("ModulesWindow", u"Modules window", None))
        self.label.setText(QCoreApplication.translate("ModulesWindow", u"Modules number: ", None))
        self.btnSaveModules.setText(QCoreApplication.translate("ModulesWindow", u"Save Modules", None))
        self.label_2.setText(QCoreApplication.translate("ModulesWindow", u"X(um)", None))
        self.label_3.setText(QCoreApplication.translate("ModulesWindow", u"Y(um)", None))
        self.label_5.setText(QCoreApplication.translate("ModulesWindow", u"Modules", None))
        self.label_6.setText(QCoreApplication.translate("ModulesWindow", u"Module 1", None))
        self.label_7.setText(QCoreApplication.translate("ModulesWindow", u"Module 2", None))
        self.label_8.setText(QCoreApplication.translate("ModulesWindow", u"Module 3", None))
        self.label_9.setText(QCoreApplication.translate("ModulesWindow", u"Module 4", None))
        self.label_10.setText(QCoreApplication.translate("ModulesWindow", u"Module 5", None))
        self.label_11.setText(QCoreApplication.translate("ModulesWindow", u"Module 6", None))
        self.label_12.setText(QCoreApplication.translate("ModulesWindow", u"Module 7", None))
        self.label_13.setText(QCoreApplication.translate("ModulesWindow", u"Module 8", None))
        self.label_14.setText(QCoreApplication.translate("ModulesWindow", u"Module 9", None))
        self.label_15.setText(QCoreApplication.translate("ModulesWindow", u"Module 10", None))
    # retranslateUi

