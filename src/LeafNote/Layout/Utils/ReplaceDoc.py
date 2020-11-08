"""
this module holds the widget that will display the replace feature in a document
"""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton


class ReplaceDoc(QWidget):
    """
    This widget shows gives the user the ability to replace text throughout the document
    """

    def __init__(self, search_and_replace, document):
        """
        Initialize the widget
        """
        super().__init__()
        logging.debug("Creating Replace Widget")

        self.search_and_replace = search_and_replace
        self.document = document

        self.initUI()
        self.hide()

    def initUI(self):
        """
        sets up the layout and properties for the qwidget
        """
        # create the overarching hbox layout of the widget
        logging.debug("Setting up UI")

        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(2, 0, 0, 0)
        self.horizontal_layout.setAlignment(Qt.AlignLeft)
        self.horizontal_layout.setSpacing(3)

        # -----------------------------------------------------------

        # add the qLineEdit
        self.replace_bar = QLineEdit()
        self.replace_bar.setContentsMargins(0, 0, 0, 0)
        self.replace_bar.setFixedWidth(200)
        self.replace_bar.setStyleSheet("QLineEdit {background: rgb(218, 218, 218)}")
        self.horizontal_layout.addWidget(self.replace_bar, alignment=Qt.AlignLeft)

        # -----------------------------------------------------------

        # create actions buttons
        def createActionBtn(title, signal):
            """
            Constructor for actions
            """
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
        logging.info("Clicked Replace")
        cursor = self.document.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_bar.text())
        self.search_and_replace.search.onNextOccurrenceSelect()

    def onReplaceAll(self):
        """
        Replaces all occurrences of the search string with the replace string
        """
        logging.info("Clicked Replace All")
        cursor = self.document.textCursor()
        while cursor.hasSelection():
            cursor.insertText(self.replace_bar.text())
            self.search_and_replace.search.onNextOccurrenceSelect()
            cursor = self.document.textCursor()
