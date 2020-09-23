from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter

from Elements.BottomBar import BottomBar
from Elements.DirectoryViewer import DirectoryViewer
from Elements.Document import Document
from Elements.OpenTabsBar import OpenTabsBar
from Elements.TopBar import TopBar


class Layout:
    def __init__(self, app, appProps, layoutProps):
        print("Layout - init")

        # Init variables
        self.app = app
        self.app_props = appProps
        self.layout_props = layoutProps

        self.central_widget = QWidget()
        # The main layout of the application is the vertical layout
        # This layout holds the top bar, main horizontal layout, as well as the bottom bar
        self.vertical_layout = QVBoxLayout(self.central_widget)
        # The horizontal layout contains the left menu, documents layout, and the right menu
        self.horizontal_layout = QHBoxLayout()
        # The splitter defines the resizing functionality of the horizontal layout
        self.splitter = QSplitter(QtCore.Qt.Horizontal)  # Splitter between LeftMenu, Doc, and Right Menu

        self.left_menu = DirectoryViewer(self.app.file_manager, self.app_props.mainPath)
        # TODO - uncomment when implementing right menu
        # self.right_menu = Color('white')

        self.bottom_bar = BottomBar()

        self.open_tabs_bar = OpenTabsBar(self.app)
        self.document = Document(self.bottom_bar)

        self.top_bar = TopBar(self.document)

    def setup(self):
        print("Layout - setup")
        self.updateDimensions()

        # Create a Vertical Box layout which will contain top bar, content, and bottom bar
        self.vertical_layout.addWidget(self.top_bar)
        self.vertical_layout.setSpacing(self.layout_props.splitter_width)

        self.splitter.addWidget(self.left_menu)

        vertical_layout_documents = QWidget()
        docs_layout = QVBoxLayout()
        docs_layout.setSpacing(self.layout_props.splitter_width)
        docs_layout.setContentsMargins(0, 0, 0, 0)
        docs_layout.addWidget(self.open_tabs_bar)
        docs_layout.addWidget(self.document)
        vertical_layout_documents.setLayout(docs_layout)
        self.splitter.addWidget(vertical_layout_documents)

        # TODO - uncomment when implementing right menu
        # self.splitter.addWidget(self.right_menu)
        self.splitter.setHandleWidth(self.layout_props.splitter_width)
        self.horizontal_layout.addWidget(self.splitter)

        # add the horizontal layout to the middle
        self.vertical_layout.addWidget(self.splitter)
        # add the bottom bar
        self.vertical_layout.addWidget(self.bottom_bar)

        return self.central_widget

    def updateDimensions(self):
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.top_bar.setFixedHeight(self.layout_props.bar_height)
        self.bottom_bar.setFixedHeight(self.layout_props.bar_height)
        self.left_menu.setMinimumWidth(int(self.layout_props.app.width() * self.layout_props.min_menu_width * (
                self.app_props.width / self.layout_props.app.width())))
        self.left_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.layout_props.app.width()))
        # TODO - uncomment when implementing right menu
        # self.right_menu.setMinimumWidth(int(self.layout_props.app.width() * self.layout_props.min_menu_width * (
        #         self.app_props.width / self.layout_props.app.width())))
        # self.right_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.layout_props.app.width()))
        self.document.setMinimumWidth(self.layout_props.min_doc_width * self.layout_props.app.width())
