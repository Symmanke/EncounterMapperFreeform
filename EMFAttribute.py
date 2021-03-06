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
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QHBoxLayout, QCheckBox,
                             QSpinBox, QFileDialog, QPushButton, QDialog)
from PyQt5.QtGui import QPalette, QPixmap

from EMFColorPicker import ColorPicker

"""
An EMFAttribute is a single variable for a DisplayItem. The base class contains
enough information to store the value, as well as a JSON value representation.
Each attribute has a corresponding EMFAttributeWidget, which enables users to
update the variables used.
"""


class EMFAttribute:
    def __init__(self, parentDI, name, widgetClass, widgetParams,
                 value, jsonValue):
        # jsonValue is used when saving items. Each application should have a
        # json Equivalent to create the value from.
        self.value = value
        self.jsonValue = jsonValue
        self.parentDI = parentDI
        self.name = name
        self.widgetclass = widgetClass
        self.widgetParams = widgetParams

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def getJSONValue(self):
        return self.jsonValue

    def setValues(self, value, jsonValue):
        self.value = value
        self.jsonValue = jsonValue
        self.parentDI.valueUpdated(self.name)

    def widgetClass(self):
        return self.widgetclass

    def widgetParams(self):
        return self.widgetParams


"""
The EMFAttributeWidget base class contains the base capabilities needed to
update an EMFAttribute. Each subclass contains the necessary widgets to update
the given value. Users should either use a subclass, or create a new one if
none of the existing subclasses are appropriate for the use case.
"""


class EMFAttributeWidget(QWidget):
    attributeChanged = pyqtSignal()

    def __init__(self, attr, params):
        super(EMFAttributeWidget, self).__init__()
        self.attribute = attr

    def updateValues(self, value, jsonValue):
        self.attribute.setValues(value, jsonValue)


"""
ScrollbarAttributeWidget contains a scrollbar used to update an integer value.
The min, max, and starting value can be set at initilization
"""


class ScrollbarAttributeWidget(EMFAttributeWidget):
    def __init__(self, attr, params):
        super(ScrollbarAttributeWidget, self).__init__(attr, params)
        self.scroll = QSlider(Qt.Horizontal, self)
        self.scroll.setMinimum(params["minimum"])
        self.scroll.setMaximum(params["maximum"])
        self.scroll.setValue(attr.getValue())

        self.scroll.sliderMoved.connect(self.updateSliderVal)
        self.valueLabel = QLabel("{}".format(self.scroll.value()))
        self.valueLabel.setFixedWidth(50)
        layout = QHBoxLayout()
        layout.addWidget(self.valueLabel)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def updateSliderVal(self, value):
        self.valueLabel.setText("{}".format(value))
        self.updateValues(value, value)


"""
SpinboxAttributeWidget contains a spinbox used to update an integer value.
The min, max, and starting value can be set at initilization
"""


class SpinboxAttributeWidget(EMFAttributeWidget):
    def __init__(self, attr, params):
        super(SpinboxAttributeWidget, self).__init__(attr, params)
        self.spin = QSpinBox()
        self.spin.setMinimum(params["minimum"])
        self.spin.setMaximum(params["maximum"])

        self.spin.setValue(attr.getValue())
        self.spin.valueChanged.connect(lambda v: self.updateValues(v, v))
        layout = QHBoxLayout()
        layout.addWidget(self.spin)
        self.setLayout(layout)


"""
The CheckBoxAttributeWidget can set a boolean checkbox for a value. The
starting value is set at initilization.
"""


class CheckBoxAttributeWidget(EMFAttributeWidget):
    def __init__(self, attr, params):
        super(CheckBoxAttributeWidget, self).__init__(attr, params)
        self.check = QCheckBox("")

        self.check.setChecked(attr.getValue())
        self.check.toggled.connect(
            lambda: self.updateValues(
                self.check.isChecked(), self.check.isChecked()))
        layout = QHBoxLayout()
        layout.addWidget(self.check)
        self.setLayout(layout)


"""
FilePickerAttributeWidget chooses a filePath for an image.
"""


class FilePickerAttributeWidget(EMFAttributeWidget):
    def __init__(self, attr, params):
        super(FilePickerAttributeWidget, self).__init__(attr, params)
        # val = attr.getValue()
        pathName = attr.getJSONValue()
        if "/" in pathName:
            pathName = pathName.split("/")[-1]

        self.fileLabel = QLabel(pathName)
        self.fileBtn = QPushButton("Select")
        self.fileBtn.clicked.connect(self.pickFile)

        layout = QHBoxLayout()
        layout.addWidget(self.fileLabel)
        layout.addWidget(self.fileBtn)
        self.setLayout(layout)

    def pickFile(self):
        pathToOpen = QFileDialog.getOpenFileName(self, 'Open File',
                                                 '', "Image (*.png)")
        if pathToOpen is not None and pathToOpen[0]:
            pathName = pathToOpen[0]
            if "/" in pathName:
                pathName = pathName.split("/")[-1]
            self.fileLabel.setText(pathName)
            img = QPixmap(pathToOpen[0])
            self.updateValues(img, pathToOpen[0])


"""
The ColorAttributeWidget allows a color picker editor to display. 
"""


class ColorAttributeWidget(EMFAttributeWidget):
    def __init__(self, attr, params):
        super(ColorAttributeWidget, self).__init__(attr, params)
        self.colorDialog = None
        self.colorEditor = None

        self.preview = QWidget()
        self.preview.setMinimumWidth(100)
        self.preview.setAutoFillBackground(True)
        self.selectedColor = attr.getValue()

        self.setPreview(self.selectedColor)
        self.cpBtn = QPushButton("Choose")
        self.cpBtn.clicked.connect(self.openColorEdit)

        layout = QHBoxLayout()
        layout.addWidget(self.preview)
        layout.addWidget(self.cpBtn)
        self.setLayout(layout)

    def setPreview(self, color):
        palette = QPalette()
        palette.setColor(QPalette.Background, color)
        self.preview.setPalette(palette)
        self.preview.repaint()

    def openColorEdit(self):
        self.colorDialog = QDialog()
        layout = QHBoxLayout()

        self.colorEditor = ColorPicker(self.selectedColor)
        self.colorEditor.acceptedAction.connect(self.applyColorEdit)
        self.colorEditor.cancelledAction.connect(self.cancelColorEdit)

        layout.addWidget(self.colorEditor)
        self.colorDialog.setLayout(layout)
        self.colorDialog.exec_()

    def applyColorEdit(self):
        self.selectedColor = self.colorEditor.getCurrentColor()
        self.colorDialog.close()
        self.colorDialog = None
        self.colorEditor = None

        self.setPreview(self.selectedColor)
        self.updateValues(
            self.selectedColor,
            (self.selectedColor.red(), self.selectedColor.green(),
             self.selectedColor.blue()))

    def cancelColorEdit(self):
        self.colorDialog.close()
        self.colorDialog = None
        self.colorEditor = None
