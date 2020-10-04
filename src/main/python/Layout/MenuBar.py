import logging

from PyQt5.QtCore import QDir
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAction, QMenuBar, QActionGroup, QMenu
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
        self.doc = document
        self.doc_props = doc_props
        self.setNativeMenuBar(False)

        self.doc.selectionChanged.connect(self.updateFormatOnSelectionChange)
        self.doc.currentCharFormatChanged.connect(self.updateFormatOnSelectionChange)

    # =====================================================================================================================--

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

        # this saves the current file that is shown in the self.doc
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

    # =====================================================================================================================--

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
        undo_act.triggered.connect(self.doc.undo)
        self.edit_menu.addAction(undo_act)

        # redo button and function
        redo_act = QAction("&Redo", app)
        redo_act.setShortcut('Ctrl+Shift+z')
        redo_act.triggered.connect(self.doc.redo)
        self.edit_menu.addAction(redo_act)

        # adds line to separate options
        self.edit_menu.addSeparator()

        # select all button and function
        select_all_act = QAction("&Select All", app)
        select_all_act.setShortcut('Ctrl+a')
        select_all_act.triggered.connect(self.doc.selectAll)
        self.edit_menu.addAction(select_all_act)

        # adds line to separate options
        self.edit_menu.addSeparator()

        # cut button and function
        cut_act = QAction("&Cut", app)
        cut_act.setShortcut('Ctrl+x')
        cut_act.triggered.connect(self.doc.cut)
        self.edit_menu.addAction(cut_act)

        # copy button and function
        copy_act = QAction("&Copy", app)
        copy_act.setShortcut('Ctrl+c')
        copy_act.triggered.connect(self.doc.copy)
        self.edit_menu.addAction(copy_act)

        # paste button and function
        paste_act = QAction("&Paste", app)
        paste_act.setShortcut('Ctrl+v')
        paste_act.triggered.connect(self.doc.paste)
        self.edit_menu.addAction(paste_act)

    # =====================================================================================================================--

    def makeViewMenu(self, app, bottom_bar) -> QMenu:
        """
        Create Format Menu
        :return: the menu created
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
        return self.view_menu

    # =====================================================================================================================--
    def makeFormatMenu(self, app) -> QMenu:
        """
        Create Format Menu
        :return: the menu created
        """
        logging.info("formatMenuSetup")
        self.format_menu = self.addMenu('&Format')

        # ========= START FONT STYLES SECTION =========
        def makeStyleAction(name: str, shortcut: str, signal, docref) -> QAction:
            style_action = QAction(name, app)
            style_action.setShortcut(shortcut)
            style_action.setCheckable(True)
            style_action.setProperty("docref", docref)
            style_action.triggered.connect(signal)
            return style_action

        self.group_style = QActionGroup(self.format_menu)
        self.group_style.setExclusive(False)
        act_bold = makeStyleAction("Bold", "Ctrl+B", self.doc.onFontBoldChanged, self.doc.fontBold)
        self.group_style.addAction(act_bold)
        act_ital = makeStyleAction("Italicize", "Ctrl+I", self.doc.onFontItalChanged, self.doc.fontItalic)
        self.group_style.addAction(act_ital)
        act_strk = makeStyleAction("Strikeout", "Ctrl+Shift+5", self.doc.onFontStrikeChanged, self.doc.fontStrike)
        self.group_style.addAction(act_strk)
        act_undr = makeStyleAction("Underline", "Ctrl+U", self.doc.onFontUnderChanged, self.doc.fontUnderline)
        self.group_style.addAction(act_undr)
        # Add all actions in group to Style Menu
        self.format_menu.addActions(self.group_style.actions())
        # ========= END FONT STYLES SECTION =========

        # ========= START EXTRA SECTION =========
        self.format_menu.addSeparator()
        act_color_picker = QAction("Color Picker", app)
        act_color_picker.triggered.connect(self.doc.openColorDialog)
        self.format_menu.addAction(act_color_picker)

        # ========= END EXTRA SECTION =========

        # ========= START ALIGNMENT SECTION =========
        def makeAlignAction(name: str, shortcut: str, default: bool = False) -> QAction:
            align_action = QAction(name, app)
            align_action.setShortcut(shortcut)
            align_action.setCheckable(True)
            align_action.setChecked(default)
            return align_action

        def onTextAlignmentChanged(state):
            self.doc.onTextAlignmentChanged(list(self.doc_props.dict_align.keys()).index(state.text()))

        self.format_menu.addSeparator()
        # Action Group for Alignments options (Exclusive picks)
        self.align_group = QActionGroup(self.format_menu)
        self.align_group.triggered.connect(onTextAlignmentChanged)
        # Add alignment options to the group
        self.align_group.addAction(makeAlignAction(list(self.doc_props.dict_align.keys())[0], 'Ctrl+Shift+L', True))
        self.align_group.addAction(makeAlignAction(list(self.doc_props.dict_align.keys())[1], 'Ctrl+Shift+R'))
        self.align_group.addAction(makeAlignAction(list(self.doc_props.dict_align.keys())[2], 'Ctrl+Shift+E'))
        self.align_group.addAction(makeAlignAction(list(self.doc_props.dict_align.keys())[3], 'Ctrl+Shift+J'))
        # Add all actions in group to Format Menu
        self.format_menu.addActions(self.align_group.actions())
        # ========= END ALIGNMENT SECTION =========
        return self.format_menu

    def setFormattingButtonsEnabled(self, state):
        """
        Sets all formatting options to Enabled or Disabled
        :param state: boolean that sets the states
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
        Selected text format reflected in the MenuBar
        :return: returns nothing
        """
        # Block signals
        logging.info("Started updating")
        a: QAction
        for a in self.format_menu.actions():
            if not a.property("persistent"):
                a.blockSignals(True)
        # Update Style options
        for action in self.group_style.actions():
            print(action.text() + " " + str(action.property("docref")()))
            action.setChecked(action.property("docref")())
        # Update Align options
        align = self.doc.alignment()
        for action in self.align_group.actions():
            action.setChecked(False)
            index = list(self.doc_props.dict_align.values()).index(align)
            if action.text() == list(self.doc_props.dict_align.keys())[index]:
                action.setChecked(True)
        # Unblock signals
        a: QAction
        for a in self.format_menu.actions():
            if not a.property("persistent"):
                a.blockSignals(False)
        logging.info("Finished updating")


