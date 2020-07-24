from EMFDisplayProperty import EMFDisplayItem
from EMFNodes import EMFNode
from EMFAttribute import (EMFAttribute, ScrollbarAttributeWidget,
                          SpinboxAttributeWidget, FilePickerAttributeWidget)


class ColorCircleDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ColorCircleDisplay, self).__init__(name, EMFNode)
        self.sharedAttributes = {
            "FillColor": EMFAttribute(ScrollbarAttributeWidget,
                                      {"minimum": 0,
                                       "maximum": 255,
                                       "startValue": 50}),
            "LineColor": EMFAttribute(ScrollbarAttributeWidget,
                                      {"minimum": 0,
                                       "maximum": 255,
                                       "startValue": 50}),
        }
        self.individualAttributes = {
            "Size": EMFAttribute(SpinboxAttributeWidget,
                                 {"minimum": 0,
                                  "maximum": 1024,
                                  "startValue": 24}),
        }


class ImageDisplay(EMFDisplayItem):
    def __init__(self, name):
        super(ImageDisplay, self).__init__(name, EMFNode)
        self.sharedAttributes = {
            "Image": EMFAttribute(FilePickerAttributeWidget, {})

        }

        self.individualAttributes = {
            "SizeRatio": EMFAttribute(ScrollbarAttributeWidget,
                                      {"minimum": 0,
                                       "maximum": 1000,
                                       "startValue": 100}),
            "Rotation": EMFAttribute(ScrollbarAttributeWidget,
                                     {"minimum": -180,
                                      "maximum": 180,
                                      "startValue": 0}),
        }
