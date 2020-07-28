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

from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPalette


# Display the full set of attributes and their values if possible for an
# EMFDisplayItem
class EMFDisplayItemWidget(QFrame):
    # displayItemUpdated = pyqtSignal()

    def __init__(self, displayItem):
        super(EMFDisplayItemWidget, self).__init__()
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setBackgroundRole(QPalette.Window)
        self.displayItem = displayItem
        layout = QGridLayout()
        layout.addWidget(QLabel(self.displayItem.getName()), 0, 0, 1, 2)
        layout.addWidget(QLabel("---SHARED---"), 1, 0, 1, 2)
        curRow = 2
        shared = self.displayItem.getSharedAttributes()
        for key in shared:
            layout.addWidget(QLabel(key), curRow, 0)
            attr = shared[key]
            widget = attr.widgetClass()(attr, attr.widgetParams)
            widget.attributeChanged.connect(self.updateAttribute)
            layout.addWidget(widget, curRow, 1)
            curRow += 1
        indiv = self.displayItem.getIndividualAttributes()
        layout.addWidget(QLabel("--INDIVIDUAL--"), curRow, 0, 1, 2)
        curRow += 1
        for key in indiv:
            layout.addWidget(QLabel(key), curRow, 0)
            attr = indiv[key]
            widget = attr.widgetClass()(attr, attr.widgetParams)
            widget.attributeChanged.connect(self.updateAttribute)
            layout.addWidget(widget, curRow, 1)
            curRow += 1

        self.setAutoFillBackground(True)
        self.setLayout(layout)

    def updateAttribute(self):
        pass


# Display item for the grid. Can be added to a Line, Shape, or Node.
# Contains methods for drawing both a simplified version while editing, as
# well as a more complex version.
# Each DisplayItem has attributes. Some attributes will be shared by all,
# While
class EMFDisplayItem:
    def __init__(self, name, allowedClass):
        self.name = name
        self.allowedClassItems = allowedClass
        self.propertyItems = []
        self.sharedAttributes = {}
        self.individualAttributes = {}

    def addItems(self, items):
        for item in items:
            self.addItem(item)

    def addItem(self, item):
        if item not in self.propertyItems:
            self.propertyItems.append(item)
            item.addIndividualAttributes(self)
            print("Property Added!")

    def getAllowedClass(self):
        return self.allowedClassItems

    def getSharedAttributes(self):
        return self.sharedAttributes

    def getIndividualAttributes(self):
        return self.individualAttributes

    def getName(self):
        return self.name

    def valueUpdated(self, attrName):
        if attrName in self.individualAttributes:
            for item in self.propertyItems:
                item.updateAttribute(self, self.individualAttributes[attrName])

    def drawDisplay(self, painter, layer, simple=True):
        print(type(self))
        drawMethod = self.drawSimple if simple else self.drawComplex
        for item in self.propertyItems:
            drawMethod(painter, item)

    # draw the simple representation, which is easier to process
    def drawSimple(self, painter, item):
        print("Need to implement!")

    # draw the complete representation, which may take time to process
    def drawComplex(self, painter, item):
        self.drawSimple(self, painter, item)
