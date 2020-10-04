import logging

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAction, QMenuBar
from PyQt5.QtWidgets import QFileDialog

from Elements import Document

"""
all properties and functionalities of the menu bar
"""


class MenuBar:
    """
    Class to hold and customize a QPlainTextEdit Widget
    """

    def __init__(self, menu_bar: QMenuBar):
        """
        sets up the menu bar
        :return: returns nothing
        """
        logging.info("")
        self.menu = menu_bar
        self.menu.setNativeMenuBar(False)

    # --------------------------------------------------------------------------------

    # TODO - Add more functionality to file tab - new, save, save as, save all, settings, etc.
    def makeFileMenu(self, app, file_manager):
        """
        sets up the file tabs drop menu
        :return: returns nothing
        """
        logging.info("makeFileMenu")

        # TODO - implement new file button that opens a new blank file in the document
        def onNewBtn():
            """
            function of the new file button
            :return: returns nothing
            """
            logging.info("MenuBar - onNewBtn")
            file_manager.newFile()

        # this function opens a dialog for the user to select a file to open. When the user
        # selects a file it will show its text in the middle of the window
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

        # this saves the current file that is shown in the document
        def onSaveBtn():
            logging.info("onSaveBtn")
            file_manager.saveDocument()

        # TODO - save the file as a specified name in any location on disk
        def onSaveAsBtn():
            logging.info("saveAsFile")
            new_file_path = QFileDialog.getSaveFileName(app, 'Save File')
            file_manager.saveAsDocument(new_file_path[0])

        def onExitBtn():
            logging.info("onExitBtn")
            file_manager.closeAll()
            app.close()

        self.file_menu = self.menu.addMenu('&File')

        # TODO - implement new file button that opens a new blank file in the document
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

        # TODO - save the file as a specified name in any location on disk
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

    # TODO - Add functionality to edit tab - undo, redo, cut, copy, paste, etc.
    def makeEditMenu(self, app, document: Document):
        """
        sets up the edit tabs drop menu
        :return: returns nothing
        """
        logging.info("makeEditMenu")

        self.edit_menu = self.menu.addMenu('&Edit')
        # Idea: select button when keyboard shortcut used

        # undo button and function
        undo_act = QAction("&Undo", app)
        undo_act.setShortcut('Ctrl+z')
        undo_act.triggered.connect(document.undo)
        self.edit_menu.addAction(undo_act)

        # redo button and function
        redo_act = QAction("&Redo", app)
        redo_act.setShortcut('Ctrl+Shift+z')
        redo_act.triggered.connect(document.redo)
        self.edit_menu.addAction(redo_act)

        # adds line to separate options
        self.edit_menu.addSeparator()

        # select all button and function
        select_all_act = QAction("&Select All", app)
        select_all_act.setShortcut('Ctrl+a')
        select_all_act.triggered.connect(document.selectAll)
        self.edit_menu.addAction(select_all_act)

        # adds line to separate options
        self.edit_menu.addSeparator()

        # cut button and function
        cut_act = QAction("&Cut", app)
        cut_act.setShortcut('Ctrl+x')
        cut_act.triggered.connect(document.cut)
        self.edit_menu.addAction(cut_act)

        # copy button and function
        copy_act = QAction("&Copy", app)
        copy_act.setShortcut('Ctrl+c')
        copy_act.triggered.connect(document.copy)
        self.edit_menu.addAction(copy_act)

        # paste button and function
        paste_act = QAction("&Paste", app)
        paste_act.setShortcut('Ctrl+v')
        paste_act.triggered.connect(document.paste)
        self.edit_menu.addAction(paste_act)

    # --------------------------------------------------------------------------------

    # TODO - uncomment when implementing these menus
    # TODO - Add functionality to view tab - appearance, etc.
    def makeViewMenu(self, app, bottom_bar):
        """
        sets up the view tabs drop menu
        :return: returns nothing
        """
        logging.info("makeViewMenu")

        self.view_menu = self.menu.addMenu('&View')

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
    # TODO - Add functionality to tools tab - tbd
    def makeFormatMenu(self, app, document, doc_props):
        """
        sets up the tools tabs drop menu
        :return: returns nothing
        """
        logging.info("formatMenuSetup")

        self.format_menu = self.menu.addMenu('&Format')
        # Sets up submene of 'Text' inside of the 'Format' menu
        self.text_menu = self.format_menu.addMenu('&Text Style')

        # sets up a submenu for alignment and indentation in the format menu
        self.align_indent_menu = self.format_menu.addMenu('&Align && Indent')

        # Adds Bold button to text_menu
        self.bold_action = QAction("Bold", app)
        self.bold_action.setShortcut('Ctrl+B')
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(document.onFontBoldChanged)
        self.text_menu.addAction(self.bold_action)

        # Adds Italicised button to text_menu
        self.ital_action = QAction("Italicised", app)
        self.ital_action.setShortcut('Ctrl+I')
        self.ital_action.setCheckable(True)
        self.ital_action.triggered.connect(document.onFontItalChanged)
        self.text_menu.addAction(self.ital_action)

        # Adds Strikeout button to text_menu
        self.strike_action = QAction("Strikout", app)
        self.strike_action.setShortcut('Ctrl+Shift+5')
        self.strike_action.setCheckable(True)
        self.strike_action.triggered.connect(document.onFontStrikeChanged)
        self.text_menu.addAction(self.strike_action)

        # Adds Underline button to text_menu
        self.under_action = QAction("Underline", app)
        self.under_action.setShortcut('Ctrl+U')
        self.under_action.setCheckable(True)
        self.under_action.triggered.connect(document.onFontUnderChanged)
        self.text_menu.addAction(self.under_action)

        # Adds Seperator to text_menu
        self.text_menu.addSeparator()

        # Adds Font Color button to text_menu
        self.font_color_action = QAction("Font Color", app)
        self.font_color_action.triggered.connect(document.openColorDialog)
        self.text_menu.addAction(self.font_color_action)

        # --- create the alignment and indentation menu ---
        # create the left alignment action
        def onTextAlignLeftClicked():
            logging.info("Align Left")
            document.setAlignment(Qt.AlignLeft)

        def onTextAlignCenterClicked():
            logging.info("Align Center")
            document.setAlignment(Qt.AlignCenter)

        def onTextAlignRightClicked():
            logging.info("Align Right")
            document.setAlignment(Qt.AlignRight)

        def onTextAlignJustifyClicked():
            logging.info("Align Justify")
            document.setAlignment(Qt.AlignJustify)

        self.left_align_action = QAction(doc_props.list_alignments[0], app)
        self.left_align_action.setShortcut('Ctrl+Shift+L')
        self.left_align_action.setCheckable(True)
        self.left_align_action.triggered.connect(onTextAlignLeftClicked)
        self.align_indent_menu.addAction(self.left_align_action)

        # create the center alignment action
        self.center_align_action = QAction(doc_props.list_alignments[1], app)
        self.center_align_action.setShortcut('Ctrl+Shift+E')
        self.center_align_action.setCheckable(True)
        self.center_align_action.triggered.connect(onTextAlignCenterClicked)
        self.align_indent_menu.addAction(self.center_align_action)

        # create the right alignment action
        self.right_align_action = QAction(doc_props.list_alignments[2], app)
        self.right_align_action.setShortcut('Ctrl+Shift+R')
        self.right_align_action.setCheckable(True)
        self.right_align_action.triggered.connect(onTextAlignRightClicked)
        self.align_indent_menu.addAction(self.right_align_action)

        # create the justify alignment action
        self.justify_align_action = QAction(doc_props.list_alignments[3], app)
        self.justify_align_action.setShortcut('Ctrl+Shift+J')
        self.justify_align_action.setCheckable(True)
        self.justify_align_action.triggered.connect(onTextAlignJustifyClicked)
        self.align_indent_menu.addAction(self.justify_align_action)

    def setFormattingButtonsEnabled(self, state):
        """
        allows formatting once file type is changed from .txt to .lef in menu bar
        :param state: this is a boolean that sets the states
        :return: returns nothing
        """
        # Toggle the state of all buttons in the menu
        logging.info(str(state))
        a: QAction
        for a in self.text_menu.actions():
            if not a.property("persistent"):
                a.setEnabled(state)

        # Toggle the state of all buttons in the menu
        a: QAction
        for a in self.align_indent_menu.actions():
            if not a.property("persistent"):
                a.setEnabled(state)

    def updateFormatOnSelectionChange(self, document):
        """
        selected text format will be checked in menu bar
        :return: returns nothing
        """
        a: QAction
        for a in self.text_menu.actions():
            if not a.property("persistent"):
                a.blockSignals(True)

        self.ital_action.setChecked(document.fontItalic())
        self.under_action.setChecked(document.fontUnderline())
        self.bold_action.setChecked(document.fontWeight() == QFont.Bold)
        self.strike_action.setChecked(document.currentCharFormat().fontStrikeOut())

        a: QAction
        for a in self.text_menu.actions():
            if not a.property("persistent"):
                a.blockSignals(False)

    # -------------------------------------------------------------------------------
