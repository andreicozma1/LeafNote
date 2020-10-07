import logging
import os

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QTextDocument, QPixmap, QIcon, QTransform
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QTextEdit


class Find(QWidget):
    def __init__(self, document):
        super(Find, self).__init__()
        self.document = document
        self.search = ""
        self.flags = QTextDocument.FindFlag(0)

        self.initUI()

    def initUI(self):
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setAlignment(Qt.AlignLeft)
        self.horizontal_layout.setSpacing(0)
        self.setLayout(self.horizontal_layout)

        # set the background
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('pink'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        # self.horizontal_layout.addStretch()

        # add the qLineEdit
        self.search_bar = QLineEdit()
        self.search_bar.setContentsMargins(0, 0, 0, 0)
        self.search_bar.textChanged[str].connect(self.onChanged)
        self.search_bar.setFixedWidth(200)
        self.horizontal_layout.addWidget(self.search_bar, 0, Qt.AlignLeft)

        def createSearchBtn(title, tool_tip, on_click, isCheckable: bool = True):
            btn = QPushButton(title)
            btn.setContentsMargins(0, 0, 0, 0)
            btn.setToolTip(tool_tip)
            btn.setCheckable(isCheckable)
            btn.setFlat(True)
            btn.setFixedWidth(25)
            btn.clicked.connect(on_click)
            return btn

        # add the case sensitive option
        self.case_sensitive = createSearchBtn("Aa", "Match Case", self.onCaseSensitiveSearchSelect)
        self.horizontal_layout.addWidget(self.case_sensitive)

        # add the case sensitive option
        self.whole_word = createSearchBtn("W", "Words", self.onWholeWordSearchSelect)
        self.horizontal_layout.addWidget(self.whole_word)

        # add the case sensitive option
        self.regex_search = createSearchBtn(".*", "Regex", self.onRegexSearchSelect)
        self.horizontal_layout.addWidget(self.regex_search)

        # get required images
        path = os.path.join("resources", "arrow.ico")
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


    def onCaseSensitiveSearchSelect(self):
        if self.regex_search.isChecked():
            self.case_sensitive.setChecked(False)
        self.onChanged(self.search_bar.text())

    def onWholeWordSearchSelect(self):
        if self.regex_search.isChecked():
            self.whole_word.setChecked(False)
        self.onChanged(self.search_bar.text())

    def onRegexSearchSelect(self):
        if self.regex_search.isChecked():
            self.case_sensitive.setChecked(False)
            self.whole_word.setChecked(False)
        self.onChanged(self.search_bar.text())

    def onPreviousOccurrenceSelect(self):
        logging.info(self.document.find(self.search, self.flags | QTextDocument.FindBackward))

    def onNextOccurrenceSelect(self):
        logging.info(self.document.find(self.search, self.flags))

    # when text is entered in search through the document
    def onChanged(self, search):
        logging.info(search)
        self.search = search

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


class FindAll(QWidget):
    def __init__(self, path):
        super(FindAll, self).__init__()
        self.path = path
