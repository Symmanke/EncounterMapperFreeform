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
    def __init__(self, name, shared=None, indiv=None):
        super(ColorCircleDisplay, self).__init__(name, EMFNode)
        if shared is None:
            shared = {"FillColor": (QColor(0, 0, 0), (0, 0, 0)),
                      "LineColor": (QColor(0, 0, 0), (0, 0, 0))}
        else:
            sfc = shared["FillColor"]
            slc = shared["LineColor"]
            shared["FillColor"] = (QColor(sfc[0], sfc[1], sfc[2]), sfc)
            shared["LineColor"] = (QColor(slc[0], slc[1], slc[2]), slc)
        if indiv is None:
            indiv = {"Size": 24,
                     "Opacity": 100}
        self.sharedAttributes = {
            "FillColor": EMFAttribute(
                self, "FillColor", ColorAttributeWidget, {},
                shared["FillColor"][0], shared["FillColor"][1]),
            "LineColor": EMFAttribute(
                self, "LineColor", ColorAttributeWidget, {},
                shared["LineColor"][0], shared["LineColor"][1]),
        }
        self.individualAttributes = {
            "Size": EMFAttribute(
                self, "Size", SpinboxAttributeWidget,
                {"minimum": 0, "maximum": 1024, },
                indiv["Size"], indiv["Size"]),

            "Opacity": EMFAttribute(
                self, "Opacity", ScrollbarAttributeWidget,
                {"minimum": 0, "maximum": 100},
                indiv["Opacity"], indiv["Opacity"]),
        }

    def classStr(self):
        return "ColorCircleDisplay"

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
    def __init__(self, name, shared=None, indiv=None):
        super(ImageDisplay, self).__init__(name, EMFNode)
        if shared is None:
            shared = {"Image": (None, "Choose a file...")}
        if indiv is None:
            indiv = {"SizeRatio": 100,
                     "Rotation": 0,
                     "Opacity": 100}
        self.sharedAttributes = {
            "Image": EMFAttribute(
                self, "Image", FilePickerAttributeWidget, {},
                shared["Image"][0], shared["Image"][1])

        }

        self.individualAttributes = {
            "SizeRatio": EMFAttribute(
                self, "SizeRatio", ScrollbarAttributeWidget,
                {"minimum": 0, "maximum": 1000},
                indiv["SizeRatio"], indiv["SizeRatio"]),
            "Rotation": EMFAttribute(
                self, "Rotation", ScrollbarAttributeWidget,
                {"minimum": -180, "maximum": 180},
                indiv["Rotation"], indiv["Rotation"]),
            "Opacity": EMFAttribute(
                self, "Opacity", ScrollbarAttributeWidget,
                {"minimum": 0, "maximum": 100},
                indiv["Opacity"], indiv["Opacity"]),
        }

    def classStr(self):
        return "ImageDisplay"

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
    def __init__(self, name, shared=None, indiv=None):
        super(CircleShadowDisplay, self).__init__(name, EMFNode)
        if shared is None:
            shared = {"FillColor": (QColor(0, 0, 0), (0, 0, 0))}
        else:
            sfc = shared["FillColor"]
            shared["FillColor"] = (QColor(sfc[0], sfc[1], sfc[2]), sfc)
        if indiv is None:
            indiv = {"Size": 24,
                     "StartOpacity": 125,
                     "EndOpacity": 0}
        self.sharedAttributes = {
            "FillColor": EMFAttribute(
                self, "FillColor", ColorAttributeWidget, {},
                shared["FillColor"][0], shared["FillColor"][1]),
        }
        self.individualAttributes = {
            "Size": EMFAttribute(
                self, "Size", SpinboxAttributeWidget,
                {"minimum": 0, "maximum": 1024},
                indiv["Size"], indiv["Size"]),

            "StartOpacity": EMFAttribute(
                self, "StartOpacity", ScrollbarAttributeWidget,
                {"minimum": 0, "maximum": 255},
                indiv["StartOpacity"], indiv["StartOpacity"]),
            "EndOpacity": EMFAttribute(
                self, "EndOpacity",
                ScrollbarAttributeWidget,
                {"minimum": 0,
                 "maximum": 255},
                indiv["EndOpacity"], indiv["EndOpacity"]),
        }

    def classStr(self):
        return "CircleShadowDisplay"

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
