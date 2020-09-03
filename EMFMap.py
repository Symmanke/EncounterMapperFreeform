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

from DisplayItemPicker import DisplayItemPicker
from EMFNodes import NodeLayer, EMFNode, EMFLine, EMFShape
import copy

"""
EMFMap contains all the necessary data for an encounter map. It has a series
of NodeLayers, each with their own EMFNodes, EMFLines, and EMFShapes, as well
as an array of DIProperties. EMFMap contains functionality to interact with
each of these elements as well.

EMFMap contains a variety of pyqtSignals that are fired off whenever a property
is changed. These should be added to the EMFNodeEditor and
 EMFDisplayItemsSidebar to make sure all elements are properly updating
"""


class EMFMap(QObject):

    selectionUpdated = pyqtSignal()
    mapLayerSwitched = pyqtSignal()
    displayItemListUpdated = pyqtSignal()
    displayItemValuesUpdated = pyqtSignal()
    selectedDIUpdated = pyqtSignal()
    mapResized = pyqtSignal()

    CLASS_TO_TYPE = {
        NodeLayer: "NONE",
        EMFNode: NodeLayer.TYPE_NODE,
        EMFLine: NodeLayer.TYPE_LINE,
        EMFShape: NodeLayer.TYPE_SHAPE
    }

    def __init__(self, width=600, height=400, layers=None, displayItems=None,
                 currentLayer=0, selectedDI=-1):
        super(EMFMap, self).__init__()
        # Node Layers, Nodes, Lines
        self.width = width
        self.height = height
        self.nodeLayers = ([NodeLayer(width*72, height*72)] if layers is None
                           else layers)
        self.currentLayer = currentLayer

        self.selectedItems = []

        # DIs
        self.displayItems = [] if displayItems is None else displayItems
        for di in self.displayItems:
            di.setMap(self)
        self.selectedDI = selectedDI

    # Load map from a json representation.
    @classmethod
    def createMapFromJSON(cls, jsContents):
        displayItems = []
        # Do things to populate those items
        for dijs in jsContents["DisplayItems"]:
            displayItems.append(DisplayItemPicker.diFromJSON(dijs))
        width = jsContents["Width"] * 72
        height = jsContents["Height"] * 72
        layers = []
        for layerContent in jsContents["Layers"]:
            layers.append(NodeLayer.createFromJSON(
                layerContent, displayItems,
                width, height))

        return cls(jsContents["Width"], jsContents["Height"],
                   layers, displayItems, jsContents["CurrentLayer"],
                   jsContents["SelectedDI"])

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setMapDimensions(self, width, height, xOff, yOff):
        for layer in self.nodeLayers:
            layer.setLayerDimensions(width*72, height*72, xOff * 72, yOff * 72)
        self.width = width
        self.height = height
        self.mapResized.emit()

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

    # Given a DisplayItem, select the elements in the current layer
    # that are part of the DI
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

    def getNumLayers(self):
        return len(self.nodeLayers)

    def getCurrentLayerIndex(self):
        return self.currentLayer

    def getCurrentLayer(self):
        return self.nodeLayers[self.currentLayer]

    def getCurrentLayerItems(self, type):
        return self.nodeLayers[self.currentLayer].getList(type)

    # //////////////////////////// #
    # Map Layer Management Methods #
    # //////////////////////////// #

    def addNewLayer(self):
        self.nodeLayers.insert(self.currentLayer+1,
                               NodeLayer(self.width*72, self.height*72))
        self.currentLayer += 1
        self.mapLayerSwitched.emit()

    def changeLayerUp(self):
        if self.currentLayer < len(self.nodeLayers):
            self.currentLayer += 1
            self.mapLayerSwitched.emit()

    def changeLayerDown(self):
        if self.currentLayer > 0:
            self.currentLayer -= 1
            self.mapLayerSwitched.emit()

    def shiftCurrentLayer(self, shiftUp):
        index = self.currentLayer
        if shiftUp:
            if index > -1 and index != len(self.displayItems)-1:
                shift = self.nodeLayers[index]
                self.nodeLayers[index] = self.nodeLayers[index+1]
                self.nodeLayers[index+1] = shift
                self.currentLayer += 1
                self.mapLayerSwitched.emit()
        else:
            if index > 0:
                shift = self.nodeLayers[index]
                self.nodeLayers[index] = self.nodeLayers[index-1]
                self.nodeLayers[index-1] = shift
                self.currentLayer -= 1
                self.mapLayerSwitched.emit()

    # /////////////////////////////// #
    # Display Item Management Methods #
    # /////////////////////////////// #

    # Create a duplicate of the displayItem from an Original
    def copyDIAttributes(self, dupe, orig):
        for di in orig.currentDIs():
            di.addItem(dupe, copy.copy(orig.diValues(di)))

    def diUpdated(self):
        self.displayItemValuesUpdated.emit()

    def getDisplayItems(self):
        return self.displayItems

    def getSelectedDI(self):
        di = None
        if self.selectedDI >= 0:
            di = self.displayItems[self.selectedDI]
        return di

    def setSelectedDI(self, index):
        self.selectedDI = index
        self.displayItemListUpdated.emit()

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
            self.displayItemListUpdated.emit()

    def applyDIToSelection(self, di):
        if di.getAllowedClass() == NodeLayer:
            di.addItem(self.nodeLayers[self.currentLayer])
        else:
            di.addItems(self.selectedItems)
        self.displayItemValuesUpdated.emit()

    def removeDisplayItem(self, di):
        if di in self.displayItems:
            di.removeAllItems()
            self.displayItems.remove(di)
            self.selectedDI = -1
            self.displayItemListUpdated.emit()
            self.displayItemValuesUpdated.emit()

    def shiftDisplayItem(self, index, shiftUp):
        def updateShiftedItemLayers(di):
            for pi in di.getPropertyItems():
                pi.ParentLayer().setNeedRedraw()
        if shiftUp:
            if index > 0:
                shift = self.displayItems[index]
                self.displayItems[index] = self.displayItems[index-1]
                self.displayItems[index-1] = shift
                self.selectedDI = index - 1
                updateShiftedItemLayers(shift)
                self.displayItemListUpdated.emit()
                self.displayItemValuesUpdated.emit()
        else:
            if index > -1 and index != len(self.displayItems)-1:
                shift = self.displayItems[index]
                self.displayItems[index] = self.displayItems[index+1]
                self.displayItems[index+1] = shift
                self.selectedDI = index + 1
                updateShiftedItemLayers(shift)
                self.displayItemListUpdated.emit()
                self.displayItemValuesUpdated.emit()

    def getLayerImages(self):
        layerImgList = []
        for nl in self.nodeLayers:
            img = nl.getLayerImage()
            if img is None or nl.NeedsRedraw():
                img = nl.redrawLayerImage(self.displayItems)
            layerImgList.append(img)
        return layerImgList

    def jsonObj(self):

        dis = []
        for di in self.displayItems:
            dis.append(di.jsonObj())

        layers = []
        # Indexes of all DIs to assist w/ cachind IDs
        diIndexes = {}
        for i in range(len(dis)):
            diIndexes[self.displayItems[i]] = i
        for l in self.nodeLayers:
            layers.append(l.jsonObj(diIndexes))
        return {
            "Width": self.width,
            "Height": self.height,
            "Layers": layers,
            "CurrentLayer": self.currentLayer,
            "DisplayItems": dis,
            "SelectedDI": self.selectedDI
        }
