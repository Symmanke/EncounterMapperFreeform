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

from PyQt5.QtWidgets import (QLabel, QSpinBox,
                             QGridLayout)
from EMFEditAction import EditAction

"""
The MapResizeDialog gives the current size of the map in 72px (1 in.) Squares,
and allows the user to resize/offset the given map by the number of squares.
"""


class MapResizeDialog(EditAction):

    def __init__(self, map):
        super(MapResizeDialog, self).__init__()
        width = map.getWidth()
        height = map.getHeight()
        self.widthEdit = QSpinBox()
        self.widthEdit.setMinimum(0)
        self.widthEdit.setMaximum(100)
        self.widthEdit.setValue(width)
        widthConvLabel = QLabel("{} px".format(width*72))
        self.heightEdit = QSpinBox()
        self.heightEdit.setMinimum(0)
        self.heightEdit.setMaximum(100)
        self.heightEdit.setValue(height)

        heightConvLabel = QLabel("{} px".format(height*72))
        self.xOffset = QSpinBox()
        self.xOffset.setMinimum(-width)
        self.xOffset.setMaximum(width)
        self.xOffset.setValue(0)

        xOffConvLabel = QLabel("0 px")
        self.yOffset = QSpinBox()
        self.yOffset.setMinimum(-height)
        self.yOffset.setMaximum(height)
        self.yOffset.setValue(0)
        yOffConvLabel = QLabel("0 px")

        self.widthEdit.valueChanged.connect(
            lambda v: widthConvLabel.setText("{} px".format(v*72)))
        self.heightEdit.valueChanged.connect(
            lambda v: heightConvLabel.setText("{} px".format(v*72)))
        self.xOffset.valueChanged.connect(
            lambda v: xOffConvLabel.setText("{} px".format(v*72)))
        self.yOffset.valueChanged.connect(
            lambda v: yOffConvLabel.setText("{} px".format(v*72)))

        layout = QGridLayout()
        layout.addWidget(self.widthEdit, 0, 0)
        layout.addWidget(widthConvLabel, 0, 1)
        layout.addWidget(self.heightEdit, 1, 0)
        layout.addWidget(heightConvLabel, 1, 1)
        layout.addWidget(self.xOffset, 2, 0)
        layout.addWidget(xOffConvLabel, 2, 1)
        layout.addWidget(self.yOffset, 3, 0)
        layout.addWidget(yOffConvLabel, 3, 1)

        layout.addWidget(self.cancelBtn, 4, 0)
        layout.addWidget(self.acceptBtn, 4, 1)
        self.setLayout(layout)

    def getUpdateDimensions(self):
        return (self.widthEdit.value(), self.heightEdit.value(),
                self.xOffset.value(), self.yOffset.value())
