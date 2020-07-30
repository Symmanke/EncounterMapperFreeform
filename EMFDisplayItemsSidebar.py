"""
Encounter Mapper Freeform is a node-based encounter map creator for tabletop
RPGs. Copyright 2020 Eric Symmank

This file is part of Encounter Mapper Freeform.

Encounter Mapper Freeform is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

Encounter Mapper Freeform is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Encounter Mapper Freeform.
If not, see <https://www.gnu.org/licenses/>.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton,
                             QListWidget, QGridLayout, QFrame, QSplitter,
                             QVBoxLayout, QDialog)
from DisplayItemPicker import DisplayItemPicker
from DisplayAttributeList import DisplayAttributeList


class DisplayItemSidebar(QFrame):
    def __init__(self, map=None):
        super(DisplayItemSidebar, self).__init__()
        self.diList = DisplayItemList(map)
        self.diAttributes = DisplayAttributeList(map)
        self.splitter = QSplitter(Qt.Vertical)

        self.splitter.addWidget(self.diList)
        self.splitter.addWidget(self.diAttributes)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)


class DisplayItemList(QFrame):

    def __init__(self, map):
        super(DisplayItemList, self).__init__()
        self.map = map
        self.map.displayItemsUpdated.connect(self.updateDIList)
        self.diEditor = None
        self.diDialog = None
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.updateCurrentDI)

        self.upBtn = QPushButton("up")
        self.upBtn.clicked.connect(self.shiftItemUp)
        self.downBtn = QPushButton("down")
        self.downBtn.clicked.connect(self.shiftItemDown)
        self.addBtn = QPushButton("new")
        self.addBtn.clicked.connect(self.openDIEdit)
        self.delBtn = QPushButton("del")
        self.delBtn.clicked.connect(self.removeSelectedDI)
        self.selAllBtn = QPushButton("Select All")
        self.selAllBtn.clicked.connect(self.selectFromDI)
        self.addSelBtn = QPushButton("Add to Selection")
        self.addSelBtn.clicked.connect(self.addDIToSelection)
        self.delSelBtn = QPushButton("Remove From Selection")
        self.delSelBtn.clicked.connect(self.removeDIFromSelection)

        layout = QGridLayout()
        layout.addWidget(QLabel("Display Items:"), 0, 0, 1, 2)
        layout.addWidget(self.listWidget, 1, 0, 1, 2)
        layout.addWidget(self.upBtn, 2, 0)
        layout.addWidget(self.downBtn, 2, 1)
        layout.addWidget(self.addBtn, 3, 0)
        layout.addWidget(self.delBtn, 3, 1)
        layout.addWidget(self.addSelBtn, 4, 0)
        layout.addWidget(self.delSelBtn, 4, 1)

        self.setLayout(layout)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)

    def updateDIList(self):
        self.listWidget.clear()
        for di in self.map.getDisplayItems():
            self.listWidget.addItem(di.getName())
        self.listWidget.setCurrentRow(self.map.getSelectedDIIndex())
        self.listWidget.repaint()

    def shiftItemUp(self):
        index = self.listWidget.currentRow()
        if index > 0:
            self.map.shiftDisplayItem(index, True)

    def shiftItemDown(self):
        index = self.listWidget.currentRow()
        if index > -1:
            self.map.shiftDisplayItem(index, False)

    def updateCurrentDI(self):
        self.map.setSelectedDI(self.listWidget.currentRow())

    def selectFromDI(self):
        di = self.map.getSelectedDI()
        if di is not None:
            self.map.selectItemsFromDI(di)

    def addDIToSelection(self):
        cr = self.listWidget.currentRow()
        if cr >= 0:
            self.map.applyDIToSelection(self.map.getDisplayItem(cr))

    def removeDIFromSelection(self):
        cr = self.listWidget.currentRow()
        if cr >= 0:
            di = self.map.getDisplayItem(cr)
            for item in self.map.getSelectedItems():
                item.removeDI(di)

    def removeSelectedDI(self):
        cr = self.listWidget.currentRow()
        if cr >= 0:
            self.map.removeDisplayItem(self.map.getDisplayItem(cr))

    def openDIEdit(self):
        self.diDialog = QDialog()
        layout = QVBoxLayout()

        self.diEditor = DisplayItemPicker()
        self.diEditor.acceptedAction.connect(self.applyDIEdit)
        self.diEditor.cancelledAction.connect(self.cancelDIEdit)

        layout.addWidget(self.diEditor)
        self.diDialog.setLayout(layout)
        self.diDialog.exec_()

    def applyDIEdit(self):
        self.map.addDisplayItem(self.diEditor.getSelectedDI(self.map))
        # self.displayItems.append()
        self.diDialog.close()
        self.diDialog = None
        self.diEditor = None
        self.updateDIList()
        # self.diSelectionChanged.emit()

    def cancelDIEdit(self):
        self.diDialog.close()
        self.diDialog = None
        self.diEditor = None


def main():
    app = QApplication([])
    mainWidget = DisplayItemSidebar()
    mainWidget.show()
    app.exec_()


if __name__ == "__main__":
    main()
