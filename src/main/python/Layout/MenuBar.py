import logging

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAction, QMenuBar, QActionGroup
from PyQt5.QtWidgets import QFileDialog

from Elements import Document
from Layout import DocProps

"""
all properties and functionalities of the menu bar
"""


class MenuBar(QMenuBar):
    """
    Class to hold and customize a QPlainTextEdit Widget
    """

    def __init__(self, document: Document, doc_props: DocProps):
        """
        sets up the menu bar
        :return: returns nothing
        """
        super(MenuBar, self).__init__()
        logging.info("")
        self.document = document
        self.doc_props = doc_props
        self.setNativeMenuBar(False)

        self.document.selectionChanged.connect(self.updateFormatOnSelectionChange)
        self.document.currentCharFormatChanged.connect(self.updateFormatOnSelectionChange)

    # --------------------------------------------------------------------------------

    def makeFileMenu(self, app, file_manager):
        """
        sets up the file tabs drop menu
        :return: returns nothing
        """
        logging.info("makeFileMenu")

        def onNewBtn():
            logging.info("MenuBar - onNewBtn")
            file_manager.newFile()

        def onOpenBtn():
            logging.info("onOpenBtn")
            # this is opens the file dialogue in the project path
            home_dir = str(QDir.currentPath())
            # opens a file dialogue for the user to select a file to open
            file_name = QFileDialog.getOpenFileName(app, 'Open file', home_dir)
            # open the chosen file and show the text in the text editor
            file_manager.openDocument(file_name[0])

        def onOpenFolderBtn():
            logging.info("onOpenFolderBtn")
            # opens a file dialogue for the user to select a file to open
            folder_name = QFileDialog.getExistingDirectory(app, 'Open folder', str(QDir.currentPath()))
            # if the user selected a new folder
            if folder_name != "":
                app.left_menu.updateDirectory(folder_name)

        # this saves the current file that is shown in the self.document
        def onSaveBtn():
            logging.info("onSaveBtn")
            file_manager.saveDocument()

        def onSaveAsBtn():
            logging.info("saveAsFile")
            new_file_path = QFileDialog.getSaveFileName(app, 'Save File')
            file_manager.saveAsDocument(new_file_path[0])

        def onExitBtn():
            logging.info("onExitBtn")
            file_manager.closeAll()
            app.close()

        self.file_menu = self.addMenu('&File')

        new_file_act = QAction("&New...", app)
        new_file_act.setStatusTip('New')
        new_file_act.triggered.connect(onNewBtn)
        self.file_menu.addAction(new_file_act)

        # opens a dialogue to chose a file an open it
        open_file_act = QAction("&Open...", app)
        open_file_act.setStatusTip('Open File')
        open_file_act.triggered.connect(onOpenBtn)
        self.file_menu.addAction(open_file_act)

        # open a folder as a workspace, showing the directory tree in the left menu
        open_folder_act = QAction("&Open Folder...", app)
        open_folder_act.setStatusTip('Open Folder')
        open_folder_act.triggered.connect(onOpenFolderBtn)
        self.file_menu.addAction(open_folder_act)

        # adds line to separate options
        self.file_menu.addSeparator()

        # save the open file
        save_file = QAction("&Save...", app)
        save_file.setStatusTip('Save')
        save_file.setShortcut('ctrl+s')
        save_file.triggered.connect(onSaveBtn)
        self.file_menu.addAction(save_file)

        save_as_file = QAction("&Save As...", app)
        save_as_file.setStatusTip('Save As')
        save_as_file.setShortcut('ctrl+shift+s')
        save_as_file.triggered.connect(onSaveAsBtn)
        self.file_menu.addAction(save_as_file)

        # adds line to separate options
        self.file_menu.addSeparator()

        # quit main window
        exit_act = QAction("&Exit", app)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(onExitBtn)
        self.file_menu.addAction(exit_act)

        return self.file_menu

    # --------------------------------------------------------------------------------

    def makeEditMenu(self, app):
        """
        sets up the edit tabs drop menu
        :return: returns nothing
        """
        logging.info("makeEditMenu")

        self.edit_menu = self.addMenu('&Edit')

        # undo button and function
        undo_act = QAction("&Undo", app)
        undo_act.setShortcut('Ctrl+z')
        undo_act.triggered.connect(self.document.undo)
        self.edit_menu.addAction(undo_act)

        # redo button and function
        redo_act = QAction("&Redo", app)
        redo_act.setShortcut('Ctrl+Shift+z')
        redo_act.triggered.connect(self.document.redo)
        self.edit_menu.addAction(redo_act)

        # adds line to separate options
        self.edit_menu.addSeparator()

        # select all button and function
        select_all_act = QAction("&Select All", app)
        select_all_act.setShortcut('Ctrl+a')
        select_all_act.triggered.connect(self.document.selectAll)
        self.edit_menu.addAction(select_all_act)

        # adds line to separate options
        self.edit_menu.addSeparator()

        # cut button and function
        cut_act = QAction("&Cut", app)
        cut_act.setShortcut('Ctrl+x')
        cut_act.triggered.connect(self.document.cut)
        self.edit_menu.addAction(cut_act)

        # copy button and function
        copy_act = QAction("&Copy", app)
        copy_act.setShortcut('Ctrl+c')
        copy_act.triggered.connect(self.document.copy)
        self.edit_menu.addAction(copy_act)

        # paste button and function
        paste_act = QAction("&Paste", app)
        paste_act.setShortcut('Ctrl+v')
        paste_act.triggered.connect(self.document.paste)
        self.edit_menu.addAction(paste_act)

    # --------------------------------------------------------------------------------

    def makeViewMenu(self, app, bottom_bar):
        """
        sets up the view tabs drop menu
        :return: returns nothing
        """
        logging.info("makeViewMenu")

        self.view_menu = self.addMenu('&View')

        zoom_in_act = QAction("&Zoom In", app)
        zoom_in_act.setShortcut('ctrl+=')
        zoom_in_act.triggered.connect(bottom_bar.onZoomInClicked)
        self.view_menu.addAction(zoom_in_act)

        zoom_out_act = QAction("&Zoom Out", app)
        # zoom_out_act.setShortcut('ctrl+-')
        zoom_out_act.setShortcut('ctrl+-')
        zoom_out_act.triggered.connect(bottom_bar.onZoomOutClicked)
        self.view_menu.addAction(zoom_out_act)

        zoom_r_act = QAction("&Zoom Reset", app)
        zoom_r_act.triggered.connect(bottom_bar.resetZoom)
        self.view_menu.addAction(zoom_r_act)

    # --------------------------------------------------------------------------------
    def makeFormatMenu(self, app):
        """
        sets up the tools tabs drop menu
        :return: returns nothing
        """
        logging.info("formatMenuSetup")

        self.format_menu = self.addMenu('&Format')

        # Adds Bold button to text_menu
        self.bold_action = QAction("Bold", app)
        self.bold_action.setShortcut('Ctrl+B')
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.document.onFontBoldChanged)
        self.format_menu.addAction(self.bold_action)

        # Adds Italicised button to text_menu
        self.ital_action = QAction("Italicized", app)
        self.ital_action.setShortcut('Ctrl+I')
        self.ital_action.setCheckable(True)
        self.ital_action.triggered.connect(self.document.onFontItalChanged)
        self.format_menu.addAction(self.ital_action)

        # Adds Strikeout button to text_menu
        self.strike_action = QAction("Strikout", app)
        self.strike_action.setShortcut('Ctrl+Shift+5')
        self.strike_action.setCheckable(True)
        self.strike_action.triggered.connect(self.document.onFontStrikeChanged)
        self.format_menu.addAction(self.strike_action)

        # Adds Underline button to text_menu
        self.under_action = QAction("Underline", app)
        self.under_action.setShortcut('Ctrl+U')
        self.under_action.setCheckable(True)
        self.under_action.triggered.connect(self.document.onFontUnderChanged)
        self.format_menu.addAction(self.under_action)

        # Adds separator after font style options
        self.format_menu.addSeparator()

        # Adds Font Color button to text_menu
        self.font_color_action = QAction("Color Picker", app)
        self.font_color_action.triggered.connect(self.document.openColorDialog)
        self.format_menu.addAction(self.font_color_action)

        # Add separator after color options
        self.format_menu.addSeparator()

        # --- create the alignment menu ---
        def onTextAlignmentChanged(state):
            self.document.onTextAlignmentChanged(list(self.doc_props.dict_align.keys()).index(state.text()))

        # Action group for alignment options. Defaults to exclusive selection in group
        align_group = QActionGroup(self)
        align_group.triggered.connect(onTextAlignmentChanged)

        # create the left alignment action
        self.left_align_action = QAction(list(self.doc_props.dict_align.keys())[0], app)
        self.left_align_action.setShortcut('Ctrl+Shift+L')
        self.left_align_action.setCheckable(True)
        align_group.addAction(self.left_align_action)
        self.format_menu.addAction(self.left_align_action)

        # create the right alignment action
        self.right_align_action = QAction(list(self.doc_props.dict_align.keys())[1], app)
        self.right_align_action.setShortcut('Ctrl+Shift+R')
        self.right_align_action.setCheckable(True)
        align_group.addAction(self.right_align_action)
        self.format_menu.addAction(self.right_align_action)

        # create the center alignment action
        self.center_align_action = QAction(list(self.doc_props.dict_align.keys())[2], app)
        self.center_align_action.setShortcut('Ctrl+Shift+E')
        self.center_align_action.setCheckable(True)
        align_group.addAction(self.center_align_action)
        self.format_menu.addAction(self.center_align_action)

        # create the justify alignment action
        self.justify_align_action = QAction(list(self.doc_props.dict_align.keys())[3], app)
        self.justify_align_action.setShortcut('Ctrl+Shift+J')
        self.justify_align_action.setCheckable(True)
        align_group.addAction(self.justify_align_action)
        self.format_menu.addAction(self.justify_align_action)

    def setFormattingButtonsEnabled(self, state):
        """
        allows formatting once file type is changed from .txt to .lef in menu bar
        :param state: this is a boolean that sets the states
        :return: returns nothing
        """
        # Toggle the state of all buttons in the menu
        logging.info(str(state))
        a: QAction
        for a in self.format_menu.actions():
            if not a.property("persistent"):
                a.setEnabled(state)

    def updateFormatOnSelectionChange(self):
        """
        selected text format will be checked in menu bar
        :return: returns nothing
        """
        a: QAction
        for a in self.format_menu.actions():
            if not a.property("persistent"):
                a.blockSignals(True)

        self.ital_action.setChecked(self.document.fontItalic())
        self.under_action.setChecked(self.document.fontUnderline())
        self.bold_action.setChecked(self.document.fontWeight() == QFont.Bold)
        self.strike_action.setChecked(self.document.currentCharFormat().fontStrikeOut())

        a: QAction
        for a in self.format_menu.actions():
            if not a.property("persistent"):
                a.blockSignals(False)

    # -------------------------------------------------------------------------------
