import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton


class Replace(QWidget):
    def __init__(self, search_and_replace, document):
        """
        Initialize the widget
        """
        logging.info("")
        super(Replace, self).__init__()
        self.search_and_replace = search_and_replace
        self.document = document

        self.initUI()
        self.hide()

    def initUI(self):
        """
        sets up the layout and properties for the qwidget
        """
        # create the overarching hbox layout of the widget
        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(2, 0, 0, 0)
        self.horizontal_layout.setAlignment(Qt.AlignLeft)
        self.horizontal_layout.setSpacing(0)

        # -----------------------------------------------------------

        # add the qLineEdit
        self.replace_bar = QLineEdit()
        self.replace_bar.setContentsMargins(0, 0, 0, 0)
        self.replace_bar.setFixedWidth(200)
        self.replace_bar.setStyleSheet("QLineEdit {background: rgb(218, 218, 218)}")
        self.horizontal_layout.addWidget(self.replace_bar, 0, Qt.AlignLeft)

        # -----------------------------------------------------------

        # create actions buttons
        def createActionBtn(title, signal):
            btn = QPushButton(title)
            btn.setContentsMargins(0, 0, 0, 0)
            btn.clicked.connect(signal)
            return btn

        self.horizontal_layout.addWidget(createActionBtn("Replace", self.onReplace))
        self.horizontal_layout.addWidget(createActionBtn("Replace all", self.onReplaceAll))

        # -----------------------------------------------------------

        self.horizontal_layout.addStretch()

    def onReplace(self):
        """
        Replaces the current selection of the search string with the replace string
        """
        cursor = self.document.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_bar.text())
        self.document.search_and_replace.search.onNextOccurrenceSelect()

    def onReplaceAll(self):
        """
        Replaces all occurrences of the search string with the replace string
        """
        cursor = self.document.textCursor()
        while cursor.hasSelection():
            cursor.insertText(self.replace_bar.text())
            self.document.search_and_replace.search.onNextOccurrenceSelect()
            cursor = self.document.textCursor()
