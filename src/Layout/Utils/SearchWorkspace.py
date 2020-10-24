"""
This module holds the widget to display all search results in a given workspace
"""

import logging
import os
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QScrollArea, QTextEdit, QSplitter, \
    QTreeView, QAbstractItemView


class Item(QStandardItem):
    def __init__(self, path):
        file_name = QFileInfo(path).fileName()
        self.path = path
        super().__init__(file_name)


class FileViewer(QTreeView):
    def __init__(self, search_workspace):
        super().__init__()
        self.search_workspace = search_workspace

        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setHeaderHidden(True)

        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.clicked.connect(self.onSelection)
        self.doubleClicked.connect(self.onDoubleClick)
        self.selectionModel().currentRowChanged.connect(self.onSelection)

    def insertFile(self, path):
        item = Item(path)
        self.model.appendRow(item)

    def clearFiles(self):
        self.model.clear()

    def onSelection(self, index):
        item = self.model.itemFromIndex(index)
        data = self.search_workspace.file_manager.getFileData(item.path)
        self.search_workspace.display.setText(data)

    def onDoubleClick(self,index):
        item = self.model.itemFromIndex(index)
        self.search_workspace.file_manager.openDocument(self.search_workspace.document, item.path)
        self.search_workspace.close()


class SearchWorkspace(QWidget):
    """
    Widget that handles searching through the current workspace.
    """

    def __init__(self, document, file_manager, path):
        """
        Sets up the widgets properties
        :param document: reference to the document
        :param file_manager: reference to the file manager
        :param path: path of the current workspace
        """
        super().__init__()
        logging.debug("Creating Search Workspace")

        self.document = document
        self.file_manager = file_manager
        self.path = path

        self.file_viewer = FileViewer(self)

        self.initUI()
        self.show()

    def initUI(self):
        """
        Sets up the widgets layout and appearance
        :return:
        """
        # set window properties
        self.setFixedWidth(400)
        self.setWindowTitle("Search Workspace")

        # create the overarching vbox layout for the widget
        self.vertical_layout = QVBoxLayout(self)

        # add the qLineEdit as a search bar
        self.search_bar = QLineEdit()
        self.search_bar.setContentsMargins(0, 0, 0, 0)
        self.search_bar.textChanged[str].connect(self.onChanged)
        self.search_bar.setFixedWidth(375)
        self.search_bar.setStyleSheet("QLineEdit {background: rgb(218, 218, 218)}")

        # create the layout to hold the search results
        self.vertical_layout.addWidget(self.search_bar, alignment=Qt.AlignLeft)


        # -----------------------------------------------------------------

        splitter = QSplitter(QtCore.Qt.Vertical)  # Splitter between files and display

        splitter.addWidget(self.file_viewer)

        # add a q text edit to display the selected file
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        splitter.addWidget(self.display)

        self.vertical_layout.addWidget(splitter)


    def onChanged(self, search):
        """
        when the search text gets changed query the workspace for the search phrase
        :param search: phrase to search for
        :return: returns nothing
        """

        # clear the the previous query
        self.file_viewer.clearFiles()

        if search == "":
            return

        # get a list of all files in the workspace
        files = getAllFiles(self.path)

        # for each file in the list open it and look for the search word
        for f in files:
            # if the file is a file and it can be opened
            if os.path.isfile(f):
                with open(f, 'r') as file:
                    if file.closed:
                        continue
                    try:
                        # get the files text
                        data = file.read()
                    except OSError as e:
                        logging.exception(e)
                        logging.error("Could not read %s", f)

                # if the search phrase is in the file add a button to the scroll area
                if search in data or search in f:
                    self.file_viewer.insertFile(f)
                file.close()


def getAllFiles(path):
    """
    returns a list of all files from the given path down the tree
    :param path: a path to the directory to get all files from
    :return: returns a list of files in the given directory
    """
    return [os.path.join(r, file) for r, d, f in os.walk(path) for file in f]