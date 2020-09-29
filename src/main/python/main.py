import sys

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QVBoxLayout, QWidget
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from Elements.BottomBar import BottomBar
from Elements.DirectoryViewer import DirectoryViewer
from Elements.Document import Document
from Elements.OpenTabsBar import OpenTabsBar
from Elements.TopBar import TopBar
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

        self.layout = Layout(self, self.app_props, self.layout_props)

        self.bar_open_tabs = OpenTabsBar(self)
        self.document = Document(self.layout)
        self.left_menu = DirectoryViewer(self.file_manager, self.app_props.mainPath)
        self.top_bar = TopBar(self.document, self.file_manager)
        self.bottom_bar = BottomBar(self.document)
        self.setupLayout()

        self.menubar = MenuBar(self)


    def setupLayout(self):
        # Setup Documents View
        self.layout.setTopBar(self.top_bar)
        self.layout.setBottomBar(self.bottom_bar)
        self.layout.setBarOpenTabs(self.bar_open_tabs)
        self.layout.setDocument(self.document)
        self.layout.setLeftMenu(self.left_menu)


    # Returns the Central Widget
    def setup(self):
        print("App - setup")
        self.setWindowTitle(self.app_props.title)
        self.setGeometry(self.app_props.left, self.app_props.top, self.app_props.width, self.app_props.height)
        self.setMinimumWidth(int(self.app_props.min_width * QDesktopWidget().availableGeometry().width()))
        self.centerWindow(self.frameGeometry())  # Must be called after setting geometry
        if not self.app_props.resizable:
            self.setFixedSize(self.app_props.width, self.app_props.height)

        self.setCentralWidget(self.layout)

        self.show()

    def centerWindow(self, app_geom):
        print("App - centerWindow")
        center = QDesktopWidget().availableGeometry().center()
        app_geom.moveCenter(center)
        self.move(app_geom.topLeft())

    def resizeEvent(self, event):
        self.layout.updateDimensions()
        return super(QMainWindow, self).resizeEvent(event)


def main():
    print("Main")
    appctxt = ApplicationContext()
    App().setup()
    sys.exit(appctxt.app.exec_())


# Starting point of the program
if __name__ == '__main__':
    main()
