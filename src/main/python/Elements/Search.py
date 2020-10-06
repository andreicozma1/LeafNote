import logging

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QTextEdit


class Find(QWidget):
    def __init__(self, document):
        super(Find, self).__init__()
        self.document = document

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

        # add the case sensitive option
        self.case_sensitive = QPushButton("Aa")
        self.case_sensitive.setContentsMargins(0, 0, 0, 0)
        self.case_sensitive.setToolTip("Match Case")
        self.case_sensitive.setCheckable(True)
        self.case_sensitive.setFlat(True)
        self.case_sensitive.setFixedWidth(25)
        self.horizontal_layout.addWidget(self.case_sensitive)

        # add the case sensitive option
        self.whole_word = QPushButton("W")
        self.whole_word.setContentsMargins(0, 0, 0, 0)
        self.whole_word.setToolTip("Match Case")
        self.whole_word.setCheckable(True)
        self.whole_word.setFlat(True)
        self.whole_word.setFixedWidth(30)
        self.horizontal_layout.addWidget(self.whole_word)

    # when text is entered in search through the document
    def onChanged(self, text):
        logging.info(text)
        file_data = self.document.toPlainText()
        flags = QTextDocument.FindFlag(0)
        # if text is not case sensitive
        if self.case_sensitive.isChecked():
            flags = flags | QTextDocument.FindCaseSensitively

        if self.whole_word.isChecked():
            flags = flags | QTextDocument.FindWholeWords

        print(self.document.find(text, flags))
        print(file_data)


class FindAll(QWidget):
    def __init__(self, path):
        super(FindAll, self).__init__()
        self.path = path
