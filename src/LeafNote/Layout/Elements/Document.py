"""
The Document module sets up and defines the methods for
used to interact with the Text Edit area.
"""

import logging
import webbrowser

import validators

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCharFormat, QTextDocument, QTextListFormat
from PyQt5.QtWidgets import QColorDialog, QTextEdit
from spellchecker import SpellChecker

from LeafNote.Props import DocProps
from LeafNote.Utils import SyntaxHighlighter, Summarizer


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

        # Spellchecker and set of misspelled_words
        self.spell_checker = SpellChecker()
        self.misspelled_words = set()
        # Defining whether features are enabled
        self.spellcheck_enabled = self.doc_props.def_enable_spellcheck
        self.autocorrect_enabled = self.doc_props.def_enable_autocorrect

        # If the dictionaries have been downloaded previously, check persistent settings
        self.summarizer = None
        if app.settings.contains("dictionaryPath"):
            path = app.settings.value("dictionaryPath")
            Summarizer.initializeSummarizer(path, app, self)

        self.textColor = "black"

        self.setAutoFillBackground(True)
        self.setBackgroundColor(self.doc_props.def_background_color)
        self.onTextColorChanged(list(self.doc_props.dict_colors.keys())
                                .index(self.doc_props.def_text_color_key))
        self.setPlaceholderText(self.doc_props.def_placeholder_text)

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        """
        if the double clicked word is a link open it
        :return: returns nothing
        """
        logging.debug("User double-clicked in document")
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
            return

        super().mouseDoubleClickEvent(e)

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
        logging.debug("Clearing all formatting")
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()
        self.setTextCursor(cursor)

    def clearSelectionFormatting(self):
        """
        Clears formatting on selected text
        :return: returns nothing
        """
        logging.debug("Clearing selection formatting")
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
        logging.debug("Resetting all title styles")
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
            if self.pressedReturn():
                super().keyPressEvent(event)
        # checks for tab
        elif event.key() == QtCore.Qt.Key_Tab:
            if self.pressedTab():
                super().keyPressEvent(event)
        # checks for shift tab
        elif event.key() == QtCore.Qt.Key_Backtab:
            if self.pressedShiftTab():
                super().keyPressEvent(event)
        # calls normal functionality of key
        else:
            super().keyPressEvent(event)

    def moveListForward(self):
        """
        helper function when tab is pressed in bullet list
        :return: returns nothing
        """
        cursor = self.textCursor()
        listIn = cursor.currentList()
        currlist = listIn.format()
        style = currlist.style()
        # updates style to next bullet
        if style == -3:
            style = -1
        else:
            style -= 1
        listFormat = QTextListFormat()
        # adds indent
        listFormat.setIndent(currlist.indent() + 1)
        listFormat.setStyle(style)
        listIn.setFormat(listFormat)

    def moveListBackward(self):
        """
        helper function when shift-tab is pressed in bullet list
        :return: returns nothing
        """
        cursor = self.textCursor()
        listIn = cursor.currentList()
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
        listFormat = QTextListFormat()
        listFormat.setIndent(indent)
        listFormat.setStyle(style)
        listIn.setFormat(listFormat)

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
            if text == "":
                listIn.removeItem(listIn.count() - 1)
                return False
            currlist = listIn.format()
            style = currlist.style()
            cursor = self.textCursor()
            cursor.insertText("\n")
            listFormat = QTextListFormat()
            listFormat.setStyle(style)
            listFormat.setIndent(currlist.indent())
            cursor.createList(listFormat)
            return False
        return True

    def pressedTab(self):
        """
        tab key is pressed
        :return: returns nothing
        """
        cursor = self.textCursor()
        # checks if cursor is in a list
        if cursor.currentList() is not None:
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            text = cursor.selectedText()
            text = text.strip()
            # checks if the bullet on the list is blank
            if text == "":
                logging.info("bullet list: tabbed")
                self.moveListForward()
                return False
            else:
                cursor.select(QtGui.QTextCursor.BlockUnderCursor - 1)
                if cursor.selectionStart() == self.textCursor().position():
                    logging.info("bullet list: tabbed")
                    self.moveListForward()
                    return False
        return True

    def pressedShiftTab(self):
        """
        shift + tab keys are pressed
        :return: returns nothing
        """
        cursor = self.textCursor()
        # checks if cursor is in a list
        if cursor.currentList() is not None:
            cursor.select(QtGui.QTextCursor.BlockUnderCursor - 2)
            text = cursor.selectedText()
            text = text.strip()
            # checks if the bullet on the list is blank
            if text == "":
                logging.info("bullet list: back-tabbed")
                self.moveListBackward()
                return False
            else:
                cursor.select(QtGui.QTextCursor.BlockUnderCursor)
                if cursor.selectionStart() + 1 == self.textCursor().position():
                    logging.info("bullet list: back-tabbed")
                    self.moveListBackward()
                    return False
        return True

    def bulletList(self):
        """
        bullet list created on cursor location
        :return: returns nothing
        """
        logging.info("bullet list: created")
        style = QTextListFormat.ListDisc
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        listFormat = QTextListFormat()
        listFormat.setStyle(style)
        cursor.createList(listFormat)

    def setFormatText(self, text: str, formatting: bool):
        """
        Sets formatted or not text
        """
        self.enableFormatting(formatting)
        self.setText(text)
        if not formatting:
            self.clearAllFormatting()

    def enableFormatting(self, enable: bool = True):
        """
        Sets formatting enabled or disabled
        """
        logging.debug("Enable formatting: %s", str(enable))
        self.setAcceptRichText(enable)
        self.setAutoFormatting(self.AutoAll if enable else self.AutoNone)

    def pastePlain(self):
        """
        Pastes from clipboard as plain text
        """
        logging.debug("Pasting as Plain Text")
        clipboard = self.app.ctx.clipboard()
        self.insertPlainText(clipboard.text())
        self.spellCheckAll()

    def undo(self):
        """
        Overload undo to be able to undo autocorrect
        """
        self.blockSignals(True)
        super().undo()
        self.blockSignals(False)

    def redo(self):
        """
        Overload undo to be able to undo autocorrect
        """
        self.blockSignals(True)
        super().redo()
        self.blockSignals(False)

    def toggle_spellcheck(self, enabled: bool):
        """
        Disables or Enables spellcheck
        """
        logging.debug("setting: %s", str(enabled))
        # Set the new state
        self.spellcheck_enabled = enabled
        self.spellCheckAll()

    def toggle_autocorrect(self, enabled: bool):
        """
        Disables or Enables Autocorrect
        """
        logging.debug("setting: %s", str(enabled))
        # Sets new state
        self.autocorrect_enabled = enabled

    def onTextChanged(self):
        """
        grabs current word in text document and runs a spell checker
        :return: returns nothing
        """
        cursor = self.textCursor()
        pos = cursor.position()
        _, _, tmp = self._getWordFromPos(pos)

        # if typed space there is no word found
        if tmp == "":
            _, _, last_word = self._getWordFromPos(pos - 1)
            # If word was misspelled
            if not self._spellCheck(last_word):
                self._autoCorrect(last_word)

    def _spellCheck(self, word: str):
        """
        Spell check functionality also calls autocorrect
        :param word: word to spell check
        """
        if (self.spellcheck_enabled or self.autocorrect_enabled) and word:
            correct = self.spell_checker[word]
            if not correct:
                self.misspelled_words.add(word)
                logging.debug("Added misspelled word to highlighter set: %s", word)
                return False
        return True

    def _autoCorrect(self, word: str) -> bool:
        """
        Autocorrect functionality
        :param word: word to autocorrect
        """
        if self.autocorrect_enabled and word:
            # Find the most likely corrected word
            corrected = self.spell_checker.correction(word)
            # Select the incorrect word
            self.find(word, QTextDocument.FindBackward)
            cursor = self.textCursor()
            # If selected, replace it
            if cursor.hasSelection():
                # Replace the word with the correct one and re-add the space
                self.blockSignals(True)
                cursor.insertText(corrected + " ")
                self.blockSignals(False)
                self.misspelled_words.remove(word)
                logging.debug("Autocorrected misspelled word: %s to %s", word, corrected)
            else:
                logging.error("Failed to autocorrect word")
            return True
        else:
            return False

    def spellCheckAll(self):
        """
        Re-checks the entire document and adds all misspelled words
        """
        if self.spellcheck_enabled:
            logging.debug("Re-checking entire document to re-construct misspelled words dictionary")
            all_words = self.toPlainText().split()
            self.misspelled_words = self.spell_checker.unknown(all_words)
            logging.debug(self.misspelled_words)
        elif self.misspelled_words:
            self.misspelled_words.clear()
        # Re-highlight entire document after change
        self.highlighter.rehighlight()
