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
from PyQt5.QtGui import QPen, QBrush, QColor, QImage

from EMFDisplayProperty import EMFDisplayItem
from EMFAttribute import (EMFAttribute, ScrollbarAttributeWidget,
                          ColorAttributeWidget,
                          FilePickerAttributeWidget)
from EMFNodes import NodeLayer


class GridDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(GridDisplay, self).__init__(name, NodeLayer)
        self.sharedAttributes = {
            "LineColor": EMFAttribute(self, "LineColor", ColorAttributeWidget,
                                      {"startValue": QColor(0, 0, 0)}),
            "Opacity": EMFAttribute(self, "Opacity", ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 100,
                                     "startValue": 100}),
        }
        self.individualAttributes = {}

    def drawSimple(self, painter, item):
        dimensions = item.getDimensions()
        pattern = (5, 3, 3)
        # pc = Qt.black
        pc = self.sharedAttributes["LineColor"].getValue()
        opacity = self.sharedAttributes["Opacity"].getValue()
        painter.setOpacity(opacity / 100)
        painter.setPen(pc)
        tileSize = 72
        xr = dimensions[0]//tileSize + 1
        yr = dimensions[1]//tileSize + 1
        # print(pattern)
        patternLen = len(pattern)
        for x in range(xr):
            painter.setPen(QPen(pc, pattern[x % patternLen]))
            xd = int(x*tileSize)
            painter.drawLine(xd, 0, xd, dimensions[1])
        for y in range(yr):
            painter.setPen(QPen(pc, pattern[y % patternLen]))
            yd = int(y*tileSize)
            painter.drawLine(0, yd, dimensions[0], yd)


class ColorBGDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ColorBGDisplay, self).__init__(name, NodeLayer)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": QColor(0, 0, 0)}),
        }
        self.individualAttributes = {
            "Opacity": EMFAttribute(self, "Opacity", ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 100,
                                     "startValue": 100}),
        }

    def drawSimple(self, painter, item):
        # draw the shape's polygon
        dimensions = item.getDimensions()
        values = item.diValues(self)
        opacity = values["Opacity"]
        painter.setOpacity(opacity / 100)
        fillColor = self.sharedAttributes["FillColor"].getValue()
        painter.setPen(QPen(fillColor))
        painter.setBrush(QBrush(fillColor))
        painter.drawRect(0, 0, dimensions[0], dimensions[1])


class ImageBGDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ImageBGDisplay, self).__init__(name, NodeLayer)
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
        dimensions = item.getDimensions()
        values = item.diValues(self)
        opacity = values["Opacity"]
        painter.setOpacity(opacity / 100)
        img = self.sharedAttributes["Image"].getValue()["image"]
        img = QImage("error_image.png") if img is None else img
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(img))
        painter.drawRect(0, 0, dimensions[0], dimensions[1])
