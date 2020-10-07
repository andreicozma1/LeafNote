import logging

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter, QStackedLayout

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

        # Main layout of the application. Holds the top bar, main horizontal layout, as well as the bottom bar
        QVBoxLayout(self)  # this defines the QWidget as the parent for the layout
        # Horizontal layout contains the left menu, documents layout, and the right menu
        self.horizontal_workspace = QSplitter(QtCore.Qt.Horizontal)  # Splitter between LeftMenu, Doc, and Right Menu

        # Documents view holds the open tabs as well as the actual document
        self.documents_view = QWidget()
        self.documents_view_layout = QVBoxLayout(self.documents_view)  # Parent of layout passed in constructor

        self.document = QWidget()
        QStackedLayout(self.document).setContentsMargins(0, 0, 0, 0)

        self.bar_open_tabs = QWidget()
        QStackedLayout(self.bar_open_tabs).setContentsMargins(0, 0, 0, 0)

        self.menu_left = QWidget()
        QStackedLayout(self.menu_left).setContentsMargins(0, 0, 0, 0)

        self.top_bar = QWidget()
        QStackedLayout(self.top_bar).setContentsMargins(0, 0, 0, 0)

        self.bottom_bar = QWidget()
        QStackedLayout(self.bottom_bar).setContentsMargins(0, 0, 0, 0)

        self.setup()

    def setup(self):
        """
        sets up the workspace of the application
        :return: returns nothing
        """
        logging.info("")
        # Set up the main vertical layout
        # add the top bar at the top
        self.layout().addWidget(self.top_bar)
        # add the horizontal layout to the middle
        self.layout().addWidget(self.horizontal_workspace)
        # add the bottom bar at the bottom
        self.layout().addWidget(self.bottom_bar)

        self.documents_view_layout.addWidget(self.bar_open_tabs)
        self.documents_view_layout.addWidget(self.document)

        # Set up the secondary vertical layout
        self.horizontal_workspace.addWidget(self.menu_left)
        self.horizontal_workspace.addWidget(self.documents_view)
        # self.horizontal_workspace.addWidget(self.menu_right)

    def setTopBar(self, topBar: QWidget):
        """
        sets up top bar
        :param topBar: reference to top bar
        :return: returns nothing
        """
        self.top_bar.layout().addWidget(topBar)

    def setBottomBar(self, bottomBar: QWidget):
        """
        sets up bottom bar
        :param bottomBar: reference to bottom bar
        :return: returns nothing
        """
        self.bottom_bar.layout().addWidget(bottomBar)

    def setLeftMenu(self, leftMenu: QWidget):
        """
        sets up the left menu
        :param leftMenu: reference to left menu
        :return: returns nothing
        """
        self.menu_left.layout().addWidget(leftMenu)

    def setBarOpenTabs(self, barOpenTabs: QWidget):
        """
        sets up the tabs
        :param barOpenTabs: reference to tabs
        :return: returns nothing
        """
        self.bar_open_tabs.layout().addWidget(barOpenTabs)

    def setDocument(self, document: QWidget):
        """
        sets up the document
        :param document: reference to document
        :return: returns nothing
        """
        self.document.layout().addWidget(document)

    def updateDimensions(self, app):
        """
        changes the dimensions of the application
        :param app: reference to application
        :return: returns nothing
        """
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(self.layout_props.splitter_width)
        self.horizontal_workspace.setHandleWidth(self.layout_props.splitter_width)
        self.documents_view.layout().setContentsMargins(0, 0, 0, 0)
        self.documents_view.layout().setSpacing(self.layout_props.splitter_width)
        self.bar_open_tabs.setFixedHeight(self.layout_props.bar_tabs_height)

        self.top_bar.setFixedHeight(self.layout_props.bar_height)
        self.bottom_bar.setFixedHeight(self.layout_props.bar_height)
        self.menu_left.setMinimumWidth(int(app.width() * self.layout_props.min_menu_width * (
                self.app_props.width / app.width())))
        self.menu_left.setMaximumWidth(int(self.layout_props.max_menu_width * app.width()))
        # TODO - uncomment when implementing right menu
        # self.menu_right.setMinimumWidth(int(app.width() * self.layout_props.min_menu_width * (
        #         self.app_props.width / app.width())))
        # self.menu_right.setMaximumWidth(int(self.layout_props.max_menu_width * app.width()))
        self.documents_view.setMinimumWidth(self.layout_props.min_doc_width * app.width())
