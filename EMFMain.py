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
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog,
                             QSplitter, QFileDialog,
                             QVBoxLayout, QScrollArea)
from PyQt5.QtGui import QPalette

from EMFDisplayItemsSidebar import DisplayItemSidebar
from EMFNodeEditor import NodeEditor
from EMFMap import EMFMap
from EMFMapResizeDialog import MapResizeDialog
from EMFExportDialog import ExportDialog

import json

"""
EMFMain is the parent widget of Encounter Mapper Freeform. It handles
functionality for creating, saving, loading, and exporting encounter maps
"""


class EMFMain(QWidget):
    def __init__(self):
        super(EMFMain, self).__init__()
        self.map = EMFMap(10, 10)
        self.splitter = QSplitter(Qt.Horizontal)
        self.editor = NodeEditor(self.map)
        self.sideBar = DisplayItemSidebar(self.map)
        scroll = QScrollArea()
        scroll.setBackgroundRole(QPalette.Dark)
        scroll.setWidget(self.editor)

        self.splitter.addWidget(scroll)
        self.splitter.addWidget(self.sideBar)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)

        self.resizeDialog = None
        self.resizeEditor = None

        self.exportDialog = None
        self.exportEditor = None

        self.keyBindings = {
            Qt.Key_E | Qt.ControlModifier: (self.exportEncounterMap,),
            Qt.Key_S | Qt.ControlModifier: (self.saveEncounter,),
            # Qt.Key_S | int(Qt.ControlModifier | Qt.ShiftModifier):
            # (self.saveAsEncounter,),
            # Qt.Key_N | Qt.ControlModifier: (self.newEncounterOpenDialog,),
            Qt.Key_O | Qt.ControlModifier: (self.openEncounter,),
            Qt.Key_R | Qt.ControlModifier: (self.resizeEncounter,),
        }

    def keyPressEvent(self, event):
        key = event.key() | int(event.modifiers())
        if key in self.keyBindings:
            command = self.keyBindings[key]
            if len(command) == 1:
                command[0]()
            else:
                command[0](command[1])

    def resizeEncounter(self):
        def applyEdit():
            rs = self.resizeEditor.getUpdateDimensions()
            self.map.setMapDimensions(rs[0], rs[1], rs[2], rs[3])
            self.resizeDialog.close()
            self.resizeDialog = None
            self.resizeEditor = None

        def cancelEdit():
            self.resizeDialog.close()
            self.resizeDialog = None
            self.resizeEditor = None
        pass

        self.resizeDialog = QDialog()
        layout = QVBoxLayout()

        self.resizeEditor = MapResizeDialog(self.map)
        self.resizeEditor.acceptedAction.connect(applyEdit)
        self.resizeEditor.cancelledAction.connect(cancelEdit)

        layout.addWidget(self.resizeEditor)
        self.resizeDialog.setLayout(layout)
        self.resizeDialog.exec_()

    # Open the Export Dialog to export images of the encounter map
    def exportEncounterMap(self):
        def endExport():
            self.exportDialog.close()
            self.exportDialog = None
            self.exportEditor = None

        def applyExport():
            self.exportEditor.performExport()
            endExport()

        self.exportDialog = QDialog()
        layout = QVBoxLayout()

        self.exportEditor = ExportDialog(self.map)
        self.exportEditor.acceptedAction.connect(applyExport)
        self.exportEditor.cancelledAction.connect(endExport)

        layout.addWidget(self.exportEditor)
        self.exportDialog.setLayout(layout)
        self.exportDialog.exec_()

    # Save a json representation of the current encounter map.
    def saveEncounter(self):
        filePath = QFileDialog.getSaveFileName(
            self, "Open Encounter", "", "Encounter Mapper Freeform (*.emf)")
        if filePath is not None:
            path = filePath[0]
            if path.endswith(".emf"):
                path = path[:-4]
            text = json.dumps(self.map.jsonObj())
            f = open(path+".emf", "w+")
            f.write(text)
            f.close()

    # Choose an .emf file from the filepicker dialog and load the json map
    def openEncounter(self):
        contentMap = None
        pathToOpen = QFileDialog.getOpenFileName(
            self, 'Open File', '', "Encounter Mapper Freeform (*.emf)")
        if pathToOpen is not None and pathToOpen[0]:
            f = open(pathToOpen[0], "r")
            if f.mode == "r":
                contents = f.read()
                jsContents = None
                try:
                    jsContents = json.loads(contents)
                except Exception:
                    # using the base exception class for now
                    # Send an alert that the JSON contents cannot be read
                    pass
                f.close()
                if jsContents is not None:
                    contentMap = EMFMap.createMapFromJSON(jsContents)
        if contentMap is not None:
            self.setMap(contentMap)

    # swap the map that is currently in use from the editor.
    def setMap(self, map):
        self.map = map
        self.editor.setMap(map)
        self.sideBar.setMap(map)


def main():
    app = QApplication([])
    mainWidget = EMFMain()
    mainWidget.show()
    app.exec_()


if __name__ == "__main__":
    main()
