from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter

from ColorWidget import Color
from Document import Document


class Layout():
    def __init__(self, appCtx, minDocWidth, maxMenuWidth, barSize):

        # Vertical main layout. TODO - The middle section of VBox should be a horizontal 3 section box
        # TODO - Make top bar slimmer. This is for main actions like saving, undo, etc.
        self.topBar = Color('blue')  # TODO - Topbar is a HBoxLayout
        self.topBar.setMaximumHeight(barSize)
        # TODO - Left menu is used to show workspace and directory structure for notes
        self.leftMenu = Color('yellow')  # TODO - Leftmenu is a VBoxLayout
        self.leftMenu.setMaximumWidth(int(maxMenuWidth * appCtx.width))
        # Middle block (text box) is the area where you can type in
        self.textBox = Document(minDocWidth * appCtx.width)
        # TODO - right menu is for document context actions like customizations, reminders, properties, etc.
        self.rightMenu = Color('red')  # TODO - Rightmenu is a VBoxLayout
        self.rightMenu.setMaximumWidth(int(maxMenuWidth * appCtx.width))

        # TODO - Make bottom bar slimmer. This is for certain actions and information
        self.bottomBar = Color("purple")  # TODO - Bottombar is a HBoxLayout
        self.bottomBar.setMaximumHeight(barSize)

    def initLayout(self):
        # Create the Central Widget and return it
        centralWidget = QWidget()
        self.verticalLayout = QVBoxLayout(centralWidget)

        # Create a Vertical Box layout which will contain top bar, content, and bottom bar
        self.verticalLayout.addWidget(self.topBar)
        # Create the horizontal layout which contains the left menu, text box, and right menu
        self.horizontalLayout = QHBoxLayout()
        # self.horizontalLayout.addWidget(self.leftMenu)
        # self.horizontalLayout.addWidget(self.textBox, 0, Qt.AlignCenter)
        # self.horizontalLayout.addWidget(self.rightMenu)

        splitter = QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.leftMenu)
        splitter.addWidget(self.textBox)
        splitter.addWidget(self.rightMenu)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([100, self.textBox.minimumWidth(), 100])
        self.horizontalLayout.addWidget(splitter)

        # add the horizontal layout to the middle
        self.verticalLayout.addWidget(splitter)
        # add the bottom bar
        self.verticalLayout.addWidget(self.bottomBar)

        return centralWidget