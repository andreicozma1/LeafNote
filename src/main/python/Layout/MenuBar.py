from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import qApp, QAction


# Class to hold and customize a QPlainTextEdit Widget
class MenuBar():
    def __init__(self, app):
        print("MenuBar - init")
        self.app = app
        self.file_manager = app.file_manager
        self.layout = app.layout
        self.menu = app.menuBar()
        self.menu.setNativeMenuBar(False)

        self.file_menu = self.menu.addMenu('&File')
        self.edit_menu = self.menu.addMenu('&Edit')

        # TODO - uncomment when implementing these menus individually
        # self.view_menu = self.menu.addMenu('&View')
        # self.tools_menu = self.menu.addMenu('&Tools')
        # self.help_menu = self.menu.addMenu('&Help')

    def setup(self):
        print("MenuBar - setup")
        # File tab submenus and actions
        self.fileMenuSetup()
        self.editMenuSetup()

        # TODO - uncomment when implementing these menus individually
        # self.viewMenuSetup()
        # self.toolsMenuSetup()
        # self.helpMenuSetup()

    # --------------------------------------------------------------------------------

    # TODO - Add more functionality to file tab - new, save, save as, save all, settings, etc.
    # this function sets up the file tabs drop menu
    def fileMenuSetup(self):
        print("MenuBar - fileMenuSetup")

        # TODO - implement new file button that opens a new blank file in the document
        # new_file_act = QAction("&New...", self.app)
        # new_file_act.setStatusTip('New')
        # new_file_act.triggered.connect(self.onNewBtn)
        # self.file_menu.addAction(new_file_act)

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
        self.button_strike.setShortcut('ctrl+shift+s')
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
    # def onNewBtn(self):
    #     print("MenuBar - onNewBtn")

    # this function opens a dialog for the user to select a file to open. When the user
    # selects a file it will show its text in the middle of the window
    def onOpenBtn(self):
        print("MenuBar - onOpenBtn")
        # open the dialogue using the home directory as root

        # this is opens the file dialogue in the project path
        # ***** Delete this line in the future
        home_dir = str(QDir.currentPath())

        # opens a file dialogue for the user to select a file to open
        # ***** Currently only looks for text files
        file_name = QFileDialog.getOpenFileName(self.app, 'Open file',
                                                home_dir, "Text files (*.txt)")

        # open the chosen file and show the text in the text editor
        self.file_manager.openDocument(file_name[0])

    def onOpenFolderBtn(self):
        # open the dialogue using the home directory as root
        print("MenuBar - onOpenFolderBtn")

        home_dir = self.app.app_props.mainPath

        # opens a file dialogue for the user to select a file to open
        # ***** Currently only looks for text files
        folder_name = QFileDialog.getExistingDirectory(self.app, 'Open file', home_dir)

        self.app.app_props.mainPath = folder_name

        self.app.layout.left_menu.updateDirectory(self.app.app_props.mainPath)

    # this saves the current file that is shown in the document
    def onSaveBtn(self):
        print("MenuBar - onSaveBtn")
        self.file_manager.saveDocument()

    # TODO - save the file as a specified name in any location on disk
    def onSaveAsBtn(self):
        print("MenuBar - saveAsFile")
        new_file_path = QFileDialog.getSaveFileName(self.app, 'Save File')
        self.file_manager.saveAsDocument(new_file_path)

    def onExitBtn(self):
        print("MenuBar - onExitBtn")
        self.file_manager.closeAll()

        qApp.quit()

    # --------------------------------------------------------------------------------

    # TODO - Add functionality to edit tab - undo, redo, cut, copy, paste, etc.
    # this function sets up the edit tabs drop menu
    def editMenuSetup(self):
        print("MenuBar - editMenuSetup")

        # Idea: select button when keyboard shortcut used

        # undo button and function
        undo_act = QAction("&Undo", self.app)
        undo_act.setShortcut('Ctrl+z')
        undo_act.triggered.connect(self.layout.document.undo)
        self.edit_menu.addAction(undo_act)

        # redo button and function
        redo_act = QAction("&Redo", self.app)
        redo_act.setShortcut('Ctrl+Shift+z')
        redo_act.triggered.connect(self.layout.document.redo)
        self.edit_menu.addAction(redo_act)

        # adds line to separate options
        self.edit_menu.addSeparator()

        # select all button and function
        select_all_act = QAction("&Select All", self.app)
        select_all_act.setShortcut('Ctrl+a')
        select_all_act.triggered.connect(self.layout.document.selectAll)
        self.edit_menu.addAction(select_all_act)

        # adds line to separate options
        self.edit_menu.addSeparator()

        # cut button and function
        cut_act = QAction("&Cut", self.app)
        cut_act.setShortcut('Ctrl+x')
        cut_act.triggered.connect(self.layout.document.cut)
        self.edit_menu.addAction(cut_act)

        # copy button and function
        copy_act = QAction("&Copy", self.app)
        copy_act.setShortcut('Ctrl+c')
        copy_act.triggered.connect(self.layout.document.copy)
        self.edit_menu.addAction(copy_act)

        # paste button and function
        paste_act = QAction("&Paste", self.app)
        paste_act.setShortcut('Ctrl+v')
        paste_act.triggered.connect(self.layout.document.paste)
        self.edit_menu.addAction(paste_act)

    # --------------------------------------------------------------------------------

    # TODO - uncomment when implementing these menus
    """
    # TODO - Add functionality to view tab - appearance, etc.
    # this function sets up the view tabs drop menu
    def viewMenuSetup(self):
        print("MenuBar - viewMenuSetup")

    # --------------------------------------------------------------------------------

    # TODO - Add functionality to tools tab - tbd
    # this function sets up the tools tabs drop menu
    def toolsMenuSetup(self):
        print("MenuBar - toolsMenuSetup")

    # --------------------------------------------------------------------------------

    # TODO - Add functionality to help tab - find action, help, getting started, about, etc.
    # this function sets up the help tabs drop menu
    def helpMenuSetup(self):
        print("MenuBar - helpMenuSetup")
    """
