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
from PyQt5.QtWidgets import (QApplication, QLabel,
                             QPushButton, QScrollArea,
                             QListWidget, QGridLayout, QFrame, QSplitter,
                             QVBoxLayout, QDialog)
from EMFDisplayProperty import EMFDisplayItemWidget
from EMFNodeDisplayItems import ColorCircleDisplay, ImageDisplay
from DisplayItemPicker import DisplayItemPicker


class DisplayItemSidebar(QFrame):
    def __init__(self):
        super(DisplayItemSidebar, self).__init__()
        self.diList = DisplayItemList()
        self.diAttributes = DisplayAttributeList()
        attributescroll = QScrollArea()
        attributescroll.setAlignment(Qt.AlignCenter)
        attributescroll.setWidget(self.diAttributes)
        self.splitter = QSplitter(Qt.Vertical)

        self.splitter.addWidget(self.diList)
        self.splitter.addWidget(attributescroll)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)


class DisplayItemList(QFrame):
    def __init__(self):
        super(DisplayItemList, self).__init__()
        self.displayItems = []
        self.diEditor = None
        self.diDialog = None
        self.listWidget = QListWidget()

        self.upBtn = QPushButton("up")
        self.downBtn = QPushButton("down")
        self.addBtn = QPushButton("add")
        self.addBtn.clicked.connect(self.openDIEdit)
        self.delBtn = QPushButton("del")

        layout = QGridLayout()
        layout.addWidget(QLabel("Display Items:"), 0, 0, 1, 2)
        layout.addWidget(self.listWidget, 1, 0, 1, 2)
        layout.addWidget(self.upBtn, 2, 0)
        layout.addWidget(self.downBtn, 2, 1)
        layout.addWidget(self.addBtn, 3, 0)
        layout.addWidget(self.delBtn, 3, 1)

        self.setLayout(layout)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)

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
        self.selectedColor = self.diEditor.getCurrentColor()
        self.diDialog.close()
        self.diDialog = None
        self.diEditor = None

        self.setPreview(self.selectedColor)
        self.updateValue(self.selectedColor)

    def cancelDIEdit(self):
        self.diDialog.close()
        self.diDialog = None
        self.diEditor = None


# Display the EMFDisplayItemWidget for each selected DisplayItem.
class DisplayAttributeList(QFrame):
    def __init__(self):
        super(DisplayAttributeList, self).__init__()
        self.diws = [EMFDisplayItemWidget(ColorCircleDisplay("Test 1")),
                     EMFDisplayItemWidget(ImageDisplay("Hello"))]
        self.updateDisplayedDIWS()

    def updateDisplayedDIWS(self):
        layout = QVBoxLayout()

        for diw in self.diws:
            layout.addWidget(diw)
        self.setLayout(layout)


def main():
    app = QApplication([])
    mainWidget = DisplayItemSidebar()
    mainWidget.show()
    app.exec_()


if __name__ == "__main__":
    main()
