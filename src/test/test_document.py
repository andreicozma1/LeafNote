"""
test Document default behavior
"""
import unittest

from PyQt5.QtGui import QFont
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