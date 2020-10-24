"""
holds the class with the layout properties
"""

import logging


class LayoutProps:
    """
    class has the default layout properties
    """

    def __init__(self):
        """
        the default properties for the layout
        :return: returns nothing
        """
        logging.debug("Setting up Layout Props")

        self.min_doc_width = .4
        self.min_menu_width = .2
        self.max_menu_width = .3
        self.bar_height = 35

    # ========= START GENERAL LAYOUT SECTION =========

    @staticmethod
    def getDefSplitterWidth():
        """
        Returns the default columns shown in the left menu at startup
        """
        return 1

    # ========= END GENERAL LAYOUT SECTION =========

    # ========= START OPEN TABS BAR SECTION =========
    @staticmethod
    def getDefOpenTabWidth():
        """
        Returns the fixed size of each tab in Open Tabs Bar
        If None, then the width will be calculated automatically based on content
        """
        return None

    @staticmethod
    def getDefOpenTabHeight():
        """
        Returns the default Open Tabs Bar height
        """
        return 35

    @staticmethod
    def getDefTabsBarSpacing():
        """
        Returns the default Open Tabs Bar spacing between tabs
        """
        return 1

    # ========= END OPEN TABS BAR SECTION =========

    # ========= START LEFT MENU SECTION =========

    @staticmethod
    def getDefaultLeftMenuCols():
        """
        Returns the default columns shown in the left menu at startup
        """
        return ["Name"]

    @staticmethod
    def getDefaultLeftMenuItemHeight():
        """
        Returns the default Left Menu Item height
        """
        return 30

    @staticmethod
    def getDefaultLeftMenuHeaderMargin():
        """
        Returns the default Left Menu Header Margin
        """
        return 4

    @staticmethod
    def getDefaultLeftMenuHeaderColor():
        """
        Returns the default Left Menu Header Color
        """
        return "rgba(56, 90, 125, 1.0)"

    @staticmethod
    def getDefaultLeftMenuSelectColor():
        """
        Returns the default Left Menu Select color
        """
        return "rgba(249, 145, 146, 0.6)"

    @staticmethod
    def getDefaultLeftMenuHoverColor():
        """
        Returns the default Left Menu Hover Color
        """
        return "rgba(249, 145, 146, 0.1)"

    # ========= END LEFT MENU SECTION =========
