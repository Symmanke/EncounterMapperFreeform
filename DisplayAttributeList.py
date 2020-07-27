from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QListWidget, QLabel, QListWidgetItem)
from EMFDisplayProperty import EMFDisplayItemWidget


class DisplayAttributeList(QListWidget):
    def __init__(self, editor):
        super(DisplayAttributeList, self).__init__()
        self.nodeEditor = editor
        self.nodeEditor.selectedItemsUpdated.connect(
            self.updateDisplayedDIWS)
        self.nodeEditor.selectTypeSwitched.connect(
            self.updateDisplayedDIWS)
        self.selectedListDI = None

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

        dis = list(self.nodeEditor.getCurrentDIs())
        if len(dis) > 0:
            addWidgetToList(QLabel("Active Display Items:"))
            for di in dis:
                addWidgetToList(EMFDisplayItemWidget(di))

    def setSelectedDI(self, di):
        self.selectedListDI = di
        self.updateDisplayedDIWS()
