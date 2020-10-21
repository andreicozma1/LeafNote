"""
holds the class with the layout properties
"""

import logging


class LayoutProps:
    """
    class has the default layout properties
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes

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

        self.header_margin = 5
        self.header_color = "rgba(249, 145, 146, 0.8)"
        self.item_height = 30
        self.item_hover_color = "rgba(249, 145, 146, 0.2)"


        self.splitter_width = 1
