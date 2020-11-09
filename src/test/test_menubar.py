"""
test Menu Bar default behavior
"""
import unittest

from PyQt5.QtWidgets import QApplication, QComboBox, QFontComboBox, QAbstractButton

from LeafNote import App

ctx = QApplication([])
app = App(ctx)


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
        self.doc_props = app.doc_props
        self.layout_props = app.layout_props
        self.file_manager = app.file_manager
        self.bottom_bar = app.bottom_bar
        self.left_menu = app.left_menu
        self.document = app.document

    # ========= START GENERAL LAYOUT SECTION =========

    def testBarHeight(self):
        """
        Test default height
        """
        exp_height = self.layout_props.getDefaultMenuBarHeight()
        act_height = self.menu_bar.height()
        self.assertEqual(exp_height, act_height)

    # ========= END GENERAL LAYOUT SECTION =========

    # ========= START FILE TAB SECTION =========

    def testFileTab(self):
        """
        Test File Tab
        """
        element = self.menu_bar.makeFileMenu(app, self.file_manager)
        # Test is in layout
        self.assertIn(element, self.menu_bar.children())
        self.assertEqual(element.title(), "&File")

    # ========= END FILE TAB SECTION =========

    # ========= START EDIT TAB SECTION =========

    def testEditTab(self):
        """
        Test Edit Tab
        """
        element = self.menu_bar.makeEditMenu(app, self.file_manager)
        # Test is in layout
        self.assertIn(element, self.menu_bar.children())
        self.assertEqual(element.title(), "&Edit")

    # ========= END EDIT TAB SECTION =========

    # ========= START VIEW TAB SECTION =========

    def testViewTab(self):
        """
        Test View Tab
        """
        element = self.menu_bar.makeViewMenu(app, self.bottom_bar, self.left_menu)
        # Test is in layout
        self.assertIn(element, self.menu_bar.children())
        self.assertEqual(element.title(), "&View")

    # ========= END VIEW TAB SECTION =========

    # ========= START FORMAT TAB SECTION =========

    def testFormatTab(self):
        """
        Test Format Tab
        """
        element = self.menu_bar.makeFormatMenu(app)
        # Test is in layout
        self.assertIn(element, self.menu_bar.children())
        self.assertEqual(element.title(), "&Format")

    # def testFormattingMode(self):
    #     """
    #     Test default format mode btn behavior
    #     """
    #     element: QAbstractButton = self.top_bar.button_mode_switch
    #     self.assertTrue(element.isCheckable())
    #     self.assertFalse(element.isChecked())
    #     # Test is in layout
    #     self.assertIn(element, self.top_bar.children())

    # ========= END FORMAT TAB SECTION =========

    # ========= START TOOLS TAB SECTION =========

    def testToolsTab(self):
        """
        Test Tools Tab
        """
        element = self.menu_bar.makeToolsMenu(app, self.document)
        # Test is in layout
        self.assertIn(element, self.menu_bar.children())
        self.assertEqual(element.title(), "&Tools")

    # ========= END TOOLS TAB SECTION =========
