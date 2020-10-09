import logging
import sys

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QDialogButtonBox, QWidget, QVBoxLayout
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from Elements.BottomBar import BottomBar
from Elements.ColorWidget import Color
from Elements.ContextMenu import ContextMenu
from Elements.DirectoryViewer import DirectoryViewer
from Elements.Document import Document
from Elements.OpenTabsBar import OpenTabsBar
from Elements.TopBar import TopBar
from Layout.AppProps import AppProps
from Layout.DocProps import DocProps
from Layout.Layout import Layout
from Layout.LayoutProps import LayoutProps
from Layout.MenuBar import MenuBar
from Utils.DialogBuilder import DialogBuilder
from Utils.FileManager import FileManager

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
        creates the window and its attributes
        :return: returns nothing
        """
        super(QMainWindow, self).__init__()
        logging.info("Constructor")
        # Initialize properties.
        self.app_props = AppProps()
        self.layout_props = LayoutProps()
        self.doc_props = DocProps()
        self.file_manager = FileManager(self)
        self.summarizer = None

        # Setup Layout Class and Main Vertical Layout
        self.layout = Layout(self.app_props, self.layout_props)
        layout_main = self.layout.makeMainLayout()

        # Create Document
        self.document = Document(self.doc_props)

        # Create TopBar, depends on Document
        self.top_bar = TopBar(self.document)
        self.btn_mode_switch = self.top_bar.makeBtnFormatMode(self.setFormattingMode)
        self.setupTopBar()
        layout_main.addWidget(self.top_bar)

        # Create Main Workspace
        self.left_menu = DirectoryViewer(self.document, self.file_manager)
        self.bar_open_tabs = OpenTabsBar(self.document, self.file_manager, self.layout_props)
        self.right_menu = ContextMenu()
        self.documents_view = self.layout.makeHSplitterLayout(self.left_menu, self.bar_open_tabs, self.document, self.right_menu)
        layout_main.addWidget(self.documents_view)

        # Create BottomBar, depends on document
        self.bottom_bar = BottomBar(self.document)
        self.setupBottomBar()
        layout_main.addWidget(self.bottom_bar)

        # Setup System MenuBar
        self.menu_bar = MenuBar(self.document, self.doc_props)
        self.setupMenuBar()
        self.menu_bar.show()

        # TODO - fix this function call causing Format Mode button to not have spacer
        self.updateFormatBtnsState(False)

        self.setup()

    def setupTopBar(self):
        top_bar_layout = self.top_bar.makeMainLayout()
        top_bar_layout.addWidget(self.top_bar.makeComboFontStyleBox())
        top_bar_layout.addWidget(self.top_bar.makeComboFontSizeBox(self.doc_props.list_FontSize))
        top_bar_layout.addWidget(self.top_bar.makeBtnBold())
        top_bar_layout.addWidget(self.top_bar.makeBtnItal())
        top_bar_layout.addWidget(self.top_bar.makeBtnStrike())
        top_bar_layout.addWidget(self.top_bar.makeBtnUnder())
        top_bar_layout.addWidget(self.top_bar.makeComboFontColor(self.doc_props.color_dict))
        top_bar_layout.addWidget(self.top_bar.makeClearFormatting())
        top_bar_layout.addWidget(self.top_bar.makeComboTextAlign(self.doc_props.dict_align))
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.btn_mode_switch)
        self.top_bar.setFixedHeight(self.top_bar.minimumSizeHint().height())
        self.top_bar.show()

    def setupBottomBar(self):
        # TODO Make BottomBar Modular and similar to TopBar above
        self.bottom_bar.setFixedHeight(self.bottom_bar.minimumSizeHint().height())

    def setupMenuBar(self):
        self.menu_bar.makeFileMenu(self, self.file_manager, self.bar_open_tabs)
        self.menu_bar.makeEditMenu(self)
        self.menu_bar.makeViewMenu(self, self.bottom_bar)
        self.menu_bar.makeFormatMenu(self)
        self.menu_bar.makeToolsMenu(self, self.document)
        self.setMenuBar(self.menu_bar)

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

    def updateFormatBtnsState(self, state: bool):
        """
        Updates the state of the formatting buttons in TopBar and BottomBar
        :param state: whether to enable or disable
        :return:
        """
        self.btn_mode_switch.setChecked(state)
        self.top_bar.setFormattingButtonsEnabled(state)
        self.menu_bar.setFormattingButtonsEnabled(state)

    def setFormattingMode(self, state: bool):
        """
        Toggles between Formatting Mode and Plain-Text Mode
        :param state: this is a boolean that sets the states
        :return: returns nothing
        """
        logging.info(str(state))

        if state is True:
            convert_dialog = DialogBuilder(self, "Enable Formatting",
                                           "Would you like to convert this file?",
                                           "This file needs to be converted to use enriched text formatting features\n"
                                           "Selecting 'Yes' will convert the original "
                                           "file to the enriched text file format.")
            buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
            convert_dialog.addButtonBox(buttonBox)
            if convert_dialog.exec():
                logging.info("User converted file to Proprietary Format")
                # TODO - Convert file with FileManager to a .lef format, on success, call the function below
                self.file_manager.toLef(self.document)
            else:
                logging.info("User DID NOT convert file to Proprietary Format")
                self.updateFormatBtnsState(False)
        else:
            # Don't allow converted file to be converted back to Plain Text
            # TODO - allow option to save different file as plain text, or allow conversion back but discard formatting options

            self.file_manager.lefToExt(self.document)
            logging.info("Convert back to a txt file")

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
        self.left_menu.setMinimumWidth(int(self.width() * self.layout_props.min_menu_width * (self.app_props.width / self.width())))
        self.left_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.width()))
        self.right_menu.setMinimumWidth(int(self.width() * self.layout_props.min_menu_width * (self.app_props.width / self.width())))
        self.right_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.width()))
        self.documents_view.setMinimumWidth(int(self.layout_props.min_doc_width * self.width()))

        return super(QMainWindow, self).resizeEvent(event)

def main():
    logging.info("Starting application")
    appctxt = ApplicationContext()
    App()
    sys.exit(appctxt.app.exec_())


# Starting point of the program
if __name__ == '__main__':
    main()
