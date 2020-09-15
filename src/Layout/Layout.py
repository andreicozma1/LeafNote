from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter

from src.Elements.ColorWidget import Color
from src.Elements.DirectoryViewer import DirectoryViewer
from src.Elements.Document import Document


class Layout():
    def __init__(self, app, appProps, layoutProps):
        print("Layout - init")

        # Init variables
        self.app = app
        self.app_props = appProps
        self.layout_props = layoutProps

        self.central_widget = QWidget()
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.horizontal_layout = QHBoxLayout()
        self.splitter = QSplitter(QtCore.Qt.Horizontal)  # Splitter between LeftMenu, Doc, and Right Menu

        # TODO - Top Bar (HBoxLayout) for Font Style, Size, Color, Highlighting, etc
        self.top_bar = Color('red')
        # TODO - BottomBar (HBoxLayout) for certain actions and information
        self.bottom_bar = Color("purple")
        # TODO - Left menu (VBoxLayout) is used to show workspaces and directory structure for notes
        self.left_menu = DirectoryViewer(self.app.file_manager, self.app_props.mainPath)
        # TODO - Right menu (VBoxLayout) for document context actions like customizations, reminders, properties, etc.
        self.right_menu = Color('red')

        self.document = Document()

    def setup(self):
        print("Layout - setup")
        self.updateDimensions()

        # Create a Vertical Box layout which will contain top bar, content, and bottom bar
        self.vertical_layout.addWidget(self.top_bar)
        self.vertical_layout.setSpacing(self.layout_props.splitter_width * 3)
        # Create the horizontal layout which contains the left menu, text box, and right menu

        self.splitter.addWidget(self.left_menu)
        self.splitter.addWidget(self.document)
        self.splitter.addWidget(self.right_menu)
        self.splitter.setHandleWidth(self.layout_props.splitter_width)
        self.horizontal_layout.addWidget(self.splitter)

        # add the horizontal layout to the middle
        self.vertical_layout.addWidget(self.splitter)
        # add the bottom bar
        self.vertical_layout.addWidget(self.bottom_bar)

        return self.central_widget

    def updateDimensions(self):
        app_props = self.layout_props.app.app_props
        # print("Layout - set_dimensions")
        self.top_bar.setMaximumHeight(self.layout_props.bar_height)
        self.bottom_bar.setMaximumHeight(self.layout_props.bar_height)
        self.left_menu.setMinimumWidth(int(self.layout_props.app.width() * self.layout_props.min_menu_width * (
                app_props.width / self.layout_props.app.width())))
        self.left_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.layout_props.app.width()))
        self.right_menu.setMinimumWidth(int(self.layout_props.app.width() * self.layout_props.min_menu_width * (
                app_props.width / self.layout_props.app.width())))
        self.right_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.layout_props.app.width()))
        self.document.setMinimumWidth(self.layout_props.min_doc_width * self.layout_props.app.width())
