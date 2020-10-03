import logging
import sys

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
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
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

"""
all the code comes together to set up the GUI
"""


class App(QMainWindow):
    """
    puts all the pieces of code together to get finished application
    """
    def __init__(self):
        """
        creates the windown and its attributes
        :return: returns nothing
        """
        super(QMainWindow, self).__init__()
        logging.info("Constructor")
        # Initialize properties.
        self.app_props = AppProps()
        self.layout_props = LayoutProps()

        self.file_manager = FileManager(self)

        self.layout = Layout(self.app_props, self.layout_props)

        self.bar_open_tabs = OpenTabsBar(self.file_manager, self.layout_props)

        self.document = Document()

        self.top_bar = TopBar(self, self.document)
        self.top_bar_combo_font_style = self.top_bar.makeComboFontStyleBox()
        self.top_bar_combo_font_size = self.top_bar.makeComboFontSizeBox()
        self.top_bar_btn_bold = self.top_bar.makeBtnBold()
        self.top_bar_btn_ital = self.top_bar.makeBtnItal()
        self.top_bar_btn_strike = self.top_bar.makeBtnStrike()
        self.top_bar_btn_under = self.top_bar.makeBtnUnder()
        self.top_bar_combo_font_color = self.top_bar.makeComboFontColor()
        self.top_bar_combo_text_align = self.top_bar.makeComboTextAlign()
        self.top_bar.addLayoutSpacer()
        self.top_bar_btn_format_mode = self.top_bar.makeBtnFormatMode()
        self.document.selectionChanged.connect(self.top_bar.updateFormatOnSelectionChange)
        self.setFormattingEnabled(False)
        self.top_bar.setLayout(self.top_bar.horizontal_layout)



        self.left_menu = DirectoryViewer(self.file_manager, self.app_props.mainPath)
        self.bottom_bar = BottomBar(self.document)

        self.menubar = MenuBar(self, self.file_manager, self.document, self.top_bar, self.bottom_bar)

        self.setupLayout()

    def setFormattingEnabled(self, state:bool):
        self.top_bar.setFormattingEnabled(False)

    def setupLayout(self):
        """
        sets up the layout within the window
        :return: returns nothing
        """
        logging.info("Setting up layout members")
        # Setup Layout View
        self.layout.setTopBar(self.top_bar)
        self.layout.setBottomBar(self.bottom_bar)
        self.layout.setBarOpenTabs(self.bar_open_tabs)
        self.layout.setDocument(self.document)
        self.layout.setLeftMenu(self.left_menu)


    def setup(self):
        """
        sets up the window
        :return: returns nothing
        """
        logging.info("Setting up Main Window")
        self.setWindowTitle(self.app_props.title)
        self.setGeometry(self.app_props.left, self.app_props.top, self.app_props.width, self.app_props.height)
        self.setMinimumWidth(int(self.app_props.min_width * QDesktopWidget().availableGeometry().width()))
        self.centerWindow(self.frameGeometry())  # Must be called after setting geometry
        if not self.app_props.resizable:
            logging.debug("Window is not resizable")
            self.setFixedSize(self.app_props.width, self.app_props.height)

        self.setCentralWidget(self.layout)

        self.show()

    def centerWindow(self, app_geom):
        """
        aligns window in the middle of given space
        :param app_geom: the application geometry
        :return: returns nothing
        """
        logging.info("Centering Window")
        center = QDesktopWidget().availableGeometry().center()
        app_geom.moveCenter(center)
        self.move(app_geom.topLeft())

    def resizeEvent(self, event):
        """
        resizes based on updated dimensions
        :param event: item that will be resized
        :return: returns nothing
        """
        self.layout.updateDimensions(self)
        return super(QMainWindow, self).resizeEvent(event)


def main():
    logging.info("Starting application")
    appctxt = ApplicationContext()
    App().setup()
    sys.exit(appctxt.app.exec_())


# Starting point of the program
if __name__ == '__main__':
    main()
