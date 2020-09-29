from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter, QStackedLayout


class Layout(QWidget):
    def __init__(self, app, appProps, layoutProps):
        super().__init__()
        print("Layout - init")

        # Init variables
        self.app = app
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

        # self.menu_right = QWidget()
        # QStackedLayout(self.menu_right).setContentsMargins(0, 0, 0, 0)

        # TODO - uncomment when implementing right menu
        self.top_bar = QWidget()
        QStackedLayout(self.top_bar).setContentsMargins(0, 0, 0, 0)

        self.bottom_bar = QWidget()
        QStackedLayout(self.bottom_bar).setContentsMargins(0, 0, 0, 0)

        self.setup()

    def setup(self):
        print("Layout - setup")
        self.updateDimensions()

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
        self.top_bar.layout().addWidget(topBar)

    def setBottomBar(self, bottomBar: QWidget):
        self.bottom_bar.layout().addWidget(bottomBar)

    def setLeftMenu(self, leftMenu: QWidget):
        self.menu_left.layout().addWidget(leftMenu)

    # def setRightMenu(self, rightMenu: QWidget):
    #     self.menu_right.layout().addWidget(rightMenu)

    def setBarOpenTabs(self, barOpenTabs: QWidget):
        self.bar_open_tabs.layout().addWidget(barOpenTabs)

    def setDocument(self, document: QWidget):
        self.document.layout().addWidget(document)

    def updateDimensions(self):
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(self.layout_props.splitter_width)
        self.horizontal_workspace.setHandleWidth(self.layout_props.splitter_width)
        self.documents_view.layout().setContentsMargins(0, 0, 0, 0)
        self.documents_view.layout().setSpacing(self.layout_props.splitter_width)
        self.bar_open_tabs.setFixedHeight(self.app.layout_props.bar_tabs_height)

        self.top_bar.setFixedHeight(self.layout_props.bar_height)
        self.bottom_bar.setFixedHeight(self.layout_props.bar_height)
        self.menu_left.setMinimumWidth(int(self.layout_props.app.width() * self.layout_props.min_menu_width * (
                self.app_props.width / self.layout_props.app.width())))
        self.menu_left.setMaximumWidth(int(self.layout_props.max_menu_width * self.layout_props.app.width()))
        # TODO - uncomment when implementing right menu
        # self.menu_right.setMinimumWidth(int(self.layout_props.app.width() * self.layout_props.min_menu_width * (
        #         self.app_props.width / self.layout_props.app.width())))
        # self.menu_right.setMaximumWidth(int(self.layout_props.max_menu_width * self.layout_props.app.width()))
        self.documents_view.setMinimumWidth(self.layout_props.min_doc_width * self.layout_props.app.width())
