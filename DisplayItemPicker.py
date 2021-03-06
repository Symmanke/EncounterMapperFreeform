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
from PyQt5.QtWidgets import (QLineEdit, QComboBox,
                             QVBoxLayout, QHBoxLayout, QWidget)
from EMFEditAction import EditAction

from EMFNodeDisplayItems import (ColorCircleDisplay, ImageDisplay,
                                 CircleShadowDisplay)
from EMFLineDisplayItems import (ImageLineDisplay,
                                 ImageDoorDisplay,
                                 LineShadowRadiusDisplay,
                                 LineShadowLengthDisplay)
from EMFShapeDisplayItems import ColorShapeDisplay, ImageShapeDisplay
from EMFSpecialDisplay import ColorBGDisplay, ImageBGDisplay, GridDisplay

"""
The DisplayItemPicker is brought up whenever one is trying to create a new
DisplayItem. This dialog contains a list of possible displayItems as well
as a text input for a name.
"""


class DisplayItemPicker(EditAction):
    DIClasses = {
        #  Nodes
        "ColorCircleDisplay": ColorCircleDisplay,
        "ImageDisplay": ImageDisplay,
        "CircleShadowDisplay": CircleShadowDisplay,
        #   Lines
        # "ColorLineDisplay": ColorLineDisplay,
        "ImageLineDisplay": ImageLineDisplay,
        # "ColorDoorDisplay": ColorDoorDisplay,
        "ImageDoorDisplay": ImageDoorDisplay,
        "LineShadowRadiusDisplay": LineShadowRadiusDisplay,
        "LineShadowLengthDisplay": LineShadowLengthDisplay,
        #  Shapes
        "ColorShapeDisplay": ColorShapeDisplay,
        "ImageShapeDisplay": ImageShapeDisplay,
        # Special
        "ColorBGDisplay": ColorBGDisplay,
        "ImageBGDisplay": ImageBGDisplay,
        "GridDisplay": GridDisplay
    }

    def __init__(self):
        super(DisplayItemPicker, self).__init__()
        self.nameEdit = QLineEdit()
        self.diPicker = QComboBox()
        self.diPicker.addItems(DisplayItemPicker.DIClasses.keys())

        diWidget = QWidget()
        diLayout = QHBoxLayout()
        diLayout.addWidget(self.nameEdit)
        diLayout.addWidget(self.diPicker)
        diWidget.setLayout(diLayout)

        btnWidget = QWidget()
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.acceptBtn)
        btnLayout.addWidget(self.cancelBtn)
        btnWidget.setLayout(btnLayout)

        layout = QVBoxLayout()
        layout.addWidget(diWidget)
        layout.addWidget(btnWidget)
        self.setLayout(layout)

    def getSelectedDI(self, map):
        diSelection = DisplayItemPicker.DIClasses[self.diPicker.currentText()]
        return diSelection(self.nameEdit.text())

    @classmethod
    def diFromJSON(cls, jsonObj):
        di = None
        if jsonObj["class"] in cls.DIClasses:
            di = cls.DIClasses[jsonObj["class"]](
                jsonObj["name"],
                jsonObj["sharedAttributes"], jsonObj["individualAttributes"])
        return di
