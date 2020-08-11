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
from PyQt5.QtGui import QPalette

from EMFNodes import NodeLayer


# Display the full set of attributes and their values if possible for an
# EMFDisplayItem
class EMFDisplayItemWidget(QFrame):

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
        self.parentMap = None
        self.allowedClassItems = allowedClass
        self.propertyItems = []
        self.sharedAttributes = {}
        self.individualAttributes = {}

    def setMap(self, map):
        self.parentMap = map

    def addItems(self, items):
        for item in items:
            self.addItem(item)

    def addItem(self, item):
        if (isinstance(item, self.allowedClassItems) and
                item not in self.propertyItems):
            self.propertyItems.append(item)
            item.addIndividualAttributes(self)

    def removeAllItems(self):
        for item in self.propertyItems:
            item.removeDI(self)

    def removeItem(self, item):
        if item in self.propertyItems:
            self.propertyItems.remove(item)

    def getAllowedClass(self):
        return self.allowedClassItems

    def getPropertyItems(self):
        return self.propertyItems

    def getSharedAttributes(self):
        return self.sharedAttributes

    def getIndividualAttributes(self):
        return self.individualAttributes

    def getName(self):
        return self.name

    def valueUpdated(self, attrName):
        if attrName in self.individualAttributes:
            if self.allowedClassItems == NodeLayer:
                curLayer = self.parentMap.getCurrentLayer()
                if curLayer in self.propertyItems:
                    curLayer.updateAttribute(
                        self, self.individualAttributes[attrName])
            else:
                selectedItems = self.parentMap.getSelectedItems()
                itemSet = set(selectedItems).intersection(self.propertyItems)
                for item in itemSet:
                    item.updateAttribute(self,
                                         self.individualAttributes[attrName])

        self.parentMap.diUpdated()

    def drawDisplay(self, painter, layer, simple=True):
        drawMethod = self.drawSimple if simple else self.drawComplex
        for item in self.propertyItems:
            drawMethod(painter, item)

    # draw the simple representation, which is easier to process
    def drawSimple(self, painter, item):
        print("Need to implement!")

    # draw the complete representation, which may take time to process
    def drawComplex(self, painter, item):
        self.drawSimple(self, painter, item)

    def jsonObj(self):
        shared = {}
        for sKey in self.sharedAttributes:
            shared[sKey] = self.sharedAttributes[sKey].getJSONValue()
        indiv = {}
        for iKey in self.individualAttributes:
            indiv[iKey] = self.individualAttributes[iKey].getJSONValue()
        return {
            "name": self.name,
            "sharedAttributes": shared,
            "individualAttributes": indiv,
            "class": self.classStr()

        }
