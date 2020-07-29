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
from EMFDisplayProperty import EMFDisplayItem
from EMFNodes import EMFNode
from EMFAttribute import (EMFAttribute, ScrollbarAttributeWidget,
                          ColorAttributeWidget, SpinboxAttributeWidget,
                          FilePickerAttributeWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QPen, QBrush, QColor, QPixmap, QTransform,
                         QRadialGradient)


class ColorCircleDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ColorCircleDisplay, self).__init__(name, EMFNode)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": QColor(0, 0, 0)}),
            "LineColor": EMFAttribute(self, "LineColor", ColorAttributeWidget,
                                      {"startValue": QColor(0, 0, 0)}),
        }
        self.individualAttributes = {
            "Size": EMFAttribute(self, "Size", SpinboxAttributeWidget,
                                 {"minimum": 0,
                                  "maximum": 1024,
                                  "startValue": 24}),

            "Opacity": EMFAttribute(self, "Opacity", ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 100,
                                     "startValue": 100}),
        }

    def drawSimple(self, painter, item):
        # draw a circle node with the given size
        point = item.point()
        values = item.diValues(self)
        radius = values["Size"]
        opacity = values["Opacity"]
        painter.setOpacity(opacity / 100)
        lineColor = self.sharedAttributes["LineColor"].getValue()
        fillColor = self.sharedAttributes["FillColor"].getValue()
        painter.setPen(QPen(lineColor))
        painter.setBrush(QBrush(fillColor))
        painter.drawEllipse(point.x()-radius, point.y()-radius, radius * 2,
                            radius * 2)


class ImageDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ImageDisplay, self).__init__(name, EMFNode)
        self.sharedAttributes = {
            "Image": EMFAttribute(self, "Image", FilePickerAttributeWidget,
                                  {"startValue": {
                                      "path": "Choose a file...",
                                      "image": None}})

        }

        self.individualAttributes = {
            "SizeRatio": EMFAttribute(self, "SizeRatio",
                                      ScrollbarAttributeWidget,
                                      {"minimum": 0,
                                       "maximum": 1000,
                                       "startValue": 100}),
            "Rotation": EMFAttribute(self, "Rotation",
                                     ScrollbarAttributeWidget,
                                     {"minimum": -180,
                                      "maximum": 180,
                                      "startValue": 0}),
            "Opacity": EMFAttribute(self, "Opacity", ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 100,
                                     "startValue": 100}),
        }

    def drawSimple(self, painter, item):
        # draw the shape's polygon
        point = item.point()
        values = item.diValues(self)

        pm = self.sharedAttributes["Image"].getValue()["image"]
        pm = QPixmap("error_image.png") if pm is None else pm

        # opacity values
        opacity = values["Opacity"]
        painter.setOpacity(opacity / 100)

        # transform values
        rotate = values["Rotation"]
        scale = values["SizeRatio"] / 100
        transform = QTransform()

        transform.rotate(rotate)
        transform.scale(scale, scale)
        pm = pm.transformed(transform)

        painter.drawPixmap(point.x() - pm.width()/2,
                           point.y() - pm.height()/2,
                           pm)


class CircleShadowDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(CircleShadowDisplay, self).__init__(name, EMFNode)
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
        }

    def drawSimple(self, painter, item):
        # draw a circle node with the given gradient size
        point = item.point()
        values = item.diValues(self)
        radius = values["Size"]
        sOpacity = values["StartOpacity"]
        eOpacity = values["EndOpacity"]

        # set gradient colors
        fillColor = self.sharedAttributes["FillColor"].getValue()
        sFill = QColor(fillColor.red(), fillColor.green(),
                       fillColor.blue(), sOpacity)
        eFill = QColor(fillColor.red(), fillColor.green(),
                       fillColor.blue(), eOpacity)

        rGradient = QRadialGradient(point.x(), point.y(),
                                    radius)
        rGradient.setColorAt(0, sFill)
        rGradient.setColorAt(0.95, eFill)
        rGradient.setColorAt(1, QColor(0, 0, 0, 0))

        painter.setOpacity(1)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(rGradient))
        painter.drawEllipse(point.x()-radius, point.y()-radius, radius * 2,
                            radius * 2)
