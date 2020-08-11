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
    def __init__(self, name, shared=None, indiv=None):
        super(ColorShapeDisplay, self).__init__(name, EMFShape)
        if shared is None:
            shared = {"FillColor": (QColor(0, 0, 0), (0, 0, 0)),
                      "LineColor": (QColor(0, 0, 0), (0, 0, 0))}
        else:
            sfc = shared["FillColor"]
            slc = shared["LineColor"]
            shared["FillColor"] = (QColor(sfc[0], sfc[1], sfc[2]), sfc)
            shared["LineColor"] = (QColor(slc[0], slc[1], slc[2]), slc)
        if indiv is None:
            indiv = {"Opacity": 100}
        self.sharedAttributes = {
            "FillColor": EMFAttribute(
                self, "FillColor", ColorAttributeWidget, {},
                shared["FillColor"][0], shared["FillColor"][1]),
            "LineColor": EMFAttribute(
                self, "LineColor", ColorAttributeWidget, {},
                shared["LineColor"][0], shared["LineColor"][1]),
        }
        self.individualAttributes = {
            "Opacity": EMFAttribute(
                self, "Opacity", ScrollbarAttributeWidget,
                {"minimum": 0, "maximum": 100},
                shared["Opacity"], shared["Opacity"]),
        }

    def classStr(self):
        return "ColorShapeDisplay"

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
    def __init__(self, name, shared=None, indiv=None):
        super(ImageShapeDisplay, self).__init__(name, EMFShape)
        if shared is None:
            shared = {"Image": (None, "Choose a file...")}
        else:
            shared["Image"] = (QPixmap(shared["Image"]), shared["Image"])
        if indiv is None:
            indiv = {"Opacity": 100}
        self.sharedAttributes = {
            "Image": EMFAttribute(
                self, "Image", FilePickerAttributeWidget, {},
                shared["Image"][0], shared["Image"][1])
        }

        self.individualAttributes = {
            "Opacity": EMFAttribute(
                self, "Opacity", ScrollbarAttributeWidget,
                {"minimum": 0, "maximum": 100},
                indiv["Opacity"], indiv["Opacity"]),
        }

    def classStr(self):
        return "ImageShapeDisplay"

    def drawSimple(self, painter, item):
        # draw the shape's polygon
        poly = item.poly()
        values = item.diValues(self)
        opacity = values["Opacity"]
        painter.setOpacity(opacity / 100)
        img = self.sharedAttributes["Image"].getValue()
        img = QPixmap("error_image.png") if img is None else img
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(img))
        painter.drawPolygon(poly)
