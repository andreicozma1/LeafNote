import logging

from PyQt5.QtGui import QFont

from Elements.TextBox import TextBox

"""
The active document - area where user types
"""


class Document(TextBox):
    """
    Creates the widget in the middle of the text editor
    where the text is input and displayed
    """
    def __init__(self):
        """
        creates the default layout of the text document
        :return: returns nothing
        """
        super(Document, self).__init__("")
        logging.info("")

        self.setBackgroundColor("white")
        self.setTextColorByString("black")
        self.setPlaceholderText("Start typing here...")

    def onFontItalChanged(self, state):
        """
        Sets the font to italic
        :param state: boolean - format true or false
        :return: returns nothing
        """
        logging.info(str(state))
        self.setFontItalic(state)

    def onFontBoldChanged(self, state):
        """
        Sets the font to bold
        :param state: boolean - format true or false
        :return: returns nothing
        """
        logging.info(str(QFont.Bold if state else QFont.Normal))
        self.setFontWeight(QFont.Bold if state else QFont.Normal)

    def onFontUnderChanged(self, state):
        """
        Sets the font to underlined
        :param state: boolean - format true or false
        :return: returns nothing
        """
        logging.info(str(state))
        self.setFontUnderline(state)

    def onFontStrikeChanged(self, state):
        """
        Sets the font to strike
        :param state: boolean - format true or false
        :return: returns nothing
        """
        logging.info(str(state))
        font_format = self.currentCharFormat()
        font_format.setFontStrikeOut(state)
        self.setCurrentCharFormat(font_format)

    def resetFormatting(self):
        """
        Clears formatting on text
        :return: returns nothing
        """
        logging.info("")
        self.onFontUnderChanged(False)
        self.onFontItalChanged(False)
        self.onFontBoldChanged(False)
        self.onFontStrikeChanged(False)
