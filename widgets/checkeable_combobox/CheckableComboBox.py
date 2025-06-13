from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class CheckableComboBox(QComboBox):
    def __init__(self, layout):
        super().__init__()
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.closeOnLineEditClick = False

        self.lineEdit().installEventFilter(self)

        self.view().viewport().installEventFilter(self)

        self.model().dataChanged.connect(self.updateLineEditField)

        self.lineEdit().setText('')


    def eventFilter(self, widget, event):
        if widget == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True

            return super().eventFilter(widget, event)

        if widget == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                indx = self.view().indexAt(event.pos())
                item = self.model().item(indx.row())
                # All parameters, All wafers, All runs, ...
                if "All " in item.text():
                    estado = Qt.Checked
                    for i in range (self.model().rowCount()):
                        item_check = self.model().item(i)
                        if "All " not in item_check.text():
                            if item_check.checkState() == Qt.Checked:
                                estado = Qt.Unchecked
                    for i in range (self.model().rowCount()):
                        item_check = self.model().item(i)
                        if "All " not in item_check.text():
                            item_check.setCheckState(estado)


                else:
                    if item.checkState() == Qt.Checked:
                        item.setCheckState(Qt.Unchecked)
                    else:
                        item.setCheckState(Qt.Checked)
                return True
            return super().eventFilter(widget, event)            

    
    def hidePopup(self):
        super().hidePopup()
        self.startTimer(100)


    def addItems(self, items, itemList=None):
        self.clear() # clear all before add items
        for indx, text in enumerate(items):
            try:
                data = itemList[indx]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)
        # clear lineEdit after addItems
        self.lineEdit().setText('')

    def addItem(self, text, userData=None):
        item = QStandardItem()
        item.setText(text)
        if not userData is None:
            item.setData(userData)

        # enable checkbox setting
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)


    def updateLineEditField(self):
        text_container = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                text_container.append(self.model().item(i).text())

        text_string = ', '.join(text_container)
        self.lineEdit().setText(text_string)

    def itemsChecked(self):
        itemsChecked = 0
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                itemsChecked += 1
        return itemsChecked