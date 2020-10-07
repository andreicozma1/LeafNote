import logging
import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QTextDocument, QPixmap, QIcon, QTransform
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel


############################################################################
# SEARCH CURRENT FILE

class SearchFile(QWidget):
    def __init__(self, document):
        logging.info("")
        super(SearchFile, self).__init__(document)
        self.document = document
        self.search = ""
        self.flags = QTextDocument.FindFlag(0)

        self.initUI()
        self.hide()

    def initUI(self):
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

        self.setFixedWidth(400)
        self.setFixedHeight(self.height())

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


class FindWorkspace(QWidget):
    def __init__(self, path):
        super(FindWorkspace, self).__init__()
        self.path = path
