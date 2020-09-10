from PyQt5.QtWidgets import qApp, QAction


# Class to hold and customize a QPlainTextEdit Widget
class MenuBar():
    def __init__(self, appCtx):
        # super(QMenuBar, self).__init__()
        self.appCtx = appCtx
        self.menu = appCtx.menuBar()
        self.menu.setNativeMenuBar(False)

        self.file_menu = self.menu.addMenu('&File')
        self.edit_menu = self.menu.addMenu('&Edit')
        self.view_menu = self.menu.addMenu('&View')
        self.tools_menu = self.menu.addMenu('&Tools')
        self.help_menu = self.menu.addMenu('&Help')

    def initMenuBar(self):
        # File tab submenus and actions
        exitAct = QAction("&Exit", self.appCtx)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.file_menu.addAction(exitAct)
        # menu.addAction(self.file_menu.menuAction())
        # self.view_menu.addAction(exitAct)
        # self.addAction(self.view_menu.menuAction())
        # TODO - Add more submenus and action for each of the menu tabs
        return self
