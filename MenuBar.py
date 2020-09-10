from PyQt5.QtGui import QActionEvent , QColor, QPalette
from PyQt5.QtWidgets import QMenuBar, qApp, QAction, QMenu


# Class to hold and customize a QPlainTextEdit Widget
class MenuBar(QMenuBar):
    def __init__(self):
        super(QMenuBar, self).__init__()
        self.file_menu = QMenu('&File', self)
        self.addMenu(self.file_menu)
        self.edit_menu = QMenu('&Edit', self)
        self.addMenu(self.edit_menu)
        self.view_menu = QMenu('&View', self)
        self.addMenu(self.view_menu)
        self.tools_menu = QMenu('&Tools', self)
        self.addMenu(self.tools_menu)
        self.help_menu = QMenu('&Help', self)
        self.addMenu(self.help_menu)


        self.initTopBar()

    def initTopBar(self):
        # File tab submenus and actions
        exitAct = QAction("&Exit")
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.file_menu.addAction(exitAct)
        self.addAction(self.file_menu.menuAction())
        # self.view_menu.addAction(exitAct)
        # self.addAction(self.view_menu.menuAction())
        # TODO - Add more submenus and action for each of the menu tabs
        return self
