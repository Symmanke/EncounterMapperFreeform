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
from PyQt5.QtGui import QPolygon
from PyQt5.QtCore import Qt
import operator
import math


class EMFNode:
    def __init__(self, x, y):
        # super(EMFNode, self).__init__(x, y)
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

    def connectedNodes(self):
        nodeSet = set()
        for line in self.lines:
            nodeSet.update(line.nodes())
        if self in nodeSet:
            nodeSet.remove(self)
        return nodeSet

    def removeLine(self, line):
        pass

    def addShape(self, shape):
        self.shapes.append(shape)

    def getShapes(self):
        return self.shapes

    def removeShape(self, shape):
        pass

    def inSelectRange(self, point, threshold=100):
        return EMFNodeHelper.nodeDistanceSqr(point, self) <= threshold


class EMFLine:
    def __init__(self, n1, n2, shape=None):
        self.lineNodes = (n1, n2)

        n1.addLine(self)
        n2.addLine(self)
        self.shapes = [] if shape is None else [shape]

    def addShape(self, shape):
        if shape is not None:
            self.shapes.append(shape)

    def nodes(self):
        return self.lineNodes

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


class EMFShape:
    def __init__(self, nodes, needSort=True):
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
            if len(line) == 0:
                self.shapeLines.append(EMFLine(lastNode, node, self))
            else:
                self.shapeLines.append(line.pop())
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


class EMFNodeHelper:

    # Determine if a line between two nodes already exists
    @classmethod
    def existingLine(cls, n1, n2):
        return set(n1.getLines()).intersection(n2.getLines())

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
        print("BEGIN LINE SORT")
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
