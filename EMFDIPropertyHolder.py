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

    def currentDIs(self):
        return list(self.diProperties.keys())

    def addIndividualAttributes(self, di):
        # wat
        if di not in self.diProperties:
            attrValues = {"Value": {}, "JSON": {}}
            diAttr = di.getIndividualAttributes()
            for attrStr in diAttr:
                attrValues["Value"][attrStr] = diAttr[attrStr].getValue()
                attrValues["JSON"][attrStr] = diAttr[attrStr].getJSONValue()
            self.diProperties[di] = attrValues

    def updateAttribute(self, di, attr):
        if di in self.diProperties:
            self.diProperties[di]["Value"][attr.getName()] = attr.getValue()
            self.diProperties[di]["JSON"][attr.getName()] = attr.getJSONValue()

    def removeAllDIs(self):
        for di in self.diProperties:
            di.removeItem(self)
        self.diProperties.clear()

    def removeDI(self, di):
        if di in self.diProperties:
            di.removeItem(self)
            self.diProperties.pop(di)

    def diValues(self, di):
        values = None
        if di in self.diProperties:
            values = self.diProperties[di]["Value"]
        return values

    def indivAttributesJSON(self, diIndexes):
        properties = {}
        for di in self.diProperties:
            propertyJS = {}
            # Fill in PropertyJS
            for attr in self.diProperties[di]["JSON"]:
                # print(attr)
                propertyJS[attr] = self.diProperties[di]["JSON"][attr]
            properties[diIndexes[di]] = propertyJS
        return properties
