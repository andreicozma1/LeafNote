"""
This module holds the widget to display all search results in a given workspace
"""

import logging
import os
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QFileInfo, QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QKeySequence, QTextDocument
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QSplitter, \
    QTreeView, QAbstractItemView, QShortcut, QPushButton, QHBoxLayout


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
        self.search_workspace.onNextOccurrenceSelect()

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

        self.search_bar = None
        self.case_sensitive = None
        self.whole_word = None
        self.regex_search = None
        self.display = None

        self.file_viewer = FileViewer(self)
        self.close_dialog_callback = None
        self.flags = QTextDocument.FindFlag(0)
        self.search = ""

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
        vertical_layout = QVBoxLayout(self)

        # -------------------------------------------------------------------
        # create layout to hold the search bar and filters
        widget = QWidget()
        search_layout = QHBoxLayout(widget)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setAlignment(Qt.AlignLeft)
        search_layout.setSpacing(3)

        # add the qLineEdit as a search bar
        self.search_bar = QLineEdit()
        self.search_bar.setContentsMargins(0, 0, 0, 0)
        self.search_bar.textChanged[str].connect(self.onChanged)
        self.search_bar.setFixedWidth(298)
        self.search_bar.setStyleSheet("QLineEdit {background: rgb(218, 218, 218)}")

        # create shortcuts for the line edit
        def createShortcut(keys, shortcut_object, action):
            shortcut = QShortcut(QKeySequence(keys), shortcut_object)
            shortcut.activated.connect(partial(action, True))

        createShortcut(Qt.Key_Up, self.search_bar, self.onPreviousFile)
        createShortcut(Qt.Key_Down, self.search_bar, self.onNextFile)
        createShortcut(Qt.Key_Return, self.search_bar, self.openFile)

        # create the layout to hold the search results
        search_layout.addWidget(self.search_bar)

        def createSearchBtn(title, tool_tip, on_click, is_checkable: bool = True):
            """
            """
            btn = QPushButton(title)
            btn.setContentsMargins(0, 0, 0, 0)
            btn.setToolTip(tool_tip)
            btn.setCheckable(is_checkable)
            btn.setFlat(True)
            btn.setFixedWidth(25)
            btn.clicked.connect(on_click)
            return btn

        # add the case sensitive option
        self.case_sensitive = createSearchBtn("Aa", "Match Case", self.onCaseSensitiveSearchSelect)
        createShortcut(Qt.ALT + Qt.Key_C, self.case_sensitive, self.onCaseSensitiveSearchSelect)
        search_layout.addWidget(self.case_sensitive, alignment=Qt.AlignLeft)

        # add the case sensitive option
        self.whole_word = createSearchBtn("W", "Words", self.onWholeWordSearchSelect)
        createShortcut(Qt.ALT + Qt.Key_O, self.whole_word, self.onWholeWordSearchSelect)
        search_layout.addWidget(self.whole_word, alignment=Qt.AlignLeft)

        # add the case sensitive option
        self.regex_search = createSearchBtn(".*", "Regex", self.onRegexSearchSelect)
        createShortcut(Qt.ALT + Qt.Key_X, self.regex_search, self.onRegexSearchSelect)
        search_layout.addWidget(self.regex_search, alignment=Qt.AlignLeft)

        search_layout.addStretch()
        vertical_layout.addWidget(widget)

        # -------------------------------------------------------------------

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
        vertical_layout.addWidget(splitter)

        # -------------------------------------------------------------------

        widget = QWidget()
        button_hbox = QHBoxLayout(widget)
        button_hbox.setContentsMargins(0, 0, 0, 0)
        button_hbox.setSpacing(3)

        # button to go to the previous occurrence
        previous_occurrence = QPushButton("Previous")
        previous_occurrence.setFixedWidth(80)
        previous_occurrence.clicked.connect(self.onPreviousOccurrenceSelect)
        button_hbox.addWidget(previous_occurrence, alignment=Qt.AlignRight)

        # button to go to the next occurrence
        next_occurrence = QPushButton("Next")
        next_occurrence.setFixedWidth(80)
        next_occurrence.clicked.connect(self.onNextOccurrenceSelect)
        button_hbox.addWidget(next_occurrence, alignment=Qt.AlignRight)

        # create button top open the selected file
        open_file = QPushButton("Open File")
        open_file.setFixedWidth(80)
        open_file.clicked.connect(self.openFile)
        button_hbox.addWidget(open_file, alignment=Qt.AlignRight)

        vertical_layout.addWidget(widget, alignment=Qt.AlignRight)

    def setCloseDialogCallback(self, callback):
        """
        sets the callback function that is called when the widget is closed
        :param callback: the callback function to be called
        :return: returns nothing
        """
        self.close_dialog_callback = callback

    def onCaseSensitiveSearchSelect(self, from_shortcut=False):
        """
        handles the button click for the case sensitive search
        """
        logging.info("Clicked Case Sensitive")
        if from_shortcut:
            self.case_sensitive.setChecked(not self.case_sensitive.isChecked())
        if self.regex_search.isChecked():
            self.case_sensitive.setChecked(False)
        self.onChanged(self.search_bar.text())

    def onWholeWordSearchSelect(self, from_shortcut=False):
        """
        handles the button click for the whole word search
        """
        logging.info("Clicked Whole Word")
        if from_shortcut:
            self.whole_word.setChecked(not self.whole_word.isChecked())
        if self.regex_search.isChecked():
            self.whole_word.setChecked(False)
        self.onChanged(self.search_bar.text())

    def onRegexSearchSelect(self, from_shortcut=False):
        """
        handles the button click for the regex search
        """
        logging.info("Clicked Regex")
        if from_shortcut:
            self.regex_search.setChecked(not self.regex_search.isChecked())
        if self.regex_search.isChecked():
            self.case_sensitive.setChecked(False)
            self.whole_word.setChecked(False)
        self.onChanged(self.search_bar.text())

    def onPreviousFile(self, from_shortcut=False):
        """
        moves to the previous shown file
        :return: returns nothing
        """
        if from_shortcut:
            logging.debug("User selected previous file")
        index = self.file_viewer.currentIndex()
        index = self.file_viewer.indexAbove(index)
        self.file_viewer.setCurrentIndex(index)

    def onNextFile(self, from_shortcut=False):
        """
        moves to the next shown file
        :return: returns nothing
        """
        if from_shortcut:
            logging.debug("User selected next file")
        index = self.file_viewer.currentIndex()
        index = self.file_viewer.indexBelow(index)
        self.file_viewer.setCurrentIndex(index)

    def openFile(self, from_shortcut=False):
        """
        opens the selected file
        :returns nothing
        """
        if from_shortcut:
            logging.debug("User opening file from shortcut")
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
                # if the search phrase is in the file add a button to the scroll area
                if self.searchFile(f, search) or str(search) in f:
                    self.file_viewer.insertFile(f)

        # set the focus on the first search result
        # index = self.file_viewer.indexBelow(self.file_viewer.rootIndex())
        index = self.file_viewer.model.index(0, 0)
        self.file_viewer.setCurrentIndex(index)
        self.onNextOccurrenceSelect()

    def searchFile(self, file_name: str, search: str) -> bool:
        """
        this will search the given file for the search string
        :return: returns if the search string is in the file
        """
        text_edit = QTextEdit()
        text_edit.setText(self.file_manager.getFileData(file_name))
        self.search = search

        # set the cursor to the beginning of the document
        cursor = text_edit.textCursor()
        cursor.setPosition(0)
        text_edit.setTextCursor(cursor)

        # set up the default search flags
        self.flags = QTextDocument.FindFlag(0)

        # if search is case sensitive
        if self.case_sensitive.isChecked():
            self.flags = self.flags | QTextDocument.FindCaseSensitively

        # if search is whole word sensitive
        if self.whole_word.isChecked():
            self.flags = self.flags | QTextDocument.FindWholeWords

        # if the user IS searching for regex
        if self.regex_search.isChecked():
            self.search = QRegExp(self.search)

        return text_edit.find(self.search, self.flags)

    def onPreviousOccurrenceSelect(self):
        """
        handles the button click for the previous occurrence search
        """
        logging.info("Clicked Previous")
        self.display.find(self.search, self.flags | QTextDocument.FindBackward)

    def onNextOccurrenceSelect(self):
        """
        handles the button click for the next occurrence search
        """
        logging.info("Clicked Next")
        self.display.find(self.search, self.flags)

def getAllFiles(path):
    """
    returns a list of all files from the given path down the tree
    :param path: a path to the directory to get all files from
    :return: returns a list of files in the given directory
    """
    return [os.path.join(r, file) for r, d, f in os.walk(path) for file in f]
