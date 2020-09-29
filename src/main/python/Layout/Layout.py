from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter

from Elements.BottomBar import BottomBar
from Elements.DirectoryViewer import DirectoryViewer
from Elements.Document import Document
from Elements.OpenTabsBar import OpenTabsBar
from Elements.TopBar import TopBar


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
        self.documents_view_layout = QVBoxLayout(self.documents_view) # Parent of layout passed in constructor
        self.bar_open_tabs = OpenTabsBar(self.app)
        self.document = Document(self)

        self.menu_left = DirectoryViewer(self.app.file_manager, self.app_props.mainPath)
        # TODO - uncomment when implementing right menu
        # self.menu_right = Color('white')

        self.top_bar = TopBar(self.document)
        self.bottom_bar = BottomBar(self.document)

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

        # Set up the secondary vertical layout
        self.horizontal_workspace.addWidget(self.menu_left)
        self.horizontal_workspace.addWidget(self.documents_view)
        # TODO - uncomment when implementing right menu
        # self.horizontal_workspace.addWidget(self.menu_right)

        self.documents_view.layout().addWidget(self.bar_open_tabs)
        self.documents_view.layout().addWidget(self.document)

    def updateDimensions(self):
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(self.layout_props.splitter_width)
        self.horizontal_workspace.setHandleWidth(self.layout_props.splitter_width)
        self.documents_view.layout().setContentsMargins(0, 0, 0, 0)
        self.documents_view.layout().setSpacing(self.layout_props.splitter_width)

        self.top_bar.setFixedHeight(self.layout_props.bar_height)
        self.bottom_bar.setFixedHeight(self.layout_props.bar_height)
        self.menu_left.setMinimumWidth(int(self.layout_props.app.width() * self.layout_props.min_menu_width * (
                self.app_props.width / self.layout_props.app.width())))
        self.menu_left.setMaximumWidth(int(self.layout_props.max_menu_width * self.layout_props.app.width()))
        # TODO - uncomment when implementing right menu
        # self.menu_right.setMinimumWidth(int(self.layout_props.app.width() * self.layout_props.min_menu_width * (
        #         self.app_props.width / self.layout_props.app.width())))
        # self.menu_right.setMaximumWidth(int(self.layout_props.max_menu_width * self.layout_props.app.width()))
        self.document.setMinimumWidth(self.layout_props.min_doc_width * self.layout_props.app.width())
