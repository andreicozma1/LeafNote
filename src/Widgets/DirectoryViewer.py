"""
This module holds a class that will display the current workspace to the user
"""
import logging
import os

from PyQt5.QtCore import Qt, QDir, QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QAbstractItemView, QShortcut

from Utils.Encryptor import Encryptor


class DirectoryViewer(QTreeView):
    """
    displays interactive directory on
    left side of text editor
    """

    def __init__(self, layout_props, document, file_manager, abs_path=None):
        """
        creates the directory display
        :param file_manager: instance of FileManager class - manages all file communication
        :param abs_path: default path to file being displayed
        :return: returns nothing
        """
        super().__init__()
        logging.debug("Creating Directory Viewer")
        self.layout_props = layout_props
        self.document = document
        self.fileManager = file_manager

        if abs_path is None:
            abs_path = QDir.currentPath()

        self.model = QFileSystemModel()

        self.initUI()
        self.updateDirectory(abs_path)

        self.updateAppearance()

    def initUI(self):
        """
        Initializes the Directory Viewer properties, signals, and model
        :return: returns nothing
        """
        logging.debug("Initializing Directory Viewer Props")
        self.setModel(self.model)

        # Default hide all columns except Name
        for i in range(1, self.model.columnCount()):
            name = self.model.headerData(i, Qt.Horizontal)
            if name not in self.layout_props.getDefaultLeftMenuCols():
                self.hideColumn(i)

        self.setAnimated(True)
        self.setIndentation(10)
        self.setSortingEnabled(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setExpandsOnDoubleClick(True)

        # Expand or collapse directory on click
        self.doubleClicked.connect(self.onClickItem)
        # Shortcut for pressing enter on directory
        shortcut = QShortcut(Qt.Key_Return, self)
        shortcut.activated.connect(self.onClickItem)

    def updateDirectory(self, abs_path: str):
        """
        Updates the path of the model to the given path, sorts, and looks for the encryption key.
        :param abs_path: default path to file being displayed
        :return: returns nothing
        """
        logging.info(abs_path)

        self.model.setRootPath(abs_path)
        self.setRootIndex(self.model.index(abs_path))
        self.sortByColumn(0, Qt.AscendingOrder)

        self.fileManager.encryptor = None
        # Check for encryption key in Workspace
        path_key = os.path.join(abs_path, ".leafCryptoKey")
        if os.path.exists(path_key):
            logging.debug("Encryption key found! %s", path_key)
            with open(path_key, 'r') as f:
                key = f.read()
                self.fileManager.encryptor = Encryptor(key)
        else:
            logging.info("Workspace not encrypted")

    def onClickItem(self, index: QModelIndex = None):
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
        if not self.model.isDir(index):
            logging.info("Opening document")
            self.fileManager.openDocument(self.document, path)

    def toggleHeaderColByName(self, name: str):
        """
        Shows or Hides a column based on it's name
        """
        logging.debug("Toggling header column %s", name)
        for i in range(1, self.model.columnCount()):
            col_name = self.model.headerData(i, Qt.Horizontal)
            if col_name == name:
                self.setColumnHidden(i, not self.isColumnHidden(i))

    def resizeColumnsToContent(self):
        """
        Resizes all columns to fit content
        """
        logging.debug("Resizing columns to contents")
        for i in range(1, self.model.columnCount()):
            self.resizeColumnToContents(i)

    def selectItemFromPath(self, path: str):
        """
        "Programmatically selects a path in the File System model
        """
        logging.debug("Selecting path %s", path)
        self.selectionModel().blockSignals(True)
        self.setCurrentIndex(self.model.index(path))
        self.selectionModel().blockSignals(False)

    def updateAppearance(self):
        """
        Updates the layout appearance based on properties
        """
        logging.debug("Setting up appearance")
        prop_header_margin = str(self.layout_props.getDefaultLeftMenuHeaderMargin())
        prop_header_color = self.layout_props.getDefaultHeaderColor()
        prop_item_height = str(self.layout_props.getDefaultItemHeight())
        prop_item_select_color = self.layout_props.getDefaultSelectColor()
        prop_item_hover_color = self.layout_props.getDefaultHoverColor()

        style = "QTreeView::item { height: " + prop_item_height + "px; }" + \
                "QTreeView::item:selected {" \
                "background-color: " + prop_item_select_color + "; }" + \
                "QTreeView::item:hover:!selected { " + \
                "background-color: " + prop_item_hover_color + "; }" + \
                "QHeaderView::section { margin: " + prop_header_margin + ";" + \
                " margin-left: 0; " + \
                " background-color: " + prop_header_color + ";" + \
                " color: white; }"
        self.setStyleSheet(style)
