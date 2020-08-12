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

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QApplication, QWidget)

import math

from EMFNodes import NodeLayer, EMFNode, EMFShape, EMFLine, EMFNodeHelper
from EMFMap import EMFMap


class NodeEditor(QWidget):
    INTERACT_SELECT = "SELECT"
    INTERACT_GRAB = "GRAB"
    INTERACT_ROTATE = "ROTATE"
    INTERACT_SCALE = "SCALE"

    selectedItemsUpdated = pyqtSignal()
    selectTypeSwitched = pyqtSignal()
    modeTypeSwitched = pyqtSignal()

    def __init__(self, map):
        super(NodeEditor, self).__init__()
        self.showDebug = True
        self.map = map
        self.map.selectionUpdated.connect(self.mapSelectionUpdated)
        self.map.displayItemValuesUpdated.connect(self.repaint)
        self.map.mapResized.connect(self.updateMapDimensions)
        self.layerWidth = map.getWidth()*72
        self.layerHeight = map.getHeight()*72
        # self.currentNodeLayer = NodeLayer(width, height)
        self.selectedType = NodeLayer.TYPE_NODE
        self.selectedItems = []
        self.selectedNodes = None
        self.medianNode = None
        self.formerMedian = None
        self.interactMode = NodeEditor.INTERACT_SELECT
        self.interactNode = None
        self.currentMousePos = EMFNode(0, 0)
        self.diList = None

        nodes = (
            EMFNode(72, 72),
            EMFNode(144, 72),
            EMFNode(144, 144),
            EMFNode(72, 144))
        shape = EMFShape(nodes)
        self.map.addItemToCurrentLayer(NodeLayer.TYPE_SHAPE, shape)
        self.map.addItemsToCurrentLayer(NodeLayer.TYPE_NODE, nodes)

        self.setFixedWidth(self.layerWidth)
        self.setFixedHeight(self.layerHeight)
        self.setMouseTracking(True)

        self.keyBindings = {
            # Select Modifications
            Qt.Key_1: (self.changeSelectionType, NodeLayer.TYPE_NODE),
            Qt.Key_2: (self.changeSelectionType, NodeLayer.TYPE_LINE),
            Qt.Key_3: (self.changeSelectionType, NodeLayer.TYPE_SHAPE),
            # Actions
            Qt.Key_G: (self.beginInteraction, NodeEditor.INTERACT_GRAB),
            Qt.Key_S: (self.beginInteraction, NodeEditor.INTERACT_SCALE),
            Qt.Key_R: (self.beginInteraction, NodeEditor.INTERACT_ROTATE),
            # Select all
            Qt.Key_A: (self.selectAll,),
            # Extrude, Duplicate, Delete
            Qt.Key_D: (self.duplicateItems,),
            Qt.Key_F: (self.formItem,),
            Qt.Key_E: (self.extrudeItems,),
            Qt.Key_X: (self.deleteItems, False),
            Qt.Key_X | Qt.ShiftModifier: (self.deleteItems, True),
            # Toggle
            Qt.Key_T: (self.toggleView,),
        }

    def setMap(self, map):
        self.map = map
        self.map.selectionUpdated.connect(self.mapSelectionUpdated)
        self.map.displayItemValuesUpdated.connect(self.repaint)
        self.map.mapResized.connect(self.updateMapDimensions)
        self.mapSelectionUpdated()
        self.updateMapDimensions()

    def updateMapDimensions(self):
        self.layerWidth = self.map.getWidth() * 72
        self.layerHeight = self.map.getHeight() * 72
        self.setFixedWidth(self.layerWidth)
        self.setFixedHeight(self.layerHeight)
        self.repaint()

    def toggleView(self):
        self.showDebug = not self.showDebug

    def resizeEditField(self, newWidth, newHeight, xOff=0, yOff=0):
        self.setFixedWidth(newWidth)
        self.setFixedHeight(newHeight)

    def getSelectedItems(self):
        return self.selectedItems

        # DI STUFF
    def setDIList(self, diList):
        self.diList = diList

    def addDIToSelection(self, di):
        if di.getAllowedClass() == NodeLayer:
            di.addItem(self.currentNodeLayer)
        else:
            di.addItems(self.selectedItems)

    def getCurrentDIs(self):
        dis = set(self.currentNodeLayer.currentDIs())
        for item in self.selectedItems:
            dis = dis.union(item.currentDIs())
        return dis

    # //////////// #
    # INTERACTIONS #
    # //////////// #

    def mapSelectionUpdated(self):
        self.selectedItems = self.map.getSelectedItems()
        self.updateMedianPoint()

    # Select a singular item to add to existing items.
    def selectItem(self, inclusiveSelect=False):
        itemTypeList = self.map.getCurrentLayerItems(self.selectedType)
        selectedItem = None
        for item in itemTypeList:
            if (item.inSelectRange(self.currentMousePos)
                    and item not in self.selectedItems):
                selectedItem = item
                break
        if not inclusiveSelect:
            self.map.clearSelectedItems()
        if selectedItem is not None:
            self.map.addItemToSelection(selectedItem)
        self.updateMedianPoint()

    # deselect either a singlular or all selected items

    def deselectItem(self, singleDeselect=False):
        if singleDeselect:
            itemTypeList = self.map.getCurrentLayerItems(self.selectedType)
            for item in itemTypeList:
                if (item.inSelectRange(self.currentMousePos)
                        and item in self.selectedItems):
                    self.map.removeSelectedItem(item)
                    break
        else:
            self.map.clearSelectedItems()

    # toggle between selecting all and no nodes
    def selectAll(self):
        itemTypeList = self.map.getCurrentLayerItems(self.selectedType)
        if len(itemTypeList) == len(self.selectedItems):
            self.map.clearSelectedItems()
        else:
            self.map.addItemsToSelection(itemTypeList)

    # form a new line or shape from the existing selected items
    def formItem(self):
        if self.interactMode == NodeEditor.INTERACT_SELECT:
            # shape is too complex; save logic for later
            if self.selectedType != NodeLayer.TYPE_SHAPE:
                nodes = EMFNodeHelper.listOfNodes(self.selectedItems)
                if (len(nodes) == 2 and
                        len(EMFNodeHelper.existingLine(
                        nodes[0], nodes[1])) == 0):
                    self.map.addItemToCurrentLayer(
                        NodeLayer.TYPE_LINE, EMFLine(nodes[0], nodes[1]))
                elif EMFNodeHelper.existingShape(nodes) is None:
                    shape = EMFShape(nodes)
                    self.map.addItemToCurrentLayer(NodeLayer.TYPE_SHAPE, shape)

    def deleteItems(self, deleteTouchingNodes=False):
        if self.interactMode == NodeEditor.INTERACT_SELECT:
            if deleteTouchingNodes:
                self.deleteNodes(EMFNodeHelper.listOfNodes(self.selectedItems))
            else:
                delMethods = {NodeLayer.TYPE_NODE:
                              self.deleteNodes,
                              NodeLayer.TYPE_LINE:
                              self.deleteLines,
                              NodeLayer.TYPE_SHAPE:
                              self.deleteShapes}
                delMethods[self.selectedType](self.selectedItems)
            self.map.clearSelectedItems()

    # Delete all selected nodes. also removes all touching lines and shapes
    def deleteNodes(self, nodes):
        shapesTBD = set()
        linesTBD = set()
        # grab shapes to remove
        for node in nodes:
            for line in node.getLines():
                linesTBD.add(line)
            for shape in node.getShapes():
                shapesTBD.add(shape)
        # remove shapes
        for shape in shapesTBD:
            shape.shapeDeleted()
            self.map.removeItemFromCurrentLayer(NodeLayer.TYPE_SHAPE, shape)
        for line in linesTBD:
            # delete lines
            line.lineDeleted()
            self.map.removeItemFromCurrentLayer(NodeLayer.TYPE_LINE, line)
        for node in nodes:
            node.nodeDeleted()
            self.map.removeItemFromCurrentLayer(NodeLayer.TYPE_NODE, node)
        pass

    # Delete all selected lines. also removes all touching shapes
    def deleteLines(self, lines):
        # Generate set of shapes
        shapesTBD = set()
        # grab shapes to remove
        for line in lines:
            for shape in line.shapes():
                shapesTBD.add(shape)
        # remove shapes
        for shape in shapesTBD:
            shape.shapeDeleted()
            # self.shapes.remove(shape)
            self.map.removeItemFromCurrentLayer(NodeLayer.TYPE_SHAPE, shape)
        for line in lines:
            # delete lines
            line.lineDeleted()
            # self.lines.remove(line)
            self.map.removeItemFromCurrentLayer(NodeLayer.TYPE_LINE, line)

    # delete all selected shapes. Does not affect nodes or lines.
    def deleteShapes(self, shapes):
        for shape in shapes:
            shape.shapeDeleted()
            self.map.removeItemFromCurrentLayer(NodeLayer.TYPE_SHAPE, shape)

    def extrudeItems(self):
        if self.interactMode == NodeEditor.INTERACT_SELECT:
            extMethods = {NodeLayer.TYPE_NODE: self.extrudeNodes,
                          NodeLayer.TYPE_LINE: self.extrudeLines,
                          NodeLayer.TYPE_SHAPE: self.extrudeShapes}
            extMethods[self.selectedType](self.selectedItems)
            self.selectedItemsUpdated.emit()
            self.updateMedianPoint()
            self.beginInteraction(NodeEditor.INTERACT_GRAB)

    # add a single node based off the current position of the cursor
    def addNode(self):
        addedNode = EMFNode(
            self.currentMousePos.x(), self.currentMousePos.y())
        self.map.addItemToCurrentLayer(NodeLayer.TYPE_NODE, addedNode)
        self.selectedItems.append(addedNode)

    # Form a line out of each Node
    def extrudeNodes(self, nodes):
        if len(nodes) == 0:
            self.addNode()
        else:
            newNodes = []
            for node in nodes:
                newNode = EMFNode.createFromNode(node)
                newNodes.append(newNode)
                self.map.addItemToCurrentLayer(
                    NodeLayer.TYPE_NODE, newNode)
                self.map.addItemToCurrentLayer(
                    NodeLayer.TYPE_LINE, EMFLine(node, newNode))
            self.map.setSelectedItems(newNodes)

    # form a shape out of each line
    def extrudeLines(self, lines):
        if len(lines) > 0:
            newNodes = []
            oldNodes = []
            newLines = []
            for line in lines:
                lineNodes = []
                for node in line.nodes():
                    if node not in oldNodes:
                        dupeNode = EMFNode.createFromNode(node)
                        newNodes.append(dupeNode)
                        oldNodes.append(node)
                        self.map.addItemToCurrentLayer(
                            NodeLayer.TYPE_LINE, EMFLine(node, dupeNode))
                        lineNodes.append(dupeNode)
                    else:
                        lineNodes.append(newNodes[oldNodes.index(node)])
                newLines.append(EMFLine(lineNodes[0], lineNodes[1]))
                self.map.addItemToCurrentLayer(
                    NodeLayer.TYPE_SHAPE,
                    EMFShape.createFromLines((line, newLines[-1])))

            self.map.addItemsToCurrentLayer(
                NodeLayer.TYPE_NODE, newNodes)
            self.map.addItemsToCurrentLayer(
                NodeLayer.TYPE_LINE, newLines)
            self.map.setSelectedItems(newLines)

    # Duplicate the shape
    def extrudeShapes(self, shapes):
        self.duplicateShapes(shapes)

    def duplicateItems(self):
        if self.interactMode == NodeEditor.INTERACT_SELECT:
            dupeMethods = {NodeLayer.TYPE_NODE:
                           self.duplicateNodes,
                           NodeLayer.TYPE_LINE:
                           self.duplicateLines,
                           NodeLayer.TYPE_SHAPE:
                           self.duplicateShapes}
            dupeMethods[self.selectedType](self.selectedItems)
            self.beginInteraction(NodeEditor.INTERACT_GRAB)

    # duplicate a selected series of nodes. doesn't duplicate the connected
    # lines or shapes

    def duplicateNodes(self, nodes):
        newNodes = []
        for node in nodes:
            newNode = EMFNode.createFromNode(node)
            self.map.copyDIAttributes(newNode, node)
            newNodes.append(newNode)

        self.map.addItemsToCurrentLayer(NodeLayer.TYPE_NODE, newNodes)
        self.map.setSelectedItems(newNodes)

    # Duplicate a series of lines. doesn't duplicate the shapes
    def duplicateLines(self, lines):
        newNodes = []
        oldNodes = []
        newLines = []
        for line in lines:
            lineNodes = []
            for node in line.nodes():
                if node not in oldNodes:
                    newNode = EMFNode.createFromNode(node)
                    self.map.copyDIAttributes(newNode, node)
                    newNodes.append(newNode)
                    oldNodes.append(node)
                    lineNodes.append(newNode)
                else:
                    # grab node somewhere else
                    lineNodes.append(newNodes[oldNodes.index(node)])
            newLine = EMFLine(lineNodes[0], lineNodes[1])
            self.map.copyDIAttributes(newLine, line)
            newLines.append(newLine)

        self.map.addItemsToCurrentLayer(NodeLayer.TYPE_NODE, newNodes)
        self.map.addItemsToCurrentLayer(NodeLayer.TYPE_LINE, newLines)

        self.map.setSelectedItems(newLines)

    def duplicateShapes(self, shapes):
        newShapes = []
        newNodes = []
        oldNodes = []
        for shape in shapes:
            shapeNodes = []
            for node in shape.nodes():
                if node not in oldNodes:
                    newNode = EMFNode.createFromNode(node)
                    self.map.copyDIAttributes(newNode, node)
                    newNodes.append(newNode)
                    oldNodes.append(node)
                    shapeNodes.append(newNode)
                else:
                    shapeNodes.append(newNodes[oldNodes.index(node)])
            newShape = EMFShape(shapeNodes, False)
            self.map.copyDIAttributes(newShape, shape)
            newShapes.append(newShape)
            # grab shape lines, duplicate those DIs:
            osLines = shape.lines()
            nsLines = newShape.lines()
            for i in range(len(osLines)):
                self.map.copyDIAttributes(nsLines[i], osLines[i])
        self.map.addItemsToCurrentLayer(NodeLayer.TYPE_NODE, newNodes)
        self.map.addItemsToCurrentLayer(NodeLayer.TYPE_SHAPE, newShapes)

        self.map.setSelectedItems(newShapes)

    # update to a new median point. should do when grabbing nodes, or
    # chaning the number of selected items
    def updateMedianPoint(self):
        if len(self.selectedItems) > 0:
            self.medianNode = EMFNodeHelper.medianNode(self.selectedItems)
        else:
            self.medianNode = None

    # switch between the types of selection (Node, Line, Shape)
    def changeSelectionType(self, selectionType):
        if (self.selectedType != selectionType
                and self.interactMode == NodeEditor.INTERACT_SELECT):
            self.selectedType = selectionType
            self.map.clearSelectedItems()

    # drag the selected nodes based on the offset between the initial mouse
    # position and current one
    def interactGrab(self, incremental=False):
        offset = (self.currentMousePos.x() - self.interactNode.x(),
                  self.currentMousePos.y() - self.interactNode.y())
        if incremental:
            offset = (offset[0] - offset[0] % 9, offset[1] - offset[1] % 9)
        for node in self.selectedNodes:
            node.grab(offset)
        self.updateMedianPoint()

    # Rotate the selected nodes around the median using a delta of the initial
    # mouse angle and current
    def interactRotate(self, incremental=False):
        oldDelta = EMFNodeHelper.nodeAngles(
            self.formerMedian, self.interactNode)
        newDelta = EMFNodeHelper.nodeAngles(
            self.formerMedian, self.currentMousePos)
        delta = newDelta - oldDelta
        if(incremental):
            delta = delta - (delta % 15)
        for node in self.selectedNodes:
            node.rotate(delta - 90)

    # Scale the selected nodes based off a ratio of the initial mouse pos and
    # current pos
    def interactScale(self, incremental=False):
        # get a ratio of the two distances
        oldDist = math.sqrt(EMFNodeHelper.nodeDistanceSqr(
            self.formerMedian, self.interactNode))
        oldDist = 0.1 if oldDist == 0 else oldDist
        newDist = math.sqrt(EMFNodeHelper.nodeDistanceSqr(
            self.formerMedian, self.currentMousePos))
        if(incremental):
            newDist = newDist - newDist % 36
        ratio = newDist / oldDist
        for node in self.selectedNodes:
            node.scale(ratio)

    # helper method to navigate to the correct interaction
    def updateInteraction(self):
        selections = {NodeEditor.INTERACT_GRAB: self.interactGrab,
                      NodeEditor.INTERACT_ROTATE: self.interactRotate,
                      NodeEditor.INTERACT_SCALE: self.interactScale}
        if self.interactMode in selections:
            selections[self.interactMode](
                QApplication.keyboardModifiers() == Qt.ShiftModifier)

    # Helper cleanup before beginning an interaction (Grab, Scale, Rotate)
    def beginInteraction(self, interactionType):
        if (self.interactMode != interactionType
                and len(self.selectedItems) > 0):
            if self.interactMode != NodeEditor.INTERACT_SELECT:
                # cancel previous interaction
                self.cancelInteraction()
            self.interactMode = interactionType
            self.formerMedian = self.medianNode
            # Produce a node based off my last mouse position
            self.interactNode = self.currentMousePos
            self.selectedNodes = EMFNodeHelper.listOfNodes(self.selectedItems)
            for node in self.selectedNodes:
                node.beginTransform(self.medianNode)

    # Reset node info to state before interaction began
    def cancelInteraction(self):
        self.interactMode = NodeEditor.INTERACT_SELECT
        for node in self.selectedNodes:
            node.cancelTransform()
        self.selectedNodes = None
        self.interactNode = None
        self.formerMedian = None
        self.updateMedianPoint()

    # Apply interaction changes
    def applyInteraction(self):
        self.interactMode = NodeEditor.INTERACT_SELECT
        for node in self.selectedNodes:
            node.applyTransform()
        self.selectedNodes = None
        self.interactNode = None
        self.formerMedian = None
        self.updateMedianPoint()

    # ////// #
    # EVENTS #
    # ////// #

    def mousePressEvent(self, event):
        self.setFocus()
        if self.interactMode == NodeEditor.INTERACT_SELECT:
            modifiers = QApplication.keyboardModifiers()
            if event.buttons() == Qt.LeftButton:
                self.selectItem(modifiers == Qt.ShiftModifier)
            elif event.buttons() == Qt.RightButton:
                self.deselectItem(modifiers == Qt.ShiftModifier)
        else:
            if event.buttons() == Qt.LeftButton:
                self.applyInteraction()
            elif event.buttons() == Qt.RightButton:
                self.cancelInteraction()
        self.repaint()

    # def mouseReleaseEvent(self, event):
    #     pass

    def mouseMoveEvent(self, event):
        pos = event.pos()
        self.currentMousePos = EMFNode(pos.x(), pos.y())
        if self.interactMode == NodeEditor.INTERACT_SELECT:
            pass
        else:
            self.updateInteraction()
        self.repaint()

    # Handle the key presses here.
    def keyPressEvent(self, event):
        key = event.key() | int(event.modifiers())
        if key in self.keyBindings:
            command = self.keyBindings[key]
            if len(command) == 1:
                command[0]()
            else:
                command[0](command[1])

            self.repaint()
        else:
            # Ignore event so it can percolate up
            event.ignore()

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.drawDebug(painter)

    def drawDebug(self, painter):
        painter.setBrush(Qt.white)
        painter.setPen(Qt.white)
        painter.drawRect(0, 0, self.layerWidth, self.layerHeight)
        # draw the list
        diList = self.map.getDisplayItems()
        if diList is not None:
            diImg = self.map.getCurrentLayer().redrawLayerImage(diList)
            painter.drawImage(0, 0, diImg)
        if self.showDebug:
            painter.setOpacity(.3)
            painter.setPen(Qt.black)
            painter.drawText(10, 10, self.selectedType)
            painter.drawText(10, 20, self.interactMode)
            self.drawShapes(painter)
            self.drawLines(painter)
            self.drawNodes(painter)

            self.drawMedianNode(painter)
            self.drawInteractionNode(painter)
            painter.drawText(50, 10, "{}".format(self.currentMousePos))
            if self.interactMode == NodeEditor.INTERACT_ROTATE:
                newDelta = EMFNodeHelper.nodeAngles(
                    self.formerMedian, self.currentMousePos)
                painter.drawText(10, 30, "{}".format(newDelta))

    # //////////////// #
    # DRAWING ELEMENTS #
    # //////////////// #

    # draw the shapes displayed here
    def drawShapes(self, painter):
        drawColor = (Qt.blue if self.selectedType ==
                     NodeLayer.TYPE_SHAPE else Qt.lightGray)

        for shape in self.map.getCurrentLayerItems(NodeLayer.TYPE_SHAPE):
            dc = Qt.red if shape in self.selectedItems else drawColor
            painter.setPen(dc)
            painter.setBrush(dc)
            painter.drawPolygon(shape.poly())

    # draw the displayed lines
    def drawLines(self, painter):
        drawColor = (Qt.blue if self.selectedType ==
                     NodeLayer.TYPE_LINE else Qt.black)

        for line in self.map.getCurrentLayerItems(NodeLayer.TYPE_LINE):
            dc = Qt.red if line in self.selectedItems else drawColor
            painter.setPen(dc)
            painter.setBrush(dc)
            nodes = line.nodes()
            painter.drawLine(nodes[0].point(), nodes[1].point())

    # draw the displayed nodes
    def drawNodes(self, painter):
        drawColor = (Qt.blue if self.selectedType ==
                     NodeLayer.TYPE_NODE else Qt.darkGray)
        radius = 5
        d = radius * 2
        for node in self.map.getCurrentLayerItems(NodeLayer.TYPE_NODE):
            dc = Qt.red if node in self.selectedItems else drawColor
            painter.setPen(dc)
            painter.setBrush(dc)
            painter.drawEllipse(node.x()-radius, node.y()-radius, d, d)

    def drawMedianNode(self, painter):
        if self.medianNode is not None:
            radius = 5
            d = radius * 2
            painter.setBrush(Qt.darkRed)
            painter.setPen(Qt.black)
            painter.drawEllipse(
                self.medianNode.x()-radius, self.medianNode.y()-radius, d, d)

    def drawInteractionNode(self, painter):
        painter.setPen(Qt.darkRed)
        if self.interactMode == NodeEditor.INTERACT_GRAB:
            painter.drawLine(self.formerMedian.point(),
                             self.medianNode.point())
        elif (self.interactMode == NodeEditor.INTERACT_SCALE
              or self.interactMode == NodeEditor.INTERACT_ROTATE):
            painter.drawLine(self.formerMedian.point(),
                             self.currentMousePos.point())


def main():
    app = QApplication([])
    map = EMFMap()
    mainWidget = NodeEditor(map)
    mainWidget.show()
    app.exec_()


if __name__ == "__main__":
    main()
