"""
Tests Top Bar default behavior
"""
import unittest

from PyQt5.QtWidgets import QApplication, QComboBox, QFontComboBox, QAbstractButton

from main import App


class TestTopBar(unittest.TestCase):
    """
    Unit Tests for all Top Bar functionality
    """

    def setUp(self):
        """
        Set up environment
        """
        ctx = QApplication([])
        self.app = App(ctx)
        self.top_bar = self.app.top_bar
        self.doc_props = self.app.doc_props
        self.layout_props = self.app.layout_props

    def testBarHeight(self):
        """
        Test default height
        """
        exp_height = self.layout_props.getDefaultBarHeight()
        act_height = self.top_bar.height()
        self.assertEqual(exp_height, act_height)

    def testTitleStyle(self):
        """
        Test default title style behavior
        """
        element: QComboBox = self.top_bar.combo_title_style
        # Test Default (expected, actual)
        def_style = self.doc_props.default
        exp_index = list(self.doc_props.dict_title_styles.values()).index(def_style)
        act_index = element.currentIndex()
        self.assertEqual(exp_index, act_index)
        # Test is in layout
        self.assertIn(element, self.top_bar.children())

    def testFontStyle(self):
        """
        Test default font style behavior
        """
        element: QFontComboBox = self.top_bar.combo_font_style
        # Test is in layout
        self.assertIn(element, self.top_bar.children())

    def testFontSize(self):
        """
        Test default font size behavior
        """
        element: QComboBox = self.top_bar.combo_font_size
        # Test Default (expected, actual)
        def_index = self.doc_props.def_font_size_index
        self.assertEqual(def_index, element.currentIndex())
        # Test has all elements
        exp_len = len(self.doc_props.list_font_sizes)
        act_len = element.count()
        self.assertEqual(exp_len, act_len)
        # Test is in layout
        self.assertIn(element, self.top_bar.children())

    def testFontBold(self):
        """
        Test default bold btn behavior
        """
        element: QAbstractButton = self.top_bar.button_bold
        # Test defaults
        self.assertTrue(element.isCheckable())
        self.assertFalse(element.isChecked())
        # Test is in layout
        self.assertIn(element, self.top_bar.children())

    def testFontItalic(self):
        """
        Test default ital btn behavior
        """
        element: QAbstractButton = self.top_bar.button_ital
        # Test defaults
        self.assertTrue(element.isCheckable())
        self.assertFalse(element.isChecked())
        # Test is in layout
        self.assertIn(element, self.top_bar.children())

    def testFontStrike(self):
        """
        Test default strike btn behavior
        """
        element: QAbstractButton = self.top_bar.button_strike
        # Test defaults
        self.assertTrue(element.isCheckable())
        self.assertFalse(element.isChecked())
        # Test is in layout
        self.assertIn(element, self.top_bar.children())

    def testFontUnder(self):
        """
        Test default under btn behavior
        """
        element: QAbstractButton = self.top_bar.button_under
        # Test defaults
        self.assertTrue(element.isCheckable())
        self.assertFalse(element.isChecked())
        # Test is in layout
        self.assertIn(element, self.top_bar.children())

    def testTextColor(self):
        """
        Test default text color behavior
        """
        element: QComboBox = self.top_bar.combo_text_color
        # Test Default (expected, actual)
        def_index = list(self.doc_props.dict_colors).index(
            self.doc_props.def_text_color_key)
        self.assertEqual(def_index, element.currentIndex())
        # Test Default Stylesheet
        def_color = self.doc_props.dict_colors[self.doc_props.def_text_color_key]
        self.assertIn(def_color, element.styleSheet())
        # Test has all elements
        exp_len = len(self.doc_props.dict_colors)
        act_len = element.count()
        self.assertEqual(exp_len, act_len)
        # Test is in layout
        self.assertIn(element, self.top_bar.children())

    def testTextColorChange(self):
        """
            Test stylesheet change on index change
        """
        element: QComboBox = self.top_bar.combo_text_color
        # iterate through the color list
        for index, key in enumerate(self.doc_props.dict_colors.keys()):
            value_hex = self.doc_props.dict_colors[key]
            element.setCurrentIndex(index)
            self.assertIn(value_hex, element.styleSheet())

    def testClearFormat(self):
        """
        Test default clear format btn behavior
        """
        element: QAbstractButton = self.top_bar.button_clear
        self.assertFalse(element.isCheckable())
        # Test is in layout
        self.assertIn(element, self.top_bar.children())

    def testTextAlign(self):
        """
        Test default text align behavior
        """
        element: QComboBox = self.top_bar.combo_text_align
        # Test Default (expected, actual)
        def_index = list(self.doc_props.dict_text_aligns).index(
            self.doc_props.def_text_align_key)
        self.assertEqual(def_index, element.currentIndex())
        # Test has all elements
        exp_len = len(self.doc_props.dict_text_aligns)
        act_len = element.count()
        self.assertEqual(exp_len, act_len)
        # Test is in layout
        self.assertIn(element, self.top_bar.children())

    def testFormattingMode(self):
        """
        Test default format mode btn behavior
        """
        element: QAbstractButton = self.top_bar.button_mode_switch
        self.assertTrue(element.isCheckable())
        self.assertFalse(element.isChecked())
        # Test is in layout
        self.assertIn(element, self.top_bar.children())
