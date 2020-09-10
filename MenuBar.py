from PyQt5.QtWidgets import qApp, QAction


# Class to hold and customize a QPlainTextEdit Widget
class MenuBar():
    def __init__(self, app):
        # super(QMenuBar, self).__init__()
        self.app = app
        self.menu = app.menuBar()
        self.menu.setNativeMenuBar(False)

        self.file_menu = self.menu.addMenu('&File')
        self.edit_menu = self.menu.addMenu('&Edit')
        self.view_menu = self.menu.addMenu('&View')
        self.tools_menu = self.menu.addMenu('&Tools')
        self.help_menu = self.menu.addMenu('&Help')

    def setup(self):
        # File tab submenus and actions
        exit_act = QAction("&Exit", self.app)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)

        self.file_menu.addAction(exit_act)
        # menu.addAction(self.file_menu.menuAction())
        # self.view_menu.addAction(exit_act)
        # self.addAction(self.view_menu.menuAction())
        # TODO - Add more submenus and action for each of the menu tabs
        return self
