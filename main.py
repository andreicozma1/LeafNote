import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QMainWindow, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtGui import QIcon
import matplotlib


class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
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
        # Vertical main layout. TODO - The middle section of VBox should be a horizontal 3 section box
        # TODO - Make top bar slimmer. This is for main actions like saving, undo, etc.
        self.topBar = Color('blue')  # TODO - Topbar is a HBoxLayout
        # TODO - Left menu is used to show workspace and directory structure for notes
        self.leftMenu = Color('yellow')  # TODO - Leftmenu is a VBoxLayout
        # TODO - Middle block (text box) is the area where you can type in
        self.textBox = Color('orange')  # TODO - use QPlainTextEdit(self)
        # TODO - right menu is for document context actions like customizations, reminders, properties, etc.
        self.rightMenu = Color('red')  # TODO - Rightmenu is a VBoxLayout
        # TODO - Make bottom bar slimmer. This is for certain actions and information
        self.bottomBar = Color("purple")  # TODO - Bottombar is a HBoxLayout

        self.setCentralWidget(self.initWindow())
        self.show()

    # Returns the Central Widget
    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.verticalLayout = QVBoxLayout()
        # Create a Vertical Box layout which will contain top bar, content, and bottom bar
        self.verticalLayout.addWidget(self.topBar)

        # Create the horizontal layout which contains the left menu, text box, and right menu
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.leftMenu)
        self.horizontalLayout.addWidget(self.textBox)  #
        self.horizontalLayout.addWidget(self.rightMenu)

        # add the horizontal layout to the middle
        self.verticalLayout.addLayout(self.horizontalLayout)
        # add the bottom bar
        self.verticalLayout.addWidget(self.bottomBar)

        # Create the Central Widget and return it
        centralWidget = QWidget()
        centralWidget.setLayout(self.verticalLayout)
        return centralWidget


# Starting point of the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
