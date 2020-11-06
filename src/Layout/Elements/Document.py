"""
The Document module sets up and defines the methods for
used to interact with the Text Edit area.
"""

import logging
import webbrowser

import validators
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCharFormat, QTextListFormat
from PyQt5.QtWidgets import QColorDialog, QTextEdit
from spellchecker import SpellChecker

from Layout.DocProps import DocProps
from Utils import DocumentSummarizer
from Utils.SyntaxHighlighter import SyntaxHighlighter


class Document(QTextEdit):
    """
    Creates the widget in the middle of the text editor
    where the text is input and displayed
    """

    def __init__(self, app, doc_props):
        """
        creates the default layout of the text document
        :return: returns nothing
        """
        super().__init__("")
        logging.debug("Creating Document")
        self.app = app
        self.doc_props: DocProps = doc_props

        self.highlighter = SyntaxHighlighter(self)
        self.spell_checker = SpellChecker()
        self.textChanged.connect(self.onTextChanged)

        # If the dictionaries have been downloaded previously, check persistent settings
        self.summarizer = None
        if app.settings.contains("dictionaryPath"):
            path = app.settings.value("dictionaryPath")
            DocumentSummarizer.initializeSummarizer(path, app, self)

        self.textColor = "black"

        self.setAutoFillBackground(True)
        self.setBackgroundColor(self.doc_props.def_background_color)
        self.setPlaceholderText(self.doc_props.def_placeholder_text)

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        """
        if the double clicked word is a link open it
        :return: returns nothing
        """
        # get the cursor where the user double clicked
        cursor = self.cursorForPosition(e.pos())
        pos = cursor.position()

        # get the selected words position and full word
        _, _, url = self._getWordFromPos(pos)

        # check if the url is valid
        valid = validators.url(url)

        # if the link is valid open it
        if valid:
            webbrowser.open(url)
            logging.info("User opened link - %s", url)

    def _getWordFromPos(self, pos):
        """
        this get the word at the selected position
        :param pos: the position in the document
        :return: returns a tuple of the start and end position as well as the word
        """
        # get the start and end index of the current selection
        start = self.toPlainText().rfind(" ", 0, pos) + 1
        new_line = self.toPlainText().rfind("\n", 0, pos) + 1
        start = start if start > new_line else new_line

        end = self.toPlainText().find(" ", pos)
        new_line = self.toPlainText().find("\n", pos)
        end = end if end > new_line else new_line

        # fix the indices if they are equal to -1
        end = len(self.toPlainText()) if end == -1 else end

        # get the selected word
        word = self.toPlainText()[start:end]
        return start, end, word

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

    def fontBold(self) -> bool:
        """
        returns true the current font weight is bolded
        :return: returns whether or not the text is bolded
        """
        return self.fontWeight() == QFont.Bold

    def fontStrike(self) -> bool:
        """
        returns true the current font is strikethrough
        :return: returns whether or not the text is struck through
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
        cursor.setCharFormat(self.doc_props.default)
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
        Sets the font to the new font based on title style selected
        updates style of title
        resets title styles to default
        :return: returns nothing
        """
        logging.info(state)
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.BlockUnderCursor)
        if state == "":
            cursor.setCharFormat(self.doc_props.dict_title_styles["Normal Text"])
            self.setCurrentCharFormat(self.doc_props.dict_title_styles["Normal Text"])
            return
        if self.doc_props.text_update_title not in state and \
                self.doc_props.text_reset_title not in state:
            cursor.setCharFormat(self.doc_props.dict_title_styles[state])
            self.setCurrentCharFormat(self.doc_props.dict_title_styles[state])
        elif self.doc_props.text_update_title in state:
            self.doc_props.dict_title_styles[
                state[len(self.doc_props.text_update_title):]] = cursor.charFormat()
        else:
            self.resetTitleStyle()

    def resetTitleStyle(self):
        """
        resets title styles to default style
        :return: returns nothing
        """
        self.doc_props.dict_title_styles["Normal Text"] = self.doc_props.default
        self.doc_props.dict_title_styles["Title"] = self.doc_props.title
        self.doc_props.dict_title_styles["Subtitle"] = self.doc_props.subtitle
        self.doc_props.dict_title_styles["Header 1"] = self.doc_props.heading1
        self.doc_props.dict_title_styles["Header 2"] = self.doc_props.heading2
        self.doc_props.dict_title_styles["Header 3"] = self.doc_props.heading3
        self.doc_props.dict_title_styles["Header 4"] = self.doc_props.heading4

    def keyPressEvent(self, event):
        """
        intercepts key press to check for bullet list
        :return: returns nothing
        """
        # checks for enter
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.pressedReturn()
            super().keyPressEvent(event)
        # checks for tab
        elif event.key() == QtCore.Qt.Key_Tab:
            super().keyPressEvent(event)
            self.pressedTab()
        # checks for shift tab
        elif event.key() == QtCore.Qt.Key_Backtab:
            super().keyPressEvent(event)
            self.pressedShiftTab()
        # calls normal functionality of key
        else:
            super().keyPressEvent(event)

    def pressedReturn(self):
        """
        enter or return key is pressed
        :return: returns nothing
        """
        cursor = self.textCursor()
        listIn = cursor.currentList()
        # checks if cursor is in a list
        if cursor.currentList() is not None:
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            text = cursor.selectedText()
            text = text.strip()
            # checks if the bullet on the list is blank
            if text == "":
                logging.info("bullet list: removed last bullet")
                # removes bullet
                listIn.removeItem(listIn.count() - 1)

    def pressedTab(self):
        """
        tab key is pressed
        :return: returns nothing
        """
        cursor = self.textCursor()
        listIn = cursor.currentList()
        # checks if cursor is in a list
        if cursor.currentList() is not None:
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            text = cursor.selectedText()
            text = text.strip()
            # checks if the bullet on the list is blank
            if text == "":
                logging.info("bullet list: tabbed")
                currlist = listIn.format()
                style = currlist.style()
                # updates style to next bullet
                if style == -3:
                    style = -1
                else:
                    style -= 1
                listFormat2 = QTextListFormat()
                # adds indent
                listFormat2.setIndent(currlist.indent() + 1)
                listFormat2.setStyle(style)
                cursor.insertList(listFormat2)

    def pressedShiftTab(self):
        """
        shift + tab keys are pressed
        :return: returns nothing
        """
        cursor = self.textCursor()
        listIn = cursor.currentList()
        # checks if cursor is in a list
        if cursor.currentList() is not None:
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            text = cursor.selectedText()
            text = text.strip()
            # checks if the bullet on the list is blank
            if text == "":
                logging.info("bullet list: back-tabbed")
                currlist = listIn.format()
                indent = currlist.indent()
                style = currlist.style()
                # checks if indent can be removed then removes
                if indent != 1:
                    indent -= 1
                    # if indent can be removed get previous bullet style
                    if style == -1:
                        style = -3
                    else:
                        style += 1
                listFormat2 = QTextListFormat()
                listFormat2.setIndent(indent)
                listFormat2.setStyle(style)
                cursor.insertList(listFormat2)

    def bulletList(self):
        """
        bullet list created on cursor location
        :return: returns nothing
        """
        logging.info("bullet list: created")
        style = QTextListFormat.ListDisc
        cursor = self.textCursor()
        listFormat = QTextListFormat()
        listFormat.setStyle(style)
        cursor.createList(listFormat)

    def setFormatText(self, text: str, formatting: bool):
        """
        Sets formatted or not text
        """
        self.setAcceptRichText(formatting)
        self.setAutoFormatting(self.AutoAll if formatting else self.AutoNone)
        self.setText(text)
        if not formatting:
            self.clearAllFormatting()

    def onTextChanged(self):
        """
        grabs current word in text document and runs a spell checker
        :return: returns nothing
        """
        cursor = self.textCursor()
        pos = cursor.position()
        _, _, word = self._getWordFromPos(pos)

        if word == "":
            _, _, word_temp = self._getWordFromPos(pos - 1)
            self.spellChecker(word_temp)

    def spellChecker(self, word_t):
        """
        runs word_t through a spell checker
        :param word_t: The word itself
        :return: returns nothing
        """
        if word_t != '':
            misspelled = self.spell_checker.unknown([word_t])

            for word in misspelled:
                self.highlighter.misspelled_words[word] = None
