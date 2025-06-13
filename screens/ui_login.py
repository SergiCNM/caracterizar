# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginYFTsuF.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(600, 550)
        MainWindow.setMinimumSize(QSize(600, 550))
        MainWindow.setMaximumSize(QSize(600, 550))
        MainWindow.setStyleSheet(u"background-color: #282a36;\n"
"	color: #f8f8f2;\n"
"\n"
"QPushButton::pressed {\n"
"     background-color: rgb(224, 0, 0);     \n"
" }\n"
" QPushButton::hover {\n"
"     background-color: rgb(224, 255, 0);\n"
" }\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setStyleSheet(u"QPushButton:hover\n"
"{\n"
"   	border:none;\n"
"}\n"
"\n"
"QPushButton#btnLogin {\n"
"	background-color: #6272a4;\n"
"	border-radius: 10px;\n"
"	font: 12pt \"Segoe UI\";\n"
"}\n"
"\n"
"QPushButton:hover#btnLogin\n"
"{\n"
"  background-color: #ffb86c;\n"
"}")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(150, 62, 371, 50))
        font = QFont()
        font.setPointSize(36)
        font.setBold(True)
        self.label.setFont(font)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(156, 117, 191, 16))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(170, 180, 251, 41))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_5.setFont(font1)
        self.label_5.setStyleSheet(u"color: #f8f8f2;")
        self.label_5.setAlignment(Qt.AlignCenter)
        self.password = QLineEdit(self.centralwidget)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(170, 360, 250, 30))
        self.password.setMinimumSize(QSize(250, 30))
        self.password.setMaximumSize(QSize(180, 30))
        self.password.setFocusPolicy(Qt.StrongFocus)
        self.password.setStyleSheet(u"background-color: #44475a;\n"
"font: 12pt \"Segoe UI\";\n"
"border-top: 0px solid #44475a;\n"
"border-left: 0px solid #44475a;\n"
"border-right: 0px solid #44475a;\n"
"border-bottom: 3px solid #6272a4;\n"
"border-radius:10px;")
        self.password.setFrame(True)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setAlignment(Qt.AlignCenter)
        self.username = QLineEdit(self.centralwidget)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(170, 290, 250, 30))
        self.username.setMinimumSize(QSize(250, 30))
        self.username.setMaximumSize(QSize(180, 30))
        self.username.setFocusPolicy(Qt.StrongFocus)
        self.username.setStyleSheet(u"background-color: #44475a;\n"
"font: 12pt \"Segoe UI\";\n"
"border-top: 0px solid #44475a;\n"
"border-left: 0px solid #44475a;\n"
"border-right: 0px solid #44475a;\n"
"border-bottom: 3px solid #6272a4;\n"
"border-radius:10px;")
        self.username.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(210, 328, 211, 30))
        self.label_3.setMaximumSize(QSize(16777215, 30))
        self.label_3.setStyleSheet(u"color: #8be9fd;")
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.btnLogin = QPushButton(self.centralwidget)
        self.btnLogin.setObjectName(u"btnLogin")
        self.btnLogin.setGeometry(QRect(170, 420, 250, 40))
        self.btnLogin.setMinimumSize(QSize(250, 40))
        self.btnLogin.setMaximumSize(QSize(180, 40))
        self.btnLogin.setMouseTracking(True)
        self.btnLogin.setTabletTracking(False)
        self.btnLogin.setStyleSheet(u"")
        self.btnLogin.setFlat(False)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(210, 256, 211, 30))
        self.label_2.setMaximumSize(QSize(16777215, 30))
        self.label_2.setStyleSheet(u"color: #8be9fd;")
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(80, 70, 64, 64))
        self.label_6.setMinimumSize(QSize(64, 64))
        self.label_6.setStyleSheet(u"background-color: #282a36;\n"
"")
        self.label_6.setPixmap(QPixmap(u":/images/wafer_64_gris.png"))
        self.version = QLabel(self.centralwidget)
        self.version.setObjectName(u"version")
        self.version.setGeometry(QRect(490, 520, 100, 24))
        self.version.setMinimumSize(QSize(100, 24))
        self.version.setMaximumSize(QSize(100, 24))
        self.version.setStyleSheet(u"QLabel {\n"
"\n"
"background-color: rgb(68,71,90);\n"
"color: #6272a4;\n"
"border-radius: 10px;\n"
"\n"
"}")
        self.version.setAlignment(Qt.AlignCenter)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 600, 32))
        self.frame.setMinimumSize(QSize(600, 32))
        self.frame.setMaximumSize(QSize(600, 32))
        self.frame.setStyleSheet(u"background-color: #6272a4;\n"
"\n"
"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.btnClose = QPushButton(self.frame)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setGeometry(QRect(569, 1, 30, 32))
        self.btnClose.setMaximumSize(QSize(30, 16777215))
        self.btnClose.setToolTipDuration(-1)
        self.btnClose.setStyleSheet(u"qproperty-icon: url(:/images/icons8-macos-close-30.png);")
        self.btnClose.setIconSize(QSize(30, 30))
        self.btnClose.setFlat(True)
        self.btnMinimize = QPushButton(self.frame)
        self.btnMinimize.setObjectName(u"btnMinimize")
        self.btnMinimize.setGeometry(QRect(539, 1, 30, 32))
        self.btnMinimize.setMaximumSize(QSize(30, 16777215))
        self.btnMinimize.setStyleSheet(u"qproperty-icon: url(:/images/icons8-macos-minimize-30.png);\n"
"\n"
"\n"
"")
        self.btnMinimize.setIconSize(QSize(30, 30))
        self.btnMinimize.setAutoRepeat(False)
        self.btnMinimize.setFlat(True)
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(171, 255, 32, 32))
        self.label_8.setMinimumSize(QSize(32, 32))
        self.label_8.setPixmap(QPixmap(u":/images/icons8-user-32.png"))
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(171, 327, 32, 32))
        self.label_9.setMinimumSize(QSize(32, 32))
        self.label_9.setPixmap(QPixmap(u":/images/icons8-password-window-32.png"))
        self.btnToggle = QPushButton(self.centralwidget)
        self.btnToggle.setObjectName(u"btnToggle")
        self.btnToggle.setEnabled(True)
        self.btnToggle.setGeometry(QRect(430, 344, 48, 48))
        self.btnToggle.setMinimumSize(QSize(0, 0))
        self.btnToggle.setMaximumSize(QSize(48, 48))
        self.btnToggle.setStyleSheet(u"qproperty-icon: url(:/images/icons8-password-48.png);\n"
"\n"
"")
        self.btnToggle.setIconSize(QSize(48, 48))
        self.btnToggle.setFlat(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.label.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.username.raise_()
        self.label_3.raise_()
        self.btnLogin.raise_()
        self.label_2.raise_()
        self.label_6.raise_()
        self.version.raise_()
        self.frame.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.password.raise_()
        self.btnToggle.raise_()
        QWidget.setTabOrder(self.username, self.password)
        QWidget.setTabOrder(self.password, self.btnLogin)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Caracterizar - Instrument control software", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"CARACTERIZAR", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Instrument control software", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Please, sign in to CARACTERIZAR", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Password", None))
#if QT_CONFIG(tooltip)
        self.btnLogin.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.btnLogin.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.btnLogin.setText(QCoreApplication.translate("MainWindow", u"Log in", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Username (or email)", None))
        self.label_6.setText("")
        self.version.setText(QCoreApplication.translate("MainWindow", u"v6.0 - Beta 1", None))
#if QT_CONFIG(tooltip)
        self.btnClose.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.btnClose.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.btnClose.setText("")
#if QT_CONFIG(tooltip)
        self.btnMinimize.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.btnMinimize.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.btnMinimize.setText("")
        self.label_8.setText("")
        self.label_9.setText("")
        self.btnToggle.setText("")
    # retranslateUi

