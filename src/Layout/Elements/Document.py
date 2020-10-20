import logging

from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCharFormat
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
        super().__init__("")
        logging.debug("Creating Document")
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

    def onFontItalChanged(self, is_italic: bool):
        """
        Sets the font to italic
        :param is_italic: boolean - format true or false
        :return: returns nothing
        """
        logging.debug(str(is_italic))
        self.setFontItalic(is_italic)

    def onFontBoldChanged(self, is_bold: bool):
        """
        Sets the font to bold
        :param is_bold: boolean - format true or false
        :return: returns nothing
        """
        logging.debug(str(QFont.Bold if is_bold else QFont.Normal))
        self.setFontWeight(QFont.Bold if is_bold else QFont.Normal)

    def onFontUnderChanged(self, is_underline: bool):
        """
        Sets the font to underlined
        :param is_underline: boolean - format true or false
        :return: returns nothing
        """
        logging.debug(str(is_underline))
        self.setFontUnderline(is_underline)

    def onFontStrikeChanged(self, is_strike: bool):
        """
        Sets the font to strike
        :param is_strike: boolean - format true or false
        :return: returns nothing
        """
        logging.debug(str(is_strike))
        font_format = self.currentCharFormat()
        font_format.setFontStrikeOut(is_strike)
        self.setCurrentCharFormat(font_format)

    def onFontStyleChanged(self, font_str):
        """
        Sets the font to the new font
        :return: returns nothing
        """
        logging.debug(font_str)
        self.setCurrentFont(font_str)

    def onFontSizeChanged(self, point_size_str: str):
        """
        Sets the current sets the font size from the ComboBox
        :return: returns nothing
        """
        logging.debug(point_size_str)
        self.setFontPointSize(int(point_size_str))

    def onTextAlignmentChanged(self, align_str):
        """
        Sets the current text alignment to  the ComboBox
        :return: Returns nothing
        """
        logging.debug(list(self.doc_props.dict_text_aligns.keys())[align_str])
        self.setAlignment(list(self.doc_props.dict_text_aligns.values())[align_str])
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

    def onTextColorChanged(self, color_index: int):
        """
        set the color the user selects to the text
        :param color_index: the location of color in the color_dict
        :return: returns nothing
        """
        logging.debug(color_index)
        # noinspection PyCompatibility
        color_list: list = list(self.doc_props.dict_colors.values())
        self.setTextColor(QColor(color_list[color_index]))

    def setBackgroundColor(self, color_str: str):
        """
        Set the background color of the QPlainTextEdit Widget
        :param color_str: color the background will be set to
        :return: returns nothing
        """
        logging.debug(color_str)
        palette = self.palette()
        # Set color for window focused
        palette.setColor(QPalette.Active, QPalette.Base, QColor(color_str))
        # Set color for window out of focus
        palette.setColor(QPalette.Inactive, QPalette.Base, QColor(color_str))

        self.setPalette(palette)
        # self.setBackgroundVisible(False)

    def setTextColorByString(self, color_str: str):
        """
        sets the text box to designated color
        :param color_str: color the text box will be set to
        :return: return nothing
        """
        logging.debug(color_str)
        palette = self.palette()
        palette.setColor(QPalette.Text, QColor(color_str))
        self.setPalette(palette)

    def fontBold(self) -> bool:
        """
        Function returns whether the font is bold
        """
        return self.fontWeight() == QFont.Bold

    def fontStrike(self) -> bool:
        """
        Function returns whether the font is strike
        """
        return self.currentCharFormat().fontStrikeOut()

    def clearAllFormatting(self):
        """
        Clears formatting on all text
        :return: returns nothing
        """
        logging.debug("")
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        cursor.setCharFormat(self.doc_props.normal)
        cursor.clearSelection()
        self.setTextCursor(cursor)

    def clearSelectionFormatting(self):
        """
        Clears formatting on selected text
        :return: returns nothing
        """
        cursor = self.textCursor()
        if cursor.hasSelection() is False:
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            cursor.setCharFormat(QTextCharFormat())
        else:
            self.setCurrentCharFormat(QTextCharFormat())

    def onTitleStyleChanged(self, state):
        """
        Sets the font to the new font
        :return: returns nothing
        """
        logging.info(state)
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.BlockUnderCursor)
        cursor.setCharFormat(self.doc_props.dict_title_styles[state])
        self.setCurrentCharFormat(self.doc_props.dict_title_styles[state])

    def setFormatText(self, text: str, formatting: bool):
        """
        Sets formatted or not text
        """
        self.setAcceptRichText(formatting)
        self.setAutoFormatting(self.AutoAll if formatting else self.AutoNone)
        self.setText(text)
        if not formatting:
            self.clearAllFormatting()
