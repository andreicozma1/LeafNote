import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget

from Layout.AppProps import AppProps
from Layout.Layout import Layout
from Layout.LayoutProps import LayoutProps
from Layout.MenuBar import MenuBar
from Utils.FileManager import FileManager


class App(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        print("App - init")
        # Initialize properties.
        self.app_props = AppProps(self)
        self.layout_props = LayoutProps(self)

        self.file_manager = FileManager(self)

        self.layout = Layout(self.app_props, self.layout_props)

        self.menubar = MenuBar(self)

    # Returns the Central Widget
    def setup(self):
        print("App - setup")
        self.setWindowTitle(self.app_props.title)
        self.setGeometry(self.app_props.left, self.app_props.top, self.app_props.width, self.app_props.height)
        self.setMinimumWidth(int(self.app_props.min_width * QDesktopWidget().availableGeometry().width()))
        self.centerWindow(self.frameGeometry())  # Must be called after setting geometry
        if not self.app_props.resizable:
            self.setFixedSize(self.app_props.width, self.app_props.height)

        self.menubar.setup()
        self.setCentralWidget(self.layout.setup())

        self.show()

    def centerWindow(self, app_geom):
        center = QDesktopWidget().availableGeometry().center()
        app_geom.moveCenter(center)
        self.move(app_geom.topLeft())

    def resizeEvent(self, event):
        self.layout.updateDimensions()
        return super(QMainWindow, self).resizeEvent(event)


def main():
    print("Main")
    app = QApplication(sys.argv)
    App().setup()
    sys.exit(app.exec_())


# Starting point of the program
if __name__ == '__main__':
    main()
