from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import qApp, QAction, QColorDialog
import logging

# Class to hold and customize a QPlainTextEdit Widget
class MenuBar():
    def __init__(self, app, file_manager, document, top_bar, bottom_bar):
        logging.info("")
        self.app = app
        self.document = document
        self.top_bar = top_bar
        self.bottom_bar = bottom_bar
        self.file_manager = file_manager

        self.menu = app.menuBar()
        self.menu.setNativeMenuBar(False)

        self.file_menu = self.menu.addMenu('&File')
        self.edit_menu = self.menu.addMenu('&Edit')

        # TODO - uncomment when implementing these menus individually
        self.view_menu = self.menu.addMenu('&View')
        self.format_menu = self.menu.addMenu('&Format')
        # self.tools_menu = self.menu.addMenu('&Tools')
        # self.help_menu = self.menu.addMenu('&Help')

        self.setup()

    def setup(self):
        logging.info("setup")
        # File tab submenus and actions
        self.fileMenuSetup()
        self.editMenuSetup()

        # TODO - uncomment when implementing these menus individually
        self.viewMenuSetup()
        self.formatMenuSetup()
        # self.toolsMenuSetup()
        # self.helpMenuSetup()

    # --------------------------------------------------------------------------------

    # TODO - Add more functionality to file tab - new, save, save as, save all, settings, etc.
    # this function sets up the file tabs drop menu
    def fileMenuSetup(self):
        logging.info("fileMenuSetup")

        # TODO - implement new file button that opens a new blank file in the document
        new_file_act = QAction("&New...", self.app)
        new_file_act.setStatusTip('New')
        new_file_act.triggered.connect(self.onNewBtn)
        self.file_menu.addAction(new_file_act)

        # opens a dialogue to chose a file an open it
        open_file_act = QAction("&Open...", self.app)
        open_file_act.setStatusTip('Open File')
        open_file_act.triggered.connect(self.onOpenBtn)
        self.file_menu.addAction(open_file_act)

        # open a folder as a workspace, showing the directory tree in the left menu
        open_folder_act = QAction("&Open Folder...", self.app)
        open_folder_act.setStatusTip('Open Folder')
        open_folder_act.triggered.connect(self.onOpenFolderBtn)
        self.file_menu.addAction(open_folder_act)

        # adds line to separate options
        self.file_menu.addSeparator()

        # save the open file
        save_file = QAction("&Save...", self.app)
        save_file.setStatusTip('Save')
        save_file.setShortcut('ctrl+s')
        save_file.triggered.connect(self.onSaveBtn)
        self.file_menu.addAction(save_file)

        # TODO - save the file as a specified name in any location on disk
        save_as_file = QAction("&Save As...", self.app)
        save_as_file.setStatusTip('Save As')
        save_as_file.setShortcut('ctrl+shift+s')
        save_as_file.triggered.connect(self.onSaveAsBtn)
        self.file_menu.addAction(save_as_file)

        # adds line to separate options
        self.file_menu.addSeparator()

        # quit main window
        exit_act = QAction("&Exit", self.app)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(self.onExitBtn)
        self.file_menu.addAction(exit_act)

    # TODO - implement new file button that opens a new blank file in the document
    def onNewBtn(self):
        logging.info("MenuBar - onNewBtn")
        self.app.file_manager.newFile()

    # this function opens a dialog for the user to select a file to open. When the user
    # selects a file it will show its text in the middle of the window
    def onOpenBtn(self):
        logging.info("onOpenBtn")
        # open the dialogue using the home directory as root

        # this is opens the file dialogue in the project path
        # ***** Delete this line in the future
        home_dir = str(QDir.currentPath())

        # opens a file dialogue for the user to select a file to open
        # TODO
        file_name = QFileDialog.getOpenFileName(self.app, 'Open file',
                                                home_dir)

        # open the chosen file and show the text in the text editor
        self.file_manager.openDocument(file_name[0])

    def onOpenFolderBtn(self):
        # open the dialogue using the home directory as root
        logging.info("onOpenFolderBtn")

        home_dir = self.app.app_props.mainPath

        # opens a file dialogue for the user to select a file to open
        # TODO - exclude certain files types like pdfs or images
        folder_name = QFileDialog.getExistingDirectory(self.app, 'Open folder', home_dir)

        # if the user selected a new folder
        if folder_name != "":
            self.app.app_props.mainPath = folder_name
            self.app.left_menu.updateDirectory(self.app.app_props.mainPath)

    # this saves the current file that is shown in the document
    def onSaveBtn(self):
        logging.info("onSaveBtn")
        self.file_manager.saveDocument()

    # TODO - save the file as a specified name in any location on disk
    def onSaveAsBtn(self):
        logging.info("saveAsFile")
        new_file_path = QFileDialog.getSaveFileName(self.app, 'Save File')
        self.file_manager.saveAsDocument(new_file_path[0])

    def onExitBtn(self):
        logging.info("onExitBtn")
        self.file_manager.closeAll()

        qApp.quit()

    # --------------------------------------------------------------------------------

    # TODO - Add functionality to edit tab - undo, redo, cut, copy, paste, etc.
    # this function sets up the edit tabs drop menu
    def editMenuSetup(self):
        logging.info("editMenuSetup")

        # Idea: select button when keyboard shortcut used

        # undo button and function
        undo_act = QAction("&Undo", self.app)
        undo_act.setShortcut('Ctrl+z')
        undo_act.triggered.connect(self.app.document.undo)
        self.edit_menu.addAction(undo_act)

        # redo button and function
        redo_act = QAction("&Redo", self.app)
        redo_act.setShortcut('Ctrl+Shift+z')
        redo_act.triggered.connect(self.app.document.redo)
        self.edit_menu.addAction(redo_act)

        # adds line to separate options
        self.edit_menu.addSeparator()

        # select all button and function
        select_all_act = QAction("&Select All", self.app)
        select_all_act.setShortcut('Ctrl+a')
        select_all_act.triggered.connect(self.app.document.selectAll)
        self.edit_menu.addAction(select_all_act)

        # adds line to separate options
        self.edit_menu.addSeparator()

        # cut button and function
        cut_act = QAction("&Cut", self.app)
        cut_act.setShortcut('Ctrl+x')
        cut_act.triggered.connect(self.app.document.cut)
        self.edit_menu.addAction(cut_act)

        # copy button and function
        copy_act = QAction("&Copy", self.app)
        copy_act.setShortcut('Ctrl+c')
        copy_act.triggered.connect(self.app.document.copy)
        self.edit_menu.addAction(copy_act)

        # paste button and function
        paste_act = QAction("&Paste", self.app)
        paste_act.setShortcut('Ctrl+v')
        paste_act.triggered.connect(self.app.document.paste)
        self.edit_menu.addAction(paste_act)

    # --------------------------------------------------------------------------------

    # TODO - uncomment when implementing these menus
    # TODO - Add functionality to view tab - appearance, etc.
    # this function sets up the view tabs drop menu
    def viewMenuSetup(self):
        logging.info("viewMenuSetup")
        zoom_in_act = QAction("&Zoom In", self.app)
        zoom_in_act.setShortcut('ctrl+=')
        zoom_in_act.triggered.connect(self.app.bottom_bar.onZoomInClicked)
        self.view_menu.addAction(zoom_in_act)

        zoom_out_act = QAction("&Zoom Out", self.app)
        # zoom_out_act.setShortcut('ctrl+-')
        zoom_out_act.setShortcut('ctrl+-')
        zoom_out_act.triggered.connect(self.app.bottom_bar.onZoomOutClicked)
        self.view_menu.addAction(zoom_out_act)

        zoom_r_act = QAction("&Zoom Reset", self.app)
        zoom_r_act.triggered.connect(self.app.bottom_bar.resetZoom)
        self.view_menu.addAction(zoom_r_act)

    # --------------------------------------------------------------------------------
    # TODO - Add functionality to tools tab - tbd
    # this function sets up the tools tabs drop menu
    def formatMenuSetup(self):
        logging.info("formatMenuSetup")
        # Sets up submenue of 'Text' inside of the 'Format' menu
        self.text_menu = self.format_menu.addMenu('&Text')

        # sets up a submenu for alignment and indentation in the format menu
        self.align_indent_menu = self.format_menu.addMenu('&Align && Indent')

        # Adds Bold button to text_menu
        self.bold_action = QAction("Bold", self.app)
        self.bold_action.setShortcut('Ctrl+B')
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.app.document.onFontBoldChanged)
        self.text_menu.addAction(self.bold_action)

        # Adds Italicised button to text_menu
        self.ital_action = QAction("Italicised", self.app)
        self.ital_action.setShortcut('Ctrl+I')
        self.ital_action.setCheckable(True)
        self.ital_action.triggered.connect(self.app.document.onFontItalChanged)
        self.text_menu.addAction(self.ital_action)

        # Adds Strikeout button to text_menu
        self.strike_action = QAction("Strikout", self.app)
        self.strike_action.setShortcut('Ctrl+Shift+5')
        self.strike_action.setCheckable(True)
        self.strike_action.triggered.connect(self.app.document.onFontStrikeChanged)
        self.text_menu.addAction(self.strike_action)

        # Adds Underline button to text_menu
        self.under_action = QAction("Underline", self.app)
        self.under_action.setShortcut('Ctrl+U')
        self.under_action.setCheckable(True)
        self.under_action.triggered.connect(self.app.document.onFontUnderChanged)
        self.text_menu.addAction(self.under_action)

        # Adds Seperator to text_menu
        self.text_menu.addSeparator()

        # Adds Font Color button to text_menu
        self.font_color_action = QAction("Font Color", self.app)
        self.font_color_action.triggered.connect(self.openColorDialog)
        self.text_menu.addAction(self.font_color_action)

        # --- create the alignment and indentation menu ---
        # create the left alignment action
        self.left_align_action = QAction("Left Align", self.app)
        self.left_align_action.setShortcut('Ctrl+Shift+L')
        self.left_align_action.triggered.connect(self.onTextAlignLeftClicked)
        self.align_indent_menu.addAction(self.left_align_action)

        # create the center alignment action
        self.center_align_action = QAction("Center Align", self.app)
        self.center_align_action.setShortcut('Ctrl+Shift+E')
        self.center_align_action.triggered.connect(self.onTextAlignCenterClicked)
        self.align_indent_menu.addAction(self.center_align_action)

        # create the right alignment action
        self.right_align_action = QAction("Right Align", self.app)
        self.right_align_action.setShortcut('Ctrl+Shift+R')
        self.right_align_action.triggered.connect(self.onTextAlignRightClicked)
        self.align_indent_menu.addAction(self.right_align_action)

        # create the justify alignment action
        self.justify_align_action = QAction("Justify Align", self.app)
        self.justify_align_action.setShortcut('Ctrl+Shift+J')
        self.justify_align_action.triggered.connect(self.onTextAlignJustifyClicked)
        self.align_indent_menu.addAction(self.justify_align_action)

        # if the enable formatting mode is toggled
        self.setFormattingEnabled(False)

        self.app.top_bar.button_mode_switch.toggled.connect(self.setFormattingEnabled)
        self.app.document.selectionChanged.connect(self.updateFormatOnSelectionChange)

    # Opens the color widget and checks for a valid color then sets document font color
    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.app.document.setTextColor(color)

    def onTextAlignLeftClicked(self):
        """
        This will left align the selected text in the document
        :return: Returns nothing
        """
        logging.info("Align Left")
        self.document.setAlignment(Qt.AlignLeft)
        self.top_bar.combo_text_align.setCurrentIndex(self.top_bar.list_alignments_align.index(Qt.AlignLeft))

    def onTextAlignCenterClicked(self):
        """
            This will center align the selected text in the document
            :return: Returns nothing
        """
        logging.info("Align Center")
        self.document.setAlignment(Qt.AlignCenter)
        self.top_bar.combo_text_align.setCurrentIndex(self.top_bar.list_alignments_align.index(Qt.AlignCenter))


    def onTextAlignRightClicked(self):
        """
            This will right align the selected text in the document
            :return: Returns nothing
        """
        logging.info("Align Right")
        self.document.setAlignment(Qt.AlignRight)
        self.top_bar.combo_text_align.setCurrentIndex(self.top_bar.list_alignments_align.index(Qt.AlignRight))

    def onTextAlignJustifyClicked(self):
        """
            This will justify align the selected text in the document
            :return: Returns nothing
        """
        logging.info("Align Justify")
        self.document.setAlignment(Qt.AlignJustify)
        self.top_bar.combo_text_align.setCurrentIndex(self.top_bar.list_alignments_align.index(Qt.AlignJustify))

    def setFormattingEnabled(self, state):
        """
        :param state: this is a boolean that sets the states
        """
        logging.info(str(state))
        a: QAction
        for a in self.text_menu.actions():
            if not a.property("persistent"):
                a.setEnabled(state)

    def updateFormatOnSelectionChange(self):
        a: QAction
        for a in self.text_menu.actions():
            if not a.property("persistent"):
                a.blockSignals(True)

        self.ital_action.setChecked(self.app.document.fontItalic())
        self.under_action.setChecked(self.app.document.fontUnderline())
        self.bold_action.setChecked(self.app.document.fontWeight() == QFont.Bold)
        self.strike_action.setChecked(self.app.document.currentCharFormat().fontStrikeOut())

        a: QAction
        for a in self.text_menu.actions():
            if not a.property("persistent"):
                a.blockSignals(False)
    # --------------------------------------------------------------------------------

    """
    # TODO - Add functionality to tools tbd
    # this function sets up the tools tabs drop menu
    def toolsMenuSetup(self):
        logging.info("toolsMenuSetup")

    # --------------------------------------------------------------------------------

    # TODO - Add functionality to help find action, help, getting started, about, etc.
    # this function sets up the help tabs drop menu
    def helpMenuSetup(self):
        logging.info("helpMenuSetup")
    """