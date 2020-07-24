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
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPolygon, QPainter
from PyQt5.QtWidgets import (QApplication, QTabWidget,
                             QWidget)

import math

"""
This file was used to test calculating the distance between lines. None of it
is used in EncounterMapperFreeform. Keeping it to document my testing process
throughout developing the application
"""


class DistanceTester(QTabWidget):
    def __init__(self):
        super(DistanceTester, self).__init__()
        pointTab = PointTestWidget(QPoint(250, 250))
        lineTab = LineTestWidget(QPoint(250, 100), QPoint(250, 350))
        shapeTab = ShapeTestWidget((QPoint(100, 100), QPoint(250, 250),
                                    QPoint(400, 100)))

        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        # self.tabMenu = QTabWidget()
        self.addTab(pointTab, "Point")
        self.addTab(lineTab, "Line")
        self.addTab(shapeTab, "Shape")

        self.setWindowTitle("Distance Tester")


class DistanceTestWidget(QWidget):
    def __init__(self):
        super(DistanceTestWidget, self).__init__()
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.lastMousePos = QPoint(-1, -1)
        self.closestPoint = QPoint(-1, -1)
        self.radius = 5

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        self.drawScreenElements(painter)
        painter.setPen(Qt.red)
        painter.drawLine(self.lastMousePos, self.closestPoint)
        painter.setPen(Qt.black)
        painter.drawText(
            10, 10, str(
                self.PointDistance(self.lastMousePos, self.closestPoint)))

    def PointDistance(self, p1, p2):
        return math.pow(p1.x() - p2.x(), 2) + math.pow(p1.y() - p2.y(), 2)

    def drawScreenElements(self, painter):
        print("DEBUG: needs to be overwritten")

    def mouseMoveEvent(self, QMouseEvent):
        # mp = QMouseEvent.pos()
        self.lastMousePos = QMouseEvent.pos()
        self.calculateClosestPoint()
        self.repaint()

    def calculateClosestPoint(self):
        print("DEBUG: needs to be overwritten")

    def closestPointOnSegment(self, p, l1, l2):
        lineLen = self.PointDistance(l1, l2)
        if lineLen == 0:
            return l1
        t = max(0, min(1, QPoint.dotProduct(p-l1, l2-l1)/lineLen))
        return l1 + t * (l2 - l1)


class PointTestWidget(DistanceTestWidget):
    def __init__(self, p):
        super(PointTestWidget, self).__init__()
        self.closestPoint = p

    def drawScreenElements(self, painter):
        painter.setPen(Qt.gray)
        painter.setBrush(Qt.gray)
        d = 2*self.radius
        # print(self.closestPoint)
        painter.drawEllipse(self.closestPoint.x()-self.radius,
                            self.closestPoint.y()-self.radius, d, d)

    def calculateClosestPoint(self):
        # closest point is the point)
        pass


class LineTestWidget(DistanceTestWidget):
    def __init__(self, p1, p2):
        super(LineTestWidget, self).__init__()
        self.linePoints = [p1, p2]
        self.closestPoint = p1
        print(self.closestPoint)

    def drawScreenElements(self, painter):
        painter.setPen(Qt.black)
        painter.drawLine(self.linePoints[0], self.linePoints[1])
        d = 2*self.radius
        painter.setPen(Qt.gray)
        painter.setBrush(Qt.gray)
        for point in self.linePoints:
            painter.drawEllipse(point.x()-self.radius,
                                point.y()-self.radius, d, d)

    def calculateClosestPoint(self):
        self.closestPoint = self.closestPointOnSegment(
            self.lastMousePos, self.linePoints[0], self.linePoints[1])


class ShapeTestWidget(DistanceTestWidget):
    def __init__(self, pList):
        super(ShapeTestWidget, self).__init__()
        self.points = pList
        self.pointPoly = QPolygon(pList)
        self.closestPoint = pList[0]

    def drawScreenElements(self, painter):
        painter.setPen(Qt.black)
        painter.drawPolygon(self.pointPoly)
        d = 2*self.radius
        painter.setPen(Qt.gray)
        painter.setBrush(Qt.gray)
        for point in self.points:
            painter.drawEllipse(point.x()-self.radius,
                                point.y()-self.radius, d, d)

    def calculateClosestPoint(self):
        # Check each of the line segments
        l2 = self.points[-1]
        dist = -1
        for point in self.points:
            cp = self.closestPointOnSegment(self.lastMousePos, point, l2)
            cpDist = self.PointDistance(self.lastMousePos, cp)
            if cpDist < dist or dist == -1:
                self.closestPoint = cp
                dist = cpDist
            l2 = point


def main():
    app = QApplication([])
    mainWidget = DistanceTester()
    mainWidget.show()
    app.exec_()


if __name__ == "__main__":
    main()
