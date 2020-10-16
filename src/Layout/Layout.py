import logging

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter

"""
sets the way the application will be layed out
"""


class Layout(QWidget):
    """
    class that hold the layout properties
    """

    def __init__(self, appProps, layoutProps):
        """
        sets up the inital workspace
        :param appProps: reference to application properties
        :param layoutProps: reference to the layout properties
        :return: returns nothing
        """
        super().__init__()
        logging.info("")

        # Init variables
        self.app_props = appProps
        self.layout_props = layoutProps

    def makeMainLayout(self):
        # Main layout of the application. Holds the top bar, main horizontal layout, as well as the bottom bar
        main_layout = QVBoxLayout()  # this defines the QWidget as the parent for the layout
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(self.layout_props.splitter_width)
        self.setLayout(main_layout)
        return main_layout

    def makeHSplitterLayout(self, left_menu, bar_open_tabs, document, right_menu, search_and_replace):
        horizontal_workspace = QSplitter(QtCore.Qt.Horizontal)  # Splitter between LeftMenu, Doc, and Right Menu
        horizontal_workspace.setHandleWidth(self.layout_props.splitter_width)

        horizontal_workspace.addWidget(left_menu)

        document_view = QWidget()
        doc_layout = QVBoxLayout(document_view)
        doc_layout.setContentsMargins(0, 0, 0, 0)
        doc_layout.setSpacing(self.layout_props.splitter_width)
        doc_layout.addWidget(bar_open_tabs)
        doc_layout.addWidget(search_and_replace)
        doc_layout.addWidget(document)
        horizontal_workspace.addWidget(document_view)

        horizontal_workspace.addWidget(right_menu)

        return horizontal_workspace
