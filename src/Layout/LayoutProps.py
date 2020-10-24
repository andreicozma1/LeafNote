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
        self.bar_tabs_height = 25
        self.bar_tabs_spacing = 1
        self.bar_tabs_tab_width = 50

        self.splitter_width = 1

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
        return 5

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
