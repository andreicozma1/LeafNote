"""
test Document default behavior
"""

import test

import unittest

from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from LeafNote.Layout.Elements import BarTop, Document
from LeafNote.Props import DocProps

string: str = "This is a test."


class TestDocument(unittest.TestCase):
    """
    Unit test for all Document functionality
    """

    def setUp(self):
        """
        Set up environment
        """
        self.document: Document = test.app.document
        self.top_bar: BarTop = test.app.top_bar
        self.doc_props: DocProps = test.app.doc_props

    def testFontBold(self):
        """
        Test the onFontBoldChanged function
        """
        self.document.setPlainText(string)

        # set the document text to bold
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontBoldChanged(True)

        # check if the text is actually bold
        act_is_bold = self.document.fontBold()
        self.assertEqual(True, act_is_bold)

        # check if the corresponding button is checked
        act_is_checked = self.top_bar.button_bold.isChecked()
        self.assertEqual(True, act_is_checked)

        # set the document text to NOT bolded
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontBoldChanged(False)

        # check if the text is actually NOT bolded
        act_is_bold = self.document.fontBold()
        self.assertEqual(False, act_is_bold)

        # check if the corresponding button is checked
        act_is_checked = self.top_bar.button_bold.isChecked()
        self.assertEqual(False, act_is_checked)

    def testFontItal(self):
        """
        Test the onFontItalChanged function
        """
        self.document.setPlainText(string)

        # set the document text to italicized
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontItalChanged(True)

        # check if the text is actually italicized
        act_is_ital = self.document.fontItalic()
        self.assertEqual(True, act_is_ital)

        # check if the corresponding button is checked
        act_is_checked = self.top_bar.button_ital.isChecked()
        self.assertEqual(True, act_is_checked)

        # set the document text to NOT italicized
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontItalChanged(False)

        # check if the text is actually NOT italicized
        act_is_ital = self.document.fontItalic()
        self.assertEqual(False, act_is_ital)

        # check if the corresponding button is checked
        act_is_checked = self.top_bar.button_ital.isChecked()
        self.assertEqual(False, act_is_checked)

    def testFontStrike(self):
        """
        Test the onFontStrikeChanged function
        """
        self.document.setPlainText(string)

        # set the document text to strikethrough
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontStrikeChanged(True)

        # check if the text is actually strikethrough
        act_is_strike = self.document.fontStrike()
        self.assertEqual(True, act_is_strike)

        # check if the corresponding button is checked
        act_is_checked = self.top_bar.button_strike.isChecked()
        self.assertEqual(True, act_is_checked)

        # set the document text to NOT strikethrough
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontStrikeChanged(False)

        # check if the text is actually NOT strikethrough
        act_is_strike = self.document.fontStrike()
        self.assertEqual(False, act_is_strike)

        # check if the corresponding button is checked
        act_is_checked = self.top_bar.button_strike.isChecked()
        self.assertEqual(False, act_is_checked)

    def testFontUnder(self):
        """
        Test the onFontUnderChanged function
        """
        self.document.setPlainText(string)

        # set the document text to italicized
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontUnderChanged(True)

        # check if the text is actually italicized
        act_is_under = self.document.fontUnderline()
        self.assertEqual(True, act_is_under)

        # check if the corresponding button is checked
        act_is_checked = self.top_bar.button_under.isChecked()
        self.assertEqual(True, act_is_checked)

        # set the document text to NOT italicized
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontUnderChanged(False)

        # check if the text is actually NOT italicized
        act_is_under = self.document.fontUnderline()
        self.assertEqual(False, act_is_under)

        # check if the corresponding button is checked
        act_is_checked = self.top_bar.button_under.isChecked()
        self.assertEqual(False, act_is_checked)

    def testClearAllFormat(self):
        """
        Test the clearAllFormatting function
        """
        # reset the doc text style
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        cursor.setCharFormat(QtGui.QTextCharFormat())
        cursor.clearSelection()
        self.document.setTextCursor(cursor)

        self.document.setPlainText(string)
        exp_html = self.document.toHtml()

        # change the text style
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)

        self.document.onFontStrikeChanged(True)
        self.document.onFontUnderChanged(True)
        self.document.onFontBoldChanged(True)
        self.document.onFontItalChanged(True)

        # clear all formatting and check
        self.document.clearAllFormatting()
        act_html = self.document.toHtml()

        self.assertEqual(exp_html, act_html)

    def testTextAlignment(self):
        """
        this function will test the paste plain
        """
        self.document.setPlainText(string)

        # set the cursor to the beginning of the document
        cursor = self.document.textCursor()
        cursor.setPosition(0)

        # check each alignment
        alignments = list(self.doc_props.dict_text_aligns.values())
        for i, exp_align in enumerate(alignments):
            self.document.onTextAlignmentChanged(i)
            act_align = self.document.alignment()
            self.assertEqual(exp_align, act_align)

    def testFontSize(self):
        """
        Test the onFontSizeChanged function
        """
        self.document.setPlainText(string)

        for exp_font_size in range(5, 25, 5):

            # set the documents font size
            cursor = self.document.textCursor()
            cursor.select(cursor.Document)
            self.document.onFontSizeChanged(str(exp_font_size))

            # get the actual font size and test
            act_font_size = self.document.fontPointSize()
            self.assertEqual(exp_font_size, act_font_size)

    def testTextColorChange(self):
        """
        Test the onTextColorChanged function
        """
        self.document.setPlainText(string)
        color_list: list = list(self.doc_props.dict_colors.values())
        for i, color in enumerate(color_list):
            # get expected color
            exp_color = QColor(color)

            # set the documents font size
            cursor = self.document.textCursor()
            cursor.select(cursor.Document)
            self.document.onTextColorChanged(i)

            # get the actual color and test
            act_color = self.document.textColor()
            self.assertEqual(exp_color, act_color)
