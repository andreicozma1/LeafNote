import logging

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCharFormat
from PyQt5.QtWidgets import QColorDialog, QTextEdit, QHBoxLayout, QVBoxLayout

from Elements.Search import SearchFile
from Utils import DocumentSummarizer

"""
The active document - area where user types
"""


class Document(QTextEdit):
    """
    Creates the widget in the middle of the text editor
    where the text is input and displayed
    """

    def __init__(self, app, doc_props, default_text: str = ""):
        """
        creates the default layout of the text document
        :return: returns nothing
        """
        super(Document, self).__init__("")
        logging.debug("Creating document")
        self.doc_props = doc_props
        self.app = app

        # If the dictionaries have been downloaded previously, check persistent settings
        self.summarizer = None
        self.initSummarizer(self.app.settings.value("dictionaryPath"), False)

        self.textColor = "black"

        if default_text is None:
            default_text = "You can type here."

        self.search = SearchFile(app.app_props.path_res, self)
        self.search_all = None
        self.find_and_replace = None

        self.setText(default_text)
        self.setAutoFillBackground(True)
        self.setBackgroundColor("white")
        self.setTextColorByString("black")
        self.setPlaceholderText("Start typing here...")
        self.initLayout()

    def initLayout(self):
        """
        Initializes the layout of document.
        :return: Returns nothing
        """
        # create v box to hold h box and stretch
        logging.debug("")
        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(0, 0, 0, 0)

        # creat h box to hold stretch and search
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setAlignment(Qt.AlignRight)
        self.hbox.addWidget(self.search)

        # add the hbox and stretch to align search to top right of screen
        self.layout_main.addLayout(self.hbox)
        self.layout_main.addStretch()

    def initSummarizer(self, dict_path, summarize=False):
        if dict_path is None:
            dp_handler = DocumentSummarizer.DependencyHandler(self.app)
            dict_path = dp_handler.getExistingPath()
            if dict_path is None:
                dp_handler.handleNewDownload(dp_handler.getDownloadPath(), self.initSummarizer)
                return

        self.initSummarizerFromPath(dict_path, summarize)

    def initSummarizerFromPath(self, dict_path, summarize):
        logging.info("Attempt Initialize Summarizer - path: " + dict_path)
        model = DocumentSummarizer.Model(dict_path).createModel()
        if model is not None:
            # create an instance of the summarizer and give it to the application
            self.app.settings.setValue("dictionaryPath", dict_path)
            self.summarizer = DocumentSummarizer.Summarizer(model)
            if summarize:
                self.updateRightMenu()
            return True
        else:
            logging.error("Model ERROR - Failed to initialize Summarizer!")
            return False

    def summarize(self):
        if self.summarizer is None:
            logging.error("Summarizer is not initialized")
            return None
        summary = self.summarizer.summarize(self.toPlainText())
        return summary

    def updateRightMenu(self):
        self.app.right_menu.updateSummary(self.summarize())

    def onFontItalChanged(self, state):
        """
        Sets the font to italic
        :param state: boolean - format true or false
        :return: returns nothing
        """
        logging.debug(str(state))
        self.setFontItalic(state)

    def onFontBoldChanged(self, state):
        """
        Sets the font to bold
        :param state: boolean - format true or false
        :return: returns nothing
        """
        logging.debug(str(QFont.Bold if state else QFont.Normal))
        self.setFontWeight(QFont.Bold if state else QFont.Normal)

    def onFontUnderChanged(self, state):
        """
        Sets the font to underlined
        :param state: boolean - format true or false
        :return: returns nothing
        """
        logging.debug(str(state))
        self.setFontUnderline(state)

    def onFontStrikeChanged(self, state):
        """
        Sets the font to strike
        :param state: boolean - format true or false
        :return: returns nothing
        """
        logging.debug(str(state))
        font_format = self.currentCharFormat()
        font_format.setFontStrikeOut(state)
        self.setCurrentCharFormat(font_format)

    def onFontStyleChanged(self, state):
        """
        Sets the font to the new font
        :return: returns nothing
        """
        logging.debug(state)
        self.setCurrentFont(state)

    def onFontSizeChanged(self, state):
        """
        Sets the current sets the font size from the ComboBox
        :return: returns nothing
        """
        logging.debug(state)
        self.setFontPointSize(int(state))

    def onTextAlignmentChanged(self, state):
        """
        Sets the current text alignment to  the ComboBox
        :return: Returns nothing
        """
        logging.debug(list(self.doc_props.dict_align.keys())[state])
        self.setAlignment(list(self.doc_props.dict_align.values())[state])
        self.currentCharFormatChanged.emit(self.currentCharFormat())

    def openColorDialog(self):
        """
        Opens the color widget and checks for a valid color then sets document font color
        :return: returns nothing
        """
        logging.debug("")
        color = QColorDialog.getColor()

        if color.isValid():
            self.setTextColor(color)

    def onTextColorChanged(self, index):
        """
        set the color the user selects to the text
        :param index: the location of color in the color_dict
        :return: returns nothing
        """
        logging.debug(index)
        color_list: list = list(self.doc_props.color_dict.values())
        self.setTextColor(QColor(color_list[index]))

    def setBackgroundColor(self, color: str):
        """
        Set the background color of the QPlainTextEdit Widget
        :param color: color the background will be set to
        :return: returns nothing
        """
        logging.debug(color)
        palette = self.palette()
        # Set color for window focused
        palette.setColor(QPalette.Active, QPalette.Base, QColor(color))
        # Set color for window out of focus
        palette.setColor(QPalette.Inactive, QPalette.Base, QColor(color))

        self.setPalette(palette)
        # self.setBackgroundVisible(False)

    def setTextColorByString(self, color: str):
        """
        sets the text box to designated color
        :param color: color the text box will be set to
        :return: return nothing
        """
        logging.debug(color)
        palette = self.palette()
        palette.setColor(QPalette.Text, QColor(color))
        self.setPalette(palette)

    def fontBold(self):
        return self.fontWeight() == QFont.Bold

    def fontStrike(self):
        return self.currentCharFormat().fontStrikeOut()

    def resetFormatting(self):
        """
        Clears formatting on text
        :return: returns nothing
        """
        logging.debug("")
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        cursor.setCharFormat(QtGui.QTextCharFormat())
        cursor.clearSelection()
        self.setTextCursor(cursor)

    def onTitleStyleChanged(self, state):
        """
        Sets the font to the new font
        :return: returns nothing
        """
        logging.info(state)
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.BlockUnderCursor)
        cursor.setCharFormat(self.doc_props.dict_title_style[state])
        self.setCurrentCharFormat(self.doc_props.dict_title_style[state])
