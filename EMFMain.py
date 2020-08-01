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
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QSplitter, QFileDialog,
                             QVBoxLayout, QScrollArea)
from PyQt5.QtGui import QPalette

from EMFDisplayItemsSidebar import DisplayItemSidebar
from EMFNodeEditor import NodeEditor
from EMFMap import EMFMap


class EMFMain(QWidget):
    def __init__(self):
        super(EMFMain, self).__init__()
        self.map = EMFMap(720, 720)
        self.splitter = QSplitter(Qt.Horizontal)
        self.editor = NodeEditor(self.map, 720, 720)
        self.sideBar = DisplayItemSidebar(self.map)
        scroll = QScrollArea()
        scroll.setBackgroundRole(QPalette.Dark)
        scroll.setWidget(self.editor)

        self.splitter.addWidget(scroll)
        self.splitter.addWidget(self.sideBar)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)

        self.keyBindings = {
            Qt.Key_E | Qt.ControlModifier: (self.exportEncounterMap,),
            # Qt.Key_S | Qt.ControlModifier: (self.saveEncounter,),
            # Qt.Key_S | Qt.ControlModifier | Qt.ShiftModifier:
            # (self.saveAsEncounter,),
            # Qt.Key_N | Qt.ControlModifier: (self.newEncounterOpenDialog,),
            # Qt.Key_O | Qt.ControlModifier: (self.openEncounter,),
        }

    def keyPressEvent(self, event):
        key = event.key() | int(event.modifiers())
        if key in self.keyBindings:
            command = self.keyBindings[key]
            if len(command) == 1:
                command[0]()
            else:
                command[0](command[1])

    def exportEncounterMap(self):  # , mods=None):
        modifiers = []
        print(modifiers)
        filePath = QFileDialog.getSaveFileName(self, "Open Encounter",
                                               "", "Image (*.png)")
        print("exporting map at: {}".format(filePath))
        if filePath is not None:
            fp = filePath[0]
            if fp.endswith(".png"):
                fp = fp[:-4]
            mapImages = self.map.getLayerImages()
            print("retrieved {} map Images".format(len(mapImages)))
            for i in range(len(mapImages)):
                mapImages[i].save(fp+"_l{}.png".format(i), "PNG")
                print("SAVED!!!")


def main():
    app = QApplication([])
    mainWidget = EMFMain()
    mainWidget.show()
    app.exec_()


if __name__ == "__main__":
    main()
