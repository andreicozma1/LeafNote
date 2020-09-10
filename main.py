import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QSplitter
from Textbox import PlainTextEdit
from MenuBar import MenuBar


class Color(QWidget):
    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)


class App(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # Initialize properties. TODO - make application properties their own class separately
        self.title = '0x432d2d'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.barSize = 25
        self.minDocWidthRatio = .4 # of width of viewport
        self.maxMenuWidthRatio = .3 # of width of viewport
        # Vertical main layout. TODO - The middle section of VBox should be a horizontal 3 section box
        # Top bar. This is for main actions like saving, undo, etc.
        # self.statusBar()
        self.topBar = MenuBar()
        # self.setMenuBar(self.topBar)
        self.topBar.setMaximumHeight(self.barSize)

        # TODO - Left menu is used to show workspace and directory structure for notes
        self.leftMenu = Color('yellow')  # TODO - Leftmenu is a VBoxLayout
        self.leftMenu.setMaximumWidth(int(self.maxMenuWidthRatio * self.width))
        # Middle block (text box) is the area where you can type in
        self.textBox = PlainTextEdit()
        self.textBox.setBackgroundColor('orange')
        self.textBox.setMinimumWidth(int(self.minDocWidthRatio * self.width))
        # TODO - right menu is for document context actions like customizations, reminders, properties, etc.
        self.rightMenu = Color('red')  # TODO - Rightmenu is a VBoxLayout
        self.rightMenu.setMaximumWidth(int(self.maxMenuWidthRatio * self.width))

        # TODO - Make bottom bar slimmer. This is for certain actions and information
        self.bottomBar = Color("purple")  # TODO - Bottombar is a HBoxLayout
        self.bottomBar.setMaximumHeight(self.barSize)

        self.setCentralWidget(self.initWindow())
        self.show()

    # Returns the Central Widget
    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

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
        splitter.setSizes([50, self.textBox.minimumWidth(), 50])
        self.horizontalLayout.addWidget(splitter)

        # add the horizontal layout to the middle
        self.verticalLayout.addWidget(splitter)
        # add the bottom bar
        self.verticalLayout.addWidget(self.bottomBar)

        return centralWidget

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

# Starting point of the program
if __name__ == '__main__':
    main()
