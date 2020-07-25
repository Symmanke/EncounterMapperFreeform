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


class ColorCircleDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ColorCircleDisplay, self).__init__(name, EMFNode)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": (0, 0, 0)}),
            "LineColor": EMFAttribute(self, "LineColor", ColorAttributeWidget,
                                      {"startValue": (0, 0, 0)}),
        }
        self.individualAttributes = {
            "Size": EMFAttribute(self, "Size", SpinboxAttributeWidget,
                                 {"minimum": 0,
                                  "maximum": 1024,
                                  "startValue": 24}),

            "Opacity": EMFAttribute(self, "Opacity", ScrollbarAttributeWidget,
                                    {"minimum": 0,
                                     "maximum": 100,
                                     "startValue": 100}),
        }


class ImageDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ImageDisplay, self).__init__(name, EMFNode)
        self.sharedAttributes = {
            "Image": EMFAttribute(self, "Image", FilePickerAttributeWidget, {})

        }

        self.individualAttributes = {
            "SizeRatio": EMFAttribute(self, "SizeRatio",
                                      ScrollbarAttributeWidget,
                                      {"minimum": 0,
                                       "maximum": 1000,
                                       "startValue": 100}),
            "Rotation": EMFAttribute(self, "Rotation",
                                     ScrollbarAttributeWidget,
                                     {"minimum": -180,
                                      "maximum": 180,
                                      "startValue": 0}),
        }


class CircleShadowDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(CircleShadowDisplay, self).__init__(name, EMFNode)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(self, "FillColor", ColorAttributeWidget,
                                      {"startValue": (0, 0, 0)}),
        }
        self.individualAttributes = {
            "Size": EMFAttribute(self, "Size", SpinboxAttributeWidget,
                                 {"minimum": 0,
                                  "maximum": 1024,
                                  "startValue": 24}),

            "StartOpacity": EMFAttribute(self, "StartOpacity",
                                         ScrollbarAttributeWidget,
                                         {"minimum": 0,
                                          "maximum": 100,
                                          "startValue": 50}),
            "EndOpacity": EMFAttribute(self, "EndOpacity",
                                       ScrollbarAttributeWidget,
                                       {"minimum": 0,
                                        "maximum": 100,
                                        "startValue": 0}),
        }
