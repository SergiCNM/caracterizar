# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modulesXmjqyF.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_ModulesWindow(object):
    def setupUi(self, ModulesWindow):
        if not ModulesWindow.objectName():
            ModulesWindow.setObjectName(u"ModulesWindow")
        ModulesWindow.resize(1050, 410)
        ModulesWindow.setMinimumSize(QSize(1050, 410))
        ModulesWindow.setMaximumSize(QSize(1050, 420))
        ModulesWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(ModulesWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
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
        self.verticalLayoutWidget.setGeometry(QRect(80, 70, 91, 311))
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
        self.verticalLayoutWidget_2.setGeometry(QRect(170, 70, 91, 311))
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
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 70, 70, 318))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_41 = QLabel(self.verticalLayoutWidget_3)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMaximumSize(QSize(16777215, 16777215))
        self.label_41.setFont(font)
        self.label_41.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_4.addWidget(self.label_41)

        self.txtN1 = QLineEdit(self.verticalLayoutWidget_3)
        self.txtN1.setObjectName(u"txtN1")
        self.txtN1.setMinimumSize(QSize(0, 24))

        self.verticalLayout_4.addWidget(self.txtN1)

        self.txtN2 = QLineEdit(self.verticalLayoutWidget_3)
        self.txtN2.setObjectName(u"txtN2")
        self.txtN2.setMinimumSize(QSize(0, 24))
        self.txtN2.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_4.addWidget(self.txtN2)

        self.txtN3 = QLineEdit(self.verticalLayoutWidget_3)
        self.txtN3.setObjectName(u"txtN3")
        self.txtN3.setMinimumSize(QSize(0, 24))
        self.txtN3.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_4.addWidget(self.txtN3)

        self.txtN4 = QLineEdit(self.verticalLayoutWidget_3)
        self.txtN4.setObjectName(u"txtN4")
        self.txtN4.setMinimumSize(QSize(0, 24))
        self.txtN4.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_4.addWidget(self.txtN4)

        self.txtN5 = QLineEdit(self.verticalLayoutWidget_3)
        self.txtN5.setObjectName(u"txtN5")
        self.txtN5.setMinimumSize(QSize(0, 24))
        self.txtN5.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_4.addWidget(self.txtN5)

        self.txtN6 = QLineEdit(self.verticalLayoutWidget_3)
        self.txtN6.setObjectName(u"txtN6")
        self.txtN6.setMinimumSize(QSize(0, 24))
        self.txtN6.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_4.addWidget(self.txtN6)

        self.txtN7 = QLineEdit(self.verticalLayoutWidget_3)
        self.txtN7.setObjectName(u"txtN7")
        self.txtN7.setMinimumSize(QSize(0, 24))
        self.txtN7.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_4.addWidget(self.txtN7)

        self.txtN8 = QLineEdit(self.verticalLayoutWidget_3)
        self.txtN8.setObjectName(u"txtN8")
        self.txtN8.setMinimumSize(QSize(0, 24))
        self.txtN8.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_4.addWidget(self.txtN8)

        self.txtN9 = QLineEdit(self.verticalLayoutWidget_3)
        self.txtN9.setObjectName(u"txtN9")
        self.txtN9.setMinimumSize(QSize(0, 24))
        self.txtN9.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_4.addWidget(self.txtN9)

        self.txtN10 = QLineEdit(self.verticalLayoutWidget_3)
        self.txtN10.setObjectName(u"txtN10")
        self.txtN10.setMinimumSize(QSize(0, 24))
        self.txtN10.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_4.addWidget(self.txtN10)

        self.verticalLayoutWidget_5 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(340, 70, 91, 311))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.verticalLayoutWidget_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 16))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.label_4)

        self.txtX11 = QDoubleSpinBox(self.verticalLayoutWidget_5)
        self.txtX11.setObjectName(u"txtX11")
        self.txtX11.setMaximumSize(QSize(85, 16777215))
        self.txtX11.setDecimals(6)
        self.txtX11.setMinimum(-999999.989999999990687)
        self.txtX11.setMaximum(999999.989999999990687)

        self.verticalLayout_3.addWidget(self.txtX11)

        self.txtX12 = QDoubleSpinBox(self.verticalLayoutWidget_5)
        self.txtX12.setObjectName(u"txtX12")
        self.txtX12.setMaximumSize(QSize(85, 16777215))
        self.txtX12.setDecimals(6)
        self.txtX12.setMinimum(-999999.989999999990687)
        self.txtX12.setMaximum(999999.989999999990687)

        self.verticalLayout_3.addWidget(self.txtX12)

        self.txtX13 = QDoubleSpinBox(self.verticalLayoutWidget_5)
        self.txtX13.setObjectName(u"txtX13")
        self.txtX13.setMaximumSize(QSize(85, 16777215))
        self.txtX13.setDecimals(6)
        self.txtX13.setMinimum(-999999.989999999990687)
        self.txtX13.setMaximum(999999.989999999990687)

        self.verticalLayout_3.addWidget(self.txtX13)

        self.txtX14 = QDoubleSpinBox(self.verticalLayoutWidget_5)
        self.txtX14.setObjectName(u"txtX14")
        self.txtX14.setMaximumSize(QSize(85, 16777215))
        self.txtX14.setDecimals(6)
        self.txtX14.setMinimum(-999999.989999999990687)
        self.txtX14.setMaximum(999999.989999999990687)

        self.verticalLayout_3.addWidget(self.txtX14)

        self.txtX15 = QDoubleSpinBox(self.verticalLayoutWidget_5)
        self.txtX15.setObjectName(u"txtX15")
        self.txtX15.setMaximumSize(QSize(85, 16777215))
        self.txtX15.setDecimals(6)
        self.txtX15.setMinimum(-999999.989999999990687)
        self.txtX15.setMaximum(999999.989999999990687)

        self.verticalLayout_3.addWidget(self.txtX15)

        self.txtX16 = QDoubleSpinBox(self.verticalLayoutWidget_5)
        self.txtX16.setObjectName(u"txtX16")
        self.txtX16.setMaximumSize(QSize(85, 16777215))
        self.txtX16.setDecimals(6)
        self.txtX16.setMinimum(-999999.989999999990687)
        self.txtX16.setMaximum(999999.989999999990687)

        self.verticalLayout_3.addWidget(self.txtX16)

        self.txtX17 = QDoubleSpinBox(self.verticalLayoutWidget_5)
        self.txtX17.setObjectName(u"txtX17")
        self.txtX17.setMaximumSize(QSize(85, 16777215))
        self.txtX17.setDecimals(6)
        self.txtX17.setMinimum(-999999.989999999990687)
        self.txtX17.setMaximum(999999.989999999990687)

        self.verticalLayout_3.addWidget(self.txtX17)

        self.txtX18 = QDoubleSpinBox(self.verticalLayoutWidget_5)
        self.txtX18.setObjectName(u"txtX18")
        self.txtX18.setMaximumSize(QSize(85, 16777215))
        self.txtX18.setDecimals(6)
        self.txtX18.setMinimum(-999999.989999999990687)
        self.txtX18.setMaximum(999999.989999999990687)

        self.verticalLayout_3.addWidget(self.txtX18)

        self.txtX19 = QDoubleSpinBox(self.verticalLayoutWidget_5)
        self.txtX19.setObjectName(u"txtX19")
        self.txtX19.setMaximumSize(QSize(85, 16777215))
        self.txtX19.setDecimals(6)
        self.txtX19.setMinimum(-999999.989999999990687)
        self.txtX19.setMaximum(999999.989999999990687)

        self.verticalLayout_3.addWidget(self.txtX19)

        self.txtX20 = QDoubleSpinBox(self.verticalLayoutWidget_5)
        self.txtX20.setObjectName(u"txtX20")
        self.txtX20.setMaximumSize(QSize(85, 16777215))
        self.txtX20.setDecimals(6)
        self.txtX20.setMinimum(-999999.989999999990687)
        self.txtX20.setMaximum(999999.989999999990687)

        self.verticalLayout_3.addWidget(self.txtX20)

        self.verticalLayoutWidget_6 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(430, 70, 91, 311))
        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_27 = QLabel(self.verticalLayoutWidget_6)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMaximumSize(QSize(16777215, 16))
        self.label_27.setFont(font)
        self.label_27.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_6.addWidget(self.label_27)

        self.txtY11 = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.txtY11.setObjectName(u"txtY11")
        self.txtY11.setMaximumSize(QSize(85, 16777215))
        self.txtY11.setDecimals(6)
        self.txtY11.setMinimum(-999999.989999999990687)
        self.txtY11.setMaximum(999999.989999999990687)

        self.verticalLayout_6.addWidget(self.txtY11)

        self.txtY12 = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.txtY12.setObjectName(u"txtY12")
        self.txtY12.setMaximumSize(QSize(85, 16777215))
        self.txtY12.setDecimals(6)
        self.txtY12.setMinimum(-999999.989999999990687)
        self.txtY12.setMaximum(999999.989999999990687)

        self.verticalLayout_6.addWidget(self.txtY12)

        self.txtY13 = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.txtY13.setObjectName(u"txtY13")
        self.txtY13.setMaximumSize(QSize(85, 16777215))
        self.txtY13.setDecimals(6)
        self.txtY13.setMinimum(-999999.989999999990687)
        self.txtY13.setMaximum(999999.989999999990687)

        self.verticalLayout_6.addWidget(self.txtY13)

        self.txtY14 = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.txtY14.setObjectName(u"txtY14")
        self.txtY14.setMaximumSize(QSize(85, 16777215))
        self.txtY14.setDecimals(6)
        self.txtY14.setMinimum(-999999.989999999990687)
        self.txtY14.setMaximum(999999.989999999990687)

        self.verticalLayout_6.addWidget(self.txtY14)

        self.txtY15 = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.txtY15.setObjectName(u"txtY15")
        self.txtY15.setMaximumSize(QSize(85, 16777215))
        self.txtY15.setDecimals(6)
        self.txtY15.setMinimum(-999999.989999999990687)
        self.txtY15.setMaximum(999999.989999999990687)

        self.verticalLayout_6.addWidget(self.txtY15)

        self.txtY16 = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.txtY16.setObjectName(u"txtY16")
        self.txtY16.setMaximumSize(QSize(85, 16777215))
        self.txtY16.setDecimals(6)
        self.txtY16.setMinimum(-999999.989999999990687)
        self.txtY16.setMaximum(999999.989999999990687)

        self.verticalLayout_6.addWidget(self.txtY16)

        self.txtY17 = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.txtY17.setObjectName(u"txtY17")
        self.txtY17.setMaximumSize(QSize(85, 16777215))
        self.txtY17.setDecimals(6)
        self.txtY17.setMinimum(-999999.989999999990687)
        self.txtY17.setMaximum(999999.989999999990687)

        self.verticalLayout_6.addWidget(self.txtY17)

        self.txtY18 = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.txtY18.setObjectName(u"txtY18")
        self.txtY18.setMaximumSize(QSize(85, 16777215))
        self.txtY18.setDecimals(6)
        self.txtY18.setMinimum(-999999.989999999990687)
        self.txtY18.setMaximum(999999.989999999990687)

        self.verticalLayout_6.addWidget(self.txtY18)

        self.txtY19 = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.txtY19.setObjectName(u"txtY19")
        self.txtY19.setMaximumSize(QSize(85, 16777215))
        self.txtY19.setDecimals(6)
        self.txtY19.setMinimum(-999999.989999999990687)
        self.txtY19.setMaximum(999999.989999999990687)

        self.verticalLayout_6.addWidget(self.txtY19)

        self.txtY20 = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.txtY20.setObjectName(u"txtY20")
        self.txtY20.setMaximumSize(QSize(85, 16777215))
        self.txtY20.setDecimals(6)
        self.txtY20.setMinimum(-999999.989999999990687)
        self.txtY20.setMaximum(999999.989999999990687)

        self.verticalLayout_6.addWidget(self.txtY20)

        self.verticalLayoutWidget_8 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_8.setObjectName(u"verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(600, 70, 91, 311))
        self.verticalLayout_8 = QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_39 = QLabel(self.verticalLayoutWidget_8)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setMaximumSize(QSize(16777215, 16))
        self.label_39.setFont(font)
        self.label_39.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_8.addWidget(self.label_39)

        self.txtX21 = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.txtX21.setObjectName(u"txtX21")
        self.txtX21.setMaximumSize(QSize(85, 16777215))
        self.txtX21.setDecimals(6)
        self.txtX21.setMinimum(-999999.989999999990687)
        self.txtX21.setMaximum(999999.989999999990687)

        self.verticalLayout_8.addWidget(self.txtX21)

        self.txtX22 = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.txtX22.setObjectName(u"txtX22")
        self.txtX22.setMaximumSize(QSize(85, 16777215))
        self.txtX22.setDecimals(6)
        self.txtX22.setMinimum(-999999.989999999990687)
        self.txtX22.setMaximum(999999.989999999990687)

        self.verticalLayout_8.addWidget(self.txtX22)

        self.txtX23 = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.txtX23.setObjectName(u"txtX23")
        self.txtX23.setMaximumSize(QSize(85, 16777215))
        self.txtX23.setDecimals(6)
        self.txtX23.setMinimum(-999999.989999999990687)
        self.txtX23.setMaximum(999999.989999999990687)

        self.verticalLayout_8.addWidget(self.txtX23)

        self.txtX24 = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.txtX24.setObjectName(u"txtX24")
        self.txtX24.setMaximumSize(QSize(85, 16777215))
        self.txtX24.setDecimals(6)
        self.txtX24.setMinimum(-999999.989999999990687)
        self.txtX24.setMaximum(999999.989999999990687)

        self.verticalLayout_8.addWidget(self.txtX24)

        self.txtX25 = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.txtX25.setObjectName(u"txtX25")
        self.txtX25.setMaximumSize(QSize(85, 16777215))
        self.txtX25.setDecimals(6)
        self.txtX25.setMinimum(-999999.989999999990687)
        self.txtX25.setMaximum(999999.989999999990687)

        self.verticalLayout_8.addWidget(self.txtX25)

        self.txtX26 = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.txtX26.setObjectName(u"txtX26")
        self.txtX26.setMaximumSize(QSize(85, 16777215))
        self.txtX26.setDecimals(6)
        self.txtX26.setMinimum(-999999.989999999990687)
        self.txtX26.setMaximum(999999.989999999990687)

        self.verticalLayout_8.addWidget(self.txtX26)

        self.txtX27 = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.txtX27.setObjectName(u"txtX27")
        self.txtX27.setMaximumSize(QSize(85, 16777215))
        self.txtX27.setDecimals(6)
        self.txtX27.setMinimum(-999999.989999999990687)
        self.txtX27.setMaximum(999999.989999999990687)

        self.verticalLayout_8.addWidget(self.txtX27)

        self.txtX28 = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.txtX28.setObjectName(u"txtX28")
        self.txtX28.setMaximumSize(QSize(85, 16777215))
        self.txtX28.setDecimals(6)
        self.txtX28.setMinimum(-999999.989999999990687)
        self.txtX28.setMaximum(999999.989999999990687)

        self.verticalLayout_8.addWidget(self.txtX28)

        self.txtX29 = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.txtX29.setObjectName(u"txtX29")
        self.txtX29.setMaximumSize(QSize(85, 16777215))
        self.txtX29.setDecimals(6)
        self.txtX29.setMinimum(-999999.989999999990687)
        self.txtX29.setMaximum(999999.989999999990687)

        self.verticalLayout_8.addWidget(self.txtX29)

        self.txtX30 = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.txtX30.setObjectName(u"txtX30")
        self.txtX30.setMaximumSize(QSize(85, 16777215))
        self.txtX30.setDecimals(6)
        self.txtX30.setMinimum(-999999.989999999990687)
        self.txtX30.setMaximum(999999.989999999990687)

        self.verticalLayout_8.addWidget(self.txtX30)

        self.verticalLayoutWidget_9 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_9.setObjectName(u"verticalLayoutWidget_9")
        self.verticalLayoutWidget_9.setGeometry(QRect(690, 70, 91, 311))
        self.verticalLayout_9 = QVBoxLayout(self.verticalLayoutWidget_9)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_40 = QLabel(self.verticalLayoutWidget_9)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMaximumSize(QSize(16777215, 16))
        self.label_40.setFont(font)
        self.label_40.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_9.addWidget(self.label_40)

        self.txtY21 = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.txtY21.setObjectName(u"txtY21")
        self.txtY21.setMaximumSize(QSize(85, 16777215))
        self.txtY21.setDecimals(6)
        self.txtY21.setMinimum(-999999.989999999990687)
        self.txtY21.setMaximum(999999.989999999990687)

        self.verticalLayout_9.addWidget(self.txtY21)

        self.txtY22 = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.txtY22.setObjectName(u"txtY22")
        self.txtY22.setMaximumSize(QSize(85, 16777215))
        self.txtY22.setDecimals(6)
        self.txtY22.setMinimum(-999999.989999999990687)
        self.txtY22.setMaximum(999999.989999999990687)

        self.verticalLayout_9.addWidget(self.txtY22)

        self.txtY23 = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.txtY23.setObjectName(u"txtY23")
        self.txtY23.setMaximumSize(QSize(85, 16777215))
        self.txtY23.setDecimals(6)
        self.txtY23.setMinimum(-999999.989999999990687)
        self.txtY23.setMaximum(999999.989999999990687)

        self.verticalLayout_9.addWidget(self.txtY23)

        self.txtY24 = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.txtY24.setObjectName(u"txtY24")
        self.txtY24.setMaximumSize(QSize(85, 16777215))
        self.txtY24.setDecimals(6)
        self.txtY24.setMinimum(-999999.989999999990687)
        self.txtY24.setMaximum(999999.989999999990687)

        self.verticalLayout_9.addWidget(self.txtY24)

        self.txtY25 = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.txtY25.setObjectName(u"txtY25")
        self.txtY25.setMaximumSize(QSize(85, 16777215))
        self.txtY25.setDecimals(6)
        self.txtY25.setMinimum(-999999.989999999990687)
        self.txtY25.setMaximum(999999.989999999990687)

        self.verticalLayout_9.addWidget(self.txtY25)

        self.txtY26 = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.txtY26.setObjectName(u"txtY26")
        self.txtY26.setMaximumSize(QSize(85, 16777215))
        self.txtY26.setDecimals(6)
        self.txtY26.setMinimum(-999999.989999999990687)
        self.txtY26.setMaximum(999999.989999999990687)

        self.verticalLayout_9.addWidget(self.txtY26)

        self.txtY27 = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.txtY27.setObjectName(u"txtY27")
        self.txtY27.setMaximumSize(QSize(85, 16777215))
        self.txtY27.setDecimals(6)
        self.txtY27.setMinimum(-999999.989999999990687)
        self.txtY27.setMaximum(999999.989999999990687)

        self.verticalLayout_9.addWidget(self.txtY27)

        self.txtY28 = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.txtY28.setObjectName(u"txtY28")
        self.txtY28.setMaximumSize(QSize(85, 16777215))
        self.txtY28.setDecimals(6)
        self.txtY28.setMinimum(-999999.989999999990687)
        self.txtY28.setMaximum(999999.989999999990687)

        self.verticalLayout_9.addWidget(self.txtY28)

        self.txtY29 = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.txtY29.setObjectName(u"txtY29")
        self.txtY29.setMaximumSize(QSize(85, 16777215))
        self.txtY29.setDecimals(6)
        self.txtY29.setMinimum(-999999.989999999990687)
        self.txtY29.setMaximum(999999.989999999990687)

        self.verticalLayout_9.addWidget(self.txtY29)

        self.txtY30 = QDoubleSpinBox(self.verticalLayoutWidget_9)
        self.txtY30.setObjectName(u"txtY30")
        self.txtY30.setMaximumSize(QSize(85, 16777215))
        self.txtY30.setDecimals(6)
        self.txtY30.setMinimum(-999999.989999999990687)
        self.txtY30.setMaximum(999999.989999999990687)

        self.verticalLayout_9.addWidget(self.txtY30)

        self.verticalLayoutWidget_10 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_10.setObjectName(u"verticalLayoutWidget_10")
        self.verticalLayoutWidget_10.setGeometry(QRect(270, 70, 70, 318))
        self.verticalLayout_10 = QVBoxLayout(self.verticalLayoutWidget_10)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_42 = QLabel(self.verticalLayoutWidget_10)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMaximumSize(QSize(16777215, 16777215))
        self.label_42.setFont(font)
        self.label_42.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_10.addWidget(self.label_42)

        self.txtN11 = QLineEdit(self.verticalLayoutWidget_10)
        self.txtN11.setObjectName(u"txtN11")
        self.txtN11.setMinimumSize(QSize(0, 24))

        self.verticalLayout_10.addWidget(self.txtN11)

        self.txtN12 = QLineEdit(self.verticalLayoutWidget_10)
        self.txtN12.setObjectName(u"txtN12")
        self.txtN12.setMinimumSize(QSize(0, 24))
        self.txtN12.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_10.addWidget(self.txtN12)

        self.txtN13 = QLineEdit(self.verticalLayoutWidget_10)
        self.txtN13.setObjectName(u"txtN13")
        self.txtN13.setMinimumSize(QSize(0, 24))
        self.txtN13.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_10.addWidget(self.txtN13)

        self.txtN14 = QLineEdit(self.verticalLayoutWidget_10)
        self.txtN14.setObjectName(u"txtN14")
        self.txtN14.setMinimumSize(QSize(0, 24))
        self.txtN14.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_10.addWidget(self.txtN14)

        self.txtN15 = QLineEdit(self.verticalLayoutWidget_10)
        self.txtN15.setObjectName(u"txtN15")
        self.txtN15.setMinimumSize(QSize(0, 24))
        self.txtN15.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_10.addWidget(self.txtN15)

        self.txtN16 = QLineEdit(self.verticalLayoutWidget_10)
        self.txtN16.setObjectName(u"txtN16")
        self.txtN16.setMinimumSize(QSize(0, 24))
        self.txtN16.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_10.addWidget(self.txtN16)

        self.txtN17 = QLineEdit(self.verticalLayoutWidget_10)
        self.txtN17.setObjectName(u"txtN17")
        self.txtN17.setMinimumSize(QSize(0, 24))
        self.txtN17.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_10.addWidget(self.txtN17)

        self.txtN18 = QLineEdit(self.verticalLayoutWidget_10)
        self.txtN18.setObjectName(u"txtN18")
        self.txtN18.setMinimumSize(QSize(0, 24))
        self.txtN18.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_10.addWidget(self.txtN18)

        self.txtN19 = QLineEdit(self.verticalLayoutWidget_10)
        self.txtN19.setObjectName(u"txtN19")
        self.txtN19.setMinimumSize(QSize(0, 24))
        self.txtN19.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_10.addWidget(self.txtN19)

        self.txtN20 = QLineEdit(self.verticalLayoutWidget_10)
        self.txtN20.setObjectName(u"txtN20")
        self.txtN20.setMinimumSize(QSize(0, 24))
        self.txtN20.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_10.addWidget(self.txtN20)

        self.verticalLayoutWidget_11 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_11.setObjectName(u"verticalLayoutWidget_11")
        self.verticalLayoutWidget_11.setGeometry(QRect(530, 70, 70, 318))
        self.verticalLayout_11 = QVBoxLayout(self.verticalLayoutWidget_11)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_43 = QLabel(self.verticalLayoutWidget_11)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setMaximumSize(QSize(16777215, 16777215))
        self.label_43.setFont(font)
        self.label_43.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_11.addWidget(self.label_43)

        self.txtN21 = QLineEdit(self.verticalLayoutWidget_11)
        self.txtN21.setObjectName(u"txtN21")
        self.txtN21.setMinimumSize(QSize(0, 24))

        self.verticalLayout_11.addWidget(self.txtN21)

        self.txtN22 = QLineEdit(self.verticalLayoutWidget_11)
        self.txtN22.setObjectName(u"txtN22")
        self.txtN22.setMinimumSize(QSize(0, 24))
        self.txtN22.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_11.addWidget(self.txtN22)

        self.txtN23 = QLineEdit(self.verticalLayoutWidget_11)
        self.txtN23.setObjectName(u"txtN23")
        self.txtN23.setMinimumSize(QSize(0, 24))
        self.txtN23.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_11.addWidget(self.txtN23)

        self.txtN24 = QLineEdit(self.verticalLayoutWidget_11)
        self.txtN24.setObjectName(u"txtN24")
        self.txtN24.setMinimumSize(QSize(0, 24))
        self.txtN24.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_11.addWidget(self.txtN24)

        self.txtN25 = QLineEdit(self.verticalLayoutWidget_11)
        self.txtN25.setObjectName(u"txtN25")
        self.txtN25.setMinimumSize(QSize(0, 24))
        self.txtN25.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_11.addWidget(self.txtN25)

        self.txtN26 = QLineEdit(self.verticalLayoutWidget_11)
        self.txtN26.setObjectName(u"txtN26")
        self.txtN26.setMinimumSize(QSize(0, 24))
        self.txtN26.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_11.addWidget(self.txtN26)

        self.txtN27 = QLineEdit(self.verticalLayoutWidget_11)
        self.txtN27.setObjectName(u"txtN27")
        self.txtN27.setMinimumSize(QSize(0, 24))
        self.txtN27.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_11.addWidget(self.txtN27)

        self.txtN28 = QLineEdit(self.verticalLayoutWidget_11)
        self.txtN28.setObjectName(u"txtN28")
        self.txtN28.setMinimumSize(QSize(0, 24))
        self.txtN28.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_11.addWidget(self.txtN28)

        self.txtN29 = QLineEdit(self.verticalLayoutWidget_11)
        self.txtN29.setObjectName(u"txtN29")
        self.txtN29.setMinimumSize(QSize(0, 24))
        self.txtN29.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_11.addWidget(self.txtN29)

        self.txtN30 = QLineEdit(self.verticalLayoutWidget_11)
        self.txtN30.setObjectName(u"txtN30")
        self.txtN30.setMinimumSize(QSize(0, 24))
        self.txtN30.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_11.addWidget(self.txtN30)

        self.verticalLayoutWidget_12 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(790, 70, 70, 318))
        self.verticalLayout_12 = QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_44 = QLabel(self.verticalLayoutWidget_12)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMaximumSize(QSize(16777215, 16777215))
        self.label_44.setFont(font)
        self.label_44.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_12.addWidget(self.label_44)

        self.txtN31 = QLineEdit(self.verticalLayoutWidget_12)
        self.txtN31.setObjectName(u"txtN31")
        self.txtN31.setMinimumSize(QSize(0, 24))

        self.verticalLayout_12.addWidget(self.txtN31)

        self.txtN32 = QLineEdit(self.verticalLayoutWidget_12)
        self.txtN32.setObjectName(u"txtN32")
        self.txtN32.setMinimumSize(QSize(0, 24))
        self.txtN32.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_12.addWidget(self.txtN32)

        self.txtN33 = QLineEdit(self.verticalLayoutWidget_12)
        self.txtN33.setObjectName(u"txtN33")
        self.txtN33.setMinimumSize(QSize(0, 24))
        self.txtN33.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_12.addWidget(self.txtN33)

        self.txtN34 = QLineEdit(self.verticalLayoutWidget_12)
        self.txtN34.setObjectName(u"txtN34")
        self.txtN34.setMinimumSize(QSize(0, 24))
        self.txtN34.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_12.addWidget(self.txtN34)

        self.txtN35 = QLineEdit(self.verticalLayoutWidget_12)
        self.txtN35.setObjectName(u"txtN35")
        self.txtN35.setMinimumSize(QSize(0, 24))
        self.txtN35.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_12.addWidget(self.txtN35)

        self.txtN36 = QLineEdit(self.verticalLayoutWidget_12)
        self.txtN36.setObjectName(u"txtN36")
        self.txtN36.setMinimumSize(QSize(0, 24))
        self.txtN36.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_12.addWidget(self.txtN36)

        self.txtN37 = QLineEdit(self.verticalLayoutWidget_12)
        self.txtN37.setObjectName(u"txtN37")
        self.txtN37.setMinimumSize(QSize(0, 24))
        self.txtN37.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_12.addWidget(self.txtN37)

        self.txtN38 = QLineEdit(self.verticalLayoutWidget_12)
        self.txtN38.setObjectName(u"txtN38")
        self.txtN38.setMinimumSize(QSize(0, 24))
        self.txtN38.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_12.addWidget(self.txtN38)

        self.txtN39 = QLineEdit(self.verticalLayoutWidget_12)
        self.txtN39.setObjectName(u"txtN39")
        self.txtN39.setMinimumSize(QSize(0, 24))
        self.txtN39.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_12.addWidget(self.txtN39)

        self.txtN40 = QLineEdit(self.verticalLayoutWidget_12)
        self.txtN40.setObjectName(u"txtN40")
        self.txtN40.setMinimumSize(QSize(0, 24))
        self.txtN40.setMaximumSize(QSize(16777215, 24))

        self.verticalLayout_12.addWidget(self.txtN40)

        self.verticalLayoutWidget_13 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_13.setObjectName(u"verticalLayoutWidget_13")
        self.verticalLayoutWidget_13.setGeometry(QRect(860, 70, 91, 311))
        self.verticalLayout_13 = QVBoxLayout(self.verticalLayoutWidget_13)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_45 = QLabel(self.verticalLayoutWidget_13)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setMaximumSize(QSize(16777215, 16))
        self.label_45.setFont(font)
        self.label_45.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_13.addWidget(self.label_45)

        self.txtX31 = QDoubleSpinBox(self.verticalLayoutWidget_13)
        self.txtX31.setObjectName(u"txtX31")
        self.txtX31.setMaximumSize(QSize(85, 16777215))
        self.txtX31.setDecimals(6)
        self.txtX31.setMinimum(-999999.989999999990687)
        self.txtX31.setMaximum(999999.989999999990687)

        self.verticalLayout_13.addWidget(self.txtX31)

        self.txtX32 = QDoubleSpinBox(self.verticalLayoutWidget_13)
        self.txtX32.setObjectName(u"txtX32")
        self.txtX32.setMaximumSize(QSize(85, 16777215))
        self.txtX32.setDecimals(6)
        self.txtX32.setMinimum(-999999.989999999990687)
        self.txtX32.setMaximum(999999.989999999990687)

        self.verticalLayout_13.addWidget(self.txtX32)

        self.txtX33 = QDoubleSpinBox(self.verticalLayoutWidget_13)
        self.txtX33.setObjectName(u"txtX33")
        self.txtX33.setMaximumSize(QSize(85, 16777215))
        self.txtX33.setDecimals(6)
        self.txtX33.setMinimum(-999999.989999999990687)
        self.txtX33.setMaximum(999999.989999999990687)

        self.verticalLayout_13.addWidget(self.txtX33)

        self.txtX34 = QDoubleSpinBox(self.verticalLayoutWidget_13)
        self.txtX34.setObjectName(u"txtX34")
        self.txtX34.setMaximumSize(QSize(85, 16777215))
        self.txtX34.setDecimals(6)
        self.txtX34.setMinimum(-999999.989999999990687)
        self.txtX34.setMaximum(999999.989999999990687)

        self.verticalLayout_13.addWidget(self.txtX34)

        self.txtX35 = QDoubleSpinBox(self.verticalLayoutWidget_13)
        self.txtX35.setObjectName(u"txtX35")
        self.txtX35.setMaximumSize(QSize(85, 16777215))
        self.txtX35.setDecimals(6)
        self.txtX35.setMinimum(-999999.989999999990687)
        self.txtX35.setMaximum(999999.989999999990687)

        self.verticalLayout_13.addWidget(self.txtX35)

        self.txtX36 = QDoubleSpinBox(self.verticalLayoutWidget_13)
        self.txtX36.setObjectName(u"txtX36")
        self.txtX36.setMaximumSize(QSize(85, 16777215))
        self.txtX36.setDecimals(6)
        self.txtX36.setMinimum(-999999.989999999990687)
        self.txtX36.setMaximum(999999.989999999990687)

        self.verticalLayout_13.addWidget(self.txtX36)

        self.txtX37 = QDoubleSpinBox(self.verticalLayoutWidget_13)
        self.txtX37.setObjectName(u"txtX37")
        self.txtX37.setMaximumSize(QSize(85, 16777215))
        self.txtX37.setDecimals(6)
        self.txtX37.setMinimum(-999999.989999999990687)
        self.txtX37.setMaximum(999999.989999999990687)

        self.verticalLayout_13.addWidget(self.txtX37)

        self.txtX38 = QDoubleSpinBox(self.verticalLayoutWidget_13)
        self.txtX38.setObjectName(u"txtX38")
        self.txtX38.setMaximumSize(QSize(85, 16777215))
        self.txtX38.setDecimals(6)
        self.txtX38.setMinimum(-999999.989999999990687)
        self.txtX38.setMaximum(999999.989999999990687)

        self.verticalLayout_13.addWidget(self.txtX38)

        self.txtX39 = QDoubleSpinBox(self.verticalLayoutWidget_13)
        self.txtX39.setObjectName(u"txtX39")
        self.txtX39.setMaximumSize(QSize(85, 16777215))
        self.txtX39.setDecimals(6)
        self.txtX39.setMinimum(-999999.989999999990687)
        self.txtX39.setMaximum(999999.989999999990687)

        self.verticalLayout_13.addWidget(self.txtX39)

        self.txtX40 = QDoubleSpinBox(self.verticalLayoutWidget_13)
        self.txtX40.setObjectName(u"txtX40")
        self.txtX40.setMaximumSize(QSize(85, 16777215))
        self.txtX40.setDecimals(6)
        self.txtX40.setMinimum(-999999.989999999990687)
        self.txtX40.setMaximum(999999.989999999990687)

        self.verticalLayout_13.addWidget(self.txtX40)

        self.verticalLayoutWidget_14 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_14.setObjectName(u"verticalLayoutWidget_14")
        self.verticalLayoutWidget_14.setGeometry(QRect(950, 70, 91, 311))
        self.verticalLayout_14 = QVBoxLayout(self.verticalLayoutWidget_14)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.label_46 = QLabel(self.verticalLayoutWidget_14)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMaximumSize(QSize(16777215, 16))
        self.label_46.setFont(font)
        self.label_46.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_14.addWidget(self.label_46)

        self.txtY31 = QDoubleSpinBox(self.verticalLayoutWidget_14)
        self.txtY31.setObjectName(u"txtY31")
        self.txtY31.setMaximumSize(QSize(85, 16777215))
        self.txtY31.setDecimals(6)
        self.txtY31.setMinimum(-999999.989999999990687)
        self.txtY31.setMaximum(999999.989999999990687)

        self.verticalLayout_14.addWidget(self.txtY31)

        self.txtY32 = QDoubleSpinBox(self.verticalLayoutWidget_14)
        self.txtY32.setObjectName(u"txtY32")
        self.txtY32.setMaximumSize(QSize(85, 16777215))
        self.txtY32.setDecimals(6)
        self.txtY32.setMinimum(-999999.989999999990687)
        self.txtY32.setMaximum(999999.989999999990687)

        self.verticalLayout_14.addWidget(self.txtY32)

        self.txtY33 = QDoubleSpinBox(self.verticalLayoutWidget_14)
        self.txtY33.setObjectName(u"txtY33")
        self.txtY33.setMaximumSize(QSize(85, 16777215))
        self.txtY33.setDecimals(6)
        self.txtY33.setMinimum(-999999.989999999990687)
        self.txtY33.setMaximum(999999.989999999990687)

        self.verticalLayout_14.addWidget(self.txtY33)

        self.txtY34 = QDoubleSpinBox(self.verticalLayoutWidget_14)
        self.txtY34.setObjectName(u"txtY34")
        self.txtY34.setMaximumSize(QSize(85, 16777215))
        self.txtY34.setDecimals(6)
        self.txtY34.setMinimum(-999999.989999999990687)
        self.txtY34.setMaximum(999999.989999999990687)

        self.verticalLayout_14.addWidget(self.txtY34)

        self.txtY35 = QDoubleSpinBox(self.verticalLayoutWidget_14)
        self.txtY35.setObjectName(u"txtY35")
        self.txtY35.setMaximumSize(QSize(85, 16777215))
        self.txtY35.setDecimals(6)
        self.txtY35.setMinimum(-999999.989999999990687)
        self.txtY35.setMaximum(999999.989999999990687)

        self.verticalLayout_14.addWidget(self.txtY35)

        self.txtY36 = QDoubleSpinBox(self.verticalLayoutWidget_14)
        self.txtY36.setObjectName(u"txtY36")
        self.txtY36.setMaximumSize(QSize(85, 16777215))
        self.txtY36.setDecimals(6)
        self.txtY36.setMinimum(-999999.989999999990687)
        self.txtY36.setMaximum(999999.989999999990687)

        self.verticalLayout_14.addWidget(self.txtY36)

        self.txtY37 = QDoubleSpinBox(self.verticalLayoutWidget_14)
        self.txtY37.setObjectName(u"txtY37")
        self.txtY37.setMaximumSize(QSize(85, 16777215))
        self.txtY37.setDecimals(6)
        self.txtY37.setMinimum(-999999.989999999990687)
        self.txtY37.setMaximum(999999.989999999990687)

        self.verticalLayout_14.addWidget(self.txtY37)

        self.txtY38 = QDoubleSpinBox(self.verticalLayoutWidget_14)
        self.txtY38.setObjectName(u"txtY38")
        self.txtY38.setMaximumSize(QSize(85, 16777215))
        self.txtY38.setDecimals(6)
        self.txtY38.setMinimum(-999999.989999999990687)
        self.txtY38.setMaximum(999999.989999999990687)

        self.verticalLayout_14.addWidget(self.txtY38)

        self.txtY39 = QDoubleSpinBox(self.verticalLayoutWidget_14)
        self.txtY39.setObjectName(u"txtY39")
        self.txtY39.setMaximumSize(QSize(85, 16777215))
        self.txtY39.setDecimals(6)
        self.txtY39.setMinimum(-999999.989999999990687)
        self.txtY39.setMaximum(999999.989999999990687)

        self.verticalLayout_14.addWidget(self.txtY39)

        self.txtY40 = QDoubleSpinBox(self.verticalLayoutWidget_14)
        self.txtY40.setObjectName(u"txtY40")
        self.txtY40.setMaximumSize(QSize(85, 16777215))
        self.txtY40.setDecimals(6)
        self.txtY40.setMinimum(-999999.989999999990687)
        self.txtY40.setMaximum(999999.989999999990687)

        self.verticalLayout_14.addWidget(self.txtY40)

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
        self.label_41.setText(QCoreApplication.translate("ModulesWindow", u"Modules", None))
        self.txtN1.setText(QCoreApplication.translate("ModulesWindow", u"Module_1", None))
        self.txtN2.setText(QCoreApplication.translate("ModulesWindow", u"Module_2", None))
        self.txtN3.setText(QCoreApplication.translate("ModulesWindow", u"Module_3", None))
        self.txtN4.setText(QCoreApplication.translate("ModulesWindow", u"Module_4", None))
        self.txtN5.setText(QCoreApplication.translate("ModulesWindow", u"Module_5", None))
        self.txtN6.setText(QCoreApplication.translate("ModulesWindow", u"Module_6", None))
        self.txtN7.setText(QCoreApplication.translate("ModulesWindow", u"Module_7", None))
        self.txtN8.setText(QCoreApplication.translate("ModulesWindow", u"Module_8", None))
        self.txtN9.setText(QCoreApplication.translate("ModulesWindow", u"Module_9", None))
        self.txtN10.setText(QCoreApplication.translate("ModulesWindow", u"Module_10", None))
        self.label_4.setText(QCoreApplication.translate("ModulesWindow", u"X(um)", None))
        self.label_27.setText(QCoreApplication.translate("ModulesWindow", u"Y(um)", None))
        self.label_39.setText(QCoreApplication.translate("ModulesWindow", u"X(um)", None))
        self.label_40.setText(QCoreApplication.translate("ModulesWindow", u"Y(um)", None))
        self.label_42.setText(QCoreApplication.translate("ModulesWindow", u"Modules", None))
        self.txtN11.setText(QCoreApplication.translate("ModulesWindow", u"Module_11", None))
        self.txtN12.setText(QCoreApplication.translate("ModulesWindow", u"Module_12", None))
        self.txtN13.setText(QCoreApplication.translate("ModulesWindow", u"Module_13", None))
        self.txtN14.setText(QCoreApplication.translate("ModulesWindow", u"Module_14", None))
        self.txtN15.setText(QCoreApplication.translate("ModulesWindow", u"Module_15", None))
        self.txtN16.setText(QCoreApplication.translate("ModulesWindow", u"Module_16", None))
        self.txtN17.setText(QCoreApplication.translate("ModulesWindow", u"Module_17", None))
        self.txtN18.setText(QCoreApplication.translate("ModulesWindow", u"Module_18", None))
        self.txtN19.setText(QCoreApplication.translate("ModulesWindow", u"Module_19", None))
        self.txtN20.setText(QCoreApplication.translate("ModulesWindow", u"Module_20", None))
        self.label_43.setText(QCoreApplication.translate("ModulesWindow", u"Modules", None))
        self.txtN21.setText(QCoreApplication.translate("ModulesWindow", u"Module_21", None))
        self.txtN22.setText(QCoreApplication.translate("ModulesWindow", u"Module_22", None))
        self.txtN23.setText(QCoreApplication.translate("ModulesWindow", u"Module_23", None))
        self.txtN24.setText(QCoreApplication.translate("ModulesWindow", u"Module_24", None))
        self.txtN25.setText(QCoreApplication.translate("ModulesWindow", u"Module_25", None))
        self.txtN26.setText(QCoreApplication.translate("ModulesWindow", u"Module_26", None))
        self.txtN27.setText(QCoreApplication.translate("ModulesWindow", u"Module_27", None))
        self.txtN28.setText(QCoreApplication.translate("ModulesWindow", u"Module_28", None))
        self.txtN29.setText(QCoreApplication.translate("ModulesWindow", u"Module_29", None))
        self.txtN30.setText(QCoreApplication.translate("ModulesWindow", u"Module_30", None))
        self.label_44.setText(QCoreApplication.translate("ModulesWindow", u"Modules", None))
        self.txtN31.setText(QCoreApplication.translate("ModulesWindow", u"Module_31", None))
        self.txtN32.setText(QCoreApplication.translate("ModulesWindow", u"Module_32", None))
        self.txtN33.setText(QCoreApplication.translate("ModulesWindow", u"Module_33", None))
        self.txtN34.setText(QCoreApplication.translate("ModulesWindow", u"Module_34", None))
        self.txtN35.setText(QCoreApplication.translate("ModulesWindow", u"Module_35", None))
        self.txtN36.setText(QCoreApplication.translate("ModulesWindow", u"Module_36", None))
        self.txtN37.setText(QCoreApplication.translate("ModulesWindow", u"Module_37", None))
        self.txtN38.setText(QCoreApplication.translate("ModulesWindow", u"Module_38", None))
        self.txtN39.setText(QCoreApplication.translate("ModulesWindow", u"Module_39", None))
        self.txtN40.setText(QCoreApplication.translate("ModulesWindow", u"Module_40", None))
        self.label_45.setText(QCoreApplication.translate("ModulesWindow", u"X(um)", None))
        self.label_46.setText(QCoreApplication.translate("ModulesWindow", u"Y(um)", None))
    # retranslateUi

