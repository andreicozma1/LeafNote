"""
This module holds the widget to display all search results in a given workspace
"""

import logging
import os

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QKeySequence
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QSplitter, \
    QTreeView, QAbstractItemView, QShortcut, QPushButton


class Item(QStandardItem):
    """
    This is the item that is held in the tree view model
    """
    def __init__(self, path):
        """
        this initializes the item
        """
        self.file_name = QFileInfo(path).fileName()
        self.path = path
        super().__init__(self.file_name)

    def getFileName(self):
        """
        returns the file name held by the item
        :return: returns the file name
        """
        return self.file_name

    def getPath(self):
        """
        returns the path held by the item
        :return: returns the path
        """
        return self.path


class FileViewer(QTreeView):
    """
    This shows the relevant files to the search query
    """
    def __init__(self, search_workspace):
        """
        this initializes the viewer
        :param search_workspace: the trees parent
        """
        super().__init__()
        self.search_workspace = search_workspace
        self.model = QStandardItemModel()
        self.initUI()

    def initUI(self):
        """
        initializes the tree QTreeView
        :return: returns nothing
        """

        # create the model to be displayed
        self.setModel(self.model)

        # set the objects properties
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        # set all signals
        self.clicked.connect(self.onSelection)
        self.doubleClicked.connect(self.onDoubleClick)
        self.selectionModel().currentRowChanged.connect(self.onSelection)

    def insertFile(self, path):
        """
        this inserts a new item into the model
        :param path: the file the item represents
        :return: returns nothing
        """
        item = Item(path)
        self.model.appendRow(item)

    def clearFiles(self):
        """
        clears the model
        :return: returns nothing
        """
        self.model.clear()

    def onSelection(self, index):
        """
        handles when the user clicks on an item
        :param index: the index the user clicked on
        :return: returns nothing
        """
        # get the selected item
        item = self.model.itemFromIndex(index)

        # set the display to show the file
        data = self.search_workspace.file_manager.getFileData(item.path)
        self.search_workspace.display.setText(data)

    def onDoubleClick(self, index):
        """
        handles when the user double clicks on an item
        :param index: the index the user clicked on
        :return: returns nothing
        """
        # get the selected item
        item = self.model.itemFromIndex(index)

        # open the selected file and close widget
        self.search_workspace.file_manager.openDocument(self.search_workspace.document, item.path)
        self.search_workspace.closeWidget()


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
        self.close_dialog_callback = None

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

        # create shortcuts for the line edit
        prev_file_shortcut = QShortcut(QKeySequence(Qt.Key_Up), self.search_bar)
        prev_file_shortcut.activated.connect(self.onPreviousFile)
        next_file_shortcut = QShortcut(QKeySequence(Qt.Key_Down), self.search_bar)
        next_file_shortcut.activated.connect(self.onNextFile)

        # create the layout to hold the search results
        self.vertical_layout.addWidget(self.search_bar, alignment=Qt.AlignCenter)

        # Splitter between files and display
        splitter = QSplitter(QtCore.Qt.Vertical)

        # add the file viewer
        splitter.addWidget(self.file_viewer)
        splitter.setCollapsible(0, False)

        # add a q text edit to display the selected file
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        splitter.addWidget(self.display)

        # add splitter to main layout
        self.vertical_layout.addWidget(splitter)

        # create button top open the selected file
        open_file = QPushButton("Open File")
        open_file.setFixedWidth(80)
        open_file.clicked.connect(self.openFile)
        self.vertical_layout.addWidget(open_file, alignment=Qt.AlignRight)

    def setCloseDialogCallback(self, callback):
        """
        sets the callback function that is called when the widget is closed
        :param callback: the callback function to be called
        :return: returns nothing
        """
        self.close_dialog_callback = callback

    def onPreviousFile(self):
        """
        moves to the previous shown file
        :return: returns nothing
        """
        index = self.file_viewer.currentIndex()
        index = self.file_viewer.indexAbove(index)
        self.file_viewer.setCurrentIndex(index)

    def onNextFile(self):
        """
        moves to the next shown file
        :return: returns nothing
        """
        index = self.file_viewer.currentIndex()
        index = self.file_viewer.indexBelow(index)
        self.file_viewer.setCurrentIndex(index)

    def openFile(self):
        """
        opens the selected file
        :returns nothing
        """
        # get the selected file
        index = self.file_viewer.currentIndex()
        item = self.file_viewer.model.itemFromIndex(index)
        if item is not None:
            # open the file if one is selected
            self.file_manager.openDocument(self.document, item.path)
        self.closeWidget()

    def closeWidget(self):
        """
        closes the widget
        :return: returns nothing
        """
        self.close()
        if self.close_dialog_callback is not None:
            self.close_dialog_callback()

    def onChanged(self, search):
        """
        when the search text gets changed query the workspace for the search phrase
        :param search: phrase to search for
        :return: returns nothing
        """

        # clear the previous query
        self.file_viewer.clearFiles()
        self.display.setText("")

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
                if str(search) in data or str(search) in f:
                    self.file_viewer.insertFile(f)
                file.close()

        # set the focus on the first search result
        # index = self.file_viewer.indexBelow(self.file_viewer.rootIndex())
        index = self.file_viewer.model.index(0, 0)
        self.file_viewer.setCurrentIndex(index)


def getAllFiles(path):
    """
    returns a list of all files from the given path down the tree
    :param path: a path to the directory to get all files from
    :return: returns a list of files in the given directory
    """
    return [os.path.join(r, file) for r, d, f in os.walk(path) for file in f]
