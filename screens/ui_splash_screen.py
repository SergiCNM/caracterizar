# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash_screenMsKYId.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        if not SplashScreen.objectName():
            SplashScreen.setObjectName(u"SplashScreen")
        SplashScreen.resize(300, 300)
        SplashScreen.setMinimumSize(QSize(300, 300))
        SplashScreen.setMaximumSize(QSize(300, 300))
        SplashScreen.setStyleSheet(u"")
        self.centralwidget = QWidget(SplashScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.container = QFrame(self.centralwidget)
        self.container.setObjectName(u"container")
        font = QFont()
        font.setPointSize(9)
        self.container.setFont(font)
        self.container.setStyleSheet(u"")
        self.container.setFrameShape(QFrame.NoFrame)
        self.container.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.container)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.circle_bg = QFrame(self.container)
        self.circle_bg.setObjectName(u"circle_bg")
        self.circle_bg.setStyleSheet(u"QFrame {\n"
"	background-color: #282a36;\n"
"	color: #f8f8f2;\n"
"	border-radius: 120px;\n"
"	font: 9pt \"Segoe UI\";\n"
"}")
        self.circle_bg.setFrameShape(QFrame.NoFrame)
        self.circle_bg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.circle_bg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.texts = QFrame(self.circle_bg)
        self.texts.setObjectName(u"texts")
        self.texts.setMaximumSize(QSize(16777215, 200))
        self.texts.setStyleSheet(u"background:none;")
        self.texts.setFrameShape(QFrame.NoFrame)
        self.texts.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.texts)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 25, -1, -1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(self.texts)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.version = QLabel(self.frame)
        self.version.setObjectName(u"version")
        self.version.setMinimumSize(QSize(100, 24))
        self.version.setMaximumSize(QSize(100, 24))
        self.version.setStyleSheet(u"QLabel {\n"
"\n"
"background-color: rgb(68,71,90);\n"
"color: #6272a4;\n"
"border-radius: 12px;\n"
"\n"
"}")
        self.version.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.version)


        self.gridLayout.addWidget(self.frame, 4, 0, 1, 1, Qt.AlignHCenter)

        self.label = QLabel(self.texts)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(9)
        font1.setBold(False)
        font1.setItalic(False)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.empty = QFrame(self.texts)
        self.empty.setObjectName(u"empty")
        self.empty.setMinimumSize(QSize(0, 90))
        self.empty.setFrameShape(QFrame.StyledPanel)
        self.empty.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.empty, 2, 0, 1, 1)

        self.lblStatus = QLabel(self.texts)
        self.lblStatus.setObjectName(u"lblStatus")
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setPointSize(7)
        font2.setBold(False)
        font2.setItalic(False)
        self.lblStatus.setFont(font2)
        self.lblStatus.setStyleSheet(u"font: 7pt \"Segoe UI\";")
        self.lblStatus.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lblStatus, 3, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)


        self.verticalLayout_3.addWidget(self.texts)


        self.verticalLayout_2.addWidget(self.circle_bg)


        self.verticalLayout.addWidget(self.container)

        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)

        QMetaObject.connectSlotsByName(SplashScreen)
    # setupUi

    def retranslateUi(self, SplashScreen):
        SplashScreen.setWindowTitle(QCoreApplication.translate("SplashScreen", u"Loading...", None))
        self.version.setText(QCoreApplication.translate("SplashScreen", u"v6.0 - Beta 1", None))
        self.label.setText(QCoreApplication.translate("SplashScreen", u"CARACTERIZAR", None))
        self.lblStatus.setText(QCoreApplication.translate("SplashScreen", u"loading...", None))
    # retranslateUi

