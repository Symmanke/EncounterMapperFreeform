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
from EMFNodes import EMFNode, EMFLine, EMFShape, EMFNodeHelper


class DIPropertyHolder:
    def __init__(self):
        print("Enter DIP")
        self.diProperties = {}
        print("Exit DIP")

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


class DIPNode(EMFNode, DIPropertyHolder):
    def __init__(self, x, y):
        EMFNode.__init__(self, x, y)
        DIPropertyHolder.__init__(self)


class DIPLine(EMFLine, DIPropertyHolder):
    def __init__(self, n1, n2, shape=None):
        EMFLine.__init__(self, n1, n2, shape)
        DIPropertyHolder.__init__(self)


class DIPShape(EMFShape, DIPropertyHolder):
    def __init__(self, nodes, needSort=True):
        EMFShape.__init__(self, nodes, needSort)
        DIPropertyHolder.__init__(self)

    @classmethod
    def createFromLines(cls, lines):
        return cls(EMFNodeHelper.listOfNodes(lines))
