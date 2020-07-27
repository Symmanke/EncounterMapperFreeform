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
                             QSplitter,
                             QVBoxLayout, QScrollArea)
from PyQt5.QtGui import QPalette

from EMFDisplayItemsSidebar import DisplayItemSidebar
from EMFNodeEditor import NodeEditor


class EMFMain(QWidget):
    def __init__(self):
        super(EMFMain, self).__init__()
        self.splitter = QSplitter(Qt.Horizontal)
        self.editor = NodeEditor(720, 720)
        self.sideBar = DisplayItemSidebar(self.editor)
        scroll = QScrollArea()
        scroll.setBackgroundRole(QPalette.Dark)
        scroll.setWidget(self.editor)

        self.splitter.addWidget(scroll)
        self.splitter.addWidget(self.sideBar)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)


def main():
    app = QApplication([])
    mainWidget = EMFMain()
    mainWidget.show()
    app.exec_()


if __name__ == "__main__":
    main()
