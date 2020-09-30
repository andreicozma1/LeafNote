from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from Elements.TextBox import TextBox
import logging

class Document(TextBox):
    def __init__(self):
        super(Document, self).__init__("")
        logging.info("")

        self.setBackgroundColor("white")
        self.setTextColorByString("black")
        self.setPlaceholderText("Start typing here...")

    # Sets the font to italic
    def onFontItalChanged(self, state):
        logging.info(str(state))
        self.setFontItalic(state)

    # Sets the font to bold
    def onFontBoldChanged(self, state):
        logging.info(str(QFont.Bold if state else QFont.Normal))
        self.setFontWeight(QFont.Bold if state else QFont.Normal)

    # Sets the font to underlined
    def onFontUnderChanged(self, state):
        logging.info(str(state))
        self.setFontUnderline(state)

    # Sets the font to strike
    def onFontStrikeChanged(self, state):
        logging.info(str(state))
        fontFormat = self.currentCharFormat()
        fontFormat.setFontStrikeOut(state)
        self.setCurrentCharFormat(fontFormat)

    def resetFormatting(self):
        logging.info("")
        self.onFontUnderChanged(False)
        self.onFontItalChanged(False)
        self.onFontBoldChanged(False)
        self.onFontStrikeChanged(False)
        self.setAlignment(Qt.AlignLeft)

