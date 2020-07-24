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

from PyQt5.QtWidgets import (QWidget, QPushButton)
from PyQt5.QtCore import pyqtSignal


class EditAction(QWidget):
    acceptedAction = pyqtSignal()
    cancelledAction = pyqtSignal()

    def __init__(self):
        super(EditAction, self).__init__()
        self.acceptBtn = QPushButton("OK")
        self.acceptBtn.clicked.connect(self.acceptAction)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelAction)

    def acceptAction(self):
        self.acceptedAction.emit()

    def cancelAction(self):
        self.cancelledAction.emit()
