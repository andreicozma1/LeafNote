"""
all properties and functionalities of the menu bar
"""

import logging
from functools import partial

from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtWidgets import QFileDialog, QMenuBar, QActionGroup

from LeafNote import Utils, Widgets
from LeafNote.Layout.Elements import Document
from LeafNote.Layout.Utils import SearchWorkspace
from LeafNote.Props import DocProps, LayoutProps


class MenuBar(QMenuBar):
    """
    This class is a customized QMenuBar for the application
    """

    def __init__(self, document: Document, doc_props: DocProps, layout_props: LayoutProps):
        """
        Sets up the System MenuBar
        :return: returns nothing
        """
        super().__init__()
        logging.debug("Creating MenuBar")

        self.doc = document
        self.doc_props = doc_props
        self.layout_props = layout_props
        self.setNativeMenuBar(False)

        self.menu_format = None
        self.group_style = None
        self.group_align = None

        self.updateAppearance()

    # =====================================================================================
    def makeFileMenu(self, app, file_manager):
        """
        sets up the file tabs drop menu
        :return: returns nothing
        """
        logging.debug("makeFileMenu")

        def onNewBtn():
            """
            """
            logging.info("Clicked New Action")
            file_manager.newFile(self.doc)

        def onOpenBtn():
            """
            """
            logging.info("Clicked Open Action")
            # opens a file dialogue for the user to select a file to open
            file_name = QFileDialog.getOpenFileName(app, 'Open file',
                                                    app.left_menu.model.rootPath())
            # open the chosen file and show the text in the text editor
            file_manager.openDocument(self.doc, file_name[0])

        def onOpenFolderBtn():
            """
            """
            logging.info("Clicked Open Folder Action")
            # opens a file dialogue for the user to select a file to open
            folder_name = QFileDialog.getExistingDirectory(app, 'Open folder',
                                                           app.left_menu.model.rootPath())
            # if the user selected a new folder
            if folder_name != "":
                app.left_menu.updateDirectory(folder_name)
            else:
                logging.info("User chose not to open folder")

        # this saves the current file that is shown in the self.doc
        def onSaveBtn():
            """
            """
            logging.info("Clicked Save Action")
            if file_manager.saveDocument(self.doc):
                logging.debug("Saved Document Completed.")

        def onSaveAsBtn():
            """
            """
            logging.info("Clicked Save As Action")
            if file_manager.saveAsDocument(self.doc):
                logging.debug("Saved As Document Completed.")

        def onExitBtn():
            """
            """
            logging.info("Clicked Exit Action")
            file_manager.closeAll(self.doc)
            app.close()

        menu_file = self.addMenu('&File')

        # ========= START FILE MENU SECTION =========
        def makeFileAction(name: str, shortcut: str, signal) -> QAction:
            """
            """
            file_action = QAction(name, app)
            file_action.setShortcut(shortcut)
            file_action.triggered.connect(signal)
            return file_action

        new_file_act = QAction("&New...", app)
        new_file_act.setStatusTip('New')
        new_file_act.triggered.connect(onNewBtn)

        menu_file.addAction(makeFileAction("New File", "Alt+Insert", onNewBtn))
        menu_file.addAction(makeFileAction("Open File", "Ctrl+o", onOpenBtn))
        menu_file.addAction(makeFileAction("Open Workspace", "Ctrl+Shift+o", onOpenFolderBtn))
        menu_file.addSeparator()
        menu_file.addAction(makeFileAction("Save File...", "Ctrl+s", onSaveBtn))
        menu_file.addAction(makeFileAction("Save File As...", "Ctrl+Shift+q", onSaveAsBtn))
        menu_file.addSeparator()
        menu_download = menu_file.addMenu('&Export')
        menu_download.addAction(makeFileAction("PDF Document (.pdf)", "",
                                               partial(file_manager.exportToPDF, self.doc)))
        menu_file.addAction(makeFileAction("Print", "Ctrl+p", partial(file_manager.printDocument,
                                                                      self.doc)))

        menu_file.addSeparator()
        menu_file.addAction(makeFileAction("Exit", "Ctrl+q", onExitBtn))
        # ========= END FILE MENU SECTION =========

        return menu_file

    # =====================================================================================
    def makeEditMenu(self, app, file_manager):
        """
        Create Edit Menu
        :return: the menu created
        """
        logging.debug("Creating Edit Menu")

        def onFindBtn():
            """
            """
            state_replace = app.search_and_replace.replace.isVisible()
            logging.info("Clicked Find Action - %s", str(state_replace))
            if state_replace:
                app.search_and_replace.replace.setVisible(False)

            state_search = app.search_and_replace.search.isVisible()
            app.search_and_replace.search.setVisible(not state_search)
            if not state_search:
                app.search_and_replace.search.search_bar.setFocus()

        def onFindAllBtn(replace=False):
            """
            """
            logging.info("Clicked Find All Action")
            # create the search workspace dialog
            search_workspace_dialog = Utils.DialogBuilder(app, "Search Workspace")

            # create search workspace widget
            search_workspace = SearchWorkspace(self.doc, file_manager,
                                               app.left_menu.model.rootPath())
            search_workspace.toggleReplace(replace)
            search_workspace.setCloseDialogCallback(search_workspace_dialog.close)

            # modify the dialog
            search_workspace_dialog.addWidget(search_workspace)
            search_workspace_dialog.show()

        def onFindAndReplaceBtn():
            """
            """
            state_replace = app.search_and_replace.replace.isVisible()
            logging.info("Clicked Find and Replace Action - %s", str(state_replace))
            # Toggle Find and Replace
            app.search_and_replace.replace.setVisible(not state_replace)
            if app.search_and_replace.replace.isVisible():
                app.search_and_replace.search.setVisible(True)
                app.search_and_replace.search.search_bar.setFocus()

        # ========= START EDIT MENU SECTION =========
        menu_edit = self.addMenu('&Edit')

        def makeEditAction(name: str, shortcut: str, signal) -> QAction:
            """
            """
            edit_action = QAction(name, app)
            edit_action.setShortcut(shortcut)
            edit_action.triggered.connect(signal)
            return edit_action

        # Add actions
        menu_edit.addAction(makeEditAction("Undo", "Ctrl+z", self.doc.undo))
        menu_edit.addAction(makeEditAction("Redo", "Ctrl+Shift+z", self.doc.redo))
        menu_edit.addSeparator()
        menu_edit.addAction(makeEditAction("Select All", "Ctrl+a", self.doc.selectAll))
        menu_edit.addSeparator()
        menu_edit.addAction(makeEditAction("Cut", "Ctrl+x", self.doc.cut))
        menu_edit.addAction(makeEditAction("Copy", "Ctrl+c", self.doc.copy))
        menu_edit.addAction(makeEditAction("Paste", "Ctrl+v", self.doc.paste))
        menu_edit.addAction(makeEditAction("Paste Plain", "Ctrl+Shift+v", self.doc.pastePlain))
        menu_edit.addSeparator()
        menu_edit.addAction(makeEditAction("Find", "Ctrl+f", onFindBtn))
        menu_edit.addAction(makeEditAction("Find All", "Ctrl+Shift+f", onFindAllBtn))
        menu_edit.addAction(makeEditAction("Replace", "Ctrl+r", onFindAndReplaceBtn))
        menu_edit.addAction(makeEditAction("Find All", "Ctrl+Shift+r", partial(onFindAllBtn, True)))

        # ========= END EDIT MENU SECTION =========
        return menu_edit

    # =====================================================================================
    def makeViewMenu(self, app, left_menu) -> QMenu:
        """
        Create View Menu
        :return: the menu created
        """
        logging.debug("Creating View Menu")
        menu_view = self.addMenu('&View')

        # ========= START VIEW MENU SECTION =========
        def makeViewAction(name: str, shortcut: str, signal) -> QAction:
            """
            Creates action button for View Menu
            :param name: Name displayed in menu
            :param shortcut: shortcut used
            :pram signal: callback
            """
            view_action = QAction(name, app)
            view_action.setShortcut(shortcut)
            view_action.triggered.connect(signal)
            return view_action

        # ========= START LEFT MENU OPTIONS SECTION =========
        menu_view.addSeparator()
        menu_view.addAction(
            makeViewAction("Expand All", "", left_menu.expandAll))
        menu_view.addAction(
            makeViewAction("Collapse All", "", left_menu.collapseAll))
        menu_view.addSeparator()
        menu_view.addAction(
            makeViewAction("Toggle Size", "",
                           partial(left_menu.toggleHeaderColByName, "Size")))
        menu_view.addAction(
            makeViewAction("Toggle Type", "",
                           partial(left_menu.toggleHeaderColByName, "Type")))
        menu_view.addAction(
            makeViewAction("Toggle Date", "",
                           partial(left_menu.toggleHeaderColByName, "Date Modified")))
        menu_view.addAction(
            makeViewAction("Fit Columns", "", left_menu.resizeColumnsToContent))
        # ========= END LEFT MENU OPTIONS SECTION =========

        # ========= END VIEW MENU SECTION =========
        return menu_view

    # =====================================================================================
    def makeFormatMenu(self, app) -> QMenu:
        """
        Create Format Menu
        :return: the menu created
        """
        logging.debug("Creating Format Menu")
        self.menu_format = self.addMenu('&Format')

        # ========= START FONT STYLES SECTION =========
        def makeStyleAction(name: str, shortcut: str, signal, docref) -> QAction:
            """
            """
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
        act_ital = makeStyleAction("Italicize", "Ctrl+I", self.doc.onFontItalChanged,
                                   self.doc.fontItalic)
        self.group_style.addAction(act_ital)
        act_strk = makeStyleAction("Strikeout", "Ctrl+Shift+5", self.doc.onFontStrikeChanged,
                                   self.doc.fontStrike)
        self.group_style.addAction(act_strk)
        act_undr = makeStyleAction("Underline", "Ctrl+U", self.doc.onFontUnderChanged,
                                   self.doc.fontUnderline)
        self.group_style.addAction(act_undr)
        # Add all actions in group to Style Menu
        self.menu_format.addActions(self.group_style.actions())
        # ========= END FONT STYLES SECTION =========

        # ========= START EXTRA SECTION =========
        self.menu_format.addSeparator()

        clear_format = QAction("Clear Format", app)
        clear_format.setShortcut("Ctrl+0")
        clear_format.triggered.connect(self.doc.clearSelectionFormatting)
        self.menu_format.addAction(clear_format)

        act_color_picker = QAction("Color Picker", app)
        act_color_picker.triggered.connect(self.doc.openColorDialog)
        self.menu_format.addAction(act_color_picker)

        # ========= END EXTRA SECTION =========

        # ========= START ALIGNMENT SECTION =========
        def makeAlignAction(name: str, shortcut: str, default: bool = False) -> QAction:
            """
            """
            align_action = QAction(name, app)
            align_action.setShortcut(shortcut)
            align_action.setCheckable(True)
            align_action.setChecked(default)
            return align_action

        def onTextAlignmentChanged(state):
            """
            """
            self.doc.onTextAlignmentChanged(
                list(self.doc_props.dict_text_aligns.keys()).index(state.text()))

        self.menu_format.addSeparator()
        # Action Group for Alignments options (Exclusive picks)
        self.group_align = QActionGroup(self.menu_format)
        self.group_align.triggered.connect(onTextAlignmentChanged)

        def getName(index: int):
            """
            """
            return list(self.doc_props.dict_text_aligns.keys())[index]

        # Add alignment options to the group
        self.group_align.addAction(makeAlignAction(getName(0), 'Ctrl+Shift+[', True))
        self.group_align.addAction(makeAlignAction(getName(1), 'Ctrl+Shift+]'))
        self.group_align.addAction(makeAlignAction(getName(2), 'Ctrl+Shift+\\'))
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
        logging.debug("Creating Tools Menu")
        menu_tools = self.addMenu('&Tools')

        # ========= START TOOLS MENU SECTION =========

        def onSummaryAction():
            """
            Called on clicking summary action
            """
            logging.info("Clicked Summary Action")
            if document.summarizer is None:
                Utils.Summarizer.onSummaryAction(app, document)
            if document.summarizer is not None:
                selection = document.textCursor().selectedText()
                if selection != "":
                    app.right_menu.col_summary_body.setText(
                        document.summarizer.summarize(selection))
                else:
                    app.right_menu.col_summary_body.setText(
                        document.summarizer.summarize(document.toPlainText()))
            app.right_menu.col_summary_main.collapse()

        def onEncryptionAction():
            """
            Called on clicking encryptor action
            """
            logging.info("Clicked Encryptor Action")
            Utils.Encryptor.onEncryptionAction(app, app.file_manager)

        def onCalculatorAction():
            """
            Called on clicking calculator action
            """
            logging.info("Clicked Calculator Action")
            dialog = Utils.DialogBuilder(text_window="Calculator")
            dialog.layout().setContentsMargins(0, 0, 0, 0)
            dialog.addWidget(Widgets.CalculatorWidget())
            dialog.exec()

        def onRemindersAction():
            """
            Called on clicking reminders action
            """
            logging.info("Clicked Reminders Action")
            app.reminders.showDialog(app)

        def onEquationEditorAction():
            """
            Called on clicking equation editor action
            """
            logging.info("Clicked Equation Editor Action")
            Widgets.EquationEditorWidget(document)

        def onDictionaryAction():
            """
            Called on clicking dictionary action
            """
            logging.info("Clicked Dictionary Action")
            dictionary = Widgets.DictionaryWidget()
            dialog = Utils.DialogBuilder(text_window="Dictionary")
            dictionary.onCloseClicked(dialog.close)
            dictionary.onLookupClicked(dialog.adjustSize)
            dialog.layout().setContentsMargins(0, 0, 0, 0)
            dialog.setFixedWidth(600)
            dialog.addWidget(dictionary)
            dialog.show()

        def makeToolsAction(name: str, shortcut: str, signal) -> QAction:
            """
            Makes a Tools action
            """
            tools_action = QAction(name, app)
            tools_action.setShortcut(shortcut)
            tools_action.triggered.connect(signal)

            return tools_action

        def makeToolsToggle(name: str, shortcut: str, signal,
                            checkable: bool = False,
                            checked: bool = False) -> QAction:
            """
            Makes a Tools action
            """
            tools_action = QAction(name, app)
            tools_action.setShortcut(shortcut)
            tools_action.setCheckable(checkable)
            tools_action.setChecked(checked)
            tools_action.toggled.connect(signal)

            return tools_action

        menu_tools.addAction(makeToolsToggle("Spell Check", "",
                                             self.doc.toggle_spellcheck, True,
                                             self.doc_props.def_enable_spellcheck))
        menu_tools.addAction(makeToolsToggle("Auto Correct", "",
                                             self.doc.toggle_autocorrect, True,
                                             self.doc_props.def_enable_autocorrect))
        menu_tools.addSeparator()
        menu_tools.addAction(makeToolsAction("Summarize", "", onSummaryAction))
        menu_tools.addAction(
            makeToolsAction("Encrypt/Decrypt", "", onEncryptionAction))
        menu_tools.addAction(makeToolsAction("Add Reminder", "", onRemindersAction))
        menu_tools.addAction(makeToolsAction("Calculator", "", onCalculatorAction))
        menu_tools.addAction(makeToolsAction("Equation Editor ", "", onEquationEditorAction))
        menu_tools.addAction(makeToolsAction("Word Dictionary ", "", onDictionaryAction))

        # ========= END TOOLS MENU SECTION =========

        return menu_tools

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
            align_list = list(self.doc_props.dict_text_aligns.values())
            if alignment in align_list:
                index = align_list.index(alignment)
                if action.text() == list(self.doc_props.dict_text_aligns.keys())[index]:
                    action.setChecked(True)
        # Unblock signals

        a: QAction
        for a in self.menu_format.actions():
            if not a.property("persistent"):
                a.blockSignals(False)

    def updateAppearance(self):
        """
        Updates appearance of MenuBar according to styles
        """
        prop_select_color = self.layout_props.getDefaultHeaderColorLight()
        style = "QMenu::item:selected { background-color: " + prop_select_color + ";}"
        self.setStyleSheet(style)
