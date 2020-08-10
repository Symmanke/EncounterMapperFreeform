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
from PyQt5.QtGui import (QBrush, QColor, QPixmap, QTransform, QPainter,
                         QRadialGradient, QLinearGradient, QGradient)


from EMFDisplayProperty import EMFDisplayItem
from EMFNodes import EMFLine, EMFNodeHelper
from EMFAttribute import (EMFAttribute, ScrollbarAttributeWidget,
                          ColorAttributeWidget, SpinboxAttributeWidget,
                          FilePickerAttributeWidget, CheckBoxAttributeWidget)
import math


class ColorLineDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ColorLineDisplay, self).__init__(name, EMFLine)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": (0, 0, 0)}),
            "LineColor": EMFAttribute(self, "LineColor", ColorAttributeWidget,
                                      {"startValue": (0, 0, 0)}),
        }
        self.individualAttributes = {
            "Width": EMFAttribute(self, "Width", ScrollbarAttributeWidget,
                                  {"minimum": 0,
                                   "maximum": 36,
                                   "startValue": 24}),

            "Opacity": EMFAttribute(self, "Opacity", ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 100,
                                     "startValue": 100}),
        }

    def classStr(self):
        return "ColorLineDisplay"


class ImageLineDisplay(EMFDisplayItem):
    def __init__(self, name, shared=None, indiv=None):
        super(ImageLineDisplay, self).__init__(name, EMFLine)
        self.sharedAttributes = {
            "Image": EMFAttribute(self, "Image", FilePickerAttributeWidget,
                                  {"startValue": {
                                      "path": "Choose a file...",
                                      "image": None}})

        }

        self.individualAttributes = {
            "Opacity": EMFAttribute(self, "Opacity", ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 100,
                                     "startValue": 100}),
            "ShowEndCaps": EMFAttribute(self, "ShowEndCaps",
                                        CheckBoxAttributeWidget,
                                        {"startValue": True}),
            "EndCapRatio": EMFAttribute(self, "EndCapRatio",
                                        ScrollbarAttributeWidget,
                                        {"minimum": 0,
                                         "maximum": 100,
                                         "startValue": 100}),
            "ReverseImage": EMFAttribute(self, "ReverseImage",
                                         CheckBoxAttributeWidget,
                                         {"startValue": False}),
        }

    def classStr(self):
        return "ImageLineDisplay"

    def drawSimple(self, painter, item):
        # draw the shape's polygon
        points = item.nodes()
        comparison = EMFNodeHelper.nodeComparison(points[0], points[1], True)
        median = EMFNodeHelper.medianNode(points)
        values = item.diValues(self)

        pm = self.sharedAttributes["Image"].getValue()["image"]
        pm = QPixmap("error_image.png") if pm is None else pm
        thickness = pm.height()
        wallpm = None
        if values["ShowEndCaps"]:
            ratio = values["EndCapRatio"] / 100
            ecThickness = math.ceil(thickness*ratio)
            wallpm = QPixmap(comparison[3] + ecThickness, pm.height())
            wallpm.fill(QColor(0, 0, 0, 0))
            wallPainter = QPainter(wallpm)
            wallPainter.setBrush(QBrush(pm))
            wallPainter.setPen(Qt.NoPen)
            wallPainter.drawEllipse(0, (thickness-ecThickness)/2,
                                    ecThickness, ecThickness)
            wallPainter.drawEllipse(wallpm.width() - ecThickness,
                                    (thickness-ecThickness)/2,
                                    ecThickness, ecThickness)
            wallPainter.drawRect(ecThickness/2, 0, comparison[3], thickness)
            wallPainter.end()
        else:
            wallpm = QPixmap(comparison[3], pm.height())
            wallpm.fill(QColor(0, 0, 0, 0))
            wallPainter = QPainter(wallpm)
            wallPainter.setBrush(QBrush(pm))
            wallPainter.setPen(Qt.NoPen)
            wallPainter.drawRect(0, 0, comparison[3], thickness)
            wallPainter.end()

            # opacity values
        opacity = values["Opacity"]
        painter.setOpacity(opacity / 100)

        # transform values
        transform = QTransform()

        transform.rotate(comparison[2]-90 + 180 * values["ReverseImage"])
        wallpm = wallpm.transformed(transform)

        painter.drawPixmap(median.x() - wallpm.width()/2,
                           median.y() - wallpm.height()/2,
                           wallpm)


class ColorDoorDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ColorDoorDisplay, self).__init__(name, EMFLine)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": (0, 0, 0)}),
            "LineColor": EMFAttribute(self, "LineColor", ColorAttributeWidget,
                                      {"startValue": (0, 0, 0)}),
        }
        self.individualAttributes = {
            "Length": EMFAttribute(self, "Length", ScrollbarAttributeWidget,
                                   {"minimum": 0,
                                    "maximum": 36,
                                    "startValue": 24}),
            "Width": EMFAttribute(self, "Width", ScrollbarAttributeWidget,
                                  {"minimum": 0,
                                   "maximum": 36,
                                   "startValue": 24}),

            "Opacity": EMFAttribute(self, "Opacity", ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 100,
                                     "startValue": 100}),
            "Position": EMFAttribute(self, "Position",
                                     ScrollbarAttributeWidget,
                                     {"minimum": 0,
                                      "maximum": 100,
                                      "startValue": 50}),
        }

    def classStr(self):
        return "ColorDoorDisplay"


class ImageDoorDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ImageDoorDisplay, self).__init__(name, EMFLine)
        self.sharedAttributes = {
            "Image": EMFAttribute(self, "Image", FilePickerAttributeWidget,
                                  {"startValue": {
                                      "path": "Choose a file...",
                                      "image": None}})

        }

        self.individualAttributes = {
            "Position": EMFAttribute(self, "Position",
                                     ScrollbarAttributeWidget,
                                     {"minimum": 0,
                                      "maximum": 100,
                                      "startValue": 50}),
            "ReverseImage": EMFAttribute(self, "ReverseImage",
                                         CheckBoxAttributeWidget,
                                         {"startValue": False}),
            "Number": EMFAttribute(self, "Number",
                                   ScrollbarAttributeWidget,
                                   {"minimum": 0,
                                    "maximum": 5,
                                    "startValue": 1}),
            "Spacing": EMFAttribute(self, "Spacing",
                                    ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 360,
                                     "startValue": 0}),
        }

    def classStr(self):
        return "ImageDoorDisplay"

    def drawSimple(self, painter, item):
        points = item.nodes()
        comparison = EMFNodeHelper.nodeComparison(points[0], points[1], True)

        values = item.diValues(self)
        drawPos = EMFNodeHelper.pointOnLine(item, values["Position"]/100)

        pm = self.sharedAttributes["Image"].getValue()["image"]
        pm = QPixmap("error_image.png") if pm is None else pm
        num = values["Number"]
        print("NUMBER: {}".format(num))
        w = pm.width()
        if num > 1:

            wallPm = QPixmap(
                w*num + values["Spacing"] * (num - 1), pm.height())
            wallPm.fill(QColor(0, 0, 0, 0))
            wallPainter = QPainter(wallPm)
            for n in range(num):
                print("{}".format(n))
                wallPainter.drawPixmap((w+values["Spacing"]) * n, 0, pm)
            wallPainter.end()
            pm = wallPm

        transform = QTransform()

        transform.rotate(comparison[2]-90 + 180 * values["ReverseImage"])
        pm = pm.transformed(transform)

        painter.drawPixmap(drawPos.x() - pm.width()/2,
                           drawPos.y() - pm.height()/2,
                           pm)


class LineShadowRadiusDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(LineShadowRadiusDisplay, self).__init__(name, EMFLine)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": QColor(0, 0, 0)}),
        }
        self.individualAttributes = {
            "Size": EMFAttribute(self, "Size", SpinboxAttributeWidget,
                                 {"minimum": 0,
                                  "maximum": 1024,
                                  "startValue": 24}),

            "StartOpacity": EMFAttribute(self, "StartOpacity",
                                         ScrollbarAttributeWidget,
                                         {"minimum": 0,
                                          "maximum": 255,
                                          "startValue": 125}),
            "EndOpacity": EMFAttribute(self, "EndOpacity",
                                       ScrollbarAttributeWidget,
                                       {"minimum": 0,
                                        "maximum": 255,
                                        "startValue": 0}),
            "ShowEndCaps": EMFAttribute(self, "ShowEndCaps",
                                        CheckBoxAttributeWidget,
                                        {"startValue": True})
        }

    def classStr(self):
        return "LineShadowRadiusDisplay"

    def drawSimple(self, painter, item):
        points = item.nodes()
        comparison = EMFNodeHelper.nodeComparison(points[0], points[1], True)
        median = EMFNodeHelper.medianNode(points)

        values = item.diValues(self)
        thickness = values["Size"]
        sOpacity = values["StartOpacity"]
        eOpacity = values["EndOpacity"]
        fillColor = self.sharedAttributes["FillColor"].getValue()
        sFill = QColor(fillColor.red(), fillColor.green(),
                       fillColor.blue(), sOpacity)
        eFill = QColor(fillColor.red(), fillColor.green(),
                       fillColor.blue(), eOpacity)
        # Create the gradients
        lg = QLinearGradient(0, thickness/2, 0, thickness)
        lg.setSpread(QGradient.ReflectSpread)
        lg.setColorAt(0, sFill)
        lg.setColorAt(1, eFill)

        pm = None

        if values["ShowEndCaps"]:
            rg1 = QRadialGradient(thickness/2, thickness/2, thickness/2)
            rg1.setColorAt(0, sFill)
            rg1.setColorAt(1, eFill)

            rg2 = QRadialGradient(comparison[3] + thickness/2,
                                  thickness/2, thickness/2)
            rg2.setColorAt(0, sFill)
            rg2.setColorAt(1, eFill)

            pm = QPixmap(comparison[3] + thickness, thickness)
            noColor = QColor(0, 0, 0, 0)
            pm.fill(noColor)
            semi = 2880  # 16 * 180, b/c drawPie is silly
            quarter = 1440

            pmPainter = QPainter(pm)
            pmPainter.setPen(Qt.NoPen)

            pmPainter.setBrush(rg1)
            pmPainter.drawPie(0, 0, thickness, thickness, quarter, semi)
            pmPainter.setBrush(rg2)
            pmPainter.drawPie(pm.width() - thickness, 0,
                              thickness, thickness, quarter, -semi)

            pmPainter.setBrush(lg)
            pmPainter.drawRect(math.ceil(thickness / 2),
                               0, comparison[3], thickness)
            pmPainter.end()
        else:
            pm = QPixmap(comparison[3], thickness)
            noColor = QColor(0, 0, 0, 0)
            pm.fill(noColor)

            pmPainter = QPainter(pm)
            pmPainter.setPen(Qt.NoPen)

            pmPainter.setBrush(lg)
            pmPainter.drawRect(0, 0, comparison[3], thickness)
            pmPainter.end()

        # set gradient colors

        transform = QTransform()

        transform.rotate(comparison[2]-90)
        pm = pm.transformed(transform)

        painter.drawPixmap(median.x() - pm.width()/2,
                           median.y() - pm.height()/2,
                           pm)


class LineShadowLengthDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(LineShadowLengthDisplay, self).__init__(name, EMFLine)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": QColor(0, 0, 0)}),
        }
        self.individualAttributes = {
            "Width": EMFAttribute(self, "Width", ScrollbarAttributeWidget,
                                  {"minimum": 0,
                                   "maximum": 360,
                                   "startValue": 24}),

            "StartOpacity": EMFAttribute(self, "StartOpacity",
                                         ScrollbarAttributeWidget,
                                         {"minimum": 0,
                                          "maximum": 255,
                                          "startValue": 125}),
            "EndOpacity": EMFAttribute(self, "EndOpacity",
                                       ScrollbarAttributeWidget,
                                       {"minimum": 0,
                                        "maximum": 255,
                                        "startValue": 0}),
            "ShowEndCaps": EMFAttribute(self, "ShowEndCaps",
                                        CheckBoxAttributeWidget,
                                        {"startValue": True})
        }

    def classStr(self):
        return "LineShadowLengthDisplay"

    def drawSimple(self, painter, item):
        points = item.nodes()
        comparison = EMFNodeHelper.nodeComparison(points[0], points[1], True)
        median = EMFNodeHelper.medianNode(points)

        values = item.diValues(self)
        thickness = values["Width"]
        sOpacity = values["StartOpacity"]
        eOpacity = values["EndOpacity"]
        fillColor = self.sharedAttributes["FillColor"].getValue()
        sFill = QColor(fillColor.red(), fillColor.green(),
                       fillColor.blue(), sOpacity)
        eFill = QColor(fillColor.red(), fillColor.green(),
                       fillColor.blue(), eOpacity)

        # Set linear Gradient
        pm = None
        if values["ShowEndCaps"]:
            gradient = QLinearGradient(thickness/2, 0,
                                       comparison[3]+thickness/2, 0)
            gradient.setColorAt(0, sFill)
            gradient.setColorAt(1, eFill)

            semi = 2880  # 16 * 180, b/c drawPie is silly
            quarter = 1440
            pm = QPixmap(comparison[3] + thickness, thickness)
            pm.fill(QColor(0, 0, 0, 0))
            pmPainter = QPainter(pm)
            pmPainter.setBrush(gradient)
            pmPainter.setPen(Qt.NoPen)
            pmPainter.drawPie(0, 0, thickness, thickness, quarter, semi)
            pmPainter.drawPie(pm.width() - thickness, 0,
                              thickness, thickness, quarter, -semi)
            pmPainter.drawRect(math.ceil(thickness/2),
                               0, comparison[3], thickness)
            pmPainter.end()
        else:
            gradient = QLinearGradient(0, 0, comparison[3], 0)
            gradient.setColorAt(0, sFill)
            gradient.setColorAt(1, eFill)

            pm = QPixmap(comparison[3], thickness)
            pm.fill(QColor(0, 0, 0, 0))
            pmPainter = QPainter(pm)
            pmPainter.setBrush(gradient)
            pmPainter.setPen(Qt.NoPen)
            pmPainter.drawRect(0, 0, comparison[3], thickness)
            pmPainter.end()

        # set gradient colors

        transform = QTransform()

        transform.rotate(comparison[2]-90)
        pm = pm.transformed(transform)

        painter.drawPixmap(median.x() - pm.width()/2,
                           median.y() - pm.height()/2,
                           pm)
