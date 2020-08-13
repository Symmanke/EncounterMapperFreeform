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
from PyQt5.QtCore import pyqtSignal, QObject


class DIPropertyHolder(QObject):
    propertyUpdated = pyqtSignal()

    def __init__(self):
        self.diProperties = {}
        self.parentLayer = None

    def setParentLayer(self, layer):
        self.parentLayer = layer

    def currentDIs(self):
        return list(self.diProperties.keys())

    def addIndividualAttributes(self, di, values=None):
        # wat
        if di not in self.diProperties:
            attrValues = values
            if attrValues is None:
                attrValues = {}
                diAttr = di.getIndividualAttributes()
                for attrStr in diAttr:
                    attrValues[attrStr] = diAttr[attrStr].getValue()
            self.diProperties[di] = attrValues
            if self.parentLayer is not None:
                self.parentLayer.setNeedRedraw()

    def sharedAttributeUpdated(self):
        self.parentLayer.setNeedRedraw()

    def updateAttribute(self, di, attr):
        if di in self.diProperties:
            self.diProperties[di][attr.getName()] = attr.getValue()
            if self.parentLayer is not None:
                self.parentLayer.setNeedRedraw()

    def removeAllDIs(self):
        for di in self.diProperties:
            di.removeItem(self)
        self.diProperties.clear()
        self.parentLayer.setNeedRedraw()

    def removeDI(self, di):
        if di in self.diProperties:
            di.removeItem(self)
            self.diProperties.pop(di)
            self.parentLayer.setNeedRedraw()

    def diValues(self, di):
        values = None
        if di in self.diProperties:
            values = self.diProperties[di]
        return values

    def indivAttributesJSON(self, diIndexes):
        properties = {}
        for di in self.diProperties:
            propertyJS = {}
            # Fill in PropertyJS
            for attr in self.diProperties[di]:
                # print(attr)
                propertyJS[attr] = self.diProperties[di][attr]
            properties[diIndexes[di]] = propertyJS
        return properties
