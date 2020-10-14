import logging

from PyQt5 import QtGui
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel, QVBoxLayout, QCheckBox


class FindAndReplace(QWidget):
    def __init__(self, document):
        """
        Initialize the widget
        """
        logging.info("")
        super(FindAndReplace, self).__init__()
        self.document = document
        self.search = ""
        self.flags = QTextDocument.FindFlag(0)

        self.initUI()
        self.show()

    def initUI(self):
        """
        sets up the layout and properties for the qwidget
        """
        # set properties
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(400)

        # create main layout
        self.vertical_layout = QVBoxLayout(self)

        # set the background
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#ffffff'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # -----------------------------------------------------------

        # create top layout for title and exit button
        widget = QWidget()
        self.title_hbox = QHBoxLayout()
        widget.setLayout(self.title_hbox)

        # create title
        self.title = QLabel('Find and replace')
        self.title.setStyleSheet("font-size: 21px;")
        self.title_hbox.addWidget(self.title)
        self.title_hbox.addStretch()

        # create exit button
        self.exit = QPushButton("X")
        self.exit.setContentsMargins(0, 0, 0, 0)
        self.exit.setFixedWidth(25)
        self.exit.setFlat(True)
        self.exit.clicked.connect(self.close)
        self.title_hbox.addWidget(self.exit)

        # add top layout to the main layout
        self.vertical_layout.addWidget(widget)

        # -----------------------------------------------------------

        def createLineEdit():
            """
            create a new line edit
            """
            bar = QLineEdit()
            bar.setContentsMargins(0, 0, 0, 0)
            bar.setFixedWidth(200)
            bar.setStyleSheet("QLineEdit {background: rgb(218, 218, 218)}")
            return bar

        # -----------------------------------------------------------

        # set find search bar layer
        widget = QWidget()
        self.find_hbox = QHBoxLayout()
        widget.setLayout(self.find_hbox)

        # create find label
        self.find_label = QLabel("Find")
        self.find_hbox.addWidget(self.find_label)
        self.find_hbox.addStretch()

        # create find bar
        self.find_bar = createLineEdit()
        self.find_bar.textChanged[str].connect(self.onChanged)
        self.find_hbox.addWidget(self.find_bar)

        # add find layer to main layout
        self.vertical_layout.addWidget(widget)

        # -----------------------------------------------------------

        # set find search bar layer
        widget = QWidget()
        self.replace_hbox = QHBoxLayout()
        widget.setLayout(self.replace_hbox)

        # create replace label
        self.replace_label = QLabel("Replace with")
        self.replace_hbox.addWidget(self.replace_label)
        self.replace_hbox.addStretch()

        # create replace bar
        self.replace_bar = createLineEdit()
        self.replace_hbox.addWidget(self.replace_bar)

        # add replace layer to main layout
        self.vertical_layout.addWidget(widget)

        # -----------------------------------------------------------

        # create match case option
        widget = QWidget()
        self.match_case_hbox = QHBoxLayout()
        self.match_case_hbox.setContentsMargins(100, 0, 0, 0)
        widget.setLayout(self.match_case_hbox)

        # create match case checkbox
        self.match_case_checkbox = QCheckBox("Match case")
        self.match_case_checkbox.stateChanged.connect(self.onOptionChanged)
        self.match_case_hbox.addWidget(self.match_case_checkbox)

        # add match case layer to main layout
        self.vertical_layout.addWidget(widget)

        # -----------------------------------------------------------

        # create match word option
        widget = QWidget()
        self.whole_word_hbox = QHBoxLayout()
        self.whole_word_hbox.setContentsMargins(100, 0, 0, 0)
        widget.setLayout(self.whole_word_hbox)

        # create match word checkbox
        self.whole_word_checkbox = QCheckBox("Match whole word")
        self.whole_word_checkbox.stateChanged.connect(self.onOptionChanged)
        self.whole_word_hbox.addWidget(self.whole_word_checkbox)

        # add match word layer to main layout
        self.vertical_layout.addWidget(widget)

        # -----------------------------------------------------------

        # create match regex option
        widget = QWidget()
        self.regex_hbox = QHBoxLayout()
        self.regex_hbox.setContentsMargins(100, 0, 0, 0)
        widget.setLayout(self.regex_hbox)

        # create match regex checkbox
        self.regex_checkbox = QCheckBox("Match using regular expressions")
        self.regex_checkbox.stateChanged.connect(self.onOptionChanged)

        self.regex_hbox.addWidget(self.regex_checkbox)

        # add match regex layer to main layout
        self.vertical_layout.addWidget(widget)

        # -----------------------------------------------------------

        # create actions buttons
        widget = QWidget()
        self.actions_hbox = QHBoxLayout()
        widget.setLayout(self.actions_hbox)

        def createActionBtn(title, signal):
            btn = QPushButton(title)
            btn.clicked.connect(signal)
            return btn
        self.actions_hbox.addWidget(createActionBtn("Replace", self.onReplace))
        self.actions_hbox.addWidget(createActionBtn("Replace all", self.onReplaceAll))
        self.actions_hbox.addWidget(createActionBtn("Previous", self.onPrevious))
        self.actions_hbox.addWidget(createActionBtn("Next", self.onNext))

        self.vertical_layout.addWidget(widget)

    def onOptionChanged(self):
        """
        Handle the selections when an option is changed
        """
        if self.regex_checkbox.isChecked():
            self.whole_word_checkbox.setCheckState(False)
            self.match_case_checkbox.setCheckState(False)

        self.onChanged(self.find_bar.text())

    def onReplace(self):
        """
        Replaces the current selection of the search string with the replace string
        """
        cursor = self.document.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_bar.text())
        self.document.find(self.search, self.flags)

    def onReplaceAll(self):
        """
        Replaces all occurrences of the search string with the replace string
        """
        cursor = self.document.textCursor()
        while cursor.hasSelection():
            cursor.insertText(self.replace_bar.text())
            self.document.find(self.search, self.flags)
            cursor = self.document.textCursor()

    def onPrevious(self):
        """
        Moves to the previous selection
        """
        self.document.find(self.search, self.flags | QTextDocument.FindBackward)

    def onNext(self):
        """
        Moves to the next found selection
        """
        self.document.find(self.search, self.flags)

    def onChanged(self, search):
        """
        When the text is changed reset and query for the new search phrase
        :param search: The phrase to search for
        :return: Returns nothing
        """

        logging.info(search)
        self.search = search

        # set the cursor to the beginning of the document
        cursor = self.document.textCursor()
        cursor.setPosition(0)
        self.document.setTextCursor(cursor)

        # set up the default search flags
        self.flags = QTextDocument.FindFlag(0)

        # if search is case sensitive
        if self.match_case_checkbox.isChecked():
            self.flags = self.flags | QTextDocument.FindCaseSensitively

        # if search is whole word sensitive
        if self.whole_word_checkbox.isChecked():
            self.flags = self.flags | QTextDocument.FindWholeWords

        # if the user IS searching for regex
        if self.regex_checkbox.isChecked():
            self.search = QRegExp(self.search)

        logging.info(self.document.find(self.search, self.flags))