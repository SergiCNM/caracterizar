# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainxlmEBf.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QCommandLinkButton, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QPlainTextEdit, QProgressBar, QPushButton,
    QRadioButton, QScrollArea, QScrollBar, QSizePolicy,
    QSlider, QSpacerItem, QStackedWidget, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from widgets import CheckableComboBox
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1301, 942)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"TabWidget */\n"
"\n"
"QTabWidget::pane { /* The tab widget frame */\n"
"    border-bottom: 2px solid #C2C7CB;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"	padding: 5px;\n"
"    background-color: #FaFaFa;\n"
"	margin-left: 5px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"background-color: rgb(52, 59, 72);\n"
"border-top: 2px solid #C4C4C3;\n"
"color: #FFFFFF;\n"
"}\n"
"QTabBar::tab:!selected {\n"
"background-color: rgb(40, 44, 52);\n"
"color: #CCC;\n"
"border: none;\n"
"}\n"
"\n"
" \n"
"\n"
"/* //////////////////////////////////////////"
                        "///////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/electric-meter.png);\n"
"	background-position: centered;\n"
""
                        "	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushBu"
                        "tton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position"
                        ": center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
""
                        "#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font"
                        "-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-"
                        "left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
""
                        "	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* //////////////////////////////////////////////////////////////////////////////////////"
                        "///////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrol"
                        "lBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScro"
                        "llBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    "
                        "border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	col"
                        "or: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
""
                        "}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLinkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* ////////////////////////////////////////////////////////////"
                        "/////////////////////////////////////\n"
"Button */\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"#pagesContainer .QPushButton:disabled {\n"
"	background: none !important;\n"
"	background-color: #333333; border: none;\n"
"}\n"
"\n"
"QProgressBar {\n"
"border: 1px solid rgb(64, 71, 88);\n"
"text-align: right;\n"
"padding:  1px;\n"
"margin-right: 35px;\n"
"border-top-left-radius: 2px;\n"
"border-bottom-left-radius: 2px;\n"
"border-top-right-radius: 2px;\n"
"border-bottom-right-radius: 2px;\n"
"background: #333333;\n"
"width: 15px;\n"
"\n"
"}\n"
"QProgressBar::chunk {\n"
"background: rgb(43, 50, 61);\n"
"border-top-left-radius: 2px;\n"
"border-bottom-le"
                        "ft-radius: 2px;\n"
"border-top-right-radius: 2px;\n"
"border-bottom-right-radius: 2px;\n"
"\n"
"border: 1px solid black;\n"
"}")
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setObjectName(u"appMargins")
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setEnabled(True)
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setStyleSheet(u"background-image: url(:/images/images/images/PyCaracterizar.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;")
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setEnabled(True)
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Semibold"])
        font1.setPointSize(12)
        #font1.setWeight(QFont.PreferDefault)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_page_home = QPushButton(self.topMenu)
        self.btn_page_home.setObjectName(u"btn_page_home")
        sizePolicy.setHeightForWidth(self.btn_page_home.sizePolicy().hasHeightForWidth())
        self.btn_page_home.setSizePolicy(sizePolicy)
        self.btn_page_home.setMinimumSize(QSize(0, 45))
        self.btn_page_home.setFont(font)
        self.btn_page_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_page_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_page_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_page_home)

        self.btn_page_measurements = QPushButton(self.topMenu)
        self.btn_page_measurements.setObjectName(u"btn_page_measurements")
        sizePolicy.setHeightForWidth(self.btn_page_measurements.sizePolicy().hasHeightForWidth())
        self.btn_page_measurements.setSizePolicy(sizePolicy)
        self.btn_page_measurements.setMinimumSize(QSize(0, 45))
        self.btn_page_measurements.setFont(font)
        self.btn_page_measurements.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_page_measurements.setLayoutDirection(Qt.LeftToRight)
        self.btn_page_measurements.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-chart-line.png);\n"
"\n"
"\n"
"")

        self.verticalLayout_8.addWidget(self.btn_page_measurements)

        self.btn_page_instruments = QPushButton(self.topMenu)
        self.btn_page_instruments.setObjectName(u"btn_page_instruments")
        sizePolicy.setHeightForWidth(self.btn_page_instruments.sizePolicy().hasHeightForWidth())
        self.btn_page_instruments.setSizePolicy(sizePolicy)
        self.btn_page_instruments.setMinimumSize(QSize(0, 45))
        self.btn_page_instruments.setFont(font)
        self.btn_page_instruments.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_page_instruments.setLayoutDirection(Qt.LeftToRight)
        self.btn_page_instruments.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-gamepad.png);")

        self.verticalLayout_8.addWidget(self.btn_page_instruments)

        self.btn_page_probers = QPushButton(self.topMenu)
        self.btn_page_probers.setObjectName(u"btn_page_probers")
        sizePolicy.setHeightForWidth(self.btn_page_probers.sizePolicy().hasHeightForWidth())
        self.btn_page_probers.setSizePolicy(sizePolicy)
        self.btn_page_probers.setMinimumSize(QSize(0, 45))
        self.btn_page_probers.setFont(font)
        self.btn_page_probers.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_page_probers.setLayoutDirection(Qt.LeftToRight)
        self.btn_page_probers.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-cursor-move.png);\n"
"")

        self.verticalLayout_8.addWidget(self.btn_page_probers)

        self.btn_page_estepa = QPushButton(self.topMenu)
        self.btn_page_estepa.setObjectName(u"btn_page_estepa")
        sizePolicy.setHeightForWidth(self.btn_page_estepa.sizePolicy().hasHeightForWidth())
        self.btn_page_estepa.setSizePolicy(sizePolicy)
        self.btn_page_estepa.setMinimumSize(QSize(0, 45))
        self.btn_page_estepa.setFont(font)
        self.btn_page_estepa.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_page_estepa.setLayoutDirection(Qt.LeftToRight)
        self.btn_page_estepa.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-description.png);\n"
"")

        self.verticalLayout_8.addWidget(self.btn_page_estepa)

        self.btn_page_consult = QPushButton(self.topMenu)
        self.btn_page_consult.setObjectName(u"btn_page_consult")
        sizePolicy.setHeightForWidth(self.btn_page_consult.sizePolicy().hasHeightForWidth())
        self.btn_page_consult.setSizePolicy(sizePolicy)
        self.btn_page_consult.setMinimumSize(QSize(0, 45))
        self.btn_page_consult.setFont(font)
        self.btn_page_consult.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_page_consult.setLayoutDirection(Qt.LeftToRight)
        self.btn_page_consult.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-find-in-page.png);\n"
"\n"
"")

        self.verticalLayout_8.addWidget(self.btn_page_consult)

        self.btn_page_inbase = QPushButton(self.topMenu)
        self.btn_page_inbase.setObjectName(u"btn_page_inbase")
        sizePolicy.setHeightForWidth(self.btn_page_inbase.sizePolicy().hasHeightForWidth())
        self.btn_page_inbase.setSizePolicy(sizePolicy)
        self.btn_page_inbase.setMinimumSize(QSize(0, 45))
        self.btn_page_inbase.setFont(font)
        self.btn_page_inbase.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_page_inbase.setLayoutDirection(Qt.LeftToRight)
        self.btn_page_inbase.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-cloud-upload.png);\n"
"")

        self.verticalLayout_8.addWidget(self.btn_page_inbase)

        self.btn_page_reports = QPushButton(self.topMenu)
        self.btn_page_reports.setObjectName(u"btn_page_reports")
        sizePolicy.setHeightForWidth(self.btn_page_reports.sizePolicy().hasHeightForWidth())
        self.btn_page_reports.setSizePolicy(sizePolicy)
        self.btn_page_reports.setMinimumSize(QSize(0, 45))
        self.btn_page_reports.setFont(font)
        self.btn_page_reports.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_page_reports.setLayoutDirection(Qt.LeftToRight)
        self.btn_page_reports.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-briefcase.png);\n"
"")

        self.verticalLayout_8.addWidget(self.btn_page_reports)

        self.btn_exit = QPushButton(self.topMenu)
        self.btn_exit.setObjectName(u"btn_exit")
        sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        self.btn_exit.setSizePolicy(sizePolicy)
        self.btn_exit.setMinimumSize(QSize(0, 45))
        self.btn_exit.setFont(font)
        self.btn_exit.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_exit.setLayoutDirection(Qt.LeftToRight)
        self.btn_exit.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x.png);")

        self.verticalLayout_8.addWidget(self.btn_exit)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggleLeftBox = QPushButton(self.bottomMenu)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LeftToRight)
        self.toggleLeftBox.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_settings.png);")

        self.verticalLayout_9.addWidget(self.toggleLeftBox)


        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setFrameShape(QFrame.NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.stackedWidget_configuration = QStackedWidget(self.extraTopMenu)
        self.stackedWidget_configuration.setObjectName(u"stackedWidget_configuration")
        self.stackedWidget_configuration.setStyleSheet(u"\n"
"background: transparent;\n"
"\n"
"")
        self.stackedWidget_configuration.setFrameShape(QFrame.NoFrame)
        self.configuration_measurements = QWidget()
        self.configuration_measurements.setObjectName(u"configuration_measurements")
        self.verticalLayout_config_meas = QVBoxLayout(self.configuration_measurements)
        self.verticalLayout_config_meas.setObjectName(u"verticalLayout_config_meas")
        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.label_txtProcess = QLabel(self.configuration_measurements)
        self.label_txtProcess.setObjectName(u"label_txtProcess")

        self.verticalLayout_23.addWidget(self.label_txtProcess)

        self.txtProcess = QLineEdit(self.configuration_measurements)
        self.txtProcess.setObjectName(u"txtProcess")
        self.txtProcess.setMaximumSize(QSize(200, 40))
        self.txtProcess.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.txtProcess.setReadOnly(False)

        self.verticalLayout_23.addWidget(self.txtProcess)

        self.verticalSpacer_txtProcess = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_23.addItem(self.verticalSpacer_txtProcess)

        self.label_txtLot = QLabel(self.configuration_measurements)
        self.label_txtLot.setObjectName(u"label_txtLot")

        self.verticalLayout_23.addWidget(self.label_txtLot)

        self.txtLot = QLineEdit(self.configuration_measurements)
        self.txtLot.setObjectName(u"txtLot")
        self.txtLot.setMaximumSize(QSize(200, 40))
        self.txtLot.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.txtLot.setReadOnly(False)

        self.verticalLayout_23.addWidget(self.txtLot)

        self.verticalSpacer_txtLot = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_23.addItem(self.verticalSpacer_txtLot)

        self.label_txtWafer = QLabel(self.configuration_measurements)
        self.label_txtWafer.setObjectName(u"label_txtWafer")

        self.verticalLayout_23.addWidget(self.label_txtWafer)

        self.txtWafer = QLineEdit(self.configuration_measurements)
        self.txtWafer.setObjectName(u"txtWafer")
        self.txtWafer.setMaximumSize(QSize(200, 40))
        self.txtWafer.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.txtWafer.setReadOnly(False)

        self.verticalLayout_23.addWidget(self.txtWafer)

        self.verticalSpacer_txtWafer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_23.addItem(self.verticalSpacer_txtWafer)

        self.label_txtMask = QLabel(self.configuration_measurements)
        self.label_txtMask.setObjectName(u"label_txtMask")

        self.verticalLayout_23.addWidget(self.label_txtMask)

        self.txtMask = QLineEdit(self.configuration_measurements)
        self.txtMask.setObjectName(u"txtMask")
        self.txtMask.setMaximumSize(QSize(200, 40))
        self.txtMask.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.txtMask.setReadOnly(False)

        self.verticalLayout_23.addWidget(self.txtMask)

        self.verticalSpacer_txtWafer1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_23.addItem(self.verticalSpacer_txtWafer1)

        self.label_txtTemperature = QLabel(self.configuration_measurements)
        self.label_txtTemperature.setObjectName(u"label_txtTemperature")

        self.verticalLayout_23.addWidget(self.label_txtTemperature)

        self.txtTemperature = QLineEdit(self.configuration_measurements)
        self.txtTemperature.setObjectName(u"txtTemperature")
        self.txtTemperature.setMaximumSize(QSize(200, 40))
        self.txtTemperature.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.txtTemperature.setReadOnly(False)

        self.verticalLayout_23.addWidget(self.txtTemperature)

        self.verticalSpacer_txtWafer2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_23.addItem(self.verticalSpacer_txtWafer2)

        self.label_txtHumidity = QLabel(self.configuration_measurements)
        self.label_txtHumidity.setObjectName(u"label_txtHumidity")

        self.verticalLayout_23.addWidget(self.label_txtHumidity)

        self.txtHumidity = QLineEdit(self.configuration_measurements)
        self.txtHumidity.setObjectName(u"txtHumidity")
        self.txtHumidity.setMaximumSize(QSize(200, 40))
        self.txtHumidity.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.txtHumidity.setReadOnly(False)

        self.verticalLayout_23.addWidget(self.txtHumidity)

        self.verticalSpacer_txtMask = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_23.addItem(self.verticalSpacer_txtMask)

        self.chkDarkMode = QCheckBox(self.configuration_measurements)
        self.chkDarkMode.setObjectName(u"chkDarkMode")
        self.chkDarkMode.setEnabled(True)
        self.chkDarkMode.setAutoFillBackground(False)
        self.chkDarkMode.setStyleSheet(u"")
        self.chkDarkMode.setChecked(True)

        self.verticalLayout_23.addWidget(self.chkDarkMode)

        self.verticalSpacer_dark_4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_23.addItem(self.verticalSpacer_dark_4)

        self.chkViewEstepa = QCheckBox(self.configuration_measurements)
        self.chkViewEstepa.setObjectName(u"chkViewEstepa")
        self.chkViewEstepa.setEnabled(True)
        self.chkViewEstepa.setAutoFillBackground(False)
        self.chkViewEstepa.setStyleSheet(u"")
        self.chkViewEstepa.setChecked(True)

        self.verticalLayout_23.addWidget(self.chkViewEstepa)

        self.verticalSpacer_viewEstepa = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_23.addItem(self.verticalSpacer_viewEstepa)

        self.chkViewGraph = QCheckBox(self.configuration_measurements)
        self.chkViewGraph.setObjectName(u"chkViewGraph")
        self.chkViewGraph.setEnabled(True)
        self.chkViewGraph.setAutoFillBackground(False)
        self.chkViewGraph.setStyleSheet(u"")
        self.chkViewGraph.setChecked(False)

        self.verticalLayout_23.addWidget(self.chkViewGraph)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_23.addItem(self.verticalSpacer_4)

        self.chkViewPosition = QCheckBox(self.configuration_measurements)
        self.chkViewPosition.setObjectName(u"chkViewPosition")
        self.chkViewPosition.setAutoFillBackground(False)
        self.chkViewPosition.setStyleSheet(u"")
        self.chkViewPosition.setChecked(False)

        self.verticalLayout_23.addWidget(self.chkViewPosition)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_23.addItem(self.verticalSpacer_5)

        self.chkSaveMeasurementAuto = QCheckBox(self.configuration_measurements)
        self.chkSaveMeasurementAuto.setObjectName(u"chkSaveMeasurementAuto")
        self.chkSaveMeasurementAuto.setAutoFillBackground(False)
        self.chkSaveMeasurementAuto.setStyleSheet(u"")
        self.chkSaveMeasurementAuto.setChecked(True)

        self.verticalLayout_23.addWidget(self.chkSaveMeasurementAuto)


        self.verticalLayout_config_meas.addLayout(self.verticalLayout_23)

        self.stackedWidget_configuration.addWidget(self.configuration_measurements)
        self.configuration_estepa = QWidget()
        self.configuration_estepa.setObjectName(u"configuration_estepa")
        self.verticalLayout_config_estepa = QVBoxLayout(self.configuration_estepa)
        self.verticalLayout_config_estepa.setObjectName(u"verticalLayout_config_estepa")
        self.Outliner_2 = QLabel(self.configuration_estepa)
        self.Outliner_2.setObjectName(u"Outliner_2")
        self.Outliner_2.setMaximumSize(QSize(400, 20))
        self.Outliner_2.setStyleSheet(u"")

        self.verticalLayout_config_estepa.addWidget(self.Outliner_2)

        self.cmbOutlinerMethod = QComboBox(self.configuration_estepa)
        self.cmbOutlinerMethod.addItem("")
        self.cmbOutlinerMethod.addItem("")
        self.cmbOutlinerMethod.addItem("")
        self.cmbOutlinerMethod.setObjectName(u"cmbOutlinerMethod")
        self.cmbOutlinerMethod.setEditable(False)
        self.cmbOutlinerMethod.setMinimumContentsLength(0)

        self.verticalLayout_config_estepa.addWidget(self.cmbOutlinerMethod)

        self.chkNonAutomaticLimits = QCheckBox(self.configuration_estepa)
        self.chkNonAutomaticLimits.setObjectName(u"chkNonAutomaticLimits")

        self.verticalLayout_config_estepa.addWidget(self.chkNonAutomaticLimits)

        self.optionsNonAutomatic = QStackedWidget(self.configuration_estepa)
        self.optionsNonAutomatic.setObjectName(u"optionsNonAutomatic")
        self.optionsNonAutomatic.setMinimumSize(QSize(200, 20))
        self.optionsNonAutomatic.setMaximumSize(QSize(200, 100))
        self.config_Automatic = QWidget()
        self.config_Automatic.setObjectName(u"config_Automatic")
        self.optionsNonAutomatic.addWidget(self.config_Automatic)
        self.config_nonAutomatic = QWidget()
        self.config_nonAutomatic.setObjectName(u"config_nonAutomatic")
        self.verticalLayout_22 = QVBoxLayout(self.config_nonAutomatic)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.chkGetAutoLimits = QCheckBox(self.config_nonAutomatic)
        self.chkGetAutoLimits.setObjectName(u"chkGetAutoLimits")

        self.verticalLayout_22.addWidget(self.chkGetAutoLimits)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.labelVersion_25 = QLabel(self.config_nonAutomatic)
        self.labelVersion_25.setObjectName(u"labelVersion_25")
        self.labelVersion_25.setMaximumSize(QSize(200, 20))
        self.labelVersion_25.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_25.setLineWidth(1)
        self.labelVersion_25.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.labelVersion_25, 0, 1, 1, 1)

        self.labelVersion_24 = QLabel(self.config_nonAutomatic)
        self.labelVersion_24.setObjectName(u"labelVersion_24")
        self.labelVersion_24.setMaximumSize(QSize(200, 20))
        self.labelVersion_24.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_24.setLineWidth(1)
        self.labelVersion_24.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.labelVersion_24, 0, 0, 1, 1)

        self.txtLimitMin = QLineEdit(self.config_nonAutomatic)
        self.txtLimitMin.setObjectName(u"txtLimitMin")
        self.txtLimitMin.setEnabled(True)
        self.txtLimitMin.setMinimumSize(QSize(50, 30))
        self.txtLimitMin.setMaximumSize(QSize(50, 30))
        self.txtLimitMin.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_4.addWidget(self.txtLimitMin, 1, 0, 1, 1)

        self.txtLimitMax = QLineEdit(self.config_nonAutomatic)
        self.txtLimitMax.setObjectName(u"txtLimitMax")
        self.txtLimitMax.setEnabled(True)
        self.txtLimitMax.setMinimumSize(QSize(50, 30))
        self.txtLimitMax.setMaximumSize(QSize(50, 30))
        self.txtLimitMax.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_4.addWidget(self.txtLimitMax, 1, 1, 1, 1)


        self.verticalLayout_22.addLayout(self.gridLayout_4)

        self.optionsNonAutomatic.addWidget(self.config_nonAutomatic)

        self.verticalLayout_config_estepa.addWidget(self.optionsNonAutomatic)

        self.verticalSpacer_estepa = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_config_estepa.addItem(self.verticalSpacer_estepa)

        self.Font_2 = QLabel(self.configuration_estepa)
        self.Font_2.setObjectName(u"Font_2")
        self.Font_2.setMaximumSize(QSize(400, 16777215))
        self.Font_2.setStyleSheet(u"")

        self.verticalLayout_config_estepa.addWidget(self.Font_2)

        self.cmbFontSize = QComboBox(self.configuration_estepa)
        self.cmbFontSize.addItem("")
        self.cmbFontSize.addItem("")
        self.cmbFontSize.setObjectName(u"cmbFontSize")
        self.cmbFontSize.setEditable(False)
        self.cmbFontSize.setMinimumContentsLength(0)

        self.verticalLayout_config_estepa.addWidget(self.cmbFontSize)

        self.Performance_2 = QLabel(self.configuration_estepa)
        self.Performance_2.setObjectName(u"Performance_2")
        self.Performance_2.setMaximumSize(QSize(400, 16777215))
        self.Performance_2.setStyleSheet(u"")

        self.verticalLayout_config_estepa.addWidget(self.Performance_2)

        self.cmbPerformancePresentation = QComboBox(self.configuration_estepa)
        self.cmbPerformancePresentation.addItem("")
        self.cmbPerformancePresentation.addItem("")
        self.cmbPerformancePresentation.setObjectName(u"cmbPerformancePresentation")
        self.cmbPerformancePresentation.setEditable(False)
        self.cmbPerformancePresentation.setMinimumContentsLength(0)

        self.verticalLayout_config_estepa.addWidget(self.cmbPerformancePresentation)

        self.Wafer_2 = QLabel(self.configuration_estepa)
        self.Wafer_2.setObjectName(u"Wafer_2")
        self.Wafer_2.setMaximumSize(QSize(400, 16777215))
        self.Wafer_2.setStyleSheet(u"")

        self.verticalLayout_config_estepa.addWidget(self.Wafer_2)

        self.cmbWaferRepresentation = QComboBox(self.configuration_estepa)
        self.cmbWaferRepresentation.addItem("")
        self.cmbWaferRepresentation.addItem("")
        self.cmbWaferRepresentation.addItem("")
        self.cmbWaferRepresentation.setObjectName(u"cmbWaferRepresentation")
        self.cmbWaferRepresentation.setEditable(False)
        self.cmbWaferRepresentation.setMinimumContentsLength(0)

        self.verticalLayout_config_estepa.addWidget(self.cmbWaferRepresentation)

        self.HistogramTextLabel = QLabel(self.configuration_estepa)
        self.HistogramTextLabel.setObjectName(u"HistogramTextLabel")

        self.verticalLayout_config_estepa.addWidget(self.HistogramTextLabel)

        self.scrollHistogramChunks = QScrollBar(self.configuration_estepa)
        self.scrollHistogramChunks.setObjectName(u"scrollHistogramChunks")
        self.scrollHistogramChunks.setStyleSheet(u" QScrollBar:vertical { background: rgb(52, 59, 72); }\\n QScrollBar:horizontal { background: rgb(52, 59, 72); }")
        self.scrollHistogramChunks.setMinimum(2)
        self.scrollHistogramChunks.setMaximum(21)
        self.scrollHistogramChunks.setSingleStep(1)
        self.scrollHistogramChunks.setValue(16)
        self.scrollHistogramChunks.setOrientation(Qt.Horizontal)

        self.verticalLayout_config_estepa.addWidget(self.scrollHistogramChunks)

        self.txtHistogramChunks = QLineEdit(self.configuration_estepa)
        self.txtHistogramChunks.setObjectName(u"txtHistogramChunks")
        self.txtHistogramChunks.setEnabled(False)
        self.txtHistogramChunks.setMinimumSize(QSize(100, 30))
        self.txtHistogramChunks.setMaximumSize(QSize(100, 30))
        self.txtHistogramChunks.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.verticalLayout_config_estepa.addWidget(self.txtHistogramChunks)

        self.stackedWidget_configuration.addWidget(self.configuration_estepa)
        self.configuration_reports = QWidget()
        self.configuration_reports.setObjectName(u"configuration_reports")
        self.verticalLayout_config_report = QVBoxLayout(self.configuration_reports)
        self.verticalLayout_config_report.setObjectName(u"verticalLayout_config_report")
        self.verticalLayout_report = QVBoxLayout()
        self.verticalLayout_report.setSpacing(0)
        self.verticalLayout_report.setObjectName(u"verticalLayout_report")
        self.reportTitleLabel = QLabel(self.configuration_reports)
        self.reportTitleLabel.setObjectName(u"reportTitleLabel")

        self.verticalLayout_report.addWidget(self.reportTitleLabel)

        self.txtReportTitle = QLineEdit(self.configuration_reports)
        self.txtReportTitle.setObjectName(u"txtReportTitle")
        self.txtReportTitle.setMaximumSize(QSize(200, 40))
        self.txtReportTitle.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.txtReportTitle.setReadOnly(False)

        self.verticalLayout_report.addWidget(self.txtReportTitle)

        self.verticalSpacer_title = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_report.addItem(self.verticalSpacer_title)

        self.reportSubtitleLabel = QLabel(self.configuration_reports)
        self.reportSubtitleLabel.setObjectName(u"reportSubtitleLabel")

        self.verticalLayout_report.addWidget(self.reportSubtitleLabel)

        self.txtReportSubtitle = QLineEdit(self.configuration_reports)
        self.txtReportSubtitle.setObjectName(u"txtReportSubtitle")
        self.txtReportSubtitle.setMaximumSize(QSize(200, 40))
        self.txtReportSubtitle.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.txtReportSubtitle.setReadOnly(False)

        self.verticalLayout_report.addWidget(self.txtReportSubtitle)

        self.verticalSpacer_subtitle = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_report.addItem(self.verticalSpacer_subtitle)

        self.reportDateLabel = QLabel(self.configuration_reports)
        self.reportDateLabel.setObjectName(u"reportDateLabel")

        self.verticalLayout_report.addWidget(self.reportDateLabel)

        self.txtReportDate = QLineEdit(self.configuration_reports)
        self.txtReportDate.setObjectName(u"txtReportDate")
        self.txtReportDate.setMaximumSize(QSize(200, 40))
        self.txtReportDate.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.txtReportDate.setReadOnly(False)

        self.verticalLayout_report.addWidget(self.txtReportDate)

        self.verticalSpacer_date = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_report.addItem(self.verticalSpacer_date)

        self.reportAuthorLabel = QLabel(self.configuration_reports)
        self.reportAuthorLabel.setObjectName(u"reportAuthorLabel")

        self.verticalLayout_report.addWidget(self.reportAuthorLabel)

        self.txtReportAuthor = QLineEdit(self.configuration_reports)
        self.txtReportAuthor.setObjectName(u"txtReportAuthor")
        self.txtReportAuthor.setMaximumSize(QSize(200, 40))
        self.txtReportAuthor.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.txtReportAuthor.setReadOnly(False)

        self.verticalLayout_report.addWidget(self.txtReportAuthor)

        self.verticalSpacer_reportTitle = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_report.addItem(self.verticalSpacer_reportTitle)


        self.verticalLayout_config_report.addLayout(self.verticalLayout_report)

        self.stackedWidget_configuration.addWidget(self.configuration_reports)

        self.verticalLayout_11.addWidget(self.stackedWidget_configuration)


        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignTop)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")

        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsTopBtn.setIcon(icon1)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.btn_message = QPushButton(self.topMenus)
        self.btn_message.setObjectName(u"btn_message")
        sizePolicy.setHeightForWidth(self.btn_message.sizePolicy().hasHeightForWidth())
        self.btn_message.setSizePolicy(sizePolicy)
        self.btn_message.setMinimumSize(QSize(0, 45))
        self.btn_message.setFont(font)
        self.btn_message.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_message.setLayoutDirection(Qt.LeftToRight)
        self.btn_message.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-envelope-open.png);")

        self.verticalLayout_14.addWidget(self.btn_message)

        self.btn_print = QPushButton(self.topMenus)
        self.btn_print.setObjectName(u"btn_print")
        sizePolicy.setHeightForWidth(self.btn_print.sizePolicy().hasHeightForWidth())
        self.btn_print.setSizePolicy(sizePolicy)
        self.btn_print.setMinimumSize(QSize(0, 45))
        self.btn_print.setFont(font)
        self.btn_print.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_print.setLayoutDirection(Qt.LeftToRight)
        self.btn_print.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-print.png);")

        self.verticalLayout_14.addWidget(self.btn_print)

        self.btn_logout = QPushButton(self.topMenus)
        self.btn_logout.setObjectName(u"btn_logout")
        sizePolicy.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
        self.btn_logout.setSizePolicy(sizePolicy)
        self.btn_logout.setMinimumSize(QSize(0, 45))
        self.btn_logout.setFont(font)
        self.btn_logout.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_logout.setLayoutDirection(Qt.LeftToRight)
        self.btn_logout.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-account-logout.png);")

        self.verticalLayout_14.addWidget(self.btn_logout)


        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)


        self.verticalLayout_7.addWidget(self.contentSettings)


        self.horizontalLayout_4.addWidget(self.extraRightBox)

        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_33 = QHBoxLayout(self.pagesContainer)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(0, 0))
        self.stackedWidget.setStyleSheet(u"\n"
"background: transparent;\n"
"\n"
"")
        self.stackedWidget.setFrameShape(QFrame.NoFrame)
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"background-image: url(:/images/images/images/PyDracula_vertical.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;")
        self.stackedWidget.addWidget(self.home)
        self.measurements = QWidget()
        self.measurements.setObjectName(u"measurements")
        self.verticalLayout_24 = QVBoxLayout(self.measurements)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_2 = QLabel(self.measurements)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 20))
        self.label_2.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_24.addWidget(self.label_2)

        self.verticalSpacer = QSpacerItem(13, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_24.addItem(self.verticalSpacer)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.verticalLayout_40 = QVBoxLayout()
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.gridLayout_18 = QGridLayout()
        self.gridLayout_18.setSpacing(0)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_18.setContentsMargins(-1, 0, 0, -1)
        self.cmbInstruments = QComboBox(self.measurements)
        self.cmbInstruments.addItem("")
        self.cmbInstruments.setObjectName(u"cmbInstruments")
        self.cmbInstruments.setMinimumSize(QSize(150, 0))
        self.cmbInstruments.setMaximumSize(QSize(150, 16777215))
        self.cmbInstruments.setFont(font)
        self.cmbInstruments.setAutoFillBackground(False)
        self.cmbInstruments.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbInstruments.setIconSize(QSize(16, 16))
        self.cmbInstruments.setFrame(True)

        self.gridLayout_18.addWidget(self.cmbInstruments, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(24, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.cmbTests = QComboBox(self.measurements)
        self.cmbTests.addItem("")
        self.cmbTests.setObjectName(u"cmbTests")
        self.cmbTests.setMinimumSize(QSize(150, 0))
        self.cmbTests.setMaximumSize(QSize(150, 16777215))
        self.cmbTests.setFont(font)
        self.cmbTests.setAutoFillBackground(False)
        self.cmbTests.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbTests.setIconSize(QSize(16, 16))
        self.cmbTests.setFrame(True)

        self.gridLayout_18.addWidget(self.cmbTests, 0, 2, 1, 1)


        self.verticalLayout_40.addLayout(self.gridLayout_18)


        self.horizontalLayout_29.addLayout(self.verticalLayout_40)

        self.horizontalSpacer_28 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_28)

        self.btnParameters = QPushButton(self.measurements)
        self.btnParameters.setObjectName(u"btnParameters")
        self.btnParameters.setEnabled(True)
        self.btnParameters.setMinimumSize(QSize(30, 30))
        self.btnParameters.setMaximumSize(QSize(30, 16777215))
        self.btnParameters.setFont(font)
        self.btnParameters.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnParameters.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        self.btnParameters.setIcon(icon1)
        self.btnParameters.setFlat(False)

        self.horizontalLayout_29.addWidget(self.btnParameters)

        self.horizontalSpacer_8 = QSpacerItem(15, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_8)

        self.chkCartoMeas = QCheckBox(self.measurements)
        self.chkCartoMeas.setObjectName(u"chkCartoMeas")

        self.horizontalLayout_29.addWidget(self.chkCartoMeas)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_27)

        self.verticalLayout_43 = QVBoxLayout()
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.btnStart = QPushButton(self.measurements)
        self.btnStart.setObjectName(u"btnStart")
        self.btnStart.setMinimumSize(QSize(100, 30))
        self.btnStart.setMaximumSize(QSize(100, 16777215))
        self.btnStart.setFont(font)
        self.btnStart.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnStart.setStyleSheet(u"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/cil-caret-right.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnStart.setIcon(icon4)

        self.gridLayout_6.addWidget(self.btnStart, 0, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_6, 0, 3, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_5, 0, 1, 1, 1)

        self.btnPause = QPushButton(self.measurements)
        self.btnPause.setObjectName(u"btnPause")
        self.btnPause.setEnabled(False)
        self.btnPause.setMinimumSize(QSize(100, 30))
        self.btnPause.setMaximumSize(QSize(100, 16777215))
        self.btnPause.setFont(font)
        self.btnPause.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnPause.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/icons/cil-media-pause.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnPause.setIcon(icon5)

        self.gridLayout_6.addWidget(self.btnPause, 0, 2, 1, 1)

        self.btnStop = QPushButton(self.measurements)
        self.btnStop.setObjectName(u"btnStop")
        self.btnStop.setEnabled(False)
        self.btnStop.setMinimumSize(QSize(100, 30))
        self.btnStop.setMaximumSize(QSize(100, 16777215))
        self.btnStop.setFont(font)
        self.btnStop.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnStop.setStyleSheet(u"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/icons/images/icons/cil-media-stop.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnStop.setIcon(icon6)

        self.gridLayout_6.addWidget(self.btnStop, 0, 4, 1, 1)


        self.verticalLayout_43.addLayout(self.gridLayout_6)


        self.horizontalLayout_29.addLayout(self.verticalLayout_43)


        self.verticalLayout_24.addLayout(self.horizontalLayout_29)

        self.verticalSpacer_17 = QSpacerItem(13, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_24.addItem(self.verticalSpacer_17)

        self.gridLayoutCarto = QGridLayout()
        self.gridLayoutCarto.setObjectName(u"gridLayoutCarto")
        self.cmbProbers = QComboBox(self.measurements)
        self.cmbProbers.addItem("")
        self.cmbProbers.setObjectName(u"cmbProbers")
        self.cmbProbers.setMinimumSize(QSize(150, 0))
        self.cmbProbers.setMaximumSize(QSize(150, 16777215))
        self.cmbProbers.setFont(font)
        self.cmbProbers.setAutoFillBackground(False)
        self.cmbProbers.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbProbers.setIconSize(QSize(16, 16))
        self.cmbProbers.setFrame(True)

        self.gridLayoutCarto.addWidget(self.cmbProbers, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(24, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayoutCarto.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.cmbWafermaps = QComboBox(self.measurements)
        self.cmbWafermaps.addItem("")
        self.cmbWafermaps.setObjectName(u"cmbWafermaps")
        self.cmbWafermaps.setMinimumSize(QSize(150, 0))
        self.cmbWafermaps.setMaximumSize(QSize(150, 16777215))
        self.cmbWafermaps.setFont(font)
        self.cmbWafermaps.setAutoFillBackground(False)
        self.cmbWafermaps.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbWafermaps.setIconSize(QSize(16, 16))
        self.cmbWafermaps.setFrame(True)

        self.horizontalLayout_28.addWidget(self.cmbWafermaps)

        self.horizontalSpacer_4 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_4)

        self.btnGoHome = QPushButton(self.measurements)
        self.btnGoHome.setObjectName(u"btnGoHome")
        self.btnGoHome.setEnabled(True)
        self.btnGoHome.setMinimumSize(QSize(30, 30))
        self.btnGoHome.setMaximumSize(QSize(30, 16777215))
        self.btnGoHome.setFont(font)
        self.btnGoHome.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnGoHome.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u":/icons/images/icons/cil-home.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnGoHome.setIcon(icon7)
        self.btnGoHome.setFlat(False)

        self.horizontalLayout_28.addWidget(self.btnGoHome)

        self.horizontalSpacer_26 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_26)

        self.btnViewWafermap = QPushButton(self.measurements)
        self.btnViewWafermap.setObjectName(u"btnViewWafermap")
        self.btnViewWafermap.setEnabled(True)
        self.btnViewWafermap.setMinimumSize(QSize(30, 30))
        self.btnViewWafermap.setMaximumSize(QSize(30, 16777215))
        self.btnViewWafermap.setFont(font)
        self.btnViewWafermap.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnViewWafermap.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u":/icons/images/icons/cil-window-maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnViewWafermap.setIcon(icon8)
        self.btnViewWafermap.setFlat(False)

        self.horizontalLayout_28.addWidget(self.btnViewWafermap)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_2)


        self.gridLayoutCarto.addLayout(self.horizontalLayout_28, 0, 2, 1, 1)


        self.verticalLayout_24.addLayout(self.gridLayoutCarto)

        self.verticalSpacer_2 = QSpacerItem(13, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_24.addItem(self.verticalSpacer_2)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.tabWidget = QTabWidget(self.measurements)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(400, 0))
        self.tabWidget.setMaximumSize(QSize(400, 16777215))
        self.tabWidget.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.pteTest = QPlainTextEdit(self.tab)
        self.pteTest.setObjectName(u"pteTest")
        self.pteTest.setEnabled(True)
        self.pteTest.setGeometry(QRect(0, 10, 400, 531))
        self.pteTest.setMinimumSize(QSize(400, 0))
        self.pteTest.setMaximumSize(QSize(400, 16777215))
        self.pteTest.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.pteTest.setReadOnly(True)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.pteWafermap = QPlainTextEdit(self.tab_3)
        self.pteWafermap.setObjectName(u"pteWafermap")
        self.pteWafermap.setEnabled(True)
        self.pteWafermap.setGeometry(QRect(0, 10, 400, 531))
        self.pteWafermap.setMinimumSize(QSize(400, 0))
        self.pteWafermap.setMaximumSize(QSize(400, 16777215))
        self.pteWafermap.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.pteWafermap.setReadOnly(True)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_41 = QVBoxLayout(self.tab_2)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.pteDescription = QPlainTextEdit(self.tab_2)
        self.pteDescription.setObjectName(u"pteDescription")
        self.pteDescription.setEnabled(True)
        self.pteDescription.setMinimumSize(QSize(400, 0))
        self.pteDescription.setMaximumSize(QSize(400, 16777215))
        self.pteDescription.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.pteDescription.setReadOnly(True)

        self.verticalLayout_41.addWidget(self.pteDescription)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.test_status = QLabel(self.tab_2)
        self.test_status.setObjectName(u"test_status")
        self.test_status.setMinimumSize(QSize(60, 0))
        self.test_status.setMaximumSize(QSize(60, 20))
        self.test_status.setStyleSheet(u"font: 8pt \"Segoe UI\";\n"
"background-color: #333333;\n"
"border-radius: 10px;")
        self.test_status.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.test_status)

        self.measurement_status = QLabel(self.tab_2)
        self.measurement_status.setObjectName(u"measurement_status")
        self.measurement_status.setMinimumSize(QSize(60, 0))
        self.measurement_status.setMaximumSize(QSize(60, 20))
        self.measurement_status.setStyleSheet(u"font: 8pt \"Segoe UI\";\n"
"background-color: #333333;\n"
"border-radius: 10px;")
        self.measurement_status.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.measurement_status)

        self.contact_status = QLabel(self.tab_2)
        self.contact_status.setObjectName(u"contact_status")
        self.contact_status.setMinimumSize(QSize(60, 0))
        self.contact_status.setMaximumSize(QSize(60, 20))
        self.contact_status.setStyleSheet(u"font: 8pt \"Segoe UI\";\n"
"background-color: #333333;\n"
"border-radius: 10px;")
        self.contact_status.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.contact_status)

        self.separation_status = QLabel(self.tab_2)
        self.separation_status.setObjectName(u"separation_status")
        self.separation_status.setMinimumSize(QSize(60, 0))
        self.separation_status.setMaximumSize(QSize(60, 20))
        self.separation_status.setStyleSheet(u"font: 8pt \"Segoe UI\";\n"
"background-color: #333333;\n"
"border-radius: 10px;")
        self.separation_status.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.separation_status)

        self.horizontalSpacer_10 = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_10)

        self.btnSaveDescription = QPushButton(self.tab_2)
        self.btnSaveDescription.setObjectName(u"btnSaveDescription")
        self.btnSaveDescription.setEnabled(True)
        self.btnSaveDescription.setMinimumSize(QSize(30, 30))
        self.btnSaveDescription.setMaximumSize(QSize(30, 16777215))
        self.btnSaveDescription.setFont(font)
        self.btnSaveDescription.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnSaveDescription.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u":/icons/images/icons/cil-save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnSaveDescription.setIcon(icon9)
        self.btnSaveDescription.setFlat(False)

        self.horizontalLayout_6.addWidget(self.btnSaveDescription)

        self.btnClearDescription = QPushButton(self.tab_2)
        self.btnClearDescription.setObjectName(u"btnClearDescription")
        self.btnClearDescription.setEnabled(True)
        self.btnClearDescription.setMinimumSize(QSize(30, 30))
        self.btnClearDescription.setMaximumSize(QSize(30, 16777215))
        self.btnClearDescription.setFont(font)
        self.btnClearDescription.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnClearDescription.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u":/icons/images/icons/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnClearDescription.setIcon(icon10)
        self.btnClearDescription.setFlat(False)

        self.horizontalLayout_6.addWidget(self.btnClearDescription)


        self.verticalLayout_41.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.progressBar = QProgressBar(self.tab_2)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 20))
        self.progressBar.setMaximumSize(QSize(16777215, 20))
        self.progressBar.setStyleSheet(u"")
        self.progressBar.setValue(0)

        self.gridLayout_12.addWidget(self.progressBar, 0, 0, 1, 1)


        self.verticalLayout_21.addLayout(self.gridLayout_12)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_21.addItem(self.verticalSpacer_3)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_14.addWidget(self.label)

        self.dieActual = QLineEdit(self.tab_2)
        self.dieActual.setObjectName(u"dieActual")
        self.dieActual.setMaximumSize(QSize(45, 16777215))
        self.dieActual.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.dieActual.setReadOnly(True)

        self.horizontalLayout_14.addWidget(self.dieActual)

        self.labelVersion_7 = QLabel(self.tab_2)
        self.labelVersion_7.setObjectName(u"labelVersion_7")
        self.labelVersion_7.setMinimumSize(QSize(0, 20))
        self.labelVersion_7.setMaximumSize(QSize(16, 20))
        self.labelVersion_7.setStyleSheet(u"color: rgb(113, 126, 149);\n"
"font: 8pt \"Segoe UI\";")
        self.labelVersion_7.setLineWidth(1)
        self.labelVersion_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_14.addWidget(self.labelVersion_7)

        self.dieTotal = QLineEdit(self.tab_2)
        self.dieTotal.setObjectName(u"dieTotal")
        self.dieTotal.setMaximumSize(QSize(45, 16777215))
        self.dieTotal.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.dieTotal.setReadOnly(True)

        self.horizontalLayout_14.addWidget(self.dieTotal)


        self.gridLayout_7.addLayout(self.horizontalLayout_14, 0, 0, 1, 1)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_15.addWidget(self.label_5)

        self.moduleActual = QLineEdit(self.tab_2)
        self.moduleActual.setObjectName(u"moduleActual")
        self.moduleActual.setMaximumSize(QSize(45, 16777215))
        self.moduleActual.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.moduleActual.setReadOnly(True)

        self.horizontalLayout_15.addWidget(self.moduleActual)

        self.labelVersion_8 = QLabel(self.tab_2)
        self.labelVersion_8.setObjectName(u"labelVersion_8")
        self.labelVersion_8.setMinimumSize(QSize(0, 20))
        self.labelVersion_8.setMaximumSize(QSize(16, 20))
        self.labelVersion_8.setStyleSheet(u"color: rgb(113, 126, 149);\n"
"font: 8pt \"Segoe UI\";")
        self.labelVersion_8.setLineWidth(1)
        self.labelVersion_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.labelVersion_8)

        self.moduleTotal = QLineEdit(self.tab_2)
        self.moduleTotal.setObjectName(u"moduleTotal")
        self.moduleTotal.setMaximumSize(QSize(45, 16777215))
        self.moduleTotal.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.moduleTotal.setReadOnly(True)

        self.horizontalLayout_15.addWidget(self.moduleTotal)


        self.gridLayout_7.addLayout(self.horizontalLayout_15, 1, 0, 1, 1)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_6 = QLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_16.addWidget(self.label_6)

        self.timeInit = QLineEdit(self.tab_2)
        self.timeInit.setObjectName(u"timeInit")
        self.timeInit.setMaximumSize(QSize(120, 16777215))
        self.timeInit.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.timeInit.setReadOnly(True)

        self.horizontalLayout_16.addWidget(self.timeInit)


        self.gridLayout_7.addLayout(self.horizontalLayout_16, 0, 2, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_12, 1, 1, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_11, 0, 1, 1, 1)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_17.addWidget(self.label_7)

        self.timeFinish = QLineEdit(self.tab_2)
        self.timeFinish.setObjectName(u"timeFinish")
        self.timeFinish.setMaximumSize(QSize(120, 16777215))
        self.timeFinish.setStyleSheet(u"font: 8pt \"Segoe UI\";")
        self.timeFinish.setReadOnly(True)

        self.horizontalLayout_17.addWidget(self.timeFinish)


        self.gridLayout_7.addLayout(self.horizontalLayout_17, 1, 2, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_7.addItem(self.verticalSpacer_7, 2, 1, 1, 1)


        self.verticalLayout_21.addLayout(self.gridLayout_7)


        self.horizontalLayout_27.addLayout(self.verticalLayout_21)


        self.verticalLayout_41.addLayout(self.horizontalLayout_27)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_20.addWidget(self.tabWidget)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")

        self.verticalLayout_20.addLayout(self.horizontalLayout_26)


        self.horizontalLayout_24.addLayout(self.verticalLayout_20)

        self.horizontalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_7)

        self.verticalLayout_42 = QVBoxLayout()
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")

        self.horizontalLayout_24.addLayout(self.verticalLayout_42)

        self.tabGraph = QTabWidget(self.measurements)
        self.tabGraph.setObjectName(u"tabGraph")
        self.tabGraph.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.tabWafermap_3 = QWidget()
        self.tabWafermap_3.setObjectName(u"tabWafermap_3")
        self.verticalLayout_45 = QVBoxLayout(self.tabWafermap_3)
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_34 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_34)

        self.horizontalLayout_btnGraph = QHBoxLayout()
        self.horizontalLayout_btnGraph.setObjectName(u"horizontalLayout_btnGraph")

        self.horizontalLayout_32.addLayout(self.horizontalLayout_btnGraph)

        self.horizontalSpacer_35 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_35)


        self.verticalLayout_45.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_graph = QHBoxLayout()
        self.horizontalLayout_graph.setObjectName(u"horizontalLayout_graph")
        self.horizontalLayout_graph.setSizeConstraint(QLayout.SetMaximumSize)

        self.verticalLayout_45.addLayout(self.horizontalLayout_graph)

        self.horizontalLayout_BtnGraph = QHBoxLayout()
        self.horizontalLayout_BtnGraph.setObjectName(u"horizontalLayout_BtnGraph")
        self.horizontalLayout_BtnGraph.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer_36 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_BtnGraph.addItem(self.horizontalSpacer_36)

        self.btnSaveGraph = QPushButton(self.tabWafermap_3)
        self.btnSaveGraph.setObjectName(u"btnSaveGraph")
        self.btnSaveGraph.setMinimumSize(QSize(30, 30))
        self.btnSaveGraph.setMaximumSize(QSize(30, 30))
        self.btnSaveGraph.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnSaveGraph.setIcon(icon9)

        self.horizontalLayout_BtnGraph.addWidget(self.btnSaveGraph)

        self.btnClearGraph = QPushButton(self.tabWafermap_3)
        self.btnClearGraph.setObjectName(u"btnClearGraph")
        self.btnClearGraph.setMinimumSize(QSize(30, 30))
        self.btnClearGraph.setMaximumSize(QSize(30, 30))
        self.btnClearGraph.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnClearGraph.setIcon(icon10)

        self.horizontalLayout_BtnGraph.addWidget(self.btnClearGraph)


        self.verticalLayout_45.addLayout(self.horizontalLayout_BtnGraph)

        self.tabGraph.addTab(self.tabWafermap_3, "")

        self.horizontalLayout_24.addWidget(self.tabGraph)

        self.verticalLayoutGraph = QVBoxLayout()
        self.verticalLayoutGraph.setObjectName(u"verticalLayoutGraph")

        self.horizontalLayout_24.addLayout(self.verticalLayoutGraph)


        self.verticalLayout_24.addLayout(self.horizontalLayout_24)

        self.stackedWidget.addWidget(self.measurements)
        self.instruments = QWidget()
        self.instruments.setObjectName(u"instruments")
        self.verticalLayout_26 = QVBoxLayout(self.instruments)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setSpacing(6)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.label_3 = QLabel(self.instruments)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 20))
        self.label_3.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_25.addWidget(self.label_3)

        self.verticalSpacer_8 = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_25.addItem(self.verticalSpacer_8)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_13, 0, 1, 1, 1)

        self.cmbInstruments_2 = QComboBox(self.instruments)
        self.cmbInstruments_2.addItem("")
        self.cmbInstruments_2.setObjectName(u"cmbInstruments_2")
        self.cmbInstruments_2.setMinimumSize(QSize(150, 0))
        self.cmbInstruments_2.setMaximumSize(QSize(150, 30))
        self.cmbInstruments_2.setFont(font)
        self.cmbInstruments_2.setAutoFillBackground(False)
        self.cmbInstruments_2.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbInstruments_2.setEditable(True)
        self.cmbInstruments_2.setIconSize(QSize(16, 16))
        self.cmbInstruments_2.setFrame(True)

        self.gridLayout_9.addWidget(self.cmbInstruments_2, 0, 0, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_9, 1, 1, 1, 1)


        self.verticalLayout_25.addLayout(self.gridLayout_9)


        self.verticalLayout_26.addLayout(self.verticalLayout_25)

        self.stackedWidget.addWidget(self.instruments)
        self.probers = QWidget()
        self.probers.setObjectName(u"probers")
        self.verticalLayout_28 = QVBoxLayout(self.probers)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.label_4 = QLabel(self.probers)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 20))
        self.label_4.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_27.addWidget(self.label_4)

        self.verticalSpacer_10 = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_27.addItem(self.verticalSpacer_10)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(-1, 0, 0, -1)
        self.cmbProbers_2 = QComboBox(self.probers)
        self.cmbProbers_2.addItem("")
        self.cmbProbers_2.setObjectName(u"cmbProbers_2")
        self.cmbProbers_2.setFont(font)
        self.cmbProbers_2.setAutoFillBackground(False)
        self.cmbProbers_2.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbProbers_2.setEditable(True)
        self.cmbProbers_2.setIconSize(QSize(16, 16))
        self.cmbProbers_2.setFrame(True)

        self.gridLayout_3.addWidget(self.cmbProbers_2, 0, 0, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_14, 0, 1, 1, 1)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_11, 1, 1, 1, 1)


        self.verticalLayout_27.addLayout(self.gridLayout_3)


        self.verticalLayout_28.addLayout(self.verticalLayout_27)

        self.stackedWidget.addWidget(self.probers)
        self.estepa = QWidget()
        self.estepa.setObjectName(u"estepa")
        self.verticalLayout_32 = QVBoxLayout(self.estepa)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.label_9 = QLabel(self.estepa)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 20))
        self.label_9.setMaximumSize(QSize(16777215, 20))
        self.label_9.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_32.addWidget(self.label_9)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_31 = QVBoxLayout()
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setSizeConstraint(QLayout.SetNoConstraint)
        self.optLoadFiles = QRadioButton(self.estepa)
        self.optLoadFiles.setObjectName(u"optLoadFiles")
        self.optLoadFiles.setMinimumSize(QSize(200, 0))
        self.optLoadFiles.setMaximumSize(QSize(200, 16777215))
        self.optLoadFiles.setChecked(True)

        self.gridLayout_15.addWidget(self.optLoadFiles, 0, 0, 1, 1)

        self.optLoadBBDD = QRadioButton(self.estepa)
        self.optLoadBBDD.setObjectName(u"optLoadBBDD")
        self.optLoadBBDD.setMinimumSize(QSize(200, 0))
        self.optLoadBBDD.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_15.addWidget(self.optLoadBBDD, 0, 1, 1, 1)


        self.horizontalLayout_18.addLayout(self.gridLayout_15)


        self.verticalLayout_31.addLayout(self.horizontalLayout_18)

        self.optionsESTEPA = QStackedWidget(self.estepa)
        self.optionsESTEPA.setObjectName(u"optionsESTEPA")
        self.optionsESTEPA.setMinimumSize(QSize(420, 310))
        self.optionsESTEPA.setMaximumSize(QSize(420, 310))
        self.files = QWidget()
        self.files.setObjectName(u"files")
        self.gridLayoutWidget_4 = QWidget(self.files)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(9, 20, 371, 231))
        self.gridLayout_13 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.btnLoadFiles = QPushButton(self.gridLayoutWidget_4)
        self.btnLoadFiles.setObjectName(u"btnLoadFiles")
        self.btnLoadFiles.setMinimumSize(QSize(100, 30))
        self.btnLoadFiles.setMaximumSize(QSize(300, 16777215))
        self.btnLoadFiles.setFont(font)
        self.btnLoadFiles.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnLoadFiles.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon11 = QIcon()
        icon11.addFile(u":/icons/images/icons/cil-loop-circular.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnLoadFiles.setIcon(icon11)

        self.gridLayout_13.addWidget(self.btnLoadFiles, 4, 0, 1, 1)

        self.labelVersion_13 = QLabel(self.gridLayoutWidget_4)
        self.labelVersion_13.setObjectName(u"labelVersion_13")
        self.labelVersion_13.setMaximumSize(QSize(200, 20))
        self.labelVersion_13.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_13.setLineWidth(1)
        self.labelVersion_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.labelVersion_13, 0, 0, 1, 1)

        self.btnOpenWafermapFile = QPushButton(self.gridLayoutWidget_4)
        self.btnOpenWafermapFile.setObjectName(u"btnOpenWafermapFile")
        self.btnOpenWafermapFile.setMinimumSize(QSize(40, 30))
        self.btnOpenWafermapFile.setMaximumSize(QSize(16777215, 30))
        self.btnOpenWafermapFile.setFont(font)
        self.btnOpenWafermapFile.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnOpenWafermapFile.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon12 = QIcon()
        icon12.addFile(u":/icons/images/icons/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnOpenWafermapFile.setIcon(icon12)

        self.gridLayout_13.addWidget(self.btnOpenWafermapFile, 3, 1, 1, 1)

        self.txtDataFile = QLineEdit(self.gridLayoutWidget_4)
        self.txtDataFile.setObjectName(u"txtDataFile")
        self.txtDataFile.setEnabled(False)
        self.txtDataFile.setMinimumSize(QSize(100, 30))
        self.txtDataFile.setMaximumSize(QSize(300, 30))
        self.txtDataFile.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_13.addWidget(self.txtDataFile, 1, 0, 1, 1)

        self.txtWafermapFile = QLineEdit(self.gridLayoutWidget_4)
        self.txtWafermapFile.setObjectName(u"txtWafermapFile")
        self.txtWafermapFile.setEnabled(False)
        self.txtWafermapFile.setMinimumSize(QSize(100, 30))
        self.txtWafermapFile.setMaximumSize(QSize(300, 30))
        self.txtWafermapFile.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_13.addWidget(self.txtWafermapFile, 3, 0, 1, 1)

        self.btnOpenDataFile = QPushButton(self.gridLayoutWidget_4)
        self.btnOpenDataFile.setObjectName(u"btnOpenDataFile")
        self.btnOpenDataFile.setMinimumSize(QSize(50, 30))
        self.btnOpenDataFile.setMaximumSize(QSize(50, 30))
        self.btnOpenDataFile.setFont(font)
        self.btnOpenDataFile.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnOpenDataFile.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnOpenDataFile.setIcon(icon12)

        self.gridLayout_13.addWidget(self.btnOpenDataFile, 1, 1, 1, 1)

        self.verticalSpacer_16 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_13.addItem(self.verticalSpacer_16, 5, 0, 1, 1)

        self.labelVersion_14 = QLabel(self.gridLayoutWidget_4)
        self.labelVersion_14.setObjectName(u"labelVersion_14")
        self.labelVersion_14.setMaximumSize(QSize(200, 20))
        self.labelVersion_14.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_14.setLineWidth(1)
        self.labelVersion_14.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.labelVersion_14, 2, 0, 1, 1)

        self.cmbParametersFile = CheckableComboBox(self.gridLayoutWidget_4)
        self.cmbParametersFile.addItem("")
        self.cmbParametersFile.setObjectName(u"cmbParametersFile")
        self.cmbParametersFile.setMinimumSize(QSize(100, 30))
        self.cmbParametersFile.setMaximumSize(QSize(300, 30))
        self.cmbParametersFile.setFont(font)
        self.cmbParametersFile.setAutoFillBackground(False)
        self.cmbParametersFile.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbParametersFile.setEditable(True)
        self.cmbParametersFile.setCurrentText(u"Select instrument")
        self.cmbParametersFile.setIconSize(QSize(16, 16))
        self.cmbParametersFile.setFrame(True)

        self.gridLayout_13.addWidget(self.cmbParametersFile, 7, 0, 1, 1)

        self.labelVersion_19 = QLabel(self.gridLayoutWidget_4)
        self.labelVersion_19.setObjectName(u"labelVersion_19")
        self.labelVersion_19.setMaximumSize(QSize(200, 20))
        self.labelVersion_19.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_19.setLineWidth(1)
        self.labelVersion_19.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.labelVersion_19, 6, 0, 1, 1)

        self.gridLayoutWidget_5 = QWidget(self.files)
        self.gridLayoutWidget_5.setObjectName(u"gridLayoutWidget_5")
        self.gridLayoutWidget_5.setGeometry(QRect(10, 260, 406, 41))
        self.gridLayout_14 = QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.btnNextParamFiles = QPushButton(self.gridLayoutWidget_5)
        self.btnNextParamFiles.setObjectName(u"btnNextParamFiles")
        self.btnNextParamFiles.setEnabled(True)
        self.btnNextParamFiles.setMinimumSize(QSize(30, 30))
        self.btnNextParamFiles.setMaximumSize(QSize(30, 30))
        self.btnNextParamFiles.setFont(font)
        self.btnNextParamFiles.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnNextParamFiles.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon13 = QIcon()
        icon13.addFile(u":/icons/images/icons/cil-chevron-right.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnNextParamFiles.setIcon(icon13)

        self.gridLayout_14.addWidget(self.btnNextParamFiles, 0, 3, 1, 1)

        self.txtParamSelectedFiles = QLineEdit(self.gridLayoutWidget_5)
        self.txtParamSelectedFiles.setObjectName(u"txtParamSelectedFiles")
        self.txtParamSelectedFiles.setEnabled(False)
        self.txtParamSelectedFiles.setMinimumSize(QSize(80, 30))
        self.txtParamSelectedFiles.setMaximumSize(QSize(80, 30))
        self.txtParamSelectedFiles.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_14.addWidget(self.txtParamSelectedFiles, 0, 2, 1, 1)

        self.btnCorrelationFiles = QPushButton(self.gridLayoutWidget_5)
        self.btnCorrelationFiles.setObjectName(u"btnCorrelationFiles")
        self.btnCorrelationFiles.setMinimumSize(QSize(120, 30))
        self.btnCorrelationFiles.setMaximumSize(QSize(120, 16777215))
        self.btnCorrelationFiles.setFont(font)
        self.btnCorrelationFiles.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnCorrelationFiles.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnCorrelationFiles.setIcon(icon11)

        self.gridLayout_14.addWidget(self.btnCorrelationFiles, 0, 4, 1, 1)

        self.btnAnalyzeFiles = QPushButton(self.gridLayoutWidget_5)
        self.btnAnalyzeFiles.setObjectName(u"btnAnalyzeFiles")
        self.btnAnalyzeFiles.setMinimumSize(QSize(120, 30))
        self.btnAnalyzeFiles.setMaximumSize(QSize(120, 16777215))
        self.btnAnalyzeFiles.setFont(font)
        self.btnAnalyzeFiles.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnAnalyzeFiles.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnAnalyzeFiles.setIcon(icon11)

        self.gridLayout_14.addWidget(self.btnAnalyzeFiles, 0, 0, 1, 1)

        self.btnPreviousParamFiles = QPushButton(self.gridLayoutWidget_5)
        self.btnPreviousParamFiles.setObjectName(u"btnPreviousParamFiles")
        self.btnPreviousParamFiles.setEnabled(True)
        self.btnPreviousParamFiles.setMinimumSize(QSize(30, 30))
        self.btnPreviousParamFiles.setMaximumSize(QSize(30, 30))
        self.btnPreviousParamFiles.setFont(font)
        self.btnPreviousParamFiles.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnPreviousParamFiles.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon14 = QIcon()
        icon14.addFile(u":/icons/images/icons/cil-chevron-left.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnPreviousParamFiles.setIcon(icon14)

        self.gridLayout_14.addWidget(self.btnPreviousParamFiles, 0, 1, 1, 1)

        self.optionsESTEPA.addWidget(self.files)
        self.bbdd = QWidget()
        self.bbdd.setObjectName(u"bbdd")
        self.gridLayoutWidget_9 = QWidget(self.bbdd)
        self.gridLayoutWidget_9.setObjectName(u"gridLayoutWidget_9")
        self.gridLayoutWidget_9.setGeometry(QRect(10, 0, 291, 261))
        self.gridLayout_16 = QGridLayout(self.gridLayoutWidget_9)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.labelVersion_17 = QLabel(self.gridLayoutWidget_9)
        self.labelVersion_17.setObjectName(u"labelVersion_17")
        self.labelVersion_17.setMaximumSize(QSize(200, 20))
        self.labelVersion_17.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_17.setLineWidth(1)
        self.labelVersion_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_16.addWidget(self.labelVersion_17, 2, 0, 1, 1)

        self.labelVersion_18 = QLabel(self.gridLayoutWidget_9)
        self.labelVersion_18.setObjectName(u"labelVersion_18")
        self.labelVersion_18.setMaximumSize(QSize(200, 20))
        self.labelVersion_18.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_18.setLineWidth(1)
        self.labelVersion_18.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_16.addWidget(self.labelVersion_18, 6, 0, 1, 1)

        self.cmbParametersBBDD = CheckableComboBox(self.gridLayoutWidget_9)
        self.cmbParametersBBDD.addItem("")
        self.cmbParametersBBDD.setObjectName(u"cmbParametersBBDD")
        self.cmbParametersBBDD.setMinimumSize(QSize(160, 30))
        self.cmbParametersBBDD.setMaximumSize(QSize(16777215, 30))
        self.cmbParametersBBDD.setFont(font)
        self.cmbParametersBBDD.setAutoFillBackground(False)
        self.cmbParametersBBDD.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbParametersBBDD.setEditable(True)
        self.cmbParametersBBDD.setIconSize(QSize(16, 16))
        self.cmbParametersBBDD.setFrame(True)

        self.gridLayout_16.addWidget(self.cmbParametersBBDD, 8, 0, 1, 1)

        self.verticalSpacer_12 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_16.addItem(self.verticalSpacer_12, 9, 0, 1, 1)

        self.cmbTechnology = QComboBox(self.gridLayoutWidget_9)
        self.cmbTechnology.addItem("")
        self.cmbTechnology.setObjectName(u"cmbTechnology")
        self.cmbTechnology.setMinimumSize(QSize(160, 30))
        self.cmbTechnology.setMaximumSize(QSize(16777215, 30))
        self.cmbTechnology.setFont(font)
        self.cmbTechnology.setAutoFillBackground(False)
        self.cmbTechnology.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbTechnology.setEditable(True)
        self.cmbTechnology.setIconSize(QSize(16, 16))
        self.cmbTechnology.setFrame(True)

        self.gridLayout_16.addWidget(self.cmbTechnology, 1, 0, 1, 1)

        self.labelVersion_16 = QLabel(self.gridLayoutWidget_9)
        self.labelVersion_16.setObjectName(u"labelVersion_16")
        self.labelVersion_16.setMaximumSize(QSize(200, 20))
        self.labelVersion_16.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_16.setLineWidth(1)
        self.labelVersion_16.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_16.addWidget(self.labelVersion_16, 4, 0, 1, 1)

        self.labelVersion_15 = QLabel(self.gridLayoutWidget_9)
        self.labelVersion_15.setObjectName(u"labelVersion_15")
        self.labelVersion_15.setMaximumSize(QSize(200, 20))
        self.labelVersion_15.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_15.setLineWidth(1)
        self.labelVersion_15.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_16.addWidget(self.labelVersion_15, 0, 0, 1, 1)

        self.cmbWafers = QComboBox(self.gridLayoutWidget_9)
        self.cmbWafers.addItem("")
        self.cmbWafers.setObjectName(u"cmbWafers")
        self.cmbWafers.setMinimumSize(QSize(160, 30))
        self.cmbWafers.setMaximumSize(QSize(16777215, 30))
        self.cmbWafers.setFont(font)
        self.cmbWafers.setAutoFillBackground(False)
        self.cmbWafers.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbWafers.setEditable(True)
        self.cmbWafers.setIconSize(QSize(16, 16))
        self.cmbWafers.setFrame(True)

        self.gridLayout_16.addWidget(self.cmbWafers, 5, 0, 1, 1)

        self.cmbRuns = QComboBox(self.gridLayoutWidget_9)
        self.cmbRuns.addItem("")
        self.cmbRuns.setObjectName(u"cmbRuns")
        self.cmbRuns.setMinimumSize(QSize(160, 30))
        self.cmbRuns.setMaximumSize(QSize(16777215, 30))
        self.cmbRuns.setFont(font)
        self.cmbRuns.setAutoFillBackground(False)
        self.cmbRuns.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbRuns.setEditable(True)
        self.cmbRuns.setIconSize(QSize(16, 16))
        self.cmbRuns.setFrame(True)

        self.gridLayout_16.addWidget(self.cmbRuns, 3, 0, 1, 1)

        self.gridLayoutWidget_6 = QWidget(self.bbdd)
        self.gridLayoutWidget_6.setObjectName(u"gridLayoutWidget_6")
        self.gridLayoutWidget_6.setGeometry(QRect(10, 260, 406, 41))
        self.gridLayout_21 = QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.txtParamSelectedBBDD = QLineEdit(self.gridLayoutWidget_6)
        self.txtParamSelectedBBDD.setObjectName(u"txtParamSelectedBBDD")
        self.txtParamSelectedBBDD.setEnabled(False)
        self.txtParamSelectedBBDD.setMinimumSize(QSize(80, 30))
        self.txtParamSelectedBBDD.setMaximumSize(QSize(80, 30))
        self.txtParamSelectedBBDD.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_21.addWidget(self.txtParamSelectedBBDD, 0, 2, 1, 1)

        self.btnNextParamBBDD = QPushButton(self.gridLayoutWidget_6)
        self.btnNextParamBBDD.setObjectName(u"btnNextParamBBDD")
        self.btnNextParamBBDD.setEnabled(True)
        self.btnNextParamBBDD.setMinimumSize(QSize(30, 30))
        self.btnNextParamBBDD.setMaximumSize(QSize(30, 30))
        self.btnNextParamBBDD.setFont(font)
        self.btnNextParamBBDD.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnNextParamBBDD.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnNextParamBBDD.setIcon(icon13)

        self.gridLayout_21.addWidget(self.btnNextParamBBDD, 0, 3, 1, 1)

        self.btnCorrelationBBDD = QPushButton(self.gridLayoutWidget_6)
        self.btnCorrelationBBDD.setObjectName(u"btnCorrelationBBDD")
        self.btnCorrelationBBDD.setMinimumSize(QSize(120, 30))
        self.btnCorrelationBBDD.setMaximumSize(QSize(120, 16777215))
        self.btnCorrelationBBDD.setFont(font)
        self.btnCorrelationBBDD.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnCorrelationBBDD.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnCorrelationBBDD.setIcon(icon11)

        self.gridLayout_21.addWidget(self.btnCorrelationBBDD, 0, 4, 1, 1)

        self.btnAnalyzeBBDD = QPushButton(self.gridLayoutWidget_6)
        self.btnAnalyzeBBDD.setObjectName(u"btnAnalyzeBBDD")
        self.btnAnalyzeBBDD.setMinimumSize(QSize(120, 30))
        self.btnAnalyzeBBDD.setMaximumSize(QSize(120, 16777215))
        self.btnAnalyzeBBDD.setFont(font)
        self.btnAnalyzeBBDD.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnAnalyzeBBDD.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnAnalyzeBBDD.setIcon(icon11)

        self.gridLayout_21.addWidget(self.btnAnalyzeBBDD, 0, 0, 1, 1)

        self.btnPreviousParamBBDD = QPushButton(self.gridLayoutWidget_6)
        self.btnPreviousParamBBDD.setObjectName(u"btnPreviousParamBBDD")
        self.btnPreviousParamBBDD.setEnabled(True)
        self.btnPreviousParamBBDD.setMinimumSize(QSize(30, 30))
        self.btnPreviousParamBBDD.setMaximumSize(QSize(30, 30))
        self.btnPreviousParamBBDD.setFont(font)
        self.btnPreviousParamBBDD.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnPreviousParamBBDD.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnPreviousParamBBDD.setIcon(icon14)

        self.gridLayout_21.addWidget(self.btnPreviousParamBBDD, 0, 1, 1, 1)

        self.optionsESTEPA.addWidget(self.bbdd)

        self.verticalLayout_31.addWidget(self.optionsESTEPA)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_30 = QVBoxLayout()
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.tabCalcs = QTabWidget(self.estepa)
        self.tabCalcs.setObjectName(u"tabCalcs")
        self.tabCalcs.setMinimumSize(QSize(420, 290))
        self.tabCalcs.setMaximumSize(QSize(420, 16777215))
        self.tabCalcs.setCursor(QCursor(Qt.ArrowCursor))
        self.tabCalcs.setAutoFillBackground(False)
        self.tabCalcs.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.tabCalcs.setTabPosition(QTabWidget.North)
        self.tabCalcs.setTabShape(QTabWidget.Rounded)
        self.tabCalcs.setElideMode(Qt.ElideNone)
        self.tabData = QWidget()
        self.tabData.setObjectName(u"tabData")
        self.verticalLayout_36 = QVBoxLayout(self.tabData)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.txtDataValues = QPlainTextEdit(self.tabData)
        self.txtDataValues.setObjectName(u"txtDataValues")
        self.txtDataValues.setMinimumSize(QSize(410, 0))
        self.txtDataValues.setMaximumSize(QSize(410, 16777215))
        self.txtDataValues.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.verticalLayout_36.addWidget(self.txtDataValues)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_19)

        self.btnSaveDataValues = QPushButton(self.tabData)
        self.btnSaveDataValues.setObjectName(u"btnSaveDataValues")
        self.btnSaveDataValues.setEnabled(True)
        self.btnSaveDataValues.setMinimumSize(QSize(30, 30))
        self.btnSaveDataValues.setMaximumSize(QSize(30, 16777215))
        self.btnSaveDataValues.setFont(font)
        self.btnSaveDataValues.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnSaveDataValues.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        self.btnSaveDataValues.setIcon(icon9)
        self.btnSaveDataValues.setFlat(False)

        self.horizontalLayout_10.addWidget(self.btnSaveDataValues)

        self.btnClearDataValues = QPushButton(self.tabData)
        self.btnClearDataValues.setObjectName(u"btnClearDataValues")
        self.btnClearDataValues.setEnabled(True)
        self.btnClearDataValues.setMinimumSize(QSize(30, 30))
        self.btnClearDataValues.setMaximumSize(QSize(30, 16777215))
        self.btnClearDataValues.setFont(font)
        self.btnClearDataValues.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnClearDataValues.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        self.btnClearDataValues.setIcon(icon10)
        self.btnClearDataValues.setFlat(False)

        self.horizontalLayout_10.addWidget(self.btnClearDataValues)


        self.verticalLayout_36.addLayout(self.horizontalLayout_10)

        self.tabCalcs.addTab(self.tabData, "")
        self.tabParameters = QWidget()
        self.tabParameters.setObjectName(u"tabParameters")
        self.verticalLayout_38 = QVBoxLayout(self.tabParameters)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.txtParametersResult = QPlainTextEdit(self.tabParameters)
        self.txtParametersResult.setObjectName(u"txtParametersResult")
        self.txtParametersResult.setMinimumSize(QSize(410, 290))
        self.txtParametersResult.setMaximumSize(QSize(410, 16777215))
        self.txtParametersResult.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.verticalLayout_38.addWidget(self.txtParametersResult)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_17)

        self.btnSaveParametersResult = QPushButton(self.tabParameters)
        self.btnSaveParametersResult.setObjectName(u"btnSaveParametersResult")
        self.btnSaveParametersResult.setEnabled(True)
        self.btnSaveParametersResult.setMinimumSize(QSize(30, 30))
        self.btnSaveParametersResult.setMaximumSize(QSize(30, 16777215))
        self.btnSaveParametersResult.setFont(font)
        self.btnSaveParametersResult.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnSaveParametersResult.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        self.btnSaveParametersResult.setIcon(icon9)
        self.btnSaveParametersResult.setFlat(False)

        self.horizontalLayout_20.addWidget(self.btnSaveParametersResult)

        self.btnClearParametersResult = QPushButton(self.tabParameters)
        self.btnClearParametersResult.setObjectName(u"btnClearParametersResult")
        self.btnClearParametersResult.setEnabled(True)
        self.btnClearParametersResult.setMinimumSize(QSize(30, 30))
        self.btnClearParametersResult.setMaximumSize(QSize(30, 16777215))
        self.btnClearParametersResult.setFont(font)
        self.btnClearParametersResult.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnClearParametersResult.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        self.btnClearParametersResult.setIcon(icon10)
        self.btnClearParametersResult.setFlat(False)

        self.horizontalLayout_20.addWidget(self.btnClearParametersResult)


        self.verticalLayout_38.addLayout(self.horizontalLayout_20)

        self.tabCalcs.addTab(self.tabParameters, "")

        self.horizontalLayout_7.addWidget(self.tabCalcs)


        self.verticalLayout_30.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_8.addLayout(self.verticalLayout_30)


        self.verticalLayout_31.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_13.addLayout(self.verticalLayout_31)

        self.horizontalSpacer_18 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_18)

        self.verticalLayout_33 = QVBoxLayout()
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.tabGraphs = QTabWidget(self.estepa)
        self.tabGraphs.setObjectName(u"tabGraphs")
        self.tabGraphs.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.tabWafermap = QWidget()
        self.tabWafermap.setObjectName(u"tabWafermap")
        self.verticalLayout_29 = QVBoxLayout(self.tabWafermap)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_15)

        self.horizontalLayout_btnWafermap = QHBoxLayout()
        self.horizontalLayout_btnWafermap.setObjectName(u"horizontalLayout_btnWafermap")

        self.horizontalLayout_21.addLayout(self.horizontalLayout_btnWafermap)

        self.horizontalSpacer_16 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_16)


        self.verticalLayout_29.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_wafermap = QHBoxLayout()
        self.horizontalLayout_wafermap.setObjectName(u"horizontalLayout_wafermap")
        self.horizontalLayout_wafermap.setSizeConstraint(QLayout.SetMaximumSize)

        self.verticalLayout_29.addLayout(self.horizontalLayout_wafermap)

        self.horizontalLayout_BtnWafermap = QHBoxLayout()
        self.horizontalLayout_BtnWafermap.setObjectName(u"horizontalLayout_BtnWafermap")
        self.horizontalLayout_BtnWafermap.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_BtnWafermap.addItem(self.horizontalSpacer_21)

        self.btnSaveWafermap = QPushButton(self.tabWafermap)
        self.btnSaveWafermap.setObjectName(u"btnSaveWafermap")
        self.btnSaveWafermap.setMinimumSize(QSize(30, 30))
        self.btnSaveWafermap.setMaximumSize(QSize(30, 30))
        self.btnSaveWafermap.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnSaveWafermap.setIcon(icon9)

        self.horizontalLayout_BtnWafermap.addWidget(self.btnSaveWafermap)

        self.btnClearWafermap = QPushButton(self.tabWafermap)
        self.btnClearWafermap.setObjectName(u"btnClearWafermap")
        self.btnClearWafermap.setMinimumSize(QSize(30, 30))
        self.btnClearWafermap.setMaximumSize(QSize(30, 30))
        self.btnClearWafermap.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnClearWafermap.setIcon(icon10)

        self.horizontalLayout_BtnWafermap.addWidget(self.btnClearWafermap)


        self.verticalLayout_29.addLayout(self.horizontalLayout_BtnWafermap)

        self.tabGraphs.addTab(self.tabWafermap, "")
        self.tabHistogram = QWidget()
        self.tabHistogram.setObjectName(u"tabHistogram")
        self.verticalLayout_34 = QVBoxLayout(self.tabHistogram)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_25.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_20 = QSpacerItem(180, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_20)

        self.horizontalLayout_btnHistogram = QHBoxLayout()
        self.horizontalLayout_btnHistogram.setObjectName(u"horizontalLayout_btnHistogram")

        self.horizontalLayout_25.addLayout(self.horizontalLayout_btnHistogram)

        self.horizontalSpacer_24 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_24)


        self.verticalLayout_34.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_histogram = QHBoxLayout()
        self.horizontalLayout_histogram.setObjectName(u"horizontalLayout_histogram")
        self.verticalLayout_histogram = QVBoxLayout()
        self.verticalLayout_histogram.setObjectName(u"verticalLayout_histogram")

        self.horizontalLayout_histogram.addLayout(self.verticalLayout_histogram)


        self.verticalLayout_34.addLayout(self.horizontalLayout_histogram)

        self.horizontalLayout_BtnHistogram = QHBoxLayout()
        self.horizontalLayout_BtnHistogram.setObjectName(u"horizontalLayout_BtnHistogram")
        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_BtnHistogram.addItem(self.horizontalSpacer_25)

        self.btnSaveHistogram = QPushButton(self.tabHistogram)
        self.btnSaveHistogram.setObjectName(u"btnSaveHistogram")
        self.btnSaveHistogram.setMinimumSize(QSize(30, 30))
        self.btnSaveHistogram.setMaximumSize(QSize(30, 30))
        self.btnSaveHistogram.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnSaveHistogram.setIcon(icon9)

        self.horizontalLayout_BtnHistogram.addWidget(self.btnSaveHistogram)

        self.btnClearHistogram = QPushButton(self.tabHistogram)
        self.btnClearHistogram.setObjectName(u"btnClearHistogram")
        self.btnClearHistogram.setMinimumSize(QSize(30, 30))
        self.btnClearHistogram.setMaximumSize(QSize(30, 30))
        self.btnClearHistogram.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnClearHistogram.setIcon(icon10)

        self.horizontalLayout_BtnHistogram.addWidget(self.btnClearHistogram)


        self.verticalLayout_34.addLayout(self.horizontalLayout_BtnHistogram)

        self.tabGraphs.addTab(self.tabHistogram, "")

        self.verticalLayout_33.addWidget(self.tabGraphs)


        self.horizontalLayout_13.addLayout(self.verticalLayout_33)


        self.verticalLayout_32.addLayout(self.horizontalLayout_13)

        self.stackedWidget.addWidget(self.estepa)
        self.widgets = QWidget()
        self.widgets.setObjectName(u"widgets")
        self.widgets.setStyleSheet(u"b")
        self.verticalLayout = QVBoxLayout(self.widgets)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.row_1 = QFrame(self.widgets)
        self.row_1.setObjectName(u"row_1")
        self.row_1.setFrameShape(QFrame.StyledPanel)
        self.row_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.row_1)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.frame_div_content_1 = QFrame(self.row_1)
        self.frame_div_content_1.setObjectName(u"frame_div_content_1")
        self.frame_div_content_1.setMinimumSize(QSize(0, 110))
        self.frame_div_content_1.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_1.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_div_content_1)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_title_wid_1.setObjectName(u"frame_title_wid_1")
        self.frame_title_wid_1.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_1.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_title_wid_1)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.labelBoxBlenderInstalation = QLabel(self.frame_title_wid_1)
        self.labelBoxBlenderInstalation.setObjectName(u"labelBoxBlenderInstalation")
        self.labelBoxBlenderInstalation.setFont(font)
        self.labelBoxBlenderInstalation.setStyleSheet(u"")

        self.verticalLayout_18.addWidget(self.labelBoxBlenderInstalation)


        self.verticalLayout_17.addWidget(self.frame_title_wid_1)

        self.frame_content_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_content_wid_1.setObjectName(u"frame_content_wid_1")
        self.frame_content_wid_1.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_content_wid_1)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.lineEdit = QLineEdit(self.frame_content_wid_1)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.frame_content_wid_1)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(150, 30))
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.pushButton.setIcon(icon12)

        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)

        self.labelVersion_3 = QLabel(self.frame_content_wid_1)
        self.labelVersion_3.setObjectName(u"labelVersion_3")
        self.labelVersion_3.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_3.setLineWidth(1)
        self.labelVersion_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelVersion_3, 1, 0, 1, 2)


        self.horizontalLayout_9.addLayout(self.gridLayout)


        self.verticalLayout_17.addWidget(self.frame_content_wid_1)


        self.verticalLayout_16.addWidget(self.frame_div_content_1)


        self.verticalLayout.addWidget(self.row_1)

        self.row_2 = QFrame(self.widgets)
        self.row_2.setObjectName(u"row_2")
        self.row_2.setMinimumSize(QSize(0, 150))
        self.row_2.setFrameShape(QFrame.StyledPanel)
        self.row_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.row_2)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.checkBox = QCheckBox(self.row_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setAutoFillBackground(False)
        self.checkBox.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)

        self.radioButton = QRadioButton(self.row_2)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.radioButton, 0, 1, 1, 1)

        self.verticalSlider = QSlider(self.row_2)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setStyleSheet(u"")
        self.verticalSlider.setOrientation(Qt.Vertical)

        self.gridLayout_2.addWidget(self.verticalSlider, 0, 2, 3, 1)

        self.verticalScrollBar = QScrollBar(self.row_2)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setStyleSheet(u" QScrollBar:vertical { background: rgb(52, 59, 72); }\n"
" QScrollBar:horizontal { background: rgb(52, 59, 72); }")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.gridLayout_2.addWidget(self.verticalScrollBar, 0, 4, 3, 1)

        self.scrollArea = QScrollArea(self.row_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u" QScrollBar:vertical {\n"
"    background: rgb(52, 59, 72);\n"
" }\n"
" QScrollBar:horizontal {\n"
"    background: rgb(52, 59, 72);\n"
" }")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 365, 218))
        self.scrollAreaWidgetContents.setStyleSheet(u" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }")
        self.horizontalLayout_11 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.plainTextEdit = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMinimumSize(QSize(200, 200))
        self.plainTextEdit.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.horizontalLayout_11.addWidget(self.plainTextEdit)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 5, 3, 1)

        self.comboBox = QComboBox(self.row_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setFont(font)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.comboBox.setIconSize(QSize(16, 16))
        self.comboBox.setFrame(True)

        self.gridLayout_2.addWidget(self.comboBox, 1, 0, 1, 2)

        self.horizontalScrollBar = QScrollBar(self.row_2)
        self.horizontalScrollBar.setObjectName(u"horizontalScrollBar")
        sizePolicy.setHeightForWidth(self.horizontalScrollBar.sizePolicy().hasHeightForWidth())
        self.horizontalScrollBar.setSizePolicy(sizePolicy)
        self.horizontalScrollBar.setStyleSheet(u" QScrollBar:vertical { background: rgb(52, 59, 72); }\n"
" QScrollBar:horizontal { background: rgb(52, 59, 72); }")
        self.horizontalScrollBar.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.horizontalScrollBar, 1, 3, 1, 1)

        self.commandLinkButton = QCommandLinkButton(self.row_2)
        self.commandLinkButton.setObjectName(u"commandLinkButton")
        self.commandLinkButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.commandLinkButton.setStyleSheet(u"")
        icon15 = QIcon()
        icon15.addFile(u":/icons/images/icons/cil-link.png", QSize(), QIcon.Normal, QIcon.Off)
        self.commandLinkButton.setIcon(icon15)

        self.gridLayout_2.addWidget(self.commandLinkButton, 1, 6, 1, 1)

        self.horizontalSlider = QSlider(self.row_2)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setStyleSheet(u"")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.horizontalSlider, 2, 0, 1, 2)


        self.verticalLayout_19.addLayout(self.gridLayout_2)


        self.verticalLayout.addWidget(self.row_2)

        self.row_3 = QFrame(self.widgets)
        self.row_3.setObjectName(u"row_3")
        self.row_3.setMinimumSize(QSize(0, 150))
        self.row_3.setFrameShape(QFrame.StyledPanel)
        self.row_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.row_3)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.row_3)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.tableWidget.rowCount() < 16):
            self.tableWidget.setRowCount(16)
        font4 = QFont()
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font4);
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(14, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(15, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget.setItem(0, 3, __qtablewidgetitem23)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy3)
        palette = QPalette()
        brush = QBrush(QColor(221, 221, 221, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        brush4 = QBrush(QColor(0, 0, 0, 255))
        brush4.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
#endif
        self.tableWidget.setPalette(palette)
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setStretchLastSection(True)

        self.horizontalLayout_12.addWidget(self.tableWidget)


        self.verticalLayout.addWidget(self.row_3)

        self.stackedWidget.addWidget(self.widgets)
        self.consult_estepa = QWidget()
        self.consult_estepa.setObjectName(u"consult_estepa")
        self.verticalLayout_39 = QVBoxLayout(self.consult_estepa)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.label_12 = QLabel(self.consult_estepa)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(0, 20))
        self.label_12.setMaximumSize(QSize(16777215, 20))
        self.label_12.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")
        self.label_12.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_39.addWidget(self.label_12)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout_48 = QVBoxLayout()
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.verticalLayout_48.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_48 = QHBoxLayout()
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.horizontalLayout_48.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_48.setContentsMargins(-1, 5, -1, -1)
        self.optRunsConsult = QRadioButton(self.consult_estepa)
        self.optRunsConsult.setObjectName(u"optRunsConsult")
        self.optRunsConsult.setMinimumSize(QSize(100, 40))
        self.optRunsConsult.setMaximumSize(QSize(100, 40))
        self.optRunsConsult.setChecked(True)

        self.horizontalLayout_48.addWidget(self.optRunsConsult)

        self.optWafersConsult = QRadioButton(self.consult_estepa)
        self.optWafersConsult.setObjectName(u"optWafersConsult")
        self.optWafersConsult.setMinimumSize(QSize(100, 40))
        self.optWafersConsult.setMaximumSize(QSize(100, 40))

        self.horizontalLayout_48.addWidget(self.optWafersConsult)


        self.verticalLayout_48.addLayout(self.horizontalLayout_48)

        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.horizontalLayout_49.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_49.setContentsMargins(-1, -1, -1, 10)
        self.chkHistorical = QCheckBox(self.consult_estepa)
        self.chkHistorical.setObjectName(u"chkHistorical")
        self.chkHistorical.setMinimumSize(QSize(80, 40))
        self.chkHistorical.setMaximumSize(QSize(80, 40))
        self.chkHistorical.setChecked(False)
        self.chkHistorical.setAutoRepeat(False)

        self.horizontalLayout_49.addWidget(self.chkHistorical)

        self.optionsHistorical = QStackedWidget(self.consult_estepa)
        self.optionsHistorical.setObjectName(u"optionsHistorical")
        self.optionsHistorical.setMinimumSize(QSize(300, 40))
        self.optionsHistorical.setMaximumSize(QSize(300, 40))
        self.YesHistorical = QWidget()
        self.YesHistorical.setObjectName(u"YesHistorical")
        self.gridLayoutWidget_3 = QWidget(self.YesHistorical)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 0, 271, 42))
        self.gridLayout_5 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.optYield = QRadioButton(self.gridLayoutWidget_3)
        self.optYield.setObjectName(u"optYield")
        self.optYield.setMaximumSize(QSize(70, 16777215))

        self.gridLayout_5.addWidget(self.optYield, 0, 1, 1, 1)

        self.optValues = QRadioButton(self.gridLayoutWidget_3)
        self.optValues.setObjectName(u"optValues")
        self.optValues.setMinimumSize(QSize(70, 40))
        self.optValues.setMaximumSize(QSize(70, 40))
        self.optValues.setChecked(True)

        self.gridLayout_5.addWidget(self.optValues, 0, 0, 1, 1)

        self.optionsHistorical.addWidget(self.YesHistorical)
        self.NoHistorical = QWidget()
        self.NoHistorical.setObjectName(u"NoHistorical")
        self.optionsHistorical.addWidget(self.NoHistorical)

        self.horizontalLayout_49.addWidget(self.optionsHistorical)


        self.verticalLayout_48.addLayout(self.horizontalLayout_49)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.verticalLayout_44 = QVBoxLayout()
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.labelVersion_40 = QLabel(self.consult_estepa)
        self.labelVersion_40.setObjectName(u"labelVersion_40")
        self.labelVersion_40.setMaximumSize(QSize(200, 20))
        self.labelVersion_40.setStyleSheet(u"")
        self.labelVersion_40.setLineWidth(1)
        self.labelVersion_40.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_44.addWidget(self.labelVersion_40)

        self.cmbTechnologyConsult = QComboBox(self.consult_estepa)
        self.cmbTechnologyConsult.setObjectName(u"cmbTechnologyConsult")
        self.cmbTechnologyConsult.setMinimumSize(QSize(120, 30))
        self.cmbTechnologyConsult.setMaximumSize(QSize(120, 30))
        self.cmbTechnologyConsult.setCursor(QCursor(Qt.PointingHandCursor))
        self.cmbTechnologyConsult.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbTechnologyConsult.setEditable(False)

        self.verticalLayout_44.addWidget(self.cmbTechnologyConsult)

        self.verticalSpacer_20 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_44.addItem(self.verticalSpacer_20)

        self.labelVersion_41 = QLabel(self.consult_estepa)
        self.labelVersion_41.setObjectName(u"labelVersion_41")
        self.labelVersion_41.setMaximumSize(QSize(200, 20))
        self.labelVersion_41.setStyleSheet(u"")
        self.labelVersion_41.setLineWidth(1)
        self.labelVersion_41.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_44.addWidget(self.labelVersion_41)

        self.cmbRunsConsult = QComboBox(self.consult_estepa)
        self.cmbRunsConsult.setObjectName(u"cmbRunsConsult")
        self.cmbRunsConsult.setMinimumSize(QSize(120, 30))
        self.cmbRunsConsult.setMaximumSize(QSize(120, 30))
        self.cmbRunsConsult.setCursor(QCursor(Qt.PointingHandCursor))
        self.cmbRunsConsult.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbRunsConsult.setEditable(False)

        self.verticalLayout_44.addWidget(self.cmbRunsConsult)

        self.verticalSpacer_21 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_44.addItem(self.verticalSpacer_21)

        self.labelVersion_39 = QLabel(self.consult_estepa)
        self.labelVersion_39.setObjectName(u"labelVersion_39")
        self.labelVersion_39.setMaximumSize(QSize(200, 20))
        self.labelVersion_39.setStyleSheet(u"")
        self.labelVersion_39.setLineWidth(1)
        self.labelVersion_39.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_44.addWidget(self.labelVersion_39)

        self.cmbWafersConsult = CheckableComboBox(self.consult_estepa)
        self.cmbWafersConsult.addItem("")
        self.cmbWafersConsult.setObjectName(u"cmbWafersConsult")
        self.cmbWafersConsult.setMinimumSize(QSize(120, 30))
        self.cmbWafersConsult.setMaximumSize(QSize(120, 30))
        self.cmbWafersConsult.setFont(font)
        self.cmbWafersConsult.setAutoFillBackground(False)
        self.cmbWafersConsult.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbWafersConsult.setEditable(True)
        self.cmbWafersConsult.setCurrentText(u"Select instrument")
        self.cmbWafersConsult.setIconSize(QSize(16, 16))
        self.cmbWafersConsult.setFrame(True)

        self.verticalLayout_44.addWidget(self.cmbWafersConsult)

        self.verticalSpacer_6 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_44.addItem(self.verticalSpacer_6)


        self.horizontalLayout_30.addLayout(self.verticalLayout_44)

        self.verticalLayout_47 = QVBoxLayout()
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")
        self.verticalLayout_47.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_47.setContentsMargins(-1, -1, 0, -1)
        self.verticalSpacer_24 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_47.addItem(self.verticalSpacer_24)

        self.btnAddWafers = QPushButton(self.consult_estepa)
        self.btnAddWafers.setObjectName(u"btnAddWafers")
        self.btnAddWafers.setMinimumSize(QSize(60, 30))
        self.btnAddWafers.setMaximumSize(QSize(60, 16777215))
        self.btnAddWafers.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnAddWafers.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnAddWafers.setIcon(icon13)

        self.verticalLayout_47.addWidget(self.btnAddWafers)

        self.verticalSpacer_23 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_47.addItem(self.verticalSpacer_23)


        self.horizontalLayout_30.addLayout(self.verticalLayout_47)

        self.verticalLayout_46 = QVBoxLayout()
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")
        self.verticalLayout_46.setSizeConstraint(QLayout.SetMinimumSize)
        self.labelVersion_38 = QLabel(self.consult_estepa)
        self.labelVersion_38.setObjectName(u"labelVersion_38")
        self.labelVersion_38.setMinimumSize(QSize(100, 0))
        self.labelVersion_38.setMaximumSize(QSize(100, 20))
        self.labelVersion_38.setStyleSheet(u"")
        self.labelVersion_38.setLineWidth(1)
        self.labelVersion_38.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_46.addWidget(self.labelVersion_38)

        self.lbWafers = QListWidget(self.consult_estepa)
        QListWidgetItem(self.lbWafers)
        QListWidgetItem(self.lbWafers)
        self.lbWafers.setObjectName(u"lbWafers")
        self.lbWafers.setMinimumSize(QSize(140, 180))
        self.lbWafers.setMaximumSize(QSize(140, 180))
        self.lbWafers.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.lbWafers.setFrameShape(QFrame.StyledPanel)
        self.lbWafers.setFrameShadow(QFrame.Sunken)
        self.lbWafers.setSelectionMode(QAbstractItemView.NoSelection)
        self.lbWafers.setMovement(QListView.Snap)
        self.lbWafers.setFlow(QListView.TopToBottom)
        self.lbWafers.setLayoutMode(QListView.SinglePass)
        self.lbWafers.setViewMode(QListView.ListMode)

        self.verticalLayout_46.addWidget(self.lbWafers)

        self.verticalSpacer_22 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_46.addItem(self.verticalSpacer_22)

        self.labelVersion_37 = QLabel(self.consult_estepa)
        self.labelVersion_37.setObjectName(u"labelVersion_37")
        self.labelVersion_37.setMaximumSize(QSize(200, 20))
        self.labelVersion_37.setStyleSheet(u"")
        self.labelVersion_37.setLineWidth(1)
        self.labelVersion_37.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_46.addWidget(self.labelVersion_37)

        self.cmbParametersConsult = CheckableComboBox(self.consult_estepa)
        self.cmbParametersConsult.addItem("")
        self.cmbParametersConsult.setObjectName(u"cmbParametersConsult")
        self.cmbParametersConsult.setMinimumSize(QSize(140, 30))
        self.cmbParametersConsult.setMaximumSize(QSize(140, 30))
        self.cmbParametersConsult.setFont(font)
        self.cmbParametersConsult.setAutoFillBackground(False)
        self.cmbParametersConsult.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbParametersConsult.setEditable(True)
        self.cmbParametersConsult.setCurrentText(u"Select instrument")
        self.cmbParametersConsult.setIconSize(QSize(16, 16))
        self.cmbParametersConsult.setFrame(True)

        self.verticalLayout_46.addWidget(self.cmbParametersConsult)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_46.addItem(self.verticalSpacer_18)


        self.horizontalLayout_30.addLayout(self.verticalLayout_46)


        self.verticalLayout_48.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.txtParamSelectedConsult = QLineEdit(self.consult_estepa)
        self.txtParamSelectedConsult.setObjectName(u"txtParamSelectedConsult")
        self.txtParamSelectedConsult.setEnabled(False)
        self.txtParamSelectedConsult.setMinimumSize(QSize(80, 30))
        self.txtParamSelectedConsult.setMaximumSize(QSize(80, 30))
        self.txtParamSelectedConsult.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_8.addWidget(self.txtParamSelectedConsult, 0, 2, 1, 1)

        self.btnPreviousParamConsult = QPushButton(self.consult_estepa)
        self.btnPreviousParamConsult.setObjectName(u"btnPreviousParamConsult")
        self.btnPreviousParamConsult.setEnabled(True)
        self.btnPreviousParamConsult.setMinimumSize(QSize(30, 30))
        self.btnPreviousParamConsult.setMaximumSize(QSize(30, 30))
        self.btnPreviousParamConsult.setFont(font)
        self.btnPreviousParamConsult.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnPreviousParamConsult.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnPreviousParamConsult.setIcon(icon14)

        self.gridLayout_8.addWidget(self.btnPreviousParamConsult, 0, 1, 1, 1)

        self.btnNextParamConsult = QPushButton(self.consult_estepa)
        self.btnNextParamConsult.setObjectName(u"btnNextParamConsult")
        self.btnNextParamConsult.setEnabled(True)
        self.btnNextParamConsult.setMinimumSize(QSize(30, 30))
        self.btnNextParamConsult.setMaximumSize(QSize(30, 30))
        self.btnNextParamConsult.setFont(font)
        self.btnNextParamConsult.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnNextParamConsult.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnNextParamConsult.setIcon(icon13)

        self.gridLayout_8.addWidget(self.btnNextParamConsult, 0, 3, 1, 1)

        self.btnConsult = QPushButton(self.consult_estepa)
        self.btnConsult.setObjectName(u"btnConsult")
        self.btnConsult.setMinimumSize(QSize(120, 30))
        self.btnConsult.setMaximumSize(QSize(120, 16777215))
        self.btnConsult.setFont(font)
        self.btnConsult.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnConsult.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnConsult.setIcon(icon11)

        self.gridLayout_8.addWidget(self.btnConsult, 0, 0, 1, 1)

        self.lblLoadingConsult = QLabel(self.consult_estepa)
        self.lblLoadingConsult.setObjectName(u"lblLoadingConsult")
        self.lblLoadingConsult.setEnabled(True)
        self.lblLoadingConsult.setMaximumSize(QSize(100, 30))
        self.lblLoadingConsult.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lblLoadingConsult, 0, 4, 1, 1)


        self.horizontalLayout_36.addLayout(self.gridLayout_8)


        self.verticalLayout_48.addLayout(self.horizontalLayout_36)

        self.verticalSpacer_19 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_48.addItem(self.verticalSpacer_19)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setSizeConstraint(QLayout.SetMinimumSize)
        self.tabCalcs_2 = QTabWidget(self.consult_estepa)
        self.tabCalcs_2.setObjectName(u"tabCalcs_2")
        self.tabCalcs_2.setMinimumSize(QSize(400, 0))
        self.tabCalcs_2.setMaximumSize(QSize(400, 16777215))
        self.tabCalcs_2.setCursor(QCursor(Qt.ArrowCursor))
        self.tabCalcs_2.setAutoFillBackground(False)
        self.tabCalcs_2.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.tabCalcs_2.setTabPosition(QTabWidget.North)
        self.tabCalcs_2.setTabShape(QTabWidget.Rounded)
        self.tabCalcs_2.setElideMode(Qt.ElideNone)
        self.tabData_2 = QWidget()
        self.tabData_2.setObjectName(u"tabData_2")
        self.verticalLayout_52 = QVBoxLayout(self.tabData_2)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.txtDataValuesConsult = QPlainTextEdit(self.tabData_2)
        self.txtDataValuesConsult.setObjectName(u"txtDataValuesConsult")
        self.txtDataValuesConsult.setMinimumSize(QSize(390, 0))
        self.txtDataValuesConsult.setMaximumSize(QSize(390, 16777215))
        self.txtDataValuesConsult.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.verticalLayout_52.addWidget(self.txtDataValuesConsult)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalSpacer_29 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_29)

        self.btnUploadHistorical = QPushButton(self.tabData_2)
        self.btnUploadHistorical.setObjectName(u"btnUploadHistorical")
        self.btnUploadHistorical.setMinimumSize(QSize(30, 31))
        self.btnUploadHistorical.setMaximumSize(QSize(30, 30))
        self.btnUploadHistorical.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        icon16 = QIcon()
        icon16.addFile(u":/icons/images/icons/cil-cloud-upload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnUploadHistorical.setIcon(icon16)

        self.horizontalLayout_35.addWidget(self.btnUploadHistorical)

        self.btnSaveHistorical = QPushButton(self.tabData_2)
        self.btnSaveHistorical.setObjectName(u"btnSaveHistorical")
        self.btnSaveHistorical.setEnabled(True)
        self.btnSaveHistorical.setMinimumSize(QSize(30, 30))
        self.btnSaveHistorical.setMaximumSize(QSize(30, 16777215))
        self.btnSaveHistorical.setFont(font)
        self.btnSaveHistorical.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnSaveHistorical.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        self.btnSaveHistorical.setIcon(icon9)
        self.btnSaveHistorical.setFlat(False)

        self.horizontalLayout_35.addWidget(self.btnSaveHistorical)

        self.btnClearDataValuesConsult = QPushButton(self.tabData_2)
        self.btnClearDataValuesConsult.setObjectName(u"btnClearDataValuesConsult")
        self.btnClearDataValuesConsult.setEnabled(True)
        self.btnClearDataValuesConsult.setMinimumSize(QSize(30, 30))
        self.btnClearDataValuesConsult.setMaximumSize(QSize(30, 16777215))
        self.btnClearDataValuesConsult.setFont(font)
        self.btnClearDataValuesConsult.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnClearDataValuesConsult.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        self.btnClearDataValuesConsult.setIcon(icon10)
        self.btnClearDataValuesConsult.setFlat(False)

        self.horizontalLayout_35.addWidget(self.btnClearDataValuesConsult)


        self.verticalLayout_52.addLayout(self.horizontalLayout_35)

        self.tabCalcs_2.addTab(self.tabData_2, "")

        self.horizontalLayout_34.addWidget(self.tabCalcs_2)


        self.verticalLayout_48.addLayout(self.horizontalLayout_34)


        self.horizontalLayout_31.addLayout(self.verticalLayout_48)

        self.horizontalSpacer_30 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_30)

        self.verticalLayout_49 = QVBoxLayout()
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.tabDiagrams = QTabWidget(self.consult_estepa)
        self.tabDiagrams.setObjectName(u"tabDiagrams")
        self.tabDiagrams.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.tabDiagrams_2 = QWidget()
        self.tabDiagrams_2.setObjectName(u"tabDiagrams_2")
        self.verticalLayout_55 = QVBoxLayout(self.tabDiagrams_2)
        self.verticalLayout_55.setObjectName(u"verticalLayout_55")
        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_37.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_39 = QSpacerItem(180, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_39)

        self.horizontalLayout_btnDiagrams = QHBoxLayout()
        self.horizontalLayout_btnDiagrams.setObjectName(u"horizontalLayout_btnDiagrams")

        self.horizontalLayout_37.addLayout(self.horizontalLayout_btnDiagrams)

        self.horizontalSpacer_40 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_40)


        self.verticalLayout_55.addLayout(self.horizontalLayout_37)

        self.horizontalLayout_diagram_3 = QHBoxLayout()
        self.horizontalLayout_diagram_3.setObjectName(u"horizontalLayout_diagram_3")
        self.verticalLayout_diagrams = QVBoxLayout()
        self.verticalLayout_diagrams.setObjectName(u"verticalLayout_diagrams")

        self.horizontalLayout_diagram_3.addLayout(self.verticalLayout_diagrams)


        self.verticalLayout_55.addLayout(self.horizontalLayout_diagram_3)

        self.horizontalLayout_BtnHistogram_2 = QHBoxLayout()
        self.horizontalLayout_BtnHistogram_2.setObjectName(u"horizontalLayout_BtnHistogram_2")
        self.horizontalSpacer_41 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_BtnHistogram_2.addItem(self.horizontalSpacer_41)

        self.btnSaveDiagram = QPushButton(self.tabDiagrams_2)
        self.btnSaveDiagram.setObjectName(u"btnSaveDiagram")
        self.btnSaveDiagram.setMinimumSize(QSize(30, 30))
        self.btnSaveDiagram.setMaximumSize(QSize(30, 30))
        self.btnSaveDiagram.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnSaveDiagram.setIcon(icon9)

        self.horizontalLayout_BtnHistogram_2.addWidget(self.btnSaveDiagram)

        self.btnClearDiagram = QPushButton(self.tabDiagrams_2)
        self.btnClearDiagram.setObjectName(u"btnClearDiagram")
        self.btnClearDiagram.setMinimumSize(QSize(30, 30))
        self.btnClearDiagram.setMaximumSize(QSize(30, 30))
        self.btnClearDiagram.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnClearDiagram.setIcon(icon10)

        self.horizontalLayout_BtnHistogram_2.addWidget(self.btnClearDiagram)


        self.verticalLayout_55.addLayout(self.horizontalLayout_BtnHistogram_2)

        self.tabDiagrams.addTab(self.tabDiagrams_2, "")

        self.verticalLayout_49.addWidget(self.tabDiagrams)


        self.horizontalLayout_31.addLayout(self.verticalLayout_49)


        self.verticalLayout_39.addLayout(self.horizontalLayout_31)

        self.stackedWidget.addWidget(self.consult_estepa)
        self.inbase = QWidget()
        self.inbase.setObjectName(u"inbase")
        self.verticalLayout_37 = QVBoxLayout(self.inbase)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.label_10 = QLabel(self.inbase)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 20))
        self.label_10.setMaximumSize(QSize(16777215, 20))
        self.label_10.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")
        self.label_10.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_37.addWidget(self.label_10)

        self.verticalLayout_35 = QVBoxLayout()
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.gridLayout_20 = QGridLayout()
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.labelVersion_27 = QLabel(self.inbase)
        self.labelVersion_27.setObjectName(u"labelVersion_27")
        self.labelVersion_27.setMaximumSize(QSize(200, 20))
        self.labelVersion_27.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_27.setLineWidth(1)
        self.labelVersion_27.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.labelVersion_27, 2, 0, 1, 1)

        self.verticalSpacer_13 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_20.addItem(self.verticalSpacer_13, 4, 0, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_20.addItem(self.verticalSpacer_14, 17, 0, 1, 1)

        self.btnUploadFiles = QPushButton(self.inbase)
        self.btnUploadFiles.setObjectName(u"btnUploadFiles")
        self.btnUploadFiles.setMinimumSize(QSize(150, 30))
        self.btnUploadFiles.setMaximumSize(QSize(300, 16777215))
        self.btnUploadFiles.setFont(font)
        self.btnUploadFiles.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnUploadFiles.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnUploadFiles.setIcon(icon16)

        self.gridLayout_20.addWidget(self.btnUploadFiles, 18, 0, 1, 1)

        self.txtRunUpload = QLineEdit(self.inbase)
        self.txtRunUpload.setObjectName(u"txtRunUpload")
        self.txtRunUpload.setEnabled(True)
        self.txtRunUpload.setMinimumSize(QSize(100, 30))
        self.txtRunUpload.setMaximumSize(QSize(100, 30))
        self.txtRunUpload.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_20.addWidget(self.txtRunUpload, 6, 0, 1, 1)

        self.txtLocalizationUpload = QLineEdit(self.inbase)
        self.txtLocalizationUpload.setObjectName(u"txtLocalizationUpload")
        self.txtLocalizationUpload.setEnabled(True)
        self.txtLocalizationUpload.setMinimumSize(QSize(300, 30))
        self.txtLocalizationUpload.setMaximumSize(QSize(300, 30))
        self.txtLocalizationUpload.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_20.addWidget(self.txtLocalizationUpload, 14, 0, 1, 1)

        self.txtCommentUpload = QLineEdit(self.inbase)
        self.txtCommentUpload.setObjectName(u"txtCommentUpload")
        self.txtCommentUpload.setEnabled(True)
        self.txtCommentUpload.setMinimumSize(QSize(300, 30))
        self.txtCommentUpload.setMaximumSize(QSize(300, 30))
        self.txtCommentUpload.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_20.addWidget(self.txtCommentUpload, 14, 1, 1, 1)

        self.btnOpenWafermapFileInbase = QPushButton(self.inbase)
        self.btnOpenWafermapFileInbase.setObjectName(u"btnOpenWafermapFileInbase")
        self.btnOpenWafermapFileInbase.setMinimumSize(QSize(50, 30))
        self.btnOpenWafermapFileInbase.setMaximumSize(QSize(50, 30))
        self.btnOpenWafermapFileInbase.setFont(font)
        self.btnOpenWafermapFileInbase.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnOpenWafermapFileInbase.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnOpenWafermapFileInbase.setIcon(icon12)

        self.gridLayout_20.addWidget(self.btnOpenWafermapFileInbase, 3, 1, 1, 1)

        self.labelVersion_29 = QLabel(self.inbase)
        self.labelVersion_29.setObjectName(u"labelVersion_29")
        self.labelVersion_29.setMaximumSize(QSize(200, 20))
        self.labelVersion_29.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_29.setLineWidth(1)
        self.labelVersion_29.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.labelVersion_29, 10, 1, 1, 1)

        self.cmbMaskUpload = QComboBox(self.inbase)
        self.cmbMaskUpload.addItem("")
        self.cmbMaskUpload.setObjectName(u"cmbMaskUpload")
        self.cmbMaskUpload.setMinimumSize(QSize(160, 30))
        self.cmbMaskUpload.setMaximumSize(QSize(16777215, 30))
        self.cmbMaskUpload.setFont(font)
        self.cmbMaskUpload.setAutoFillBackground(False)
        self.cmbMaskUpload.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbMaskUpload.setEditable(True)
        self.cmbMaskUpload.setIconSize(QSize(16, 16))
        self.cmbMaskUpload.setFrame(True)

        self.gridLayout_20.addWidget(self.cmbMaskUpload, 11, 1, 1, 1)

        self.btnOpenDataFileInbase = QPushButton(self.inbase)
        self.btnOpenDataFileInbase.setObjectName(u"btnOpenDataFileInbase")
        self.btnOpenDataFileInbase.setMinimumSize(QSize(50, 30))
        self.btnOpenDataFileInbase.setMaximumSize(QSize(50, 30))
        self.btnOpenDataFileInbase.setFont(font)
        self.btnOpenDataFileInbase.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnOpenDataFileInbase.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.btnOpenDataFileInbase.setIcon(icon12)

        self.gridLayout_20.addWidget(self.btnOpenDataFileInbase, 1, 1, 1, 1)

        self.txtDataFileInbase = QLineEdit(self.inbase)
        self.txtDataFileInbase.setObjectName(u"txtDataFileInbase")
        self.txtDataFileInbase.setEnabled(True)
        self.txtDataFileInbase.setMinimumSize(QSize(300, 30))
        self.txtDataFileInbase.setMaximumSize(QSize(300, 30))
        self.txtDataFileInbase.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_20.addWidget(self.txtDataFileInbase, 1, 0, 1, 1)

        self.labelVersion_32 = QLabel(self.inbase)
        self.labelVersion_32.setObjectName(u"labelVersion_32")
        self.labelVersion_32.setMaximumSize(QSize(200, 20))
        self.labelVersion_32.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_32.setLineWidth(1)
        self.labelVersion_32.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.labelVersion_32, 5, 0, 1, 1)

        self.labelVersion_31 = QLabel(self.inbase)
        self.labelVersion_31.setObjectName(u"labelVersion_31")
        self.labelVersion_31.setMaximumSize(QSize(200, 20))
        self.labelVersion_31.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_31.setLineWidth(1)
        self.labelVersion_31.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.labelVersion_31, 13, 0, 1, 1)

        self.txtWafermapFileInbase = QLineEdit(self.inbase)
        self.txtWafermapFileInbase.setObjectName(u"txtWafermapFileInbase")
        self.txtWafermapFileInbase.setEnabled(True)
        self.txtWafermapFileInbase.setMinimumSize(QSize(300, 30))
        self.txtWafermapFileInbase.setMaximumSize(QSize(300, 30))
        self.txtWafermapFileInbase.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_20.addWidget(self.txtWafermapFileInbase, 3, 0, 1, 1)

        self.labelVersion_34 = QLabel(self.inbase)
        self.labelVersion_34.setObjectName(u"labelVersion_34")
        self.labelVersion_34.setMaximumSize(QSize(200, 20))
        self.labelVersion_34.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_34.setLineWidth(1)
        self.labelVersion_34.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.labelVersion_34, 13, 1, 1, 1)

        self.txtWaferUpload = QLineEdit(self.inbase)
        self.txtWaferUpload.setObjectName(u"txtWaferUpload")
        self.txtWaferUpload.setEnabled(True)
        self.txtWaferUpload.setMinimumSize(QSize(100, 30))
        self.txtWaferUpload.setMaximumSize(QSize(100, 30))
        self.txtWaferUpload.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_20.addWidget(self.txtWaferUpload, 6, 1, 1, 1)

        self.txtTechnologyUpload = QLineEdit(self.inbase)
        self.txtTechnologyUpload.setObjectName(u"txtTechnologyUpload")
        self.txtTechnologyUpload.setEnabled(True)
        self.txtTechnologyUpload.setMinimumSize(QSize(300, 30))
        self.txtTechnologyUpload.setMaximumSize(QSize(300, 30))
        self.txtTechnologyUpload.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_20.addWidget(self.txtTechnologyUpload, 12, 0, 1, 1)

        self.labelVersion_26 = QLabel(self.inbase)
        self.labelVersion_26.setObjectName(u"labelVersion_26")
        self.labelVersion_26.setMaximumSize(QSize(200, 20))
        self.labelVersion_26.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_26.setLineWidth(1)
        self.labelVersion_26.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.labelVersion_26, 0, 0, 1, 1)

        self.labelVersion_28 = QLabel(self.inbase)
        self.labelVersion_28.setObjectName(u"labelVersion_28")
        self.labelVersion_28.setMaximumSize(QSize(200, 20))
        self.labelVersion_28.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_28.setLineWidth(1)
        self.labelVersion_28.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.labelVersion_28, 10, 0, 1, 1)

        self.cmbTechnologyUpload = QComboBox(self.inbase)
        self.cmbTechnologyUpload.addItem("")
        self.cmbTechnologyUpload.setObjectName(u"cmbTechnologyUpload")
        self.cmbTechnologyUpload.setMinimumSize(QSize(160, 30))
        self.cmbTechnologyUpload.setMaximumSize(QSize(16777215, 30))
        self.cmbTechnologyUpload.setFont(font)
        self.cmbTechnologyUpload.setAutoFillBackground(False)
        self.cmbTechnologyUpload.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbTechnologyUpload.setEditable(True)
        self.cmbTechnologyUpload.setIconSize(QSize(16, 16))
        self.cmbTechnologyUpload.setFrame(True)

        self.gridLayout_20.addWidget(self.cmbTechnologyUpload, 11, 0, 1, 1)

        self.txtMaskUpload = QLineEdit(self.inbase)
        self.txtMaskUpload.setObjectName(u"txtMaskUpload")
        self.txtMaskUpload.setEnabled(True)
        self.txtMaskUpload.setMinimumSize(QSize(300, 30))
        self.txtMaskUpload.setMaximumSize(QSize(300, 30))
        self.txtMaskUpload.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_20.addWidget(self.txtMaskUpload, 12, 1, 1, 1)

        self.labelVersion_33 = QLabel(self.inbase)
        self.labelVersion_33.setObjectName(u"labelVersion_33")
        self.labelVersion_33.setMaximumSize(QSize(200, 20))
        self.labelVersion_33.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_33.setLineWidth(1)
        self.labelVersion_33.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.labelVersion_33, 5, 1, 1, 1)

        self.labelVersion_36 = QLabel(self.inbase)
        self.labelVersion_36.setObjectName(u"labelVersion_36")
        self.labelVersion_36.setMaximumSize(QSize(220, 20))
        self.labelVersion_36.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_36.setLineWidth(1)
        self.labelVersion_36.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.labelVersion_36, 8, 0, 1, 1)

        self.txtDateUpload = QLineEdit(self.inbase)
        self.txtDateUpload.setObjectName(u"txtDateUpload")
        self.txtDateUpload.setEnabled(True)
        self.txtDateUpload.setMinimumSize(QSize(100, 30))
        self.txtDateUpload.setMaximumSize(QSize(100, 30))
        self.txtDateUpload.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.gridLayout_20.addWidget(self.txtDateUpload, 9, 0, 1, 1)


        self.horizontalLayout_19.addLayout(self.gridLayout_20)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_22)


        self.verticalLayout_35.addLayout(self.horizontalLayout_19)

        self.verticalSpacer_15 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_35.addItem(self.verticalSpacer_15)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, 20, -1, -1)
        self.labelVersion_35 = QLabel(self.inbase)
        self.labelVersion_35.setObjectName(u"labelVersion_35")
        self.labelVersion_35.setMaximumSize(QSize(200, 20))
        self.labelVersion_35.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_35.setLineWidth(1)
        self.labelVersion_35.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_22.addWidget(self.labelVersion_35)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_23)

        self.btnSaveImportReport = QPushButton(self.inbase)
        self.btnSaveImportReport.setObjectName(u"btnSaveImportReport")
        self.btnSaveImportReport.setEnabled(True)
        self.btnSaveImportReport.setMinimumSize(QSize(30, 30))
        self.btnSaveImportReport.setMaximumSize(QSize(30, 16777215))
        self.btnSaveImportReport.setFont(font)
        self.btnSaveImportReport.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnSaveImportReport.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        self.btnSaveImportReport.setIcon(icon9)
        self.btnSaveImportReport.setFlat(False)

        self.horizontalLayout_22.addWidget(self.btnSaveImportReport)

        self.btnClearImportReport = QPushButton(self.inbase)
        self.btnClearImportReport.setObjectName(u"btnClearImportReport")
        self.btnClearImportReport.setEnabled(True)
        self.btnClearImportReport.setMinimumSize(QSize(30, 30))
        self.btnClearImportReport.setMaximumSize(QSize(30, 16777215))
        self.btnClearImportReport.setFont(font)
        self.btnClearImportReport.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnClearImportReport.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        self.btnClearImportReport.setIcon(icon10)
        self.btnClearImportReport.setFlat(False)

        self.horizontalLayout_22.addWidget(self.btnClearImportReport)


        self.verticalLayout_35.addLayout(self.horizontalLayout_22)

        self.txtImportReport = QPlainTextEdit(self.inbase)
        self.txtImportReport.setObjectName(u"txtImportReport")
        self.txtImportReport.setStyleSheet(u"background-color: rgb(33, 37, 43);")

        self.verticalLayout_35.addWidget(self.txtImportReport)


        self.verticalLayout_37.addLayout(self.verticalLayout_35)

        self.stackedWidget.addWidget(self.inbase)
        self.reports = QWidget()
        self.reports.setObjectName(u"reports")
        self.label_11 = QLabel(self.reports)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(20, 10, 1164, 20))
        self.label_11.setMinimumSize(QSize(0, 20))
        self.label_11.setMaximumSize(QSize(16777215, 20))
        self.label_11.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.verticalLayoutWidget = QWidget(self.reports)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 50, 311, 121))
        self.verticalLayout_15 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.labelVersion_30 = QLabel(self.verticalLayoutWidget)
        self.labelVersion_30.setObjectName(u"labelVersion_30")
        self.labelVersion_30.setMaximumSize(QSize(200, 20))
        self.labelVersion_30.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.labelVersion_30.setLineWidth(1)
        self.labelVersion_30.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_15.addWidget(self.labelVersion_30)

        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.cmbReports = QComboBox(self.verticalLayoutWidget)
        self.cmbReports.addItem("")
        self.cmbReports.setObjectName(u"cmbReports")
        self.cmbReports.setMinimumSize(QSize(160, 30))
        self.cmbReports.setMaximumSize(QSize(16777215, 30))
        self.cmbReports.setFont(font)
        self.cmbReports.setAutoFillBackground(False)
        self.cmbReports.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.cmbReports.setEditable(True)
        self.cmbReports.setIconSize(QSize(16, 16))
        self.cmbReports.setFrame(True)

        self.horizontalLayout_38.addWidget(self.cmbReports)

        self.btnParametersReport = QPushButton(self.verticalLayoutWidget)
        self.btnParametersReport.setObjectName(u"btnParametersReport")
        self.btnParametersReport.setEnabled(True)
        self.btnParametersReport.setMinimumSize(QSize(30, 30))
        self.btnParametersReport.setMaximumSize(QSize(30, 16777215))
        self.btnParametersReport.setFont(font)
        self.btnParametersReport.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnParametersReport.setStyleSheet(u"/*background-color: rgb(52, 59, 72);*/\n"
"\n"
"#pagesContainer .QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"#pagesContainer .QPushButton:disabled {\n"
"\n"
"	background-color: #333333; border: none;\n"
"}")
        self.btnParametersReport.setIcon(icon1)
        self.btnParametersReport.setFlat(False)

        self.horizontalLayout_38.addWidget(self.btnParametersReport)


        self.verticalLayout_15.addLayout(self.horizontalLayout_38)

        self.btnReport = QPushButton(self.verticalLayoutWidget)
        self.btnReport.setObjectName(u"btnReport")
        self.btnReport.setMinimumSize(QSize(150, 30))
        self.btnReport.setMaximumSize(QSize(300, 16777215))
        self.btnReport.setFont(font)
        self.btnReport.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnReport.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon17 = QIcon()
        icon17.addFile(u":/icons/images/icons/cil-briefcase.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnReport.setIcon(icon17)

        self.verticalLayout_15.addWidget(self.btnReport)

        self.horizontalLayoutWidget = QWidget(self.reports)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 209, 1141, 281))
        self.horizontalLayout_23 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.txtResultReport = QPlainTextEdit(self.horizontalLayoutWidget)
        self.txtResultReport.setObjectName(u"txtResultReport")
        self.txtResultReport.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.txtResultReport.setReadOnly(True)

        self.horizontalLayout_23.addWidget(self.txtResultReport)

        self.stackedWidget.addWidget(self.reports)

        self.horizontalLayout_33.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(200, 16))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setBold(False)
        font5.setItalic(False)
        self.creditsLabel.setFont(font5)
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_9)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setMaximumSize(QSize(100, 16777215))
        self.version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget_configuration.setCurrentIndex(1)
        self.optionsNonAutomatic.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(8)
        self.tabWidget.setCurrentIndex(2)
        self.tabGraph.setCurrentIndex(0)
        self.optionsESTEPA.setCurrentIndex(0)
        self.tabCalcs.setCurrentIndex(0)
        self.tabGraphs.setCurrentIndex(0)
        self.optionsHistorical.setCurrentIndex(0)
        self.tabCalcs_2.setCurrentIndex(0)
        self.tabDiagrams.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.titleLeftApp.setToolTip(QCoreApplication.translate("MainWindow", u"Wafermap", None))
#endif // QT_CONFIG(tooltip)
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"Caracterizar menu", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"Modern GUI / Flat Style", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.btn_page_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_page_measurements.setText(QCoreApplication.translate("MainWindow", u"Measurements", None))
        self.btn_page_instruments.setText(QCoreApplication.translate("MainWindow", u"Instruments", None))
        self.btn_page_probers.setText(QCoreApplication.translate("MainWindow", u"Probers", None))
        self.btn_page_estepa.setText(QCoreApplication.translate("MainWindow", u"Estepa", None))
        self.btn_page_consult.setText(QCoreApplication.translate("MainWindow", u"Consult Estepa", None))
        self.btn_page_inbase.setText(QCoreApplication.translate("MainWindow", u"Inbase", None))
        self.btn_page_reports.setText(QCoreApplication.translate("MainWindow", u"Reports", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.toggleLeftBox.setText(QCoreApplication.translate("MainWindow", u"Left Box", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"Configuration", None))
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
        self.label_txtProcess.setText(QCoreApplication.translate("MainWindow", u"Process name:", None))
        self.txtProcess.setText(QCoreApplication.translate("MainWindow", u"test", None))
        self.txtProcess.setPlaceholderText("")
        self.label_txtLot.setText(QCoreApplication.translate("MainWindow", u"Lot ID:", None))
        self.txtLot.setPlaceholderText("")
        self.label_txtWafer.setText(QCoreApplication.translate("MainWindow", u"Wafer ID:", None))
        self.txtWafer.setPlaceholderText("")
        self.label_txtMask.setText(QCoreApplication.translate("MainWindow", u"Mask name:", None))
        self.txtMask.setPlaceholderText("")
        self.label_txtTemperature.setText(QCoreApplication.translate("MainWindow", u"Temperature (\u00baC):", None))
        self.txtTemperature.setPlaceholderText("")
        self.label_txtHumidity.setText(QCoreApplication.translate("MainWindow", u"Humidity (RH%):", None))
        self.txtHumidity.setPlaceholderText("")
        self.chkDarkMode.setText(QCoreApplication.translate("MainWindow", u"Dark mode", None))
        self.chkViewEstepa.setText(QCoreApplication.translate("MainWindow", u"View estepa options", None))
        self.chkViewGraph.setText(QCoreApplication.translate("MainWindow", u"View measurement graph", None))
        self.chkViewPosition.setText(QCoreApplication.translate("MainWindow", u"View wafermap position", None))
        self.chkSaveMeasurementAuto.setText(QCoreApplication.translate("MainWindow", u"Save measurement auto", None))
        self.Outliner_2.setText(QCoreApplication.translate("MainWindow", u"Outliner Removal Method:", None))
        self.cmbOutlinerMethod.setItemText(0, QCoreApplication.translate("MainWindow", u"none", None))
        self.cmbOutlinerMethod.setItemText(1, QCoreApplication.translate("MainWindow", u"f-spread", None))
        self.cmbOutlinerMethod.setItemText(2, QCoreApplication.translate("MainWindow", u"k-sigma", None))

        self.chkNonAutomaticLimits.setText(QCoreApplication.translate("MainWindow", u"Non-automatic limits", None))
        self.chkGetAutoLimits.setText(QCoreApplication.translate("MainWindow", u"Auto limits", None))
        self.labelVersion_25.setText(QCoreApplication.translate("MainWindow", u"Limit max", None))
        self.labelVersion_24.setText(QCoreApplication.translate("MainWindow", u"Limit min", None))
        self.txtLimitMin.setText("")
        self.txtLimitMin.setPlaceholderText("")
        self.txtLimitMax.setText("")
        self.txtLimitMax.setPlaceholderText("")
        self.Font_2.setText(QCoreApplication.translate("MainWindow", u"Font Size:", None))
        self.cmbFontSize.setItemText(0, QCoreApplication.translate("MainWindow", u"Small", None))
        self.cmbFontSize.setItemText(1, QCoreApplication.translate("MainWindow", u"Big", None))

        self.Performance_2.setText(QCoreApplication.translate("MainWindow", u"Performance Presentation:", None))
        self.cmbPerformancePresentation.setItemText(0, QCoreApplication.translate("MainWindow", u"Number of Points", None))
        self.cmbPerformancePresentation.setItemText(1, QCoreApplication.translate("MainWindow", u"Percentage", None))

        self.Wafer_2.setText(QCoreApplication.translate("MainWindow", u"Wafer Representation:", None))
        self.cmbWaferRepresentation.setItemText(0, QCoreApplication.translate("MainWindow", u"Colors", None))
        self.cmbWaferRepresentation.setItemText(1, QCoreApplication.translate("MainWindow", u"Gravity centers", None))
        self.cmbWaferRepresentation.setItemText(2, QCoreApplication.translate("MainWindow", u"Letters", None))

        self.HistogramTextLabel.setText(QCoreApplication.translate("MainWindow", u"Histogram chunks", None))
        self.txtHistogramChunks.setText(QCoreApplication.translate("MainWindow", u"16", None))
        self.txtHistogramChunks.setPlaceholderText("")
        self.reportTitleLabel.setText(QCoreApplication.translate("MainWindow", u"Title:", None))
        self.txtReportTitle.setText(QCoreApplication.translate("MainWindow", u"CAP REPORT", None))
        self.txtReportTitle.setPlaceholderText("")
        self.reportSubtitleLabel.setText(QCoreApplication.translate("MainWindow", u"Subtitle:", None))
        self.txtReportSubtitle.setText(QCoreApplication.translate("MainWindow", u"15813", None))
        self.txtReportSubtitle.setPlaceholderText("")
        self.reportDateLabel.setText(QCoreApplication.translate("MainWindow", u"Date:", None))
        self.txtReportDate.setText(QCoreApplication.translate("MainWindow", u"JUNE 2022", None))
        self.txtReportDate.setPlaceholderText("")
        self.reportAuthorLabel.setText(QCoreApplication.translate("MainWindow", u"Author:", None))
        self.txtReportAuthor.setText(QCoreApplication.translate("MainWindow", u"Sergi S\u00e0nchez", None))
        self.txtReportAuthor.setPlaceholderText("")
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"CARACTERIZAR - Software Instrument Control for Lab Users", None))
#if QT_CONFIG(tooltip)
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.settingsTopBtn.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.btn_message.setText(QCoreApplication.translate("MainWindow", u"Message", None))
        self.btn_print.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MEASUREMENTS", None))
        self.cmbInstruments.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.cmbInstruments.setCurrentText(QCoreApplication.translate("MainWindow", u"Select instrument", None))
        self.cmbTests.setItemText(0, QCoreApplication.translate("MainWindow", u"Select test", None))

        self.cmbTests.setCurrentText(QCoreApplication.translate("MainWindow", u"Select test", None))
#if QT_CONFIG(tooltip)
        self.btnParameters.setToolTip(QCoreApplication.translate("MainWindow", u"Parameters configuration", None))
#endif // QT_CONFIG(tooltip)
        self.btnParameters.setText("")
        self.chkCartoMeas.setText(QCoreApplication.translate("MainWindow", u"Cartographic measurement", None))
        self.btnStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btnPause.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.btnStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.cmbProbers.setItemText(0, QCoreApplication.translate("MainWindow", u"Select prober", None))

        self.cmbProbers.setCurrentText(QCoreApplication.translate("MainWindow", u"Select prober", None))
        self.cmbWafermaps.setItemText(0, QCoreApplication.translate("MainWindow", u"Select wafermap", None))

        self.cmbWafermaps.setCurrentText(QCoreApplication.translate("MainWindow", u"Select wafermap", None))
#if QT_CONFIG(tooltip)
        self.btnGoHome.setToolTip(QCoreApplication.translate("MainWindow", u"Go Home", None))
#endif // QT_CONFIG(tooltip)
        self.btnGoHome.setText("")
#if QT_CONFIG(tooltip)
        self.btnViewWafermap.setToolTip(QCoreApplication.translate("MainWindow", u"View Wafermap", None))
#endif // QT_CONFIG(tooltip)
        self.btnViewWafermap.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Test description", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Wafermap description", None))
#if QT_CONFIG(tooltip)
        self.test_status.setToolTip(QCoreApplication.translate("MainWindow", u"IDLE", None))
#endif // QT_CONFIG(tooltip)
        self.test_status.setText(QCoreApplication.translate("MainWindow", u"Test", None))
#if QT_CONFIG(tooltip)
        self.measurement_status.setToolTip(QCoreApplication.translate("MainWindow", u"IDLE", None))
#endif // QT_CONFIG(tooltip)
        self.measurement_status.setText(QCoreApplication.translate("MainWindow", u"Meas", None))
#if QT_CONFIG(tooltip)
        self.contact_status.setToolTip(QCoreApplication.translate("MainWindow", u"IDLE", None))
#endif // QT_CONFIG(tooltip)
        self.contact_status.setText(QCoreApplication.translate("MainWindow", u"Contact", None))
#if QT_CONFIG(tooltip)
        self.separation_status.setToolTip(QCoreApplication.translate("MainWindow", u"IDLE", None))
#endif // QT_CONFIG(tooltip)
        self.separation_status.setText(QCoreApplication.translate("MainWindow", u"Separation", None))
#if QT_CONFIG(tooltip)
        self.btnSaveDescription.setToolTip(QCoreApplication.translate("MainWindow", u"Save", None))
#endif // QT_CONFIG(tooltip)
        self.btnSaveDescription.setText("")
#if QT_CONFIG(tooltip)
        self.btnClearDescription.setToolTip(QCoreApplication.translate("MainWindow", u"Clear", None))
#endif // QT_CONFIG(tooltip)
        self.btnClearDescription.setText("")
        self.progressBar.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Die:", None))
        self.dieActual.setInputMask("")
        self.dieActual.setText("")
        self.labelVersion_7.setText(QCoreApplication.translate("MainWindow", u"of", None))
        self.dieTotal.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Module:", None))
        self.labelVersion_8.setText(QCoreApplication.translate("MainWindow", u"of", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Init time:", None))
        self.timeInit.setInputMask("")
        self.timeInit.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"End time:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Process description", None))
        self.btnSaveGraph.setText("")
        self.btnClearGraph.setText("")
        self.tabGraph.setTabText(self.tabGraph.indexOf(self.tabWafermap_3), QCoreApplication.translate("MainWindow", u"Graph", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"INSTRUMENTS", None))
        self.cmbInstruments_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.cmbInstruments_2.setCurrentText(QCoreApplication.translate("MainWindow", u"Select instrument", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"PROBERS", None))
        self.cmbProbers_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.cmbProbers_2.setCurrentText(QCoreApplication.translate("MainWindow", u"Select instrument", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"STATISTICS for the PARAMETRIC TEST", None))
        self.optLoadFiles.setText(QCoreApplication.translate("MainWindow", u"Load from files", None))
        self.optLoadBBDD.setText(QCoreApplication.translate("MainWindow", u"Load from BBDD", None))
        self.btnLoadFiles.setText(QCoreApplication.translate("MainWindow", u"Load from files", None))
        self.labelVersion_13.setText(QCoreApplication.translate("MainWindow", u"Load DATA file", None))
        self.btnOpenWafermapFile.setText("")
        self.txtDataFile.setText("")
        self.txtDataFile.setPlaceholderText("")
        self.txtWafermapFile.setText("")
        self.txtWafermapFile.setPlaceholderText("")
        self.btnOpenDataFile.setText("")
        self.labelVersion_14.setText(QCoreApplication.translate("MainWindow", u"Load WAFERMAP file", None))
        self.cmbParametersFile.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.labelVersion_19.setText(QCoreApplication.translate("MainWindow", u"Select parameters", None))
        self.btnNextParamFiles.setText("")
        self.txtParamSelectedFiles.setText("")
        self.txtParamSelectedFiles.setPlaceholderText("")
        self.btnCorrelationFiles.setText(QCoreApplication.translate("MainWindow", u"Correlation", None))
        self.btnAnalyzeFiles.setText(QCoreApplication.translate("MainWindow", u"Analyze", None))
        self.btnPreviousParamFiles.setText("")
        self.labelVersion_17.setText(QCoreApplication.translate("MainWindow", u"Select run", None))
        self.labelVersion_18.setText(QCoreApplication.translate("MainWindow", u"Select parameters", None))
        self.cmbParametersBBDD.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.cmbParametersBBDD.setCurrentText(QCoreApplication.translate("MainWindow", u"Select instrument", None))
        self.cmbTechnology.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.cmbTechnology.setCurrentText(QCoreApplication.translate("MainWindow", u"Select instrument", None))
        self.labelVersion_16.setText(QCoreApplication.translate("MainWindow", u"Select wafer", None))
        self.labelVersion_15.setText(QCoreApplication.translate("MainWindow", u"Select technology", None))
        self.cmbWafers.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.cmbWafers.setCurrentText(QCoreApplication.translate("MainWindow", u"Select instrument", None))
        self.cmbRuns.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.cmbRuns.setCurrentText(QCoreApplication.translate("MainWindow", u"Select instrument", None))
        self.txtParamSelectedBBDD.setText("")
        self.txtParamSelectedBBDD.setPlaceholderText("")
        self.btnNextParamBBDD.setText("")
        self.btnCorrelationBBDD.setText(QCoreApplication.translate("MainWindow", u"Correlation", None))
        self.btnAnalyzeBBDD.setText(QCoreApplication.translate("MainWindow", u"Analyze", None))
        self.btnPreviousParamBBDD.setText("")
#if QT_CONFIG(tooltip)
        self.txtDataValues.setToolTip(QCoreApplication.translate("MainWindow", u"Data values", None))
#endif // QT_CONFIG(tooltip)
        self.txtDataValues.setPlainText("")
#if QT_CONFIG(tooltip)
        self.btnSaveDataValues.setToolTip(QCoreApplication.translate("MainWindow", u"Save", None))
#endif // QT_CONFIG(tooltip)
        self.btnSaveDataValues.setText("")
#if QT_CONFIG(tooltip)
        self.btnClearDataValues.setToolTip(QCoreApplication.translate("MainWindow", u"Clear", None))
#endif // QT_CONFIG(tooltip)
        self.btnClearDataValues.setText("")
        self.tabCalcs.setTabText(self.tabCalcs.indexOf(self.tabData), QCoreApplication.translate("MainWindow", u"Data Values", None))
#if QT_CONFIG(tooltip)
        self.txtParametersResult.setToolTip(QCoreApplication.translate("MainWindow", u"Data values", None))
#endif // QT_CONFIG(tooltip)
        self.txtParametersResult.setPlainText("")
#if QT_CONFIG(tooltip)
        self.btnSaveParametersResult.setToolTip(QCoreApplication.translate("MainWindow", u"Save", None))
#endif // QT_CONFIG(tooltip)
        self.btnSaveParametersResult.setText("")
#if QT_CONFIG(tooltip)
        self.btnClearParametersResult.setToolTip(QCoreApplication.translate("MainWindow", u"Clear", None))
#endif // QT_CONFIG(tooltip)
        self.btnClearParametersResult.setText("")
        self.tabCalcs.setTabText(self.tabCalcs.indexOf(self.tabParameters), QCoreApplication.translate("MainWindow", u"Parameters Result", None))
        self.btnSaveWafermap.setText("")
        self.btnClearWafermap.setText("")
        self.tabGraphs.setTabText(self.tabGraphs.indexOf(self.tabWafermap), QCoreApplication.translate("MainWindow", u"Wafermap", None))
        self.btnSaveHistogram.setText("")
        self.btnClearHistogram.setText("")
        self.tabGraphs.setTabText(self.tabGraphs.indexOf(self.tabHistogram), QCoreApplication.translate("MainWindow", u"Histogram", None))
        self.labelBoxBlenderInstalation.setText(QCoreApplication.translate("MainWindow", u"FILE BOX", None))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type here", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.labelVersion_3.setText(QCoreApplication.translate("MainWindow", u"Label description", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Test 1", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Test 2", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Test 3", None))

        self.commandLinkButton.setText(QCoreApplication.translate("MainWindow", u"Link Button", None))
        self.commandLinkButton.setDescription(QCoreApplication.translate("MainWindow", u"Link description", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"2", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"3", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem5 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem6 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem7 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem8 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem9 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem10 = self.tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem11 = self.tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem12 = self.tableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem13 = self.tableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem14 = self.tableWidget.verticalHeaderItem(10)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem15 = self.tableWidget.verticalHeaderItem(11)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem16 = self.tableWidget.verticalHeaderItem(12)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem17 = self.tableWidget.verticalHeaderItem(13)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem18 = self.tableWidget.verticalHeaderItem(14)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem19 = self.tableWidget.verticalHeaderItem(15)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"New Row", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem20 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Test", None));
        ___qtablewidgetitem21 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Text", None));
        ___qtablewidgetitem22 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Cell", None));
        ___qtablewidgetitem23 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Line", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.label_12.setText(QCoreApplication.translate("MainWindow", u"CONSULT ESTEPA", None))
        self.optRunsConsult.setText(QCoreApplication.translate("MainWindow", u"Runs", None))
        self.optWafersConsult.setText(QCoreApplication.translate("MainWindow", u"Wafers", None))
        self.chkHistorical.setText(QCoreApplication.translate("MainWindow", u"Historical", None))
        self.optYield.setText(QCoreApplication.translate("MainWindow", u"Yield", None))
        self.optValues.setText(QCoreApplication.translate("MainWindow", u"Values", None))
        self.labelVersion_40.setText(QCoreApplication.translate("MainWindow", u"Select technology", None))
        self.cmbTechnologyConsult.setCurrentText("")
        self.labelVersion_41.setText(QCoreApplication.translate("MainWindow", u"Select run", None))
        self.cmbRunsConsult.setCurrentText("")
        self.labelVersion_39.setText(QCoreApplication.translate("MainWindow", u"Select wafer", None))
        self.cmbWafersConsult.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

#if QT_CONFIG(tooltip)
        self.btnAddWafers.setToolTip(QCoreApplication.translate("MainWindow", u"Select wafers", None))
#endif // QT_CONFIG(tooltip)
        self.btnAddWafers.setText("")
        self.labelVersion_38.setText(QCoreApplication.translate("MainWindow", u"Selected wafers", None))

        __sortingEnabled1 = self.lbWafers.isSortingEnabled()
        self.lbWafers.setSortingEnabled(False)
        ___qlistwidgetitem = self.lbWafers.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"Item 1", None));
        ___qlistwidgetitem1 = self.lbWafers.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Item 2", None));
        self.lbWafers.setSortingEnabled(__sortingEnabled1)

        self.labelVersion_37.setText(QCoreApplication.translate("MainWindow", u"Select parameters", None))
        self.cmbParametersConsult.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.txtParamSelectedConsult.setText("")
        self.txtParamSelectedConsult.setPlaceholderText("")
        self.btnPreviousParamConsult.setText("")
        self.btnNextParamConsult.setText("")
        self.btnConsult.setText(QCoreApplication.translate("MainWindow", u"Consult", None))
        self.lblLoadingConsult.setText(QCoreApplication.translate("MainWindow", u"Loading...", None))
#if QT_CONFIG(tooltip)
        self.txtDataValuesConsult.setToolTip(QCoreApplication.translate("MainWindow", u"Data values", None))
#endif // QT_CONFIG(tooltip)
        self.txtDataValuesConsult.setPlainText("")
#if QT_CONFIG(tooltip)
        self.btnUploadHistorical.setToolTip(QCoreApplication.translate("MainWindow", u"Upload", None))
#endif // QT_CONFIG(tooltip)
        self.btnUploadHistorical.setText("")
#if QT_CONFIG(tooltip)
        self.btnSaveHistorical.setToolTip(QCoreApplication.translate("MainWindow", u"Save", None))
#endif // QT_CONFIG(tooltip)
        self.btnSaveHistorical.setText("")
#if QT_CONFIG(tooltip)
        self.btnClearDataValuesConsult.setToolTip(QCoreApplication.translate("MainWindow", u"Clear", None))
#endif // QT_CONFIG(tooltip)
        self.btnClearDataValuesConsult.setText("")
        self.tabCalcs_2.setTabText(self.tabCalcs_2.indexOf(self.tabData_2), QCoreApplication.translate("MainWindow", u"Data Values", None))
        self.btnSaveDiagram.setText("")
        self.btnClearDiagram.setText("")
        self.tabDiagrams.setTabText(self.tabDiagrams.indexOf(self.tabDiagrams_2), QCoreApplication.translate("MainWindow", u"Diagram", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"UPLOAD RESULTS to ESTEPA", None))
        self.labelVersion_27.setText(QCoreApplication.translate("MainWindow", u"Load WAFERMAP file", None))
        self.btnUploadFiles.setText(QCoreApplication.translate("MainWindow", u"Upload results from files", None))
        self.txtRunUpload.setText("")
        self.txtRunUpload.setPlaceholderText("")
        self.txtLocalizationUpload.setText("")
        self.txtLocalizationUpload.setPlaceholderText("")
        self.txtCommentUpload.setText("")
        self.txtCommentUpload.setPlaceholderText("")
        self.btnOpenWafermapFileInbase.setText("")
        self.labelVersion_29.setText(QCoreApplication.translate("MainWindow", u"Select Mask", None))
        self.cmbMaskUpload.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.cmbMaskUpload.setCurrentText(QCoreApplication.translate("MainWindow", u"Select instrument", None))
        self.btnOpenDataFileInbase.setText("")
        self.txtDataFileInbase.setText("")
        self.txtDataFileInbase.setPlaceholderText("")
        self.labelVersion_32.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.labelVersion_31.setText(QCoreApplication.translate("MainWindow", u"Localization", None))
        self.txtWafermapFileInbase.setText("")
        self.txtWafermapFileInbase.setPlaceholderText("")
        self.labelVersion_34.setText(QCoreApplication.translate("MainWindow", u"Comment for wafer", None))
        self.txtWaferUpload.setText("")
        self.txtWaferUpload.setPlaceholderText("")
        self.txtTechnologyUpload.setText("")
        self.txtTechnologyUpload.setPlaceholderText("")
        self.labelVersion_26.setText(QCoreApplication.translate("MainWindow", u"Load DATA file", None))
        self.labelVersion_28.setText(QCoreApplication.translate("MainWindow", u"Select technology", None))
        self.cmbTechnologyUpload.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.cmbTechnologyUpload.setCurrentText(QCoreApplication.translate("MainWindow", u"Select instrument", None))
        self.txtMaskUpload.setText("")
        self.txtMaskUpload.setPlaceholderText("")
        self.labelVersion_33.setText(QCoreApplication.translate("MainWindow", u"Wafer", None))
        self.labelVersion_36.setText(QCoreApplication.translate("MainWindow", u"Run Date (yyyy-mm-dd)", None))
        self.txtDateUpload.setText("")
        self.txtDateUpload.setPlaceholderText("")
        self.labelVersion_35.setText(QCoreApplication.translate("MainWindow", u"Import report", None))
#if QT_CONFIG(tooltip)
        self.btnSaveImportReport.setToolTip(QCoreApplication.translate("MainWindow", u"Save", None))
#endif // QT_CONFIG(tooltip)
        self.btnSaveImportReport.setText("")
#if QT_CONFIG(tooltip)
        self.btnClearImportReport.setToolTip(QCoreApplication.translate("MainWindow", u"Clear", None))
#endif // QT_CONFIG(tooltip)
        self.btnClearImportReport.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"REPORTS", None))
        self.labelVersion_30.setText(QCoreApplication.translate("MainWindow", u"Select report", None))
        self.cmbReports.setItemText(0, QCoreApplication.translate("MainWindow", u"Select instrument", None))

        self.cmbReports.setCurrentText(QCoreApplication.translate("MainWindow", u"Select instrument", None))
#if QT_CONFIG(tooltip)
        self.btnParametersReport.setToolTip(QCoreApplication.translate("MainWindow", u"Parameters configuration", None))
#endif // QT_CONFIG(tooltip)
        self.btnParametersReport.setText("")
        self.btnReport.setText(QCoreApplication.translate("MainWindow", u"  Create report file", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"By: Sergi S\u00e0nchez", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi

