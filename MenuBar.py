from PyQt5.QtGui import QActionEvent , QColor, QPalette
from PyQt5.QtWidgets import QMenuBar, qApp, QAction


# Class to hold and customize a QPlainTextEdit Widget
class MenuBar(QMenuBar):
    def __init__(self):
        super(QMenuBar, self).__init__()
        self.file = self.addMenu('&File')
        self.edit = self.addMenu('&Edit')
        self.view = self.addMenu('&View')
        self.tools = self.addMenu('&Tools')
        self.help = self.addMenu('&Help')

    def initTopBar(self):
        # File tab submenus and actions
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.file.addAction(exitAct)

        # TODO - Add more submenus and action for each of the menu tabs
        return self
