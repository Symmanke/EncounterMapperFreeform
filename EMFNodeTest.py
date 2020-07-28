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
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QApplication, QWidget)

import math

from EMFNodes import EMFNode, EMFShape, EMFLine, EMFNodeHelper

"""
This file was used when developing a ui to handle nodes, lines, and shapes. It
is a prototype of EMFNodeEditor. EMFNodeTest is no longer used in
EncounterMapperFreeform, and is kept in the project solely to document
my process throughout developing this application.
"""


class EMFNodeTest(QWidget):
    SELECT_TYPE_NODE = "NODE"
    SELECT_TYPE_LINE = "LINE"
    SELECT_TYPE_SHAPE = "SHAPE"

    INTERACT_SELECT = "SELECT"
    INTERACT_GRAB = "GRAB"
    INTERACT_ROTATE = "ROTATE"
    INTERACT_SCALE = "SCALE"

    def __init__(self):
        super(EMFNodeTest, self).__init__()
        self.nodes = []
        self.lines = []
        self.shapes = []
        self.selectedType = EMFNodeTest.SELECT_TYPE_NODE
        self.selectedItems = []
        self.selectedNodes = None
        self.medianNode = None
        self.formerMedian = None
        self.interactMode = EMFNodeTest.INTERACT_SELECT
        self.interactNode = None
        self.currentMousePos = EMFNode(0, 0)

        self.nodes.append(EMFNode(72, 72))
        self.nodes.append(EMFNode(144, 72))
        self.nodes.append(EMFNode(144, 144))
        self.nodes.append(EMFNode(72, 144))
        self.shapes.append(EMFShape(self.nodes))
        self.addShapeLines(self.shapes[-1])

        self.setMouseTracking(True)

        testList = [EMFNode(10, 10)]
        print(EMFNode(10, 10) in testList)

    def addShapeLines(self, shape):
        for addedLine in shape.lines():
            if addedLine not in self.lines:
                self.lines.append(addedLine)
            else:
                print("We've already got one!")

    # //////////// #
    # INTERACTIONS #
    # //////////// #

    # Select a singular item to add to existing items.
    def selectItem(self, inclusiveSelect=False):
        selections = {EMFNodeTest.SELECT_TYPE_NODE: self.nodes,
                      EMFNodeTest.SELECT_TYPE_LINE: self.lines,
                      EMFNodeTest.SELECT_TYPE_SHAPE: self.shapes}
        itemTypeList = selections[self.selectedType]
        selectedItem = None
        for item in itemTypeList:
            if (item.inSelectRange(self.currentMousePos)
                    and item not in self.selectedItems):
                selectedItem = item
                break
        if not inclusiveSelect:
            self.selectedItems.clear()
        if selectedItem is not None:
            self.selectedItems.append(selectedItem)
        self.updateMedianPoint()

    # deselect either a singlular or all selected items
    def deselectItem(self, singleDeselect=False):
        if singleDeselect:
            selections = {EMFNodeTest.SELECT_TYPE_NODE: self.nodes,
                          EMFNodeTest.SELECT_TYPE_LINE: self.lines,
                          EMFNodeTest.SELECT_TYPE_SHAPE: self.shapes}
            itemTypeList = selections[self.selectedType]
            for item in itemTypeList:
                if (item.inSelectRange(self.currentMousePos)
                        and item in self.selectedItems):
                    self.selectedItems.remove(item)
                    break
        else:
            self.selectedItems.clear()
        self.updateMedianPoint()

    # toggle between selecting all and no nodes
    def selectAll(self):
        selections = {EMFNodeTest.SELECT_TYPE_NODE: self.nodes,
                      EMFNodeTest.SELECT_TYPE_LINE: self.lines,
                      EMFNodeTest.SELECT_TYPE_SHAPE: self.shapes}
        itemTypeList = selections[self.selectedType]
        if len(itemTypeList) == len(self.selectedItems):
            self.selectedItems.clear()
        else:
            self.selectedItems.clear()
            self.selectedItems.extend(itemTypeList)
        self.updateMedianPoint()

    # remove all items from selectedItems
    def clearSelectedItems(self):
        self.selectedItems.clear()
        self.medianNode = None

    # form a new line or shape from the existing selected items
    def formItem(self):
        if self.interactMode == EMFNodeTest.INTERACT_SELECT:
            # shape is too complex; save logic for later
            if self.selectedType != EMFNodeTest.SELECT_TYPE_SHAPE:
                nodes = EMFNodeHelper.listOfNodes(self.selectedItems)
                if (len(nodes) == 2 and
                        len(EMFNodeHelper.existingLine(
                        nodes[0], nodes[1])) == 0):
                    self.lines.append(EMFLine(nodes[0], nodes[1]))
                elif len(nodes) > 2:
                    self.shapes.append(EMFShape(nodes))
                    self.addShapeLines(self.shapes[-1])
                    pass

    def deleteItems(self, deleteTouchingNodes=False):
        if self.interactMode == EMFNodeTest.INTERACT_SELECT:
            if deleteTouchingNodes:
                self.deleteNodes(EMFNodeHelper.listOfNodes(self.selectedItems))
            else:
                delMethods = {EMFNodeTest.SELECT_TYPE_NODE: self.deleteNodes,
                              EMFNodeTest.SELECT_TYPE_LINE: self.deleteLines,
                              EMFNodeTest.SELECT_TYPE_SHAPE: self.deleteShapes}
                delMethods[self.selectedType](self.selectedItems)
            self.selectedItems.clear()
            self.updateMedianPoint()
            # delete selectedItems

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
            self.shapes.remove(shape)
        for line in linesTBD:
            # delete lines
            line.lineDeleted()
            self.lines.remove(line)
        for node in nodes:
            self.nodes.remove(node)
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
            self.shapes.remove(shape)
        for line in lines:
            # delete lines
            line.lineDeleted()
            self.lines.remove(line)

    # delete all selected shapes. Does not affect nodes or lines.
    def deleteShapes(self, shapes):
        for shape in shapes:
            shape.shapeDeleted()
            self.shapes.remove(shape)

    def extrudeItems(self):
        if self.interactMode == EMFNodeTest.INTERACT_SELECT:
            extMethods = {EMFNodeTest.SELECT_TYPE_NODE: self.extrudeNodes,
                          EMFNodeTest.SELECT_TYPE_LINE: self.extrudeLines,
                          EMFNodeTest.SELECT_TYPE_SHAPE: self.extrudeShapes}
            extMethods[self.selectedType](self.selectedItems)
            self.updateMedianPoint()
            self.beginInteraction(EMFNodeTest.INTERACT_GRAB)

    # add a single node based off the current position of the cursor
    def addNode(self):
        self.nodes.append(
            EMFNode(self.currentMousePos.x(), self.currentMousePos.y()))
        self.selectedItems.clear()
        self.selectedItems.append(self.nodes[-1])

    # Form a line out of each Node
    def extrudeNodes(self, nodes):
        if len(nodes) == 0:
            self.addNode()
        else:
            newNodes = []
            for node in nodes:
                newNodes.append(EMFNode.createFromNode(node))
                self.nodes.append(newNodes[-1])
                self.lines.append(EMFLine(node, newNodes[-1]))
            self.selectedItems.clear()
            self.selectedItems.extend(newNodes)

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
                        self.lines.append(EMFLine(node, dupeNode))
                        lineNodes.append(dupeNode)
                    else:
                        lineNodes.append(newNodes[oldNodes.index(node)])
                newLines.append(EMFLine(lineNodes[0], lineNodes[1]))
                self.shapes.append(
                    EMFShape.createFromLines((line, newLines[-1])))

            self.nodes.extend(newNodes)
            self.lines.extend(newLines)
            self.selectedItems.clear()
            self.selectedItems.extend(newLines)

    # Duplicate the shape
    def extrudeShapes(self, shapes):
        self.duplicateShapes(shapes)

    def duplicateItems(self):
        if self.interactMode == EMFNodeTest.INTERACT_SELECT:
            dupeMethods = {EMFNodeTest.SELECT_TYPE_NODE: self.duplicateNodes,
                           EMFNodeTest.SELECT_TYPE_LINE: self.duplicateLines,
                           EMFNodeTest.SELECT_TYPE_SHAPE: self.duplicateShapes}
            dupeMethods[self.selectedType](self.selectedItems)
            self.updateMedianPoint()
            self.beginInteraction(EMFNodeTest.INTERACT_GRAB)

    # duplicate a selected series of nodes. doesn't duplicate the connected
    # lines or shapes
    def duplicateNodes(self, nodes):
        newNodes = []
        for node in nodes:
            newNodes.append(EMFNode.createFromNode(node))
        self.nodes.extend(newNodes)
        self.selectedItems.clear()
        self.selectedItems.extend(newNodes)

    # Duplicate a series of lines. doesn't duplicate the shapes
    def duplicateLines(self, lines):
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
                    lineNodes.append(dupeNode)
                else:
                    # grab node somewhere else
                    lineNodes.append(newNodes[oldNodes.index(node)])
                    # EMFLine(lineNodes[0], lineNodes[1]))
            newLines.append(EMFLine(lineNodes[0], lineNodes[1]))

        self.nodes.extend(newNodes)
        self.lines.extend(newLines)
        self.selectedItems.clear()
        self.selectedItems.extend(newLines)

    def duplicateShapes(self, shapes):
        newShapes = []
        newNodes = []
        oldNodes = []
        for shape in shapes:
            shapeNodes = []
            for node in shape.nodes():
                if node not in oldNodes:
                    dupeNode = EMFNode.createFromNode(node)
                    newNodes.append(dupeNode)
                    oldNodes.append(node)
                    shapeNodes.append(dupeNode)
                else:
                    shapeNodes.append(newNodes[oldNodes.index(node)])
            newShapes.append(EMFShape(shapeNodes, False))
            self.addShapeLines(newShapes[-1])
        self.nodes.extend(newNodes)
        self.shapes.extend(newShapes)
        self.selectedItems.clear()
        self.selectedItems.extend(newShapes)

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
                and self.interactMode == EMFNodeTest.INTERACT_SELECT):
            self.selectedType = selectionType
            self.clearSelectedItems()

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
        selections = {EMFNodeTest.INTERACT_GRAB: self.interactGrab,
                      EMFNodeTest.INTERACT_ROTATE: self.interactRotate,
                      EMFNodeTest.INTERACT_SCALE: self.interactScale}
        if self.interactMode in selections:
            selections[self.interactMode](
                QApplication.keyboardModifiers() == Qt.ShiftModifier)

    # Helper cleanup before beginning an interaction (Grab, Scale, Rotate)
    def beginInteraction(self, interactionType):
        if (self.interactMode != interactionType
                and len(self.selectedItems) > 0):
            if self.interactMode != EMFNodeTest.INTERACT_SELECT:
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
        self.interactMode = EMFNodeTest.INTERACT_SELECT
        for node in self.selectedNodes:
            node.cancelTransform()
        self.selectedNodes = None
        self.interactNode = None
        self.formerMedian = None
        self.updateMedianPoint()

    # Apply interaction changes
    def applyInteraction(self):
        self.interactMode = EMFNodeTest.INTERACT_SELECT
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
        if self.interactMode == EMFNodeTest.INTERACT_SELECT:
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
        if self.interactMode == EMFNodeTest.INTERACT_SELECT:
            pass
        else:
            self.updateInteraction()
        self.repaint()

    # Handle the key presses here.
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            self.changeSelectionType(EMFNodeTest.SELECT_TYPE_NODE)
        elif event.key() == Qt.Key_2:
            self.changeSelectionType(EMFNodeTest.SELECT_TYPE_LINE)
        elif event.key() == Qt.Key_3:
            self.changeSelectionType(EMFNodeTest.SELECT_TYPE_SHAPE)
        elif event.key() == Qt.Key_G:
            self.beginInteraction(EMFNodeTest.INTERACT_GRAB)
        elif event.key() == Qt.Key_S:
            self.beginInteraction(EMFNodeTest.INTERACT_SCALE)
        elif event.key() == Qt.Key_R:
            self.beginInteraction(EMFNodeTest.INTERACT_ROTATE)
        elif (event.key() == Qt.Key_A
              and self.interactMode == EMFNodeTest.INTERACT_SELECT):
            self.selectAll()
        elif (event.key() == Qt.Key_D):
            self.duplicateItems()
        elif (event.key() == Qt.Key_E
              and self.interactMode == EMFNodeTest.INTERACT_SELECT):
            self.extrudeItems()
        elif event.key() == Qt.Key_F:
            self.formItem()
        elif event.key() == Qt.Key_X:
            # and event.modifiers == Qt.ShiftModifier:
            self.deleteItems(event.modifiers() == Qt.ShiftModifier)

        self.repaint()

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        painter.setOpacity(0.4)
        painter.setPen(Qt.black)
        painter.drawText(10, 10, self.selectedType)
        painter.drawText(10, 20, self.interactMode)
        self.drawShapes(painter)
        self.drawLines(painter)
        self.drawNodes(painter)

        self.drawMedianNode(painter)
        self.drawInteractionNode(painter)
        painter.drawText(50, 10, "{}".format(self.currentMousePos))
        if self.interactMode == EMFNodeTest.INTERACT_ROTATE:
            newDelta = EMFNodeHelper.nodeAngles(
                self.formerMedian, self.currentMousePos)
            painter.drawText(10, 30, "{}".format(newDelta))

    # //////////////// #
    # DRAWING ELEMENTS #
    # //////////////// #

    # draw the shapes displayed here
    def drawShapes(self, painter):
        drawColor = (Qt.blue if self.selectedType ==
                     EMFNodeTest.SELECT_TYPE_SHAPE else Qt.lightGray)

        for shape in self.shapes:
            dc = Qt.red if shape in self.selectedItems else drawColor
            painter.setPen(dc)
            painter.setBrush(dc)
            painter.drawPolygon(shape.poly())

    # draw the displayed lines
    def drawLines(self, painter):
        drawColor = (Qt.blue if self.selectedType ==
                     EMFNodeTest.SELECT_TYPE_LINE else Qt.black)

        for line in self.lines:
            dc = Qt.red if line in self.selectedItems else drawColor
            painter.setPen(dc)
            painter.setBrush(dc)
            nodes = line.nodes()
            painter.drawLine(nodes[0].point(), nodes[1].point())

    # draw the displayed nodes
    def drawNodes(self, painter):
        drawColor = (Qt.blue if self.selectedType ==
                     EMFNodeTest.SELECT_TYPE_NODE else Qt.darkGray)
        radius = 5
        d = radius * 2
        for node in self.nodes:
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
        if self.interactMode == EMFNodeTest.INTERACT_GRAB:
            painter.drawLine(self.formerMedian.point(),
                             self.medianNode.point())
        elif (self.interactMode == EMFNodeTest.INTERACT_SCALE
              or self.interactMode == EMFNodeTest.INTERACT_ROTATE):
            painter.drawLine(self.formerMedian.point(),
                             self.currentMousePos.point())


def main():
    app = QApplication([])
    mainWidget = EMFNodeTest()
    mainWidget.show()
    app.exec_()


if __name__ == "__main__":
    main()
