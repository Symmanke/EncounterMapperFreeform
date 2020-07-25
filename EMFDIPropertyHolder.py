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


class DIPropertyHolder:
    def __init__(self):
        self.diProperties = {}

    def addIndividualAttributes(self, di):
        if di not in self.diProperties:
            attrValues = {}
            diAttr = di.getIndividualAttributes()
            for attrStr in diAttr:
                attrValues[attrStr] = diAttr[attrStr].getValue()
            self.diProperties[di] = attrValues

    def updateAttribute(self, di, attr):
        if di in self.diProperties:
            self.diProperties[di][attr.getName()] = attr.getValue()

    def removeDI(self, di):
        self.diProperties.pop(di, None)

    def diValues(self, di):
        values = None
        if di in self.diProperties:
            values = self.diProperties[di]
        return values
