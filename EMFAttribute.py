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

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QHBoxLayout,
                             QSpinBox)


class EMFAttribute:
    def __init__(self, widgetClass, widgetParams):
        self.value = None
        self.attributeWidget = None
        self.widgetclass = widgetClass
        self.widgetParams = widgetParams

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def setWidget(self, widget):
        self.attributeWidget = widget

    def widgetClass(self):
        return self.widgetclass

    def widgetParams(self):
        return self.widgetParams


# Base for the attribute widget.
class EMFAttributeWidget(QWidget):
    attributeChanged = pyqtSignal()

    def __init__(self, attributes, params):
        super(EMFAttributeWidget, self).__init__()
        self.attributes = attributes

    def updateValue(self, value):
        for attribute in self.attributes:
            attribute.setValue(value)
        self.attributeChanged.emit()


class ScrollbarAttributeWidget(EMFAttributeWidget):
    def __init__(self, attributes, params):
        super(ScrollbarAttributeWidget, self).__init__(attributes, params)
        self.scroll = QSlider(Qt.Horizontal, self)
        self.scroll.setMinimum(params["minimum"])
        self.scroll.setMaximum(params["maximum"])
        if len(attributes) == 1:
            self.scroll.setValue(attributes[0].getValue())
        else:
            self.scroll.setValue(params["startValue"])
        self.scroll.sliderMoved.connect(self.updateValue)
        self.valueLabel = QLabel(self.scroll.value())
        layout = QHBoxLayout()
        layout.addWidget(self.scroll)
        layout.addWidget(self.valueLabel)
        self.setLayout(layout)


class SpinboxAttributeWidget(EMFAttributeWidget):
    def __init__(self, attributes, params):
        super(ScrollbarAttributeWidget, self).__init__(attributes, params)
        self.spin = QSpinBox(Qt.Horizontal, self)
        self.spin.setMinimum(params["minimum"])
        self.spin.setMaximum(params["maximum"])
        if len(attributes) == 1:
            self.spin.setValue(attributes[0].getValue())
        else:
            self.spin.setValue(params["startValue"])
        self.spin.valueChange.connect(self.updateValue)
        layout = QHBoxLayout()
        layout.addWidget(self.spin)
        self.setLayout(layout)
