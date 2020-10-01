import logging

"""
holds the class with the layout properties
"""


class LayoutProps():
    """
    class has the default layout properties
    """
    def __init__(self):
        """
        the default properties for the layout
        :return: returns nothing
        """
        logging.info("Setting up Layout Properties")

        self.min_doc_width = .4
        self.min_menu_width = .2
        self.max_menu_width = .3
        self.bar_height = 35
        self.bar_tabs_height = 25
        self.bar_tabs_spacing = 1
        self.bar_tabs_tab_width = 50

        self.splitter_width = 1
