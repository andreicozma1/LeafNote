import logging
import os
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRegExp, QFileInfo
from PyQt5.QtGui import QTextDocument, QPixmap, QIcon, QTransform
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel, QVBoxLayout, QScrollArea


############################################################################
# SEARCH CURRENT FILE


class SearchFile(QWidget):
    """
    This is a widget to search for users input in the current document
    """

    def __init__(self, path_res, document):
        """
        Sets up the search bar widget
        :param document: reference to the document
        """
        logging.info("")
        super(SearchFile, self).__init__(document)
        self.document = document
        self.path_res = path_res
        self.search = ""
        self.flags = QTextDocument.FindFlag(0)

        self.initUI()
        self.hide()

    def initUI(self):
        """
        Sets up the layout of the search widget
        :return: Returns nothing
        """
        # create the overarching hbox layout of the widget
        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(2, 0, 0, 0)
        self.horizontal_layout.setAlignment(Qt.AlignLeft)
        self.horizontal_layout.setSpacing(0)

        # set the background
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#dadada'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # add the qLineEdit
        self.search_bar = QLineEdit()
        self.search_bar.setContentsMargins(0, 0, 0, 0)
        self.search_bar.textChanged[str].connect(self.onChanged)
        self.search_bar.setFixedWidth(200)
        self.search_bar.setStyleSheet("QLineEdit {background: rgb(218, 218, 218)}")
        self.horizontal_layout.addWidget(self.search_bar, 0, Qt.AlignLeft)

        # add label to count occurrences
        self.occurances = QLabel("0 Results")
        self.occurances.setStyleSheet("QLabel {color: rgba(0,0,0,.5)}")
        self.occurances.setContentsMargins(10, 0, 0, 0)
        self.horizontal_layout.addWidget(self.occurances)

        self.horizontal_layout.addStretch()

        def createSearchBtn(title, tool_tip, on_click, is_checkable: bool = True):
            """
            this funciton will create a customized q push button
            :param title: title of the button
            :param tool_tip: tooltip of the button
            :param on_click: the signal function of the button
            :param is_checkable: sets the is checkable property
            :return: Returns the newly created q push button
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
        self.horizontal_layout.addWidget(self.case_sensitive, 0, Qt.AlignLeft)

        # add the case sensitive option
        self.whole_word = createSearchBtn("W", "Words", self.onWholeWordSearchSelect)
        self.horizontal_layout.addWidget(self.whole_word, 0, Qt.AlignLeft)

        # add the case sensitive option
        self.regex_search = createSearchBtn(".*", "Regex", self.onRegexSearchSelect)
        self.horizontal_layout.addWidget(self.regex_search, 0, Qt.AlignLeft)

        # get required images
        path = os.path.join(self.path_res, "arrow.ico")
        pixmap = QPixmap(path)
        down_arrow = QIcon(pixmap)
        up_arrow = QIcon(pixmap.transformed(QTransform().rotate(180)))

        # add the previous occurrence option
        self.previous_occurrence = createSearchBtn("", "Previous Occurrence", self.onPreviousOccurrenceSelect, False)
        self.previous_occurrence.setIcon(up_arrow)
        self.horizontal_layout.addWidget(self.previous_occurrence)

        # add the next occurrence option
        self.next_occurrence = createSearchBtn("", "Next Occurrence", self.onNextOccurrenceSelect, False)
        self.next_occurrence.setIcon(down_arrow)
        self.horizontal_layout.addWidget(self.next_occurrence)

        self.setFixedWidth(400)
        self.setFixedHeight(self.height())

    def onCaseSensitiveSearchSelect(self):
        """
        defines what happens when the case sensitive button is pressed
        :return: Returns nothing
        """
        if self.regex_search.isChecked():
            self.case_sensitive.setChecked(False)
        self.onChanged(self.search_bar.text())

    def onWholeWordSearchSelect(self):
        """
        defines what happens when the whole word button is pressed
        :return: returns nothing
        """
        if self.regex_search.isChecked():
            self.whole_word.setChecked(False)
        self.onChanged(self.search_bar.text())

    def onRegexSearchSelect(self):
        """
        defines what happens when the regex search button is pressed
        :return: returns nothing
        """
        if self.regex_search.isChecked():
            self.case_sensitive.setChecked(False)
            self.whole_word.setChecked(False)
        self.onChanged(self.search_bar.text())

    def onPreviousOccurrenceSelect(self):
        """
        defines what happens when the user searches for the previous selection with the up arrow button
        :return: Returns nothing
        """
        logging.info(self.document.find(self.search, self.flags | QTextDocument.FindBackward))

    def onNextOccurrenceSelect(self):
        """
        defines what happens when the user searches for the next selection with the down arrow button
        :return: Returns nothing
        """
        logging.info(self.document.find(self.search, self.flags))

    def onChanged(self, search):
        """
        When the text is changed reset and query for the new search phrase
        :param search: The phrase to search for
        :return: Returns nothing
        """

        logging.info(search)
        self.search = search

        # update the number of occurrences of the search
        if search != "":
            self.occurances.setText(str(self.document.toPlainText().count(search)) + " Results")
        else:
            self.occurances.setText("0 Results")

        # set the cursor to the beginning of the document
        cursor = self.document.textCursor()
        cursor.setPosition(0)
        self.document.setTextCursor(cursor)

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

        logging.info(self.document.find(self.search, self.flags))


############################################################################
# SEARCH CURRENT WORKSPACE


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
        super(SearchWorkspace, self).__init__()
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
        self.vertical_layout.addWidget(self.search_bar, 0, Qt.AlignLeft)

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
        files = self.getAllfiles(self.path)

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
                    except:
                        logging.error("Could not read " + f)

                # if the search phrase is in the file add a button to the scroll area
                if search in data:
                    item = File(f)
                    item.clicked.connect(partial(self.onItemClicked, item))
                    self.search_results.addWidget(item)
                file.close()

    def getAllfiles(self, path):
        """
        returns a list of all files from the given path down the tree
        :param path: a path to the directory to get all files from
        :return: returns a list of files in the given directory
        """
        return [os.path.join(r, file) for r, d, f in os.walk(path) for file in f]

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


class File(QPushButton):
    """
    This is a button that holds information about the button
    """

    def __init__(self, path):
        """
        sets up the buttons properties
        :param path: the file the button is representing
        """
        super(File, self).__init__()
        self.path = path
        self.file_name = QFileInfo(path).fileName()
        self.setUI()

    def setUI(self):
        """
        sets up the buttons appearance
        :return: Returns nothing
        """
        self.setText(self.file_name)
        self.setMinimumHeight(20)
