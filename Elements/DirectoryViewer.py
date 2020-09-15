from PyQt5.QtCore import QDir, Qt, QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QTreeView


# Class to display a directory
class DirectoryViewer(QTreeView):
    def __init__(self, fileManager, path=None):
        super(QTreeView, self).__init__()
        print("DirectoryViewer - init - ", path)
        self.fileManager = fileManager

        if path is None:
            path = QDir.currentPath()

        self.model = QFileSystemModel()
        self.updateDirectory(path)

    def updateDirectory(self, path):
        print("DirectoryViewer - updateDirectory - ", path)

        self.model.setRootPath(path)

        self.setModel(self.model)
        self.setRootIndex(self.model.index(path))

        for i in range(1, self.model.columnCount()):
            self.hideColumn(i)

        # make these functions
        self.setAnimated(False)
        self.setIndentation(10)
        self.setSortingEnabled(True)
        self.sortByColumn(1, Qt.AscendingOrder)

        self.doubleClicked.connect(self.onDoubleClick)


    # TODO - link a click on the directory viewer to open the clicked file
    def onDoubleClick(self, index):
        path = self.sender().model.filePath(index)
        print("DirectoryViewer - onDoubleClick -", path)
        if not self.sender().model.isDir(index):
            self.fileManager.openDocument(path)



