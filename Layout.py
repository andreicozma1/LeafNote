from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter

from ColorWidget import Color
from Document import Document


class Layout():
    def __init__(self, app, min_doc_width, max_menu_width, bar_size):
        # Init variables
        self.app = app
        self.min_doc_width = min_doc_width
        self.max_menu_width = max_menu_width
        self.bar_size = bar_size

        self.central_widget = QWidget()
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.horizontal_layout = QHBoxLayout()
        self.splitter = QSplitter(QtCore.Qt.Horizontal)  # Splitter between LeftMenu, Doc, and Right Menu

        # TODO - Top Bar (HBoxLayout) for Font Style, Size, Color, Highlighting, etc
        self.top_bar = Color('red')
        # TODO - BottomBar (HBoxLayout) for certain actions and information
        self.bottom_bar = Color("purple")
        # TODO - Left menu (VBoxLayout) is used to show workspace and directory structure for notes
        self.left_menu = Color('yellow')
        # TODO - Right menu (VBoxLayout) for document context actions like customizations, reminders, properties, etc.
        self.right_menu = Color('red')

        self.document = Document(min_doc_width * app.width)

    def setup(self):
        self.top_bar.setMaximumHeight(self.bar_size)
        self.bottom_bar.setMaximumHeight(self.bar_size)
        self.left_menu.setMaximumWidth(int(self.max_menu_width * self.app.width))
        self.right_menu.setMaximumWidth(int(self.max_menu_width * self.app.width))

        # Create a Vertical Box layout which will contain top bar, content, and bottom bar
        self.vertical_layout.addWidget(self.top_bar)
        # Create the horizontal layout which contains the left menu, text box, and right menu

        self.splitter.addWidget(self.left_menu)
        self.splitter.addWidget(self.document)
        self.splitter.addWidget(self.right_menu)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([100, self.document.minimumWidth(), 100])
        self.horizontal_layout.addWidget(self.splitter)

        # add the horizontal layout to the middle
        self.vertical_layout.addWidget(self.splitter)
        # add the bottom bar
        self.vertical_layout.addWidget(self.bottom_bar)

        return self.central_widget
