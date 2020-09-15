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
        self.view_menu = self.menu.addMenu('&View')
        self.tools_menu = self.menu.addMenu('&Tools')
        self.help_menu = self.menu.addMenu('&Help')

    def setup(self):
        print("MenuBar - setup")
        # File tab submenus and actions
        # TODO - Add more submenus and action for each of the menu tabs
        self.fileMenuSetup()
        self.editMenuSetup()
        self.viewMenuSetup()
        self.toolsMenuSetup()
        self.helpMenuSetup()

    # --------------------------------------------------------------------------------

    # TODO - Add more functionality to file tab - new, save, save as, save all, settings, etc.
    # this function sets up the file tabs drop menu
    def fileMenuSetup(self):
        print("MenuBar - fileMenuSetup")

        # TODO - new file

        # opens a dialogue to chose a file an open it
        open_file_act = QAction("&Open...", self.app)
        open_file_act.setStatusTip('Open File')
        open_file_act.triggered.connect(self.showOpenFileDialog)
        self.file_menu.addAction(open_file_act)

        open_folder_act = QAction("&Open Folder...", self.app)
        open_folder_act.setStatusTip('Open Folder')
        open_folder_act.triggered.connect(self.showOpenFolderDialog)
        self.file_menu.addAction(open_folder_act)

        # save the open file
        save_file = QAction("&Save...", self.app)
        save_file.setStatusTip('Save')
        save_file.triggered.connect(self.saveFile)
        self.file_menu.addAction(save_file)

        # TODO - save the file as a specified name
        '''
        save_as_file = QAction("&Save As...", self.app)
        save_as_file.setStatusTip('Save As')
        save_as_file.triggered.connect(self.saveAsFile)
        self.file_menu.addAction(save_as_file)
        '''

        # quit main window
        exit_act = QAction("&Exit", self.app)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(self.closeWindow)
        self.file_menu.addAction(exit_act)

    # this saves the current file that is shown in the document
    def saveFile(self):
        print("MenuBar - saveFile")

        self.file_manager.saveDocument()

    # TODO - save the file as a specified name
    def saveAsFile(self):
        print("MenuBar - saveAsFile")
        print("TODO")

    # this function opens a dialog for the user to select a file to open. When the user
    # selects a file it will show its text in the middle of the window
    def showOpenFileDialog(self):
        print("MenuBar - showOpenFileDialog")
        # open the dialogue using the home directory as root

        # this is opens the file dialogue in the project path
        # ***** Delete this line in the future
        home_dir = self.app.app_props.mainPath

        # this is opens the file dialogue in the project path
        # ***** Delete this line in the future

        # opens a file dialogue for the user to select a file to open
        # ***** Currently only looks for text files
        file_name = QFileDialog.getOpenFileName(self.app, 'Open file',
                                                home_dir, "Text files (*.txt)")

        # open the chosen file and show the text in the text editor
        data = self.file_manager.openDocument(file_name[0])

    def showOpenFolderDialog(self):
        # open the dialogue using the home directory as root
        print("MenuBar - showOpenFolderDialog")

        home_dir = self.app.app_props.mainPath

        # opens a file dialogue for the user to select a file to open
        # ***** Currently only looks for text files
        folder_name = QFileDialog.getExistingDirectory(self.app, 'Open file', home_dir)

        self.app.app_props.mainPath = folder_name

        self.app.layout.left_menu.updateDirectory(self.app.app_props.mainPath)

    def closeWindow(self):
        print("MenuBar - closeWindow")
        self.file_manager.closeAll()
        qApp.quit()

    # --------------------------------------------------------------------------------

    # TODO - Add functionality to edit tab - undo, redo, cut, copy, paste, etc.
    # this function sets up the edit tabs drop menu
    def editMenuSetup(self):
        print("MenuBar - cloeditMenuSetup")

    # --------------------------------------------------------------------------------

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
