import logging
import os
import sys

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QDialogButtonBox, QApplication

from Elements.BottomBar import BottomBar
from Elements.ContextMenu import ContextMenu
from Elements.DirectoryViewer import DirectoryViewer
from Elements.Document import Document
from Elements.OpenTabsBar import OpenTabsBar
from Elements.SearchAndReplace import SearchAndReplace
from Elements.TopBar import TopBar
from Layout.AppProps import AppProps
from Layout.DocProps import DocProps
from Layout.Layout import Layout
from Layout.LayoutProps import LayoutProps
from Layout.MenuBar import MenuBar
from Utils.DialogBuilder import DialogBuilder
from Utils.FileManager import FileManager
from Utils.Reminders import Reminders

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
        path_res = os.path.dirname(os.path.abspath(__file__))
        self.app_props = AppProps(path_res)
        self.layout_props = LayoutProps()
        self.doc_props = DocProps()
        self.settings = QSettings(self.app_props.domain, self.app_props.title)
        self.file_manager = FileManager(self)
        self.reminders = Reminders(self, self.settings)

        # Setup Layout Class and Main Vertical Layout
        self.layout = Layout(self.app_props, self.layout_props)
        layout_main = self.layout.makeMainLayout()
        self.setCentralWidget(self.layout)
        # self.show()

        # Create Document
        self.document = Document(self, self.doc_props)

        # Create TopBar, depends on Document
        self.top_bar = TopBar(self.app_props.path_res, self.document)
        self.btn_mode_switch = self.top_bar.makeBtnFormatMode(self.setFormattingMode)
        self.setupTopBar()
        layout_main.addWidget(self.top_bar)

        # Create Main Workspace
        last_path = self.settings.value("workspacePath")
        self.left_menu = DirectoryViewer(self.document, self.file_manager, last_path)
        self.bar_open_tabs = OpenTabsBar(self.document, self.file_manager, self.layout_props)
        self.search_and_replace = SearchAndReplace(self.app_props.path_res, self.document)
        self.right_menu = ContextMenu(self, self.document)
        self.documents_view = self.layout.makeHSplitterLayout(self.left_menu, self.bar_open_tabs, self.document,
                                                              self.right_menu, self.search_and_replace)
        layout_main.addWidget(self.documents_view)

        # Create BottomBar, depends on document
        self.bottom_bar = BottomBar(self.app_props.path_res, self.document)
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
        top_bar_layout.addWidget(self.top_bar.makeTitleStyleBox(self.doc_props.dict_title_styles))
        top_bar_layout.addWidget(self.top_bar.testButton())
        top_bar_layout.addWidget(self.top_bar.makeComboFontStyleBox())
        top_bar_layout.addWidget(self.top_bar.makeComboFontSizeBox(self.doc_props.list_font_sizes))
        top_bar_layout.addWidget(self.top_bar.makeBtnBold())
        top_bar_layout.addWidget(self.top_bar.makeBtnItal())
        top_bar_layout.addWidget(self.top_bar.makeBtnStrike())
        top_bar_layout.addWidget(self.top_bar.makeBtnUnder())
        top_bar_layout.addWidget(self.top_bar.makeComboFontColor(self.doc_props.dict_colors))
        top_bar_layout.addWidget(self.top_bar.makeClearFormatting())
        top_bar_layout.addWidget(self.top_bar.makeComboTextAlign(self.doc_props.dict_text_aligns))
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.btn_mode_switch)
        self.top_bar.setFixedHeight(self.top_bar.minimumSizeHint().height())
        self.document.selectionChanged.connect(self.top_bar.updateFormatOnSelectionChange)
        self.document.currentCharFormatChanged.connect(self.top_bar.updateFormatOnSelectionChange)
        self.top_bar.show()

    def setupBottomBar(self):
        # TODO Make BottomBar Modular and similar to TopBar above
        self.bottom_bar.setFixedHeight(self.bottom_bar.minimumSizeHint().height())

    def setupMenuBar(self):
        self.menu_bar.makeFileMenu(self, self.file_manager, self.bar_open_tabs)
        self.menu_bar.makeEditMenu(self, self.file_manager)
        self.menu_bar.makeViewMenu(self, self.bottom_bar)
        self.menu_bar.makeFormatMenu(self)
        self.menu_bar.makeToolsMenu(self, self.document)
        self.document.selectionChanged.connect(self.menu_bar.updateFormatOnSelectionChange)
        self.document.currentCharFormatChanged.connect(self.menu_bar.updateFormatOnSelectionChange)
        self.setMenuBar(self.menu_bar)

    def setup(self):
        """
        sets up the window
        :return: returns nothing
        """
        logging.info("Setting up Main Window")
        self.setWindowTitle(self.app_props.title)
        if self.settings.contains("windowSize"):
            self.resize(self.settings.value("windowSize"))
        else:
            self.setGeometry(0, 0, self.app_props.default_width, self.app_props.default_height)
        if self.settings.contains("windowGeometry"):
            self.setGeometry(self.settings.value("windowGeometry"))
        else:
            self.centerWindow(self.frameGeometry())  # Must be called after setting geometry

        self.setMinimumWidth(int(self.top_bar.width()))

        if not self.settings.contains("windowResizable") or self.settings.value("windowResizable") is False:
            logging.debug("Window is not resizable")
            if not self.app_props.resizable:
                self.setFixedSize(self.size())

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
        self.left_menu.setMinimumWidth(
            int(self.width() * self.layout_props.min_menu_width * (self.app_props.default_width / self.width())))
        self.left_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.width()))
        self.right_menu.setMinimumWidth(
            int(self.width() * self.layout_props.min_menu_width * (self.app_props.default_width / self.width())))
        self.right_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.width()))
        self.documents_view.setMinimumWidth(int(self.layout_props.min_doc_width * self.width()))

        return super(QMainWindow, self).resizeEvent(event)

    def closeEvent(self, event):
        logging.info("User triggered close event")
        self.settings.setValue("windowSize", self.size())
        self.settings.setValue("windowGeometry", self.geometry())

        path_workspace = self.left_menu.model.rootPath()
        self.settings.setValue("workspacePath", path_workspace)

        path_key = os.path.join(path_workspace, '.leafCryptoKey')
        if self.file_manager.encryptor is not None and not os.path.exists(path_key):
            dialog_encryptor = DialogBuilder(self, "Crypto - WARNING",
                                             "WARNING!! Crypto Key missing!\n"
                                             "Would you like to decrypt workspace before exiting?",
                                             "If you don't decrypt your workspace before exiting you will lose access to your files permanently.")
            buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
            dialog_encryptor.addButtonBox(buttons)
            if dialog_encryptor.exec():
                logging.info("START DECRYPT WORKSPACE: " + path_workspace)
                for dirpath, dirnames, filenames in os.walk(path_workspace):
                    for filename in [f for f in filenames if not f.startswith(".")]:
                        path = os.path.join(dirpath, filename)
                        self.file_manager.encryptor.decryptFile(path)
                        logging.info(" - Decrypted: " + path)
                logging.info("END DECRYPT WORKSPACE: " + path_workspace)


def main():
    logging.info("Starting application")
    app = QApplication([])
    App()
    sys.exit(app.exec_())


# Starting point of the program
if __name__ == '__main__':
    main()
