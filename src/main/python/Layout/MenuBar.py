import logging

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QAction, QMenuBar, QActionGroup, QMenu
from PyQt5.QtWidgets import QFileDialog

import Utils.DocumentSummarizer as DocumentSummarizer
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
        Sets up the System MenuBar
        :return: returns nothing
        """
        super(MenuBar, self).__init__()
        logging.info("")
        self.doc = document
        self.doc_props = doc_props
        self.setNativeMenuBar(False)

        self.doc.selectionChanged.connect(self.updateFormatOnSelectionChange)
        self.doc.currentCharFormatChanged.connect(self.updateFormatOnSelectionChange)

    # =====================================================================================
    def makeFileMenu(self, app, file_manager, bar_open_tabs):
        """
        sets up the file tabs drop menu
        :return: returns nothing
        """
        logging.info("makeFileMenu")

        def onNewBtn():
            logging.info("MenuBar - onNewBtn")
            file_manager.newFile(self.doc)

        def onOpenBtn():
            logging.info("onOpenBtn")
            # this is opens the file dialogue in the project path
            home_dir = str(QDir.currentPath())
            # opens a file dialogue for the user to select a file to open
            file_name = QFileDialog.getOpenFileName(app, 'Open file', home_dir)
            # open the chosen file and show the text in the text editor
            file_manager.openDocument(self.doc, file_name[0])

        def onOpenFolderBtn():
            logging.info("onOpenFolderBtn")
            # opens a file dialogue for the user to select a file to open
            folder_name = QFileDialog.getExistingDirectory(app, 'Open folder', str(QDir.currentPath()))
            # if the user selected a new folder
            if folder_name != "":
                app.left_menu.updateDirectory(folder_name)
            else:
                logging.info("User chose not to open folder")

        # this saves the current file that is shown in the self.doc
        def onSaveBtn():
            logging.info("onSaveBtn")
            if file_manager.saveDocument(self.doc):
                logging.info("Created tab")
                bar_open_tabs.addTab(file_manager.current_document.absoluteFilePath())

        def onSaveAsBtn():
            logging.info("saveAsFile")
            if file_manager.saveAsDocument(self.doc):
                logging.info("Created tab")

        def onExitBtn():
            logging.info("onExitBtn")
            file_manager.closeAll(self.document)
            app.close()

        self.menu_file = self.addMenu('&File')

        # ========= START FILE MENU SECTION =========
        def makeFileAction(name: str, shortcut: str, signal) -> QAction:
            file_action = QAction(name, app)
            file_action.setShortcut(shortcut)
            file_action.triggered.connect(signal)
            return file_action

        new_file_act = QAction("&New...", app)
        new_file_act.setStatusTip('New')
        new_file_act.triggered.connect(onNewBtn)
        self.menu_file.addAction(makeFileAction("New", "Alt+insert", onNewBtn))
        self.menu_file.addAction(makeFileAction("Open", "", onOpenBtn))
        self.menu_file.addAction(makeFileAction("Open Folder", "", onOpenFolderBtn))
        self.menu_file.addSeparator()
        self.menu_file.addAction(makeFileAction("Save...", "Ctrl+s", onSaveBtn))
        self.menu_file.addAction(makeFileAction("Save As...", "", onSaveAsBtn))
        self.menu_file.addSeparator()
        self.menu_file.addAction(makeFileAction("Exit", "", onExitBtn))
        # ========= END FILE MENU SECTION =========

        return self.menu_file

    # =====================================================================================
    def makeEditMenu(self, app):
        """
        Create Edit Menu
        :return: the menu created
        """
        logging.info("makeEditMenu")
        self.menu_edit = self.addMenu('&Edit')

        def onFindBtn():
            logging.info("")
            self.doc.search.setVisible(not self.doc.search.isVisible())

        def onFindAllBtn():
            logging.info("")

        # ========= START EDIT MENU SECTION =========
        def makeEditAction(name: str, shortcut: str, signal) -> QAction:
            edit_action = QAction(name, app)
            edit_action.setShortcut(shortcut)
            edit_action.triggered.connect(signal)
            return edit_action

        # Add actions
        self.menu_edit.addAction(makeEditAction("Undo", "Ctrl+z", self.doc.undo))
        self.menu_edit.addAction(makeEditAction("Redo", "Ctrl+Shift+z", self.doc.redo))
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(makeEditAction("Select All", "Ctrl+a", self.doc.selectAll))
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(makeEditAction("Cut", "Ctrl+x", self.doc.cut))
        self.menu_edit.addAction(makeEditAction("Copy", "Ctrl+c", self.doc.copy))
        self.menu_edit.addAction(makeEditAction("Paste", "Ctrl+v", self.doc.paste))
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(makeEditAction("Find", "Ctrl+f", onFindBtn))
        self.menu_edit.addAction(makeEditAction("Find All", "Ctrl+Shift+f", onFindAllBtn))


        # ========= END EDIT MENU SECTION =========
        return self.menu_edit



    # =====================================================================================
    def makeViewMenu(self, app, bottom_bar) -> QMenu:
        """
        Create View Menu
        :return: the menu created
        """
        logging.info("makeViewMenu")
        self.menu_view = self.addMenu('&View')

        # ========= START VIEW MENU SECTION =========
        def makeViewAction(name: str, shortcut: str, signal) -> QAction:
            view_action = QAction(name, app)
            view_action.setShortcut(shortcut)
            view_action.triggered.connect(signal)
            return view_action

        self.menu_view.addAction(makeViewAction("Zoom In", "ctrl+=", bottom_bar.onZoomInClicked))
        self.menu_view.addAction(makeViewAction("Zoom Out", "ctrl+-", bottom_bar.onZoomOutClicked))
        self.menu_view.addAction(makeViewAction("Zoom Reset", "", bottom_bar.resetZoom))
        # ========= END VIEW MENU SECTION =========
        return self.menu_view

    # =====================================================================================
    def makeFormatMenu(self, app) -> QMenu:
        """
        Create Format Menu
        :return: the menu created
        """
        logging.info("formatMenuSetup")
        self.menu_format = self.addMenu('&Format')

        # ========= START FONT STYLES SECTION =========
        def makeStyleAction(name: str, shortcut: str, signal, docref) -> QAction:
            style_action = QAction(name, app)
            style_action.setShortcut(shortcut)
            style_action.setCheckable(True)
            style_action.setProperty("docref", docref)
            style_action.triggered.connect(signal)
            return style_action

        self.group_style = QActionGroup(self.menu_format)
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
        self.menu_format.addActions(self.group_style.actions())
        # ========= END FONT STYLES SECTION =========

        # ========= START EXTRA SECTION =========
        self.menu_format.addSeparator()
        act_color_picker = QAction("Color Picker", app)
        act_color_picker.triggered.connect(self.doc.openColorDialog)
        self.menu_format.addAction(act_color_picker)

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

        self.menu_format.addSeparator()
        # Action Group for Alignments options (Exclusive picks)
        self.group_align = QActionGroup(self.menu_format)
        self.group_align.triggered.connect(onTextAlignmentChanged)

        def getName(index: int):
            return list(self.doc_props.dict_align.keys())[index]

        # Add alignment options to the group
        self.group_align.addAction(makeAlignAction(getName(0), 'Ctrl+Shift+L', True))
        self.group_align.addAction(makeAlignAction(getName(1), 'Ctrl+Shift+R'))
        self.group_align.addAction(makeAlignAction(getName(2), 'Ctrl+Shift+E'))
        self.group_align.addAction(makeAlignAction(getName(3), 'Ctrl+Shift+J'))
        # Add all actions in group to Format Menu
        self.menu_format.addActions(self.group_align.actions())
        # ========= END ALIGNMENT SECTION =========
        return self.menu_format

    # =====================================================================================
    def makeToolsMenu(self, app, document) -> QMenu:
        """
        Create View Menu
        :return: the menu created
        """
        logging.info("makeViewMenu")
        self.menu_tools = self.addMenu('&Tools')

        # ========= START TOOLS MENU SECTION =========

        def onSummaryAction():
            DocumentSummarizer.onSummaryAction(app, document)

        def makeToolsAction(name: str, shortcut: str, signal) -> QAction:
            tools_action = QAction(name, app)
            tools_action.setShortcut(shortcut)
            tools_action.triggered.connect(signal)
            return tools_action

        self.menu_tools.addAction(makeToolsAction("Generate Summary", "", onSummaryAction))

        # ========= END TOOLS MENU SECTION =========

        return self.menu_tools

    # =====================================================================================

    def setFormattingButtonsEnabled(self, state):
        """
        Sets all formatting options to Enabled or Disabled
        :param state: boolean that sets the states
        :return: returns nothing
        """
        # Toggle the state of all buttons in the menu
        logging.info(str(state))
        a: QAction
        for a in self.menu_format.actions():
            if not a.property("persistent"):
                a.setEnabled(state)

    def updateFormatOnSelectionChange(self):
        """
        Selected text format reflected in the MenuBar
        :return: returns nothing
        """
        # Block signals
        a: QAction
        for a in self.menu_format.actions():
            if not a.property("persistent"):
                a.blockSignals(True)
        # Update Style options
        for action in self.group_style.actions():
            get = action.property("docref")
            action.setChecked(get())
        # Update Align options
        alignment = self.doc.alignment()
        for action in self.group_align.actions():
            action.setChecked(False)
            get = action.property("docref")
            index = list(self.doc_props.dict_align.values()).index(alignment)
            if action.text() == list(self.doc_props.dict_align.keys())[index]:
                action.setChecked(True)
        # Unblock signals
        a: QAction
        for a in self.menu_format.actions():
            if not a.property("persistent"):
                a.blockSignals(False)
