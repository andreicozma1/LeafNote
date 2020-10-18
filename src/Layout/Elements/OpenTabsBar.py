import logging
import random

from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QToolButton

from Widgets.ColorWidget import Color

"""
when one or more file is open it
will show the file tabs under the
top bar
"""


class OpenTabsBar(QWidget):
    """
    functionality and look of Tab Bar
    """

    def __init__(self, document, file_manager, layout_props):
        """
        sets up the tab bar
        :param file_manager: instance of FileManager class - manages all file communication
        :param layout_props: properties for the layout - dimensions
        :return: returns nothing
        """
        super(OpenTabsBar, self).__init__()
        logging.info("")

        self.document = document
        self.file_manager = file_manager
        self.layout_props = layout_props
        self.active_tab = None
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

    def openTab(self, tab):
        self.active_tab = tab
        self.file_manager.openDocument(self.document, tab.path)

    def addTab(self, path: str) -> Tab:
        """
        Creates new tab and adds it to the horizontal layout
        :param path: path to file being displayed
        :return: returns the new tab that was open
        """
        logging.info(path)
        tab = Tab(self, path)
        self.layout().insertWidget(0, tab)

        # add tab to the dict holding open tabs
        self.open_tabs[path] = tab
        self.active_tab = tab
        return tab

    def closeTab(self, path: str, save: bool = True):
        """
        removes object from layout and destroys it
        :param path: path to file being displayed
        :param closeDocument: if the document is closed in file manager
        :param save: if the document is saved
        :return: returns nothing
        """
        logging.info(path)
        tab = self.open_tabs[path]
        self.layout().removeWidget(tab)
        # if close tab is called with the optional parameter
        if save:
            self.file_manager.saveDocument(self.document)
        self.file_manager.closeDocument(self.document, path)

        # pop the closed tab from the open tab dic
        self.open_tabs.pop(path)
        tab.deleteLater()

        # set the active tab
        if self.file_manager.current_document is None:
            self.active_tab = None
        else:
            self.active_tab = self.open_tabs[self.file_manager.current_document.absoluteFilePath()]

    def getTabCount(self):
        """
        gets the number of open tabs
        :return: returns nothing
        """
        logging.info(str(self.horizontal_layout.count()))
        return self.layout().count()


class Tab(Color):
    """
    sets up the file as a tab
    """

    def __init__(self, tab_bar, path: str):
        """
        creates a tab for specific file
        :param tab_bar: bar where the tabs will be stored
        :param file_manager: instance of FileManager class - manages all file communication
        :param path: path to file being displayed
        :return: returns nothing
        """
        # Generate random color for the tab TODO: Change up to preference
        color = "#" + str(format(random.randint(0, 16777215), 'x'))
        super(Tab, self).__init__(color)
        logging.info("")
        self.tab_bar = tab_bar
        self.path = path
        self.f_name = QFileInfo(self.path).fileName()  # grab substring of just the file name w/o path for asthetic

        # create horizontal layout for the tab
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(10, 0, 0, 0)
        self.horizontal_layout.setSpacing(2)

        # add the file name to the tab
        self.label = QLabel(self.f_name)
        self.horizontal_layout.addWidget(self.label)

        self.horizontal_layout.addStretch()
        self.btn_close = QToolButton()
        self.btn_close.setText("x")
        self.btn_close.setToolTip("Close tab")
        self.btn_close.setContentsMargins(0, 0, 0, 0)
        self.btn_close.setStyleSheet("background-color: transparent; text-align: center; font-size: 14px")
        self.btn_close.released.connect(self.closeTab)
        self.horizontal_layout.addWidget(self.btn_close)

        self.setLayout(self.horizontal_layout)

    def mousePressEvent(self, QMouseEvent):
        """
        opens file of the path that the tab is holding
        :QMouseEvent: registers the mouse click
        :return: returns nothing
        """
        logging.info(self.path)
        self.tab_bar.openTab(self)

    def closeTab(self):
        """
        close out tab when called
        :return: returns nothing
        """
        logging.info(self.path)
        self.tab_bar.closeTab(self.path)