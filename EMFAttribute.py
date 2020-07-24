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
                             QSpinBox, QFileDialog, QPushButton, QDialog)
from PyQt5.QtGui import QPalette, QColor

from EMFColorPicker import ColorPicker


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
        self.attributes = {} if attributes is None else attributes

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
        if len(self.attributes) == 1:
            self.scroll.setValue(attributes[0].getValue())
        else:
            self.scroll.setValue(params["startValue"])
        self.scroll.sliderMoved.connect(self.updateSliderVal)
        self.valueLabel = QLabel("{}".format(self.scroll.value()))
        self.valueLabel.setFixedWidth(50)
        layout = QHBoxLayout()
        layout.addWidget(self.valueLabel)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def updateSliderVal(self, value):
        self.valueLabel.setText("{}".format(value))
        self.updateValue(value)


class SpinboxAttributeWidget(EMFAttributeWidget):
    def __init__(self, attributes, params):
        super(SpinboxAttributeWidget, self).__init__(attributes, params)
        self.spin = QSpinBox()
        self.spin.setMinimum(params["minimum"])
        self.spin.setMaximum(params["maximum"])
        if len(self.attributes) == 1:
            self.spin.setValue(attributes[0].getValue())
        else:
            self.spin.setValue(params["startValue"])
        self.spin.valueChanged.connect(self.updateValue)
        layout = QHBoxLayout()
        layout.addWidget(self.spin)
        self.setLayout(layout)


class FilePickerAttributeWidget(EMFAttributeWidget):
    def __init__(self, attributes, params):
        super(FilePickerAttributeWidget, self).__init__(attributes, params)
        self.fileLabel = QLabel("Choose a file...")
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
            self.updateValue(pathToOpen[0])


class ColorAttributeWidget(EMFAttributeWidget):
    def __init__(self, attributes, params):
        super(ColorAttributeWidget, self).__init__(attributes, params)
        self.colorDialog = None
        self.colorEditor = None

        self.preview = QWidget()
        self.preview.setMinimumWidth(100)
        # self.preview.setMinimumHeight(100)
        self.preview.setAutoFillBackground(True)
        self.selectedColor = None
        if len(self.attributes) == 1:
            self.selectedColor = attributes[0].getValue()
        else:
            rgb = params["startValue"]
            self.selectedColor = QColor(rgb[0], rgb[1], rgb[2])
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
        self.updateValue(self.selectedColor)

    def cancelColorEdit(self):
        self.colorDialog.close()
        self.colorDialog = None
        self.colorEditor = None
