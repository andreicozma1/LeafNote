from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QTextEdit, QFileSystemModel, QTreeView


# Class to hold and customize a QPlainTextEdit Widget
class DirectoryViewer(QTreeView):
    def __init__(self, rootPath=''):
        super(QTreeView, self).__init__()
        self.model = QFileSystemModel()
        self.model.setRootPath(rootPath)
        self.setModel(self.model)

        # make these functions
        self.setAnimated(False)
        self.setIndentation(10)
        self.setSortingEnabled(True)

