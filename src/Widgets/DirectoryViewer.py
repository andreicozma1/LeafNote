"""
This module holds a class that will display the current workspace to the user
"""
import logging
import os

from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QAbstractItemView, QShortcut

from Utils.Encryptor import Encryptor


class DirectoryViewer(QTreeView):
    """
    displays interactive directory on
    left side of text editor
    """

    def __init__(self, layout_props, document, file_manager, path=None):
        """
        creates the directory display
        :param file_manager: instance of FileManager class - manages all file communication
        :param path: default path to file being displayed
        :return: returns nothing
        """
        super().__init__()
        logging.debug("Creating Directory Viewer")
        self.layout_props = layout_props
        self.document = document
        self.fileManager = file_manager

        if path is None:
            path = QDir.currentPath()

        self.model = QFileSystemModel()

        item_height = str(layout_props.item_height)
        prop_bar_height = str(layout_props.header_margin)
        prop_header_color = layout_props.header_color
        prop_item_hover_color = layout_props.item_hover_color

        style = "QTreeView::item { height: " + item_height + "px; }" + \
                "QTreeView::item:selected {" \
                "background-color: " + prop_header_color + "; }" + \
                "QTreeView::item:hover:!selected { background-color: " \
                + prop_item_hover_color + "; }" + \
                "QHeaderView::section { margin: " + prop_bar_height + ";" + \
                " margin-left: 0; " \
                " background-color: rgb(56, 90, 125);" \
                " color: white; }"
        self.setStyleSheet(style)
        self.updateDirectory(path)

    def updateDirectory(self, path):
        """
        works on the visuals and functionality of as user navigates through the open directory
        :param path: default path to file being displayed
        :return: returns nothing
        """
        logging.info(path)

        self.model.setRootPath(path)

        self.setModel(self.model)
        self.setRootIndex(self.model.index(path))

        # Default hide all columns
        for i in range(1, self.model.columnCount()):
            name = self.model.headerData(i, Qt.Horizontal)
            if name not in self.layout_props.default_left_menu_cols:
                self.hideColumn(i)

        # make these functionsPath.home()
        self.setAnimated(True)
        self.setIndentation(10)
        self.setSortingEnabled(True)
        self.sortByColumn(1, Qt.AscendingOrder)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        # Expand or collapse directory on click
        self.clicked.connect(self.onClickDir)
        # Shortcut for pressing enter on directory
        shortcut = QShortcut(Qt.Key_Return, self)
        shortcut.activated.connect(self.onClickDir)
        # Open documents on selection changed
        self.selectionModel().currentRowChanged.connect(self.onSelectionChanged)

        self.fileManager.encryptor = None
        # Check for encryption key in Workspace
        path_key = os.path.join(path, ".leafCryptoKey")
        if os.path.exists(path_key):
            logging.debug("Encryption key found! %s", path_key)
            with open(path_key, 'r') as f:
                key = f.read()
                self.fileManager.encryptor = Encryptor(key)
        else:
            logging.info("Workspace not encrypted")

    def onSelectionChanged(self, index):
        """
        functionality of double click on directory
        :param index: location of filePath
        :return: returns nothing
        """
        path = self.model.filePath(index)
        logging.info(path)
        if not self.model.isDir(index):
            logging.debug("Selected document")
            self.fileManager.openDocument(self.document, path)

    def onClickDir(self, index=None):
        """
        functionality of double click on directory
        :param index: location of filePath
        :return: returns nothing
        """
        # If coming from Enter Pressed, resolve index
        if index is None:
            index = self.selectionModel().currentIndex()
        path = self.model.filePath(index)
        # Toggle expand/collapse directory
        if self.model.isDir(index):
            if self.isExpanded(index):
                logging.debug("Collapsing dir %s", path)
                self.collapse(index)
            else:
                logging.debug("Expanding dir %s", path)
                self.expand(index)

    def toggleHeader(self, name: str):
        """
        Shows or Hides a column based on it's name
        """
        for i in range(1, self.model.columnCount()):
            col_name = self.model.headerData(i, Qt.Horizontal)
            if col_name == name:
                self.setColumnHidden(i, not self.isColumnHidden(i))

    def resizeColumnsToContent(self):
        """
        Resizes all columns to fit content
        """
        for i in range(1, self.model.columnCount()):
            self.resizeColumnToContents(i)

    def selectPath(self, path: str):
        """
        "Programmatically selects a path in the File System model
        """
        self.setCurrentIndex(self.model.index(path))
