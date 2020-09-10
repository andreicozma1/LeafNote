import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from Layout import Layout
from MenuBar import MenuBar
from LayoutProps import LayoutProps


class App(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        print("App - init")
        # Initialize properties.
        self.title = '0x432d2d'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480

        self.menubar = MenuBar(self)
        self.layout_props = LayoutProps(self)
        self.layout = Layout(self.layout_props)

    # Returns the Central Widget
    def setup(self):
        print("App - setup")
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.menubar.setup()
        self.setCentralWidget(self.layout.setup())

        self.show()


def main():
    print("Main")
    app = QApplication(sys.argv)
    App().setup()
    sys.exit(app.exec_())


# Starting point of the program
if __name__ == '__main__':
    main()
