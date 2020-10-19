import logging
import os
from functools import partial

from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QScrollArea, QPushButton


class File(QPushButton):
    """
    This is a button that holds information about the button
    """

    def __init__(self, path):
        """
        sets up the buttons properties
        :param path: the file the button is representing
        """
        super().__init__()
        self.path = path
        self.file_name = QFileInfo(path).fileName()
        self.initUI()

    def initUI(self):
        """
        sets up the buttons appearance
        :return: Returns nothing
        """
        self.setText(self.file_name)
        self.setMinimumHeight(20)


def getAllfiles(path):
    """
    returns a list of all files from the given path down the tree
    :param path: a path to the directory to get all files from
    :return: returns a list of files in the given directory
    """
    return [os.path.join(r, file) for r, d, f in os.walk(path) for file in f]


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

        # create the scroll area to display the search results
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)

        # create a widget to hold the vbox layout and to be placed in the scroll area
        widget = QWidget()
        self.search_results = QVBoxLayout()
        self.search_results.setAlignment(Qt.AlignTop)
        self.search_results.setSpacing(2)
        widget.setLayout(self.search_results)
        self.scroll.setWidget(widget)

        # add the scroll area to the main layout
        self.vertical_layout.addWidget(self.scroll)
        self.vertical_layout.addStretch()

    def onChanged(self, search):
        """
        when the search text gets changed query the workspace for the search phrase
        :param search: phrase to search for
        :return: returns nothing
        """

        # clear the the previous query
        self.clearSearchResults()

        # get a list of all files in the workspace
        files = getAllfiles(self.path)

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
                        logging.error("Could not read " + f)

                # if the search phrase is in the file add a button to the scroll area
                if search in data:
                    item = File(f)
                    item.clicked.connect(partial(self.onItemClicked, item))
                    self.search_results.addWidget(item)
                file.close()

    def onItemClicked(self, btn):
        """
        when an item is clicked open it on the document and close the search workspace widget
        :param btn: then button that has been clicked
        :return: Returns nothing
        """
        logging.info(btn.file_name)
        self.file_manager.openDocument(self.document, btn.path)
        self.close()

    def clearSearchResults(self):
        """
        Clears the vbox layout holding all the search results
        :return: returns nothing
        """
        for i in reversed(range(self.search_results.count())):
            self.search_results.itemAt(i).widget().deleteLater()
