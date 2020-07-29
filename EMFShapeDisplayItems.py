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
from PyQt5.QtGui import QPen, QBrush, QColor, QPixmap


from EMFDisplayProperty import EMFDisplayItem
from EMFNodes import EMFShape
from EMFAttribute import (EMFAttribute, ScrollbarAttributeWidget,
                          ColorAttributeWidget,
                          FilePickerAttributeWidget)


class ColorShapeDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ColorShapeDisplay, self).__init__(name, EMFShape)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": QColor(0, 0, 0)}),
            "LineColor": EMFAttribute(self, "LineColor", ColorAttributeWidget,
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
        poly = item.poly()
        values = item.diValues(self)
        opacity = values["Opacity"]
        painter.setOpacity(opacity / 100)
        lineColor = self.sharedAttributes["LineColor"].getValue()
        fillColor = self.sharedAttributes["FillColor"].getValue()
        painter.setPen(QPen(lineColor))
        painter.setBrush(QBrush(fillColor))
        painter.drawPolygon(poly)


class ImageShapeDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ImageShapeDisplay, self).__init__(name, EMFShape)
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
        poly = item.poly()
        values = item.diValues(self)
        opacity = values["Opacity"]
        painter.setOpacity(opacity / 100)
        img = self.sharedAttributes["Image"].getValue()["image"]
        img = QPixmap("error_image.png") if img is None else img
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(img))
        painter.drawPolygon(poly)
