"""
This module contains a widget that gives the user the ability to search through a document
"""
import html
import logging
from functools import partial

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QTextDocument, QKeySequence
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel, QShortcut


class SearchDoc(QWidget):
    """
    This is a widget to search for users input in the current document
    """

    def __init__(self, search_and_replace, document, path_res):
        """
        Sets up the search bar widget
        :param document: reference to the document
        """
        super().__init__()
        logging.debug("Created Search Widget")

        self.search_and_replace = search_and_replace
        self.document = document
        self.path_res = path_res
        self.search = ""
        self.current = 0
        self.total = 0
        self.flags = QTextDocument.FindFlag(0)

        self.initUI()
        self.hide()

    def initUI(self):
        """
        Sets up the layout of the search widget
        :return: Returns nothing
        """
        logging.debug("Setting up UI")
        # create the overarching hbox layout of the widget
        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(2, 0, 0, 0)
        self.horizontal_layout.setAlignment(Qt.AlignLeft)
        self.horizontal_layout.setSpacing(3)

        # -----------------------------------------------------------

        # add the qLineEdit
        self.search_bar = QLineEdit()
        self.search_bar.setContentsMargins(0, 0, 0, 0)
        self.search_bar.textChanged[str].connect(self.onChanged)
        self.search_bar.setFixedWidth(200)
        self.search_bar.setStyleSheet("QLineEdit {background: rgb(218, 218, 218)}")
        self.horizontal_layout.addWidget(self.search_bar, alignment=Qt.AlignLeft)

        # -----------------------------------------------------------

        # add label to count occurrences
        self.occurances = QLabel("0/0")
        self.occurances.setStyleSheet("QLabel {color: rgba(0,0,0,.5)}")
        self.occurances.setContentsMargins(10, 0, 0, 0)
        self.occurances.setContentsMargins(10, 0, 0, 0)
        self.horizontal_layout.addWidget(self.occurances)

        # -----------------------------------------------------------

        def createSearchBtn(title, tool_tip, on_click, is_checkable: bool = True,
                            extra_on_click_param: bool = False):
            """
            Creates buttons for the search bar
            """
            btn = QPushButton(title)
            btn.setContentsMargins(0, 0, 0, 0)
            btn.setToolTip(tool_tip)
            btn.setCheckable(is_checkable)
            btn.setFlat(True)
            btn.setFixedWidth(25)
            if extra_on_click_param:
                btn.clicked.connect(partial(on_click, False))
            else:
                btn.clicked.connect(on_click)
            return btn

        # add the case sensitive option
        self.case_sensitive = createSearchBtn("Aa", "Match Case",
                                              self.onCaseSensitiveSearchSelect, True, True)
        self.case_sensitive_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_C),
                                                 self.case_sensitive)
        self.case_sensitive_shortcut.activated.connect(
            partial(self.onCaseSensitiveSearchSelect, True)
        )
        self.horizontal_layout.addWidget(self.case_sensitive, alignment=Qt.AlignLeft)

        # add the case sensitive option
        self.whole_word = createSearchBtn("W", "Words", self.onWholeWordSearchSelect, True, True)
        self.whole_word_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_O), self.whole_word)
        self.whole_word_shortcut.activated.connect(partial(self.onWholeWordSearchSelect, True))
        self.horizontal_layout.addWidget(self.whole_word, alignment=Qt.AlignLeft)

        # add the case sensitive option
        self.regex_search = createSearchBtn(".*", "Regex", self.onRegexSearchSelect, True, True)
        self.regex_search_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_X), self.regex_search)
        self.regex_search_shortcut.activated.connect(partial(self.onRegexSearchSelect, True))
        self.horizontal_layout.addWidget(self.regex_search, alignment=Qt.AlignLeft)

        # -----------------------------------------------------------

        # add the previous occurrence option
        self.previous_occurrence = createSearchBtn(html.unescape('&#8593;'), "Previous Occurrence",
                                                   self.onPreviousOccurrenceSelect, False)
        self.previous_occurrence_shortcut = QShortcut(QKeySequence(Qt.SHIFT + Qt.Key_Return),
                                                      self.previous_occurrence)
        self.previous_occurrence_shortcut.activated.connect(self.onPreviousOccurrenceSelect)
        self.horizontal_layout.addWidget(self.previous_occurrence)

        # add the next occurrence option
        self.next_occurrence = createSearchBtn(html.unescape('&#8595;'), "Next Occurrence",
                                               self.onNextOccurrenceSelect, False)
        self.next_occurrence_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self.next_occurrence)
        self.next_occurrence_shortcut.activated.connect(self.search_and_replace.nextOccurrence)
        self.horizontal_layout.addWidget(self.next_occurrence)

        # -----------------------------------------------------------

        self.horizontal_layout.addStretch()

        # -----------------------------------------------------------

        # exit button
        self.close_search = createSearchBtn(html.unescape("&times;"), "Close Search Bar",
                                            self.search_and_replace.closeSearchAndReplace)
        self.close_search_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self.close_search)
        self.close_search_shortcut.activated.connect(self.search_and_replace.closeSearchAndReplace)
        self.horizontal_layout.addWidget(self.close_search)

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

    def onPreviousOccurrenceSelect(self):
        """
        handles the button click for the previous occurrence search
        """
        logging.info("Clicked Previous")
        self.document.find(self.search, self.flags | QTextDocument.FindBackward)
        if self.current - 1 >= 1:
            self.current -= 1
            self.occurances.setText(str(self.current) + '/' + str(self.total))

    def onNextOccurrenceSelect(self):
        """
        handles the button click for the next occurrence search
        """
        logging.info("Clicked Next")
        self.document.find(self.search, self.flags)
        if self.current + 1 <= self.total:
            self.current += 1
            self.occurances.setText(str(self.current) + '/' + str(self.total))

    def onCloseSearch(self):
        """
        handles the button click to close the search widget
        """
        logging.info("Clicked Close")
        self.search_and_replace.replace.setVisible(False)
        self.setVisible(False)

    def onChanged(self, search):
        """
        this handles any change the user makes to the search bar
        """
        self.search = search

        # update the number of occurrences of the search
        self.total = self.document.toPlainText().count(search)
        if self.total == 0:
            self.current = 0
        else:
            self.current = 1

        self.occurances.setText(str(self.current) + '/' + str(self.total))

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
        self.document.find(self.search, self.flags)
