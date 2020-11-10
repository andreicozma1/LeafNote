"""
test Bottom Bar default behavior
"""
import unittest

import test


class TestBottomBar(unittest.TestCase):
    """
    Unit test for all Bottom Bar functionality
    """

    def setUp(self):
        """
        Set up environment
        """
        self.bottom_bar = test.app.bottom_bar
        self.document = test.app.document
        self.doc_props = test.app.doc_props
        self.layout_props = test.app.layout_props

    def testBarHeight(self):
        """
        Test default height
        """
        exp_height = self.layout_props.getDefaultBarHeight()
        act_height = self.bottom_bar.height()
        self.assertEqual(exp_height, act_height)

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

        exp_count = str(len(string)) + " Characters"

        self.document.setPlainText(string)
        act_count = self.bottom_bar.label_cc.text()

        self.assertEqual(exp_count, act_count)

    def testResetZoom(self):
        """
        Test the reset zoom button
        """
        act_slider_start = self.bottom_bar.slider_start

        self.bottom_bar.onZoomOutClicked()
        self.bottom_bar.resetZoom()
        exp_slider_start = self.bottom_bar.zoom_slider.value()

        self.assertEqual(exp_slider_start, act_slider_start)
