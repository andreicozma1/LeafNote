"""
test Bottom Bar default behavior
"""
import unittest

from PyQt5.QtWidgets import QApplication

from LeafNote import App

ctx = QApplication([])
app = App(ctx)


class TestBottomBar(unittest.TestCase):
    """
    Unit test for all Bottom Bar functionality
    """

    def setUp(self):
        """
        Set up environment
        """
        self.bottom_bar = app.bottom_bar
        self.document = app.document
        self.doc_props = app.doc_props
        self.layout_props = app.layout_props

    def testWordCount(self):
        """
        Test the word count label
        """
        string = "This is a test."

        exp_count = str(len(string.split())) + " Words"

        self.document.setPlainText(string)
        act_count = self.bottom_bar.label_wc.text()

        self.assertEqual(exp_count, act_count)

    def testCharCount(self):
        """
        Test the character count label
        """
        string = "This is a test."

        exp_count = str(len(string.replace(" ", ""))) + " Characters"

        self.document.setPlainText(string)
        act_count = self.bottom_bar.label_cc.text()

        self.assertEqual(exp_count, act_count)
