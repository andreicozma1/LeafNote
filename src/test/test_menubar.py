"""
test Menu Bar default behavior
"""
import unittest

from test import app


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
        self.document = app.document
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
