from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QListWidget, QLabel, QListWidgetItem)
from EMFDisplayProperty import EMFDisplayItemWidget


class DisplayAttributeList(QListWidget):
    def __init__(self, map):
        super(DisplayAttributeList, self).__init__()
        self.map = map
        self.map.selectionUpdated.connect(self.updateDisplayedDIWS)
        self.map.displayItemListUpdated.connect(self.updateDisplayedDIWS)
        self.selectedListDI = None

        self.updateDisplayedDIWS()

    def setMap(self, map):
        self.map = map
        self.map.selectionUpdated.connect(self.updateDisplayedDIWS)
        self.map.displayItemListUpdated.connect(self.updateDisplayedDIWS)
        self.updateDisplayedDIWS()

    def updateDisplayedDIWS(self):
        self.clear()

        def addWidgetToList(widget):
            listItem = QListWidgetItem(self)
            listItem.setSizeHint(widget.sizeHint())
            listItem.setFlags(Qt.NoItemFlags)

            self.addItem(listItem)
            self.setItemWidget(listItem, widget)

        selDI = self.map.getSelectedDI()

        if selDI is not None:
            addWidgetToList(QLabel("Selected Display Item:"))
            addWidgetToList(EMFDisplayItemWidget(selDI))

        dis = list(self.map.getDisplayItemsFromSelection())
        if len(dis) > 0:
            addWidgetToList(QLabel("Active Display Items:"))
            for di in dis:
                addWidgetToList(EMFDisplayItemWidget(di))

    def setSelectedDI(self, di):
        self.selectedListDI = di
        self.updateDisplayedDIWS()
