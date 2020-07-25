from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QListWidget, QLabel, QListWidgetItem)
from EMFDisplayProperty import EMFDisplayItemWidget


class DisplayAttributeList(QListWidget):
    def __init__(self):
        super(DisplayAttributeList, self).__init__()
        self.selectedListDI = None
        self.dis = []

        self.updateDisplayedDIWS()

    def updateDisplayedDIWS(self):
        self.clear()

        def addWidgetToList(widget):
            listItem = QListWidgetItem(self)
            listItem.setSizeHint(widget.sizeHint())
            listItem.setFlags(Qt.NoItemFlags)

            self.addItem(listItem)
            self.setItemWidget(listItem, widget)

        if self.selectedListDI is not None:
            addWidgetToList(QLabel("Selected Display Item:"))
            addWidgetToList(EMFDisplayItemWidget(self.selectedListDI))
        if len(self.dis) > 0:
            addWidgetToList(QLabel("Active Display Items:"))
            for di in self.dis:
                addWidgetToList(EMFDisplayItemWidget(di))

    def setSelectedDI(self, di):
        self.selectedListDI = di
        self.updateDisplayedDIWS()
