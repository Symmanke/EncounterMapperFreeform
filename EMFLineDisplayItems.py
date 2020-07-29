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
from PyQt5.QtGui import QPen, QBrush, QColor, QPixmap, QTransform, QPainter


from EMFDisplayProperty import EMFDisplayItem
from EMFNodes import EMFLine, EMFNodeHelper
from EMFAttribute import (EMFAttribute, ScrollbarAttributeWidget,
                          ColorAttributeWidget, SpinboxAttributeWidget,
                          FilePickerAttributeWidget)


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


class ImageLineDisplay(EMFDisplayItem):
    def __init__(self, name):
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
        }

    def drawSimple(self, painter, item):
        # draw the shape's polygon
        points = item.nodes()
        comparison = EMFNodeHelper.nodeComparison(points[0], points[1], True)
        median = EMFNodeHelper.medianNode(points)
        values = item.diValues(self)

        pm = self.sharedAttributes["Image"].getValue()["image"]
        pm = QPixmap("error_image.png") if pm is None else pm
        thickness = pm.height()
        wallpm = QPixmap(comparison[3] + thickness, pm.height())
        wallpm.fill(QColor(0, 0, 0, 0))
        wallPainter = QPainter(wallpm)
        wallPainter.setBrush(QBrush(pm))
        wallPainter.setPen(Qt.NoPen)
        wallPainter.drawEllipse(0, 0, thickness, thickness)
        wallPainter.drawEllipse(wallpm.width() - thickness, 0,
                                thickness, thickness)
        wallPainter.drawRect(thickness/2, 0, comparison[3], thickness)
        wallPainter.end()

        # opacity values
        opacity = values["Opacity"]
        painter.setOpacity(opacity / 100)

        # transform values
        transform = QTransform()

        transform.rotate(comparison[2]-90)
        # transform.scale(scale, scale)
        # transform.translate(point.x() - pm.width()/2,
        #                     point.y() - pm.height()/2)
        # painter.setTransform(transform)
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


class ImageDoorDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ImageDoorDisplay, self).__init__(name, EMFLine)
        self.sharedAttributes = {
            "Image": EMFAttribute(self, "Image", FilePickerAttributeWidget, {})

        }

        self.individualAttributes = {
            "Position": EMFAttribute(self, "Position",
                                     ScrollbarAttributeWidget,
                                     {"minimum": 0,
                                      "maximum": 100,
                                      "startValue": 50}),
        }


class LineShadowRadiusDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(LineShadowRadiusDisplay, self).__init__(name, EMFLine)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": (0, 0, 0)}),
        }
        self.individualAttributes = {
            "Size": EMFAttribute(self, "Size", SpinboxAttributeWidget,
                                 {"minimum": 0,
                                  "maximum": 1024,
                                  "startValue": 24}),

            "StartOpacity": EMFAttribute(self, "StartOpacity",
                                         ScrollbarAttributeWidget,
                                         {"minimum": 0,
                                          "maximum": 100,
                                          "startValue": 50}),
            "EndOpacity": EMFAttribute(self, "EndOpacity",
                                       ScrollbarAttributeWidget,
                                       {"minimum": 0,
                                        "maximum": 100,
                                        "startValue": 0}),
        }


class LineShadowLengthDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(LineShadowLengthDisplay, self).__init__(name, EMFLine)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": (0, 0, 0)}),
        }
        self.individualAttributes = {
            "Width": EMFAttribute(self, "Width", ScrollbarAttributeWidget,
                                  {"minimum": 0,
                                   "maximum": 36,
                                   "startValue": 24}),

            "StartOpacity": EMFAttribute(self, "StartOpacity",
                                         ScrollbarAttributeWidget,
                                         {"minimum": 0,
                                          "maximum": 100,
                                          "startValue": 50}),
            "EndOpacity": EMFAttribute(self, "EndOpacity",
                                       ScrollbarAttributeWidget,
                                       {"minimum": 0,
                                        "maximum": 100,
                                        "startValue": 0}),
        }
