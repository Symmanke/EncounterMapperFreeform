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
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (QWidget, QSpinBox, QSlider,
                             QApplication, QGridLayout, QLabel)

from EMFEditAction import EditAction


class ColorPicker(EditAction):
    def __init__(self, initialColor=None):
        super(ColorPicker, self).__init__()

        initialColor = (QColor(255, 255, 255) if initialColor is None
                        else initialColor)
        self.currentSelectedColor = initialColor

        self.currentColorPreview = QWidget()
        self.currentColorPreview.setMinimumHeight(200)
        self.currentColorPreview.setMinimumWidth(200)
        self.currentColorPreview.setAutoFillBackground(True)
        self.setCurrentColor()

        # RGB Values
        self.rBox = QSpinBox()
        self.rSlider = QSlider(Qt.Horizontal)
        self.rBox.setRange(0, 255)
        self.rBox.setValue(initialColor.red())
        self.rSlider.setMaximum(255)
        self.rSlider.setValue(initialColor.red())
        self.rSlider.sliderMoved.connect(self.rUpdated)

        self.gBox = QSpinBox()
        self.gSlider = QSlider(Qt.Horizontal)
        self.gBox.setRange(0, 255)
        self.gBox.setValue(initialColor.green())
        self.gSlider.setMaximum(255)
        self.gSlider.setValue(initialColor.green())
        self.gSlider.sliderMoved.connect(self.gUpdated)

        self.bBox = QSpinBox()
        self.bSlider = QSlider(Qt.Horizontal)
        self.bBox.setRange(0, 255)
        self.bBox.setValue(initialColor.blue())
        self.bSlider.setMaximum(255)
        self.bSlider.setValue(initialColor.blue())
        self.bSlider.sliderMoved.connect(self.bUpdated)

        # HSV Values
        self.hBox = QSpinBox()
        self.hSlider = QSlider(Qt.Horizontal)
        self.hBox.setRange(0, 359)
        self.hBox.setValue(initialColor.hue())
        self.hSlider.setMaximum(359)
        self.hSlider.setValue(initialColor.hue())
        self.hSlider.sliderMoved.connect(self.hUpdated)

        self.sBox = QSpinBox()
        self.sSlider = QSlider(Qt.Horizontal)
        self.sBox.setRange(0, 255)
        self.sBox.setValue(initialColor.saturation())
        self.sSlider.setMaximum(255)
        self.sSlider.setValue(initialColor.saturation())
        self.sSlider.sliderMoved.connect(self.sUpdated)

        self.vBox = QSpinBox()
        self.vSlider = QSlider(Qt.Horizontal)
        self.vBox.setRange(0, 255)
        self.vBox.setValue(initialColor.value())
        self.vSlider.setMaximum(255)
        self.vSlider.setValue(initialColor.value())
        self.vSlider.sliderMoved.connect(self.vUpdated)

        self.colorWidget = QWidget()
        colorLayout = QGridLayout()
        colorLayout.addWidget(QLabel("R:"), 0, 0)
        colorLayout.addWidget(self.rBox, 0, 1)
        colorLayout.addWidget(self.rSlider, 0, 2)
        colorLayout.addWidget(QLabel("G:"), 1, 0)
        colorLayout.addWidget(self.gBox, 1, 1)
        colorLayout.addWidget(self.gSlider, 1, 2)
        colorLayout.addWidget(QLabel("B:"), 2, 0)
        colorLayout.addWidget(self.bBox, 2, 1)
        colorLayout.addWidget(self.bSlider, 2, 2)

        colorLayout.addWidget(QLabel("H:"), 3, 0)
        colorLayout.addWidget(self.hBox, 3, 1)
        colorLayout.addWidget(self.hSlider, 3, 2)
        colorLayout.addWidget(QLabel("S:"), 4, 0)
        colorLayout.addWidget(self.sBox, 4, 1)
        colorLayout.addWidget(self.sSlider, 4, 2)
        colorLayout.addWidget(QLabel("V:"), 5, 0)
        colorLayout.addWidget(self.vBox, 5, 1)
        colorLayout.addWidget(self.vSlider, 5, 2)
        self.colorWidget.setLayout(colorLayout)

        layout = QGridLayout()
        layout.addWidget(self.currentColorPreview, 0, 0)
        layout.addWidget(self.colorWidget, 0, 1)
        layout.addWidget(self.acceptBtn, 1, 0)
        layout.addWidget(self.cancelBtn, 1, 1)

        self.setLayout(layout)

    def setCurrentColor(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, self.currentSelectedColor)
        self.currentColorPreview.setPalette(palette)
        self.currentColorPreview.repaint()

    def rgbUpdated(self):
        qclr = QColor(self.rSlider.value(),
                      self.gSlider.value(),
                      self.bSlider.value())
        self.currentSelectedColor = qclr

        self.hBox.setValue(qclr.hue())
        self.hSlider.setValue(qclr.hue())
        self.sBox.setValue(qclr.saturation())
        self.sSlider.setValue(qclr.saturation())
        self.vBox.setValue(qclr.value())
        self.vSlider.setValue(qclr.value())

        self.setCurrentColor()

    def hsvUpdated(self):
        qclr = QColor.fromHsv(self.hSlider.value(),
                              self.sSlider.value(),
                              self.vSlider.value())
        self.currentSelectedColor = qclr

        self.rBox.setValue(qclr.red())
        self.rSlider.setValue(qclr.red())
        self.gBox.setValue(qclr.green())
        self.gSlider.setValue(qclr.green())
        self.bBox.setValue(qclr.blue())
        self.bSlider.setValue(qclr.blue())

        self.setCurrentColor()

    def rUpdated(self, r):
        self.rBox.setValue(r)
        self.rSlider.setValue(r)
        self.rgbUpdated()

    def gUpdated(self, g):
        self.gBox.setValue(g)
        self.gSlider.setValue(g)
        self.rgbUpdated()

    def bUpdated(self, b):
        self.bBox.setValue(b)
        self.bSlider.setValue(b)
        self.rgbUpdated()

    def hUpdated(self, h):
        self.hBox.setValue(h)
        self.hSlider.setValue(h)
        self.hsvUpdated()

    def sUpdated(self, s):
        self.sBox.setValue(s)
        self.sSlider.setValue(s)
        self.hsvUpdated()

    def vUpdated(self, v):
        self.vBox.setValue(v)
        self.vSlider.setValue(v)
        self.hsvUpdated()

    def getCurrentColor(self):
        return self.currentSelectedColor


def main():
    app = QApplication([])
    mainWidget = ColorPicker(QColor(10, 34, 59))
    mainWidget.show()
    app.exec_()


if __name__ == "__main__":
    main()
