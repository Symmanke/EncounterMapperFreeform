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
from PyQt5.QtGui import QPen, QBrush, QColor


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
        print("IMPLEMENTED!")
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
            "Image": EMFAttribute(self, "Image", FilePickerAttributeWidget, {})

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
        }


class CircleShadowDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(CircleShadowDisplay, self).__init__(name, EMFNode)
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
