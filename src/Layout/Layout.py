"""
sets the way the application will be layed out
"""

import logging

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter


class Layout(QWidget):
    """
    class that hold the layout properties
    """

    def __init__(self, app_props, layout_props):
        """
        sets up the inital workspace
        :param app_props: reference to application properties
        :param layout_props: reference to the layout properties
        :return: returns nothing
        """
        # noinspection PyCompatibility
        super().__init__()
        logging.info("Creating Main Application Layout")

        # Init variables
        self.app_props = app_props
        self.layout_props = layout_props

    def makeMainLayout(self):
        """
        this will create the main layout of the application
        :return: returns the created layout
        """
        logging.debug("Creating Layout - Vertical")
        # Main layout of the application. Holds the top bar,
        # main horizontal layout, as well as the bottom bar
        main_layout = QVBoxLayout()  # this defines the QWidget as the parent for the layout
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(self.layout_props.getDefSplitterWidth())
        self.setLayout(main_layout)
        return main_layout

    def makeHSplitterLayout(self, left_menu, bar_open_tabs, document,
                            right_menu, search_and_replace):
        """
        This will create the layout containing the middle section of the application
        :param left_menu: reference to the left menu of the application
        :param bar_open_tabs: reference to the bar containing the open tabs
        :param document: reference to the document
        :param right_menu: reference to the right menu of the application.
        :param search_and_replace: reference to the search and replace for the document
        :return: returns the created layout
        """
        logging.debug("Creating Layout - Horizontal")

        horizontal_workspace = QSplitter(
            QtCore.Qt.Horizontal)  # Splitter between LeftMenu, Doc, and Right Menu
        horizontal_workspace.setHandleWidth(self.layout_props.getDefSplitterWidth())

        horizontal_workspace.addWidget(left_menu)

        document_view = QWidget()
        doc_layout = QVBoxLayout(document_view)
        doc_layout.setContentsMargins(0, 0, 0, 0)
        doc_layout.setSpacing(0)
        doc_layout.addWidget(bar_open_tabs)
        doc_layout.addWidget(search_and_replace)
        doc_layout.addWidget(document)
        horizontal_workspace.addWidget(document_view)

        horizontal_workspace.addWidget(right_menu)

        return horizontal_workspace
