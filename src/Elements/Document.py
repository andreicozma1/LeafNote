import logging

from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtWidgets import QColorDialog, QTextEdit

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
        logging.debug("")
        self.doc_props = doc_props

        # If the dictionaries have been downloaded previously, check persistent settings
        self.summarizer = None
        if app.settings.contains("dictionaryPath"):
            path = app.settings.value("dictionaryPath")
            DocumentSummarizer.initializeSummarizer(path, app, self)

        self.textColor = "black"

        if default_text is None:
            default_text = "You can type here."

        self.setText(default_text)
        self.setAutoFillBackground(True)
        self.setBackgroundColor("white")
        self.setTextColorByString("black")
        self.setPlaceholderText("Start typing here...")

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
