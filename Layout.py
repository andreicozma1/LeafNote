from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QApplication

from ColorWidget import Color
from DirectoryViewer import DirectoryViewer
from Document import Document
from BottomBar import BottomBar


class Layout():
    def __init__(self, layout_props):
        print("Layout - init")

        # Init variables
        self.layout_props = layout_props

        self.central_widget = QWidget()
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.horizontal_layout = QHBoxLayout()
        self.splitter = QSplitter(QtCore.Qt.Horizontal)  # Splitter between LeftMenu, Doc, and Right Menu

        # TODO - Top Bar (HBoxLayout) for Font Style, Size, Color, Highlighting, etc
        self.top_bar = Color('red')
        # TODO - BottomBar (HBoxLayout) for certain actions and information
        self.bottom_bar = BottomBar()
        # TODO - Left menu (VBoxLayout) is used to show workspace and directory structure for notes
        self.left_menu = DirectoryViewer()
        # TODO - Right menu (VBoxLayout) for document context actions like customizations, reminders, properties, etc.
        self.right_menu = Color('red')

        self.document = Document()

    def setup(self):
        print("Layout - setup")
        self.setDimensions()

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


    def setDimensions(self):
        print("Layout - set_dimensions")
        self.top_bar.setMaximumHeight(self.layout_props.bar_height)
        self.bottom_bar.setMaximumHeight(self.layout_props.bar_height)
        self.left_menu.setMinimumWidth(int(self.layout_props.min_menu_width * self.layout_props.app.width))
        self.left_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.layout_props.app.width))
        self.right_menu.setMinimumWidth(int(self.layout_props.min_menu_width * self.layout_props.app.width))
        self.right_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.layout_props.app.width))
        self.document.setMinimumWidth(self.layout_props.min_doc_width * self.layout_props.app.width)
