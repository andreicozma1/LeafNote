"""
this module contains the main function of the application.
"""

import logging
import os

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QDialogButtonBox, QApplication

from LeafNote import Layout
from LeafNote import Props
from LeafNote import Utils
from LeafNote.Layout import Elements

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class App(QMainWindow):
    """
    puts all the pieces of code together to get finished application
    """

    def __init__(self, ctx):
        """
        creates the window and its attributes
        :return: returns nothing
        """
        super().__init__()
        self.ctx = ctx
        logging.debug("Creating Application")

        # Initialize properties.
        path_res = os.path.dirname(os.path.abspath(__file__))
        self.app_props = Props.AppProps(path_res)
        self.layout_props = Props.LayoutProps()
        self.doc_props = Props.DocProps()
        self.settings = QSettings(self.app_props.domain, self.app_props.title)
        self.file_manager = Utils.FileManager(self)
        self.reminders = Utils.Reminders(self, self.settings)
        self.btn_mode_switch = None

        # Setup Layout Class and Main Vertical Layout
        self.layout = Layout.Layout(self.app_props, self.layout_props)
        layout_main = self.layout.makeMainLayout()
        self.setCentralWidget(self.layout)

        # Create Document
        self.document = Elements.Document(self, self.doc_props)

        # Create TopBar, depends on Document
        self.top_bar = Elements.BarTop(self.app_props.path_res, self.document)
        self.btn_mode_switch = self.top_bar.makeBtnFormatMode(self.setFormattingMode)
        self.setupTopBar()
        self.top_bar.setFixedHeight(self.layout_props.getDefaultBarHeight())
        layout_main.addWidget(self.top_bar)

        # Create Main Workspace
        last_path = self.settings.value("workspacePath")
        self.left_menu = Elements.MenuLeft(self.layout_props, self.document,
                                           self.file_manager, last_path)
        self.bar_open_tabs = Elements.BarOpenTabs(self.document, self.file_manager)

        self.search_and_replace = Elements.SearchReplace(self.app_props.path_res, self.document)
        self.right_menu = Elements.MenuRight(self, self.layout_props, self.document)
        self.documents_view = self.layout.makeHSplitterLayout(self.left_menu, self.bar_open_tabs,
                                                              self.document,
                                                              self.right_menu,
                                                              self.search_and_replace)
        layout_main.addWidget(self.documents_view)

        # Create BottomBar, depends on document
        self.bottom_bar = Elements.BarBottom(self, self.document, self.settings)
        self.bottom_bar.setFixedHeight(self.layout_props.getDefaultBarHeight())

        layout_main.addWidget(self.bottom_bar)

        # Setup System MenuBar
        self.menu_bar = Elements.MenuBar(self.document, self.doc_props, self.layout_props)
        self.setupMenuBar()
        self.menu_bar.show()

        self.updateFormatBtnsState(False)

        self.setupProperties()

    def setupTopBar(self):
        """
        this sets up the top bar as a whole
        """
        top_bar_layout = self.top_bar.makeMainLayout()
        top_bar_layout.addWidget(self.top_bar.makeTitleStyleBox())
        top_bar_layout.addWidget(self.top_bar.makeComboFontStyleBox())
        top_bar_layout.addWidget(self.top_bar.makeComboFontSizeBox())
        top_bar_layout.addWidget(self.top_bar.makeBtnBold())
        top_bar_layout.addWidget(self.top_bar.makeBtnItal())
        top_bar_layout.addWidget(self.top_bar.makeBtnStrike())
        top_bar_layout.addWidget(self.top_bar.makeBtnUnder())
        top_bar_layout.addWidget(self.top_bar.makeComboFontColor())
        top_bar_layout.addWidget(self.top_bar.makeClearFormatting())
        top_bar_layout.addWidget(self.top_bar.makeComboTextAlign())
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.btn_mode_switch)
        self.document.selectionChanged.connect(self.top_bar.updateFormatOnSelectionChange)
        self.document.currentCharFormatChanged.connect(self.top_bar.updateFormatOnSelectionChange)
        self.top_bar.show()

    def setupMenuBar(self):
        """
        this sets up the menu bar as a whole
        """
        self.menu_bar.makeFileMenu(self, self.file_manager)
        self.menu_bar.makeEditMenu(self, self.file_manager)
        self.menu_bar.makeViewMenu(self, self.bottom_bar, self.left_menu)
        self.menu_bar.makeFormatMenu(self)
        self.menu_bar.makeToolsMenu(self, self.document)
        self.document.selectionChanged.connect(self.menu_bar.updateFormatOnSelectionChange)
        self.document.currentCharFormatChanged.connect(self.menu_bar.updateFormatOnSelectionChange)
        self.setMenuBar(self.menu_bar)

    def setupProperties(self):
        """
        sets up the window
        :return: returns nothing
        """
        logging.info("Setting up Main Window Geometry")
        self.setWindowTitle(self.app_props.title)
        self.setWindowIcon(QIcon(self.app_props.app_icon))
        if self.settings.contains("windowSize"):
            self.resize(self.settings.value("windowSize"))
        else:
            self.setGeometry(0, 0, self.app_props.default_width, self.app_props.default_height)

        if self.settings.contains("windowGeometry"):
            self.setGeometry(self.settings.value("windowGeometry"))
        else:
            self.centerWindow(self.frameGeometry())  # Must be called after setting geometry

        self.setMinimumWidth(int(self.top_bar.width()))

        setting_resizable = not self.settings.contains("windowResizable") or self.settings.value(
            "windowResizable") is False
        logging.debug("Resizable - %s", str(setting_resizable))
        if setting_resizable and not self.app_props.resizable:
            self.setFixedSize(self.size())

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
            convert_dialog = Utils.DialogBuilder(self, "Enable Formatting",
                                                 "Would you like to convert this file?",
                                                 "This file needs to be converted to use"
                                                 " enriched text formatting features\n"
                                                 "Selecting 'Yes' will convert the original "
                                                 "file to the enriched text file format.")
            button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
            convert_dialog.addButtonBox(button_box)
            if convert_dialog.exec():
                logging.info("User converted file to Proprietary Format")
                self.file_manager.toLef(self.document)
            else:
                logging.info("User DID NOT convert file to Proprietary Format")
                self.updateFormatBtnsState(False)
        else:
            # Don't allow converted file to be converted back to Plain Text
            convert_dialog = Utils.DialogBuilder(self, "Disable Formatting",
                                                 "Would you like to convert this file?",
                                                 "This file will be converted to plain "
                                                 "text formatting\n"
                                                 "Selecting 'Yes' will PERMANENTLY remove "
                                                 "any existing formatting.")
            button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
            convert_dialog.addButtonBox(button_box)
            if convert_dialog.exec():
                self.file_manager.lefToExt(self.document)
                logging.info("Convert back to a txt file")
            else:
                logging.info("User DID NOT convert file to Plain Text")
                self.updateFormatBtnsState(True)

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
            int(self.width() * self.layout_props.min_menu_width * (
                    self.app_props.default_width / self.width())))
        self.left_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.width()))
        self.right_menu.setMinimumWidth(
            int(self.width() * self.layout_props.min_menu_width * (
                    self.app_props.default_width / self.width())))
        self.right_menu.setMaximumWidth(int(self.layout_props.max_menu_width * self.width()))
        self.documents_view.setMinimumWidth(int(self.layout_props.min_doc_width * self.width()))

        return super().resizeEvent(event)

    def closeEvent(self, event):
        """
        this handles the closing of the application
        """
        logging.info("User triggered close event")
        self.settings.setValue("windowSize", self.size())
        self.settings.setValue("windowGeometry", self.geometry())

        path_workspace = self.left_menu.model.rootPath()
        self.settings.setValue("workspacePath", path_workspace)

        self.file_manager.saveDocument(self.document)

        path_key = os.path.join(path_workspace, '.leafCryptoKey')
        if self.file_manager.encryptor is not None and not os.path.exists(path_key):
            dialog_encryptor = Utils.DialogBuilder(self, "Crypto - WARNING",
                                                   "WARNING!! Crypto Key missing!\n"
                                                   "Would you like to decrypt"
                                                   "workspace before exiting?",
                                                   "If you don't decrypt your"
                                                   "workspace before exiting"
                                                   "you will lose access to"
                                                   "your files permanently.")
            buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
            dialog_encryptor.addButtonBox(buttons)
            if dialog_encryptor.exec():
                logging.info("START DECRYPT WORKSPACE: %s", path_workspace)
                for dirpath, dirnames, filenames in os.walk(path_workspace):
                    for filename in [f for f in filenames if not f.startswith(".")]:
                        path = os.path.join(dirpath, filename)
                        self.file_manager.encryptor.decryptFile(path)
                        logging.info(" - Decrypted: %s", path)
                        logging.debug(dirnames)
                logging.info("END DECRYPT WORKSPACE: %s", path_workspace)

        return super().closeEvent(event)


def run():
    """
    Runs main application
    """
    ctx = QApplication([])
    app = App(ctx)
    app.show()
    return ctx.exec_()
