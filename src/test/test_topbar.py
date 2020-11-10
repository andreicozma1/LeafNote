"""
test Top Bar default behavior
"""
import unittest

from PyQt5.QtWidgets import QComboBox, QFontComboBox, QAbstractButton

from test import app


class TestTopBar(unittest.TestCase):
    """
    Unit test for all Top Bar functionality
    """

    def setUp(self):
        """
        Set up environment
        """
        self.top_bar = app.top_bar
        self.doc_props = app.doc_props
        self.layout_props = app.layout_props

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

class TestMenuBar(unittest.TestCase):
    """
    Unit test for all Menu Bar functionality
    """

    # set up for the test
    def setUp(self):
        """
        Set up environment
        """
        self.menu_bar = app.menu_bar
        self.menu_bar_list = list(self.menu_bar.children())

    # ========= START GENERAL SECTION =========

    def testMenuBar(self):
        """
        Test menu_bar isEnable isVisible
        """
        self.assertEqual(self.menu_bar.isEnabled(), True)
        self.assertEqual(self.menu_bar.isVisible(), False)

    def testMenuFormat(self):
        """
        Test menu_format isEnable isVisible
        """
        self.assertEqual(self.menu_bar.menu_format.isEnabled(), True)
        self.assertEqual(self.menu_bar.menu_format.isVisible(), False)

    def testGroupStyle(self):
        """
        Test group_style isEnable isVisible
        """
        self.assertEqual(self.menu_bar.group_style.isEnabled(), True)
        self.assertEqual(self.menu_bar.group_style.isVisible(), True)

    def testGroupAlign(self):
        """
        Test group_align isEnable isVisible
        """
        self.assertEqual(self.menu_bar.group_align.isEnabled(), True)
        self.assertEqual(self.menu_bar.group_align.isVisible(), True)

    # ========= END GENERAL SECTION =========

    # ========= START FILE TAB SECTION =========

    def testFileTab(self):
        """
        Test File Tab
        """
        element = self.menu_bar_list[1]
        # Test is in layout
        self.assertIn(element, self.menu_bar.children())
        self.assertEqual(element.title(), "&File")
        self.assertEqual(element.isEnabled(), True)
        self.assertEqual(element.isVisible(), False)

    # ========= END FILE TAB SECTION =========

    # ========= START EDIT TAB SECTION =========

    def testEditTab(self):
        """
        Test Edit Tab
        """
        element = self.menu_bar_list[2]
        # Test is in layout
        self.assertIn(element, self.menu_bar.children())
        self.assertEqual(element.title(), "&Edit")
        self.assertEqual(element.isEnabled(), True)
        self.assertEqual(element.isVisible(), False)

    # ========= END EDIT TAB SECTION =========

    # ========= START VIEW TAB SECTION =========

    def testViewTab(self):
        """
        Test View Tab
        """
        element = self.menu_bar_list[3]
        # Test is in layout
        self.assertIn(element, self.menu_bar.children())
        self.assertEqual(element.title(), "&View")
        self.assertEqual(element.isEnabled(), True)
        self.assertEqual(element.isVisible(), False)

    # ========= END VIEW TAB SECTION =========

    # ========= START FORMAT TAB SECTION =========

    def testFormatTab(self):
        """
        Test Format Tab
        """
        element = self.menu_bar_list[4]
        # Test is in layout
        self.assertIn(element, self.menu_bar.children())
        self.assertEqual(element.title(), "&Format")
        self.assertEqual(element.isEnabled(), True)
        self.assertEqual(element.isVisible(), False)

    # ========= END FORMAT TAB SECTION =========

    # ========= START TOOLS TAB SECTION =========

    def testToolsTab(self):
        """
        Test Tools Tab
        """
        element = self.menu_bar_list[5]
        # Test is in layout
        self.assertIn(element, self.menu_bar.children())
        self.assertEqual(element.title(), "&Tools")
        self.assertEqual(element.isEnabled(), True)
        self.assertEqual(element.isVisible(), False)

    # ========= END TOOLS TAB SECTION =========
