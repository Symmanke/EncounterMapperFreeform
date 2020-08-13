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

from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QRadioButton,
                             QGridLayout, QFileDialog)
from EMFEditAction import EditAction


class ExportDialog(EditAction):
    SINGLE = "Single Image from Layers"
    EVERY = "Every Layer as Image"
    CUSTOM = "Custom Layers"

    def __init__(self, map):
        super(ExportDialog, self).__init__()
        self.map = map
        self.filePath = None
        self.filepathLabel = QLabel("Choose a file...")
        self.chooseFilePathBtn = QPushButton("Choose")
        self.chooseFilePathBtn.clicked.connect(self.setFilePath)
        self.singleLayerRadio = QRadioButton(ExportDialog.SINGLE)
        self.singleLayerRadio.toggled.connect(
            lambda: self.radioBtnChanged(self.singleLayerRadio))
        self.everyLayerRadio = QRadioButton(ExportDialog.EVERY)
        self.everyLayerRadio.toggled.connect(
            lambda: self.radioBtnChanged(self.everyLayerRadio))
        self.customLayerRadio = QRadioButton(ExportDialog.CUSTOM)
        self.customLayerRadio.toggled.connect(
            lambda: self.radioBtnChanged(self.customLayerRadio))
        self.imageLayerLineEdit = QLineEdit("")
        # TODO: create custom validator to handle lineEdit
        self.imageLayerLineEdit.setEnabled(False)
        lineEditExLabel = QLabel("ex. 1,2-3,5")

        self.acceptBtn.setEnabled(False)

        layout = QGridLayout()
        layout.addWidget(self.filepathLabel, 0, 0)
        layout.addWidget(self.chooseFilePathBtn, 0, 1)
        layout.addWidget(self.singleLayerRadio, 1, 0, 1, 2)
        layout.addWidget(self.everyLayerRadio, 2, 0, 1, 2)
        layout.addWidget(self.customLayerRadio, 3, 0, 1, 2)
        layout.addWidget(self.imageLayerLineEdit, 4, 0, 1, 2)
        layout.addWidget(lineEditExLabel, 5, 0, 1, 2)

        layout.addWidget(self.cancelBtn, 6, 0)
        layout.addWidget(self.acceptBtn, 6, 1)
        self.setLayout(layout)

    def setFilePath(self):
        filePath = QFileDialog.getSaveFileName(self, "Export Encounter",
                                               "", "Image (*.png)")
        if filePath is not None:
            fp = filePath[0]
            if fp.endswith(".png"):
                fp = fp[:-4]
            self.filePath = fp
            self.filepathLabel.setText(self.filePath)
            self.updateUI()

    def radioBtnChanged(self, btn):
        if btn.text() == ExportDialog.SINGLE:
            self.imageLayerLineEdit.setEnabled(False)
            str = ("1-{}".format(self.map.getNumLayers()) if
                   self.map.getNumLayers() > 1 else "1")
            self.imageLayerLineEdit.setText(str)
        elif btn.text() == ExportDialog.EVERY:
            self.imageLayerLineEdit.setEnabled(False)
            str = ""
            for i in range(1, self.map.getNumLayers()+1):
                str += "{},".format(i)
            str = str[:-1]
            self.imageLayerLineEdit.setText(str)
        elif btn.text() == ExportDialog.CUSTOM:
            self.imageLayerLineEdit.setEnabled(True)

    def updateUI(self):
        self.acceptBtn.setEnabled(self.filePath is not None)
        self.repaint()
