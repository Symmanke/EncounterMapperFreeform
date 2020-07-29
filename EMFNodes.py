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

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygon, QImage, QPainter, QColor
from PyQt5.QtCore import Qt
import operator
import math

from EMFDIPropertyHolder import DIPropertyHolder


class NodeLayer(DIPropertyHolder):
    TYPE_NODE = "NODE"
    TYPE_LINE = "LINE"
    TYPE_SHAPE = "SHAPE"

    def __init__(self, width, height):
        super(NodeLayer, self).__init__()
        self.layerItems = {
            NodeLayer.TYPE_NODE: [],
            NodeLayer.TYPE_LINE: [],
            NodeLayer.TYPE_SHAPE: []
        }

        self.layerWidth = width
        self.layerHeight = height
        self.layerImage = None

    def addItemToLayer(self, type, item):
        typeList = self.layerItems[type]
        if item not in typeList:
            typeList.append(item)
            if type == NodeLayer.TYPE_SHAPE:
                self.addItemsToLayer(NodeLayer.TYPE_LINE, item.lines())

    def addItemsToLayer(self, type, items, careful=False):
        for item in items:
            self.addItemToLayer(type, item)

    def removeFromLayer(self, type, item):
        if item in self.layerItems[type]:
            self.layerItems[type].remove(item)

    def getList(self, type):
        return self.layerItems[type]

    def getDimensions(self):
        return (self.layerWidth, self.layerHeight)

    def setLayerImage(self, image):
        self.layerImage = image

    def getLayerImage(self):
        return self.layerImage

    def redrawLayerImage(self, dis):
        self.layerImage = QImage(self.layerWidth, self.layerHeight,
                                 QImage.Format_ARGB32)
        self.layerImage.fill(QColor(0, 0, 0, 0))
        imgPainter = QPainter(self.layerImage)
        # imgPainter.begin()
        # Draw onto image
        for di in reversed(dis):
            di.drawDisplay(imgPainter, self)
        imgPainter.end()
        return self.layerImage


class EMFNode(DIPropertyHolder):
    def __init__(self, x, y):
        super(EMFNode, self).__init__()
        self.nPoint = QPoint(x, y)
        self.lines = []
        self.shapes = []

        self.tempX = self.nPoint.x()
        self.tempY = self.nPoint.y()

        self.transforming = False
        self.offsetNode = None

    @classmethod
    def createFromNode(cls, node):
        return EMFNode(node.x(), node.y())

    def beginTransform(self, median):
        if not self.transforming:
            self.transforming = True

            self.offsetNode = EMFNode(self.nPoint.x() - median.x(),
                                      self.nPoint.y() - median.y())
            self.transformComparison = EMFNodeHelper.nodeComparison(
                median, self, True)
            self.tempX = self.nPoint.x()
            self.tempY = self.nPoint.y()

    def cancelTransform(self):
        self.transforming = False
        self.nPoint.setX(self.tempX)
        self.nPoint.setY(self.tempY)

    def applyTransform(self):
        self.transforming = False

    def grab(self, offset):
        self.nPoint.setX(self.tempX + offset[0])
        self.nPoint.setY(self.tempY + offset[1])

    def rotate(self, deltaAngle):
        angle = math.radians(self.transformComparison[2] + deltaAngle)
        self.nPoint.setX(self.transformComparison[0].x() +
                         self.transformComparison[3] * math.cos(angle))
        self.nPoint.setY(self.transformComparison[0].y() +
                         self.transformComparison[3] * math.sin(angle))

    def scale(self, size):
        self.nPoint.setX(self.transformComparison[0].x() +
                         self.offsetNode.x()*size)
        self.nPoint.setY(self.transformComparison[0].y() +
                         self.offsetNode.y()*size)
        pass

    def x(self):
        return self.nPoint.x()

    def y(self):
        return self.nPoint.y()

    def point(self):
        return self.nPoint

    def addLine(self, line):
        self.lines.append(line)

    def getLines(self):
        return self.lines

    def getShapes(self):
        return self.shapes

    def connectedNodes(self):
        nodeSet = set()
        for line in self.lines:
            nodeSet.update(line.nodes())
        if self in nodeSet:
            nodeSet.remove(self)
        return nodeSet

    def addShape(self, shape):
        self.shapes.append(shape)

    def removeLineRef(self, line):
        if line in self.lines:
            self.lines.remove(line)

    def removeShapeRef(self, shape):
        if shape in self.shapes:
            self.shapes.remove(shape)

    def inSelectRange(self, point, threshold=100):
        return EMFNodeHelper.nodeDistanceSqr(point, self) <= threshold


class EMFLine(DIPropertyHolder):
    def __init__(self, n1, n2, shape=None):
        super(EMFLine, self).__init__()
        self.lineNodes = (n1, n2)

        n1.addLine(self)
        n2.addLine(self)
        self.lineShapes = [] if shape is None else [shape]

    def addShape(self, shape):
        if shape is not None and shape not in self.lineShapes:
            self.lineShapes.append(shape)

    def removeShapeRef(self, shape):
        if shape in self.lineShapes:
            self.lineShapes.remove(shape)

    def nodes(self):
        return self.lineNodes

    def shapes(self):
        return self.lineShapes

    def beginTransform(self):
        for node in self.lineNodes:
            node.beginTransform()

    def cancelTransform(self):
        for node in self.lineNodes:
            node.cancelTransform()

    def applyTransform(self):
        for node in self.lineNodes:
            node.applyTransform()

    def inSelectRange(self, point, threshold=100):
        return EMFNodeHelper.lineDistanceSqr(point, self) <= threshold

    def lineDeleted(self):
        for node in self.lineNodes:
            node.removeLineRef(self)


class EMFShape(DIPropertyHolder):
    def __init__(self, nodes, needSort=True):
        super(EMFShape, self).__init__()
        if needSort:
            sorted = EMFNodeHelper.sortNodeGroup(nodes)
            nodes = []
            for sNode in sorted:
                nodes.append(sNode[1])
        nodes = EMFNodeHelper.sortByLine(nodes)
        self.shapeNodes = nodes
        self.shapeLines = []
        self.shapeUpdating = True
        lastNode = self.shapeNodes[-1]
        for node in self.shapeNodes:
            node.addShape(self)
            line = EMFNodeHelper.existingLine(lastNode, node)
            print(line)
            if len(line) == 0:
                self.shapeLines.append(EMFLine(lastNode, node, self))
            else:
                self.shapeLines.append(line.pop())
                self.shapeLines[-1].addShape(self)
            lastNode = node
        nps = []
        for node in self.shapeNodes:
            nps.append(node.point())
        self.nodePoly = QPolygon(nps)

    @classmethod
    def createFromLines(cls, lines):
        return EMFShape(EMFNodeHelper.listOfNodes(lines))

    def poly(self):
        if self.shapeUpdating:
            nps = []
            for node in self.shapeNodes:
                nps.append(node.point())
            self.nodePoly = QPolygon(nps)
        return self.nodePoly

    def nodes(self):
        return self.shapeNodes

    def lines(self):
        return self.shapeLines

    def updating(self):
        return self.shapeUpdating

    def setUpdating(self, update):
        self.shapeUpdating = update

    def inSelectRange(self, point, threshold=100):
        return self.nodePoly.containsPoint(point.point(), Qt.OddEvenFill)

    def shapeDeleted(self):
        for line in self.shapeLines:
            line.removeShapeRef(self)
        for node in self.shapeNodes:
            node.removeShapeRef(self)
        self.nodePoly = False
        pass


class EMFNodeHelper:

    # Determine if a line between two nodes already exists
    @classmethod
    def existingLine(cls, n1, n2):
        return set(n1.getLines()).intersection(n2.getLines())

    # return a shape made from the existing nodes if possible, otherwise None
    @classmethod
    def existingShape(cls, nodeList):
        shape = None
        ns = set(nodeList)
        if len(nodeList) > 2:
            # check the shapes in here.
            possibleShapes = nodeList[0].getShapes()
            for ps in possibleShapes:
                # Check if the shape has the exact same nodes inside
                if len(ns.symmetric_difference(ps.nodes())) == 0:
                    shape = ps
                    break
        return shape

    # calculate the angle between straight up and the line generated by the
    # nodes in degreees. Angle goes clockwise, 0-360
    @classmethod
    def nodeAngles(cls, baseNode, comparisonNode):
        # cmpNode = baseNode - comparisonNode
        values = (comparisonNode.x() - baseNode.x(),
                  comparisonNode.y() - baseNode.y())

        # absValues = (cmpNode.x().abs(), cmpNode.y().abs())
        if values[0] == 0:
            return 0 if values[1] <= 0 else 180
        # Y is adjacent, X = opposite
        absRatio = abs(values[1]/values[0])
        angle = math.degrees(math.atan(absRatio))
        if values[1] < 0:
            angle = 90 - angle if values[0] >= 0 else 270 + angle
        else:
            angle = 90 + angle if values[0] >= 0 else 270 - angle
        return angle

    # calculate the distance between the two nodes
    @classmethod
    def nodeDistanceSqr(cls, n1, n2):
        return math.pow(
            n1.x() - n2.x(), 2) + math.pow(n1.y() - n2.y(), 2)

    @classmethod
    def lineDistanceSqr(cls, p, line):
        return cls.nodeDistanceSqr(p, cls.closestPointOnSegment(p, line))

    # Create a tuple containing the angle and distance of nodes
    @classmethod
    def nodeComparison(cls, base, comparison, needSquareRoot=False):
        dist = cls.nodeDistanceSqr(base, comparison)
        dist = math.sqrt(dist) if needSquareRoot else dist
        return (base, comparison, cls.nodeAngles(base, comparison),
                dist)

    # Create a node that is the median of all other nodes in the list
    @classmethod
    def medianNode(cls, itemList):
        avgNode = QPoint(0, 0)
        nodeList = cls.listOfNodes(itemList)

        for node in nodeList:
            avgNode = avgNode + node.point()
        avgNode /= len(nodeList)
        return EMFNode(avgNode.x(), avgNode.y())

    @classmethod
    def listOfNodes(cls, itemList):

        nodeList = []
        for item in itemList:
            if isinstance(item, EMFNode):
                if item not in nodeList:
                    nodeList.append(item)
            elif isinstance(item, EMFLine):
                for node in item.nodes():
                    if node not in nodeList:
                        nodeList.append(node)
            elif isinstance(item, EMFShape):
                for node in item.nodes():
                    if node not in nodeList:
                        nodeList.append(node)

        return nodeList

    # Sort a group of nodes primarily by the angles centered around median,
    # secondarily by the magnitude distance
    @classmethod
    def sortNodeGroup(cls, nodeList, median=None):
        median = cls.medianNode(nodeList) if median is None else median
        nodeCmpList = []
        for node in nodeList:
            nodeCmpList.append(cls.nodeComparison(median, node))
        return sorted(nodeCmpList, key=operator.itemgetter(2, 3))

    @classmethod
    def sortByLine(cls, nodes):
        sorted = []
        nodes.reverse()
        # Check if there are any existing lines in this
        cIndex = -1
        while len(nodes) > 0:

            node = nodes.pop(cIndex)
            cIndex = -1
            sorted.append(node)
            connections = node.connectedNodes()

            for node in list(connections.intersection(nodes)):
                # find the closest connection
                i = nodes.index(node)
                print("index: {}".format(i))
                if cIndex == -1:
                    cIndex = i
                elif i > cIndex:
                    cIndex = i

        return sorted

    @classmethod
    def closestPointOnSegment(cls, np, line):
        p = np.point()
        ln = line.nodes()
        lp = ln[0].point(), ln[1].point()
        lineLen = cls.nodeDistanceSqr(lp[0], lp[1])
        if lineLen == 0:
            return ln[0]
        t = max(0, min(1, QPoint.dotProduct(p-lp[0], lp[1]-lp[0])/lineLen))
        return lp[0] + t * (lp[1] - lp[0])
