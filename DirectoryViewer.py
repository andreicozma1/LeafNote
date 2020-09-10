from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QTextEdit, QFileSystemModel, QTreeView, QWidget
from pathlib import Path


# Class to display a directory
class DirectoryViewer(QTreeView):
    def __init__(self, rootPath=None):
        super(QTreeView, self).__init__()
        self.model = QFileSystemModel()
        if rootPath is None:
            rootPath = str(Path.home())
            print(rootPath)
        self.model.setRootPath(rootPath)
        # self.treeView = QTreeView()
        self.setModel(self.model)

        # make these functions
        self.setAnimated(False)
        self.setIndentation(10)
        self.setSortingEnabled(True)

    # TODO - link a click on the direcectory viewer to open the clicked file
    def onClicked(self, index):
        path = self.sender().model.filePath(index)
        print(path)
