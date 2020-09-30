from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from Elements.Tab import Tab
import logging

class OpenTabsBar(QWidget):
    def __init__(self, file_manager, layout_props):
        super(OpenTabsBar, self).__init__()
        logging.info("")

        self.file_manager = file_manager
        self.layout_props = layout_props

        self.open_tabs = {}

        # crate the hbox layout
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(self.layout_props.bar_tabs_spacing)
        self.setLayout(self.horizontal_layout)

        # set the background
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('grey'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.horizontal_layout.addStretch()

    # this will create a new tab and add it to the horizontal layout
    def addTab(self, path: str) -> Tab:
        logging.info(path)
        tab = Tab(self, self.file_manager, path)
        self.layout().insertWidget(0, tab)

        # add tab to the dict holding open tabs
        self.open_tabs[path] = tab

        return tab

    # removes object from layout and destroys it
    def closeTab(self, path: str, save=True):
        logging.info(path)
        tab = self.open_tabs[path]
        self.layout().removeWidget(tab)

        if save:
            self.file_manager.saveDocument()
        self.file_manager.closeDocument(tab.path)

        # pop the closed tab from the open tab dic
        self.open_tabs.pop(path)
        tab.deleteLater()

    def getTabCount(self):
        logging.info(str(self.horizontal_layout.count()))
        return self.layout().count()
