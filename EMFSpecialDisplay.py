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
from EMFAttribute import (EMFAttribute, ScrollbarAttributeWidget,
                          ColorAttributeWidget,
                          FilePickerAttributeWidget)
from EMFNodes import NodeLayer


class GridDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(GridDisplay, self).__init__(name, NodeLayer)
        self.sharedAttributes = {}
        self.individualAttributes = {}


class ColorBGDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ColorBGDisplay, self).__init__(name, NodeLayer)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": (0, 0, 0)}),
        }
        self.individualAttributes = {
            "Opacity": EMFAttribute(self, "Opacity", ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 100,
                                     "startValue": 100}),
        }


class ImageBGDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ImageBGDisplay, self).__init__(name, NodeLayer)
        self.sharedAttributes = {
            "Image": EMFAttribute(self, "Image", FilePickerAttributeWidget, {})

        }

        self.individualAttributes = {
            "Opacity": EMFAttribute(self, "Opacity", ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 100,
                                     "startValue": 100}),
        }
