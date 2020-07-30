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
from PyQt5.QtCore import pyqtSignal, QObject


from EMFNodes import NodeLayer, EMFNode, EMFLine, EMFShape


class EMFMap(QObject):

    selectionUpdated = pyqtSignal()
    layerUpdated = pyqtSignal()
    displayItemsUpdated = pyqtSignal()
    selectedDIUpdated = pyqtSignal()

    CLASS_TO_TYPE = {
        NodeLayer: "NONE",
        EMFNode: NodeLayer.TYPE_NODE,
        EMFLine: NodeLayer.TYPE_LINE,
        EMFShape: NodeLayer.TYPE_SHAPE
    }

    def __init__(self, width=600, height=400):
        super(EMFMap, self).__init__()
        # Node Layers, Nodes, Lines
        self.nodeLayers = [NodeLayer(width, height)]
        self.currentLayer = 0

        self.selectedItems = []

        # DIs
        self.displayItems = []
        self.selectedDI = -1

    # ////////////////////////////// #
    # Node and Layer Element Methods #
    # ////////////////////////////// #

    def addItemsToCurrentLayer(self, type, items):
        self.nodeLayers[self.currentLayer].addItemsToLayer(type, items)

    def addItemToCurrentLayer(self, type, item):
        self.nodeLayers[self.currentLayer].addItemToLayer(type, item)

    def removeItemFromCurrentLayer(self, type, item):
        self.nodeLayers[self.currentLayer].removeFromLayer(type, item)

    def addItemsToSelection(self, items):
        for item in items:
            self.addItemToSelection(item, False)
        self.selectionUpdated.emit()

    def addItemToSelection(self, item, emitSignal=True):
        if item not in self.selectedItems:
            self.selectedItems.append(item)
        if emitSignal:
            self.selectionUpdated.emit()

    def selectItemsFromDI(self, di):
        newSelection = []
        listType = EMFMap.CLASS_TO_TYPE[di.getAllowedClass]
        if listType in self.nodeLayers:
            newSelection = list(set(di.getPropertyItems()).intersection(
                self.nodeLayers[listType]))
        self.setSelectedItems(newSelection)

    def setSelectedItems(self, items):
        self.selectedItems.clear()
        self.selectedItems.extend(items)
        self.selectionUpdated.emit()

    def clearSelectedItems(self):
        self.selectedItems.clear()
        self.selectionUpdated.emit()

    def removeSelectedItem(self, item):
        if item in self.selectedItems:
            self.selectedItems.remove(item)
            self.selectionUpdated.emit()

    def getSelectedItems(self):
        return self.selectedItems

    def getCurrentLayer(self):
        return self.nodeLayers[self.currentLayer]

    def getCurrentLayerItems(self, type):
        return self.nodeLayers[self.currentLayer].getList(type)

    # /////////////////////////////// #
    # Display Item Management Methods #
    # /////////////////////////////// #

    def diUpdated(self):
        self.displayItemsUpdated.emit()

    def getDisplayItems(self):
        return self.displayItems

    def getSelectedDI(self):
        di = None
        if self.selectedDI > 0:
            di = self.displayItems[self.selectedDI]
        return di

    def setSelectedDI(self, index):
        self.selectedDI = index

    def getSelectedDIIndex(self):
        return self.selectedDI

    def getDisplayItem(self, index):
        return self.displayItems[index]

    def getDisplayItemsFromSelection(self):
        dis = set(self.nodeLayers[self.currentLayer].currentDIs())
        for item in self.selectedItems:
            dis = dis.union(item.currentDIs())
        return dis

    def addDisplayItem(self, di):
        if di not in self.displayItems:
            self.displayItems.append(di)
            di.setMap(self)
            self.selectedDI = len(self.displayItems) - 1

    def applyDIToSelection(self, di):
        if di.getAllowedClass() == NodeLayer:
            di.addItem(self.nodeLayers[self.currentLayer])
        else:
            di.addItems(self.selectedItems)
        self.displayItemsUpdated.emit()

    def removeDisplayItem(self, di):
        if di in self.displayItems:
            di.removeAllItems()
            self.displayItems.remove(di)
            self.selectedDI = -1
            self.displayItemsUpdated.emit()

    def shiftDisplayItem(self, index, shiftUp):
        if shiftUp:
            if index > 0:
                shift = self.displayItems[index]
                self.displayItems[index] = self.displayItems[index-1]
                self.displayItems[index-1] = shift
                self.selectedDI = index - 1
                self.displayItemsUpdated.emit()
        else:
            if index > -1 and index != len(self.displayItems)-1:
                shift = self.displayItems[index]
                self.displayItems[index] = self.displayItems[index+1]
                self.displayItems[index+1] = shift
                self.selectedDI = index + 1
                self.displayItemsUpdated.emit()

    def getLayerImages(self):
        layerImgList = []
        for i in range(self.currentLayer):
            img = self.nodeLayers[i].getLayerImage()
            if img is None or i == self.currentLayer:
                img = self.nodeLayers[i].redrawLayerImage(self.displayItems)
            layerImgList.append(img)
        return layerImgList
