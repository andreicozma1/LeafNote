import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QColorDialog

from Elements.TextBox import TextBox

"""
The active document - area where user types
"""


class Document(TextBox):
    """
    Creates the widget in the middle of the text editor
    where the text is input and displayed
    """

    def __init__(self, doc_props):
        """
        creates the default layout of the text document
        :return: returns nothing
        """
        super(Document, self).__init__("")
        logging.info("")
        self.doc_props = doc_props

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

    def onFontStyleChanged(self, state):
        """
        Sets the font to the new font
        :return: returns nothing
        """
        logging.info(state)
        self.setCurrentFont(state)

    def onFontSizeChanged(self, state):
        """
        Sets the current sets the font size from the ComboBox
        :return: returns nothing
        """
        logging.info(state)
        self.setFontPointSize(int(state))

    def onTextAlignmentChanged(self, state):
        """
        Sets the current text alignment to  the ComboBox
        :return: Returns nothing
        """
        logging.info(state)
        self.setAlignment(list(self.doc_props.dict_align.values())[state])
        self.currentCharFormatChanged.emit(self.currentCharFormat())

    def openColorDialog(self):
        """
        Opens the color widget and checks for a valid color then sets document font color
        :return: returns nothing
        """
        color = QColorDialog.getColor()

        if color.isValid():
            self.setTextColor(color)

    def onTextColorChanged(self, index):
        """
        set the color the user selects to the text
        :param index: the location of color in the color_dict
        :return: returns nothing
        """
        logging.info(index)
        color_list: list = list(self.doc_props.color_dict.values())
        self.setTextColor(QColor(color_list[index]))

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
        self.setAlignment(Qt.AlignLeft)
