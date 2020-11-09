"""
test Document default behavior
"""
import unittest

from PyQt5.QtWidgets import QApplication

from LeafNote import App

ctx = QApplication([])
app = App(ctx)


class TestDocument(unittest.TestCase):
    """
    Unit test for all Document functionality
    """

    def setUp(self):
        """
        Set up environment
        """
        self.document = app.document
        self.doc_props = app.doc_props

    def testFontBold(self):
        """
        Test the onFontBoldChanged function
        """
        string: str = "This is a test."
        self.document.setPlainText(string)

        # set the document text to bold
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontBoldChanged(True)

        # check if the text is actually bold
        act_is_bold = self.document.fontBold()
        self.assertEqual(True, act_is_bold)

        # set the document text to NOT bolded
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontBoldChanged(False)

        # check if the text is actually NOT bolded
        act_is_bold = self.document.fontBold()
        self.assertEqual(False, act_is_bold)

    def testFontItal(self):
        """
        Test the onFontItalChanged function
        """
        string: str = "This is a test."
        self.document.setPlainText(string)

        # set the document text to italicized
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontItalChanged(True)

        # check if the text is actually italicized
        act_is_ital = self.document.fontItalic()
        self.assertEqual(True, act_is_ital)

        # set the document text to NOT italicized
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontItalChanged(False)

        # check if the text is actually NOT italicized
        act_is_ital = self.document.fontItalic()
        self.assertEqual(False, act_is_ital)

    def testFontStrike(self):
        """
        Test the onFontStrikeChanged function
        """
        string: str = "This is a test."
        self.document.setPlainText(string)

        # set the document text to strikethrough
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontStrikeChanged(True)

        # check if the text is actually strikethrough
        act_is_strike = self.document.fontStrike()
        self.assertEqual(True, act_is_strike)

        # set the document text to NOT strikethrough
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontStrikeChanged(False)

        # check if the text is actually NOT strikethrough
        act_is_strike = self.document.fontStrike()
        self.assertEqual(False, act_is_strike)

    def testFontUnder(self):
        """
        Test the onFontUnderChanged function
        """
        string: str = "This is a test."
        self.document.setPlainText(string)

        # set the document text to italicized
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontUnderChanged(True)

        # check if the text is actually italicized
        act_is_under = self.document.fontUnderline()
        self.assertEqual(True, act_is_under)

        # set the document text to NOT italicized
        cursor = self.document.textCursor()
        cursor.select(cursor.Document)
        self.document.onFontUnderChanged(False)

        # check if the text is actually NOT italicized
        act_is_under = self.document.fontUnderline()
        self.assertEqual(False, act_is_under)

    def testClearAllFormat(self):
        """
        Test the clearAllFormatting function
        """
        string: str = "This is a test."
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
        string: str = "This is a test."
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
