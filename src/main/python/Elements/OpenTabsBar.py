from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from os import path
from PyQt5.QtCore import QDir

from Elements.Tab import Tab


class OpenTabsBar(QWidget):
    def __init__(self, app):
        super(OpenTabsBar, self).__init__()
        self.app = app
        self.setFixedHeight(self.app.layout_props.bar_tabs_height)

        # crate the hbox layout
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(self.app.layout_props.bar_tabs_spacing)
        self.setLayout(self.horizontal_layout)

        # set the background
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('grey'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.horizontal_layout.addStretch()

    # this will create a new tab and add it to the horizontal layout
    def addTab(self, path: str) -> Tab:
        print('OpenTabsBar - addTab -', path)
        tab = Tab(self, path)
        self.layout().insertWidget(0, tab)
        return tab

    # removes object from layout and destroys it
    def closeTab(self, tab: Tab):
        print('OpenTabsBar - closeTab -', tab.path)
        self.layout().removeWidget(tab)
        self.app.file_manager.closeDocument(tab.path)
        tab.deleteLater()

    def getTabCount(self):
        print("OpenTabsBar - getTabCount -", self.horizontal_layout.count())
        return self.layout().count()


