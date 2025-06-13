# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plotpLyegK.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from pyqtgraph import PlotWidget


class Ui_PlotWindow(object):
    def setupUi(self, PlotWindow):
        if not PlotWindow.objectName():
            PlotWindow.setObjectName(u"PlotWindow")
        PlotWindow.resize(740, 600)
        PlotWindow.setMinimumSize(QSize(740, 600))
        PlotWindow.setMaximumSize(QSize(740, 600))
        PlotWindow.setStyleSheet(u"background-color: #FFFFFF;")
        self.centralwidget = QWidget(PlotWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMaximumSize(QSize(740, 16777215))
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 722, 581))
        self.gridLayout = QGridLayout(self.horizontalLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.plot_widget = PlotWidget(self.horizontalLayoutWidget)
        self.plot_widget.setObjectName(u"plot_widget")
        self.plot_widget.setMinimumSize(QSize(720, 570))
        self.plot_widget.setMaximumSize(QSize(720, 570))

        self.gridLayout.addWidget(self.plot_widget, 0, 0, 1, 1)

        PlotWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PlotWindow)

        QMetaObject.connectSlotsByName(PlotWindow)
    # setupUi

    def retranslateUi(self, PlotWindow):
        PlotWindow.setWindowTitle(QCoreApplication.translate("PlotWindow", u"Plot Window", None))
    # retranslateUi

