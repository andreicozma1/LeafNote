"""
when one or more file is open it
will show the file tabs under the
top bar
"""

import logging

from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QTabBar, QFileIconProvider


class OpenTabsBar(QTabBar):
    """
    functionality and look of Tab Bar
    """

    def __init__(self, document, file_manager):
        """
        sets up the tab bar
        :param document: doc reference for operations
        :param file_manager: instance of FileManager class - manages all file communication
        :return: returns nothing
        """
        super().__init__()
        logging.debug("Creating Open Tabs Bar")

        self.document = document
        self.file_manager = file_manager

        self.open_tabs = {}
        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.currentChanged.connect(self.openTab)
        self.tabCloseRequested.connect(self.closeTab)

    def openTab(self, index):
        """
        Opens a tab
        """
        logging.debug("Clicked on tab %d", index)
        path = self.tabData(index)
        if path is not None:
            self.file_manager.openDocument(self.document, path)

    def addTab(self, path: str):
        """
        Creates new tab and adds it to the horizontal layout
        :param path: path to file being displayed
        :return: returns the new tab that was open
        """
        logging.info(path)
        file_info = QFileInfo(path)
        # Add new tab and save index
        index = super().addTab(file_info.fileName())
        # Set tab data and tooltip
        self.setTabData(index, path)
        self.setTabToolTip(index, path)
        # Set tab icon
        icon_provider = QFileIconProvider()
        self.setTabIcon(index, icon_provider.icon(file_info))
        # Update the current index to the new tab
        self.blockSignals(True)
        self.setCurrentIndex(index)
        self.blockSignals(False)
        # add tab to the dict holding open tabs
        self.open_tabs[path] = index

    def closeTab(self, index, save: bool = True):
        """
        removes object from layout and destroys it
        :param index: index of tab to close
        :param save: if the document is saved
        :return: returns nothing
        """
        logging.info(index)
        path = self.tabData(index)
        self.removeTab(index)
        if save:
            self.file_manager.saveDocument(self.document)
        self.file_manager.closeDocument(self.document, path)

        if path in self.open_tabs:
            # pop the closed tab from the open tab dic
            self.open_tabs.pop(path)

    def forceCloseTab(self, path: str):
        """
        removes object from layout and destroys it
        :param path: path of tab to close
        :return: returns nothing
        """
        logging.info(path)
        self.removeTab(self.open_tabs[path])
        self.file_manager.closeDocument(self.document, path)
        if path in self.open_tabs:
            # pop the closed tab from the open tab dic
            self.open_tabs.pop(path)
