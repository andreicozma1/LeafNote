from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QFileSystemModel, QTreeView


# Class to display a directory
class DirectoryViewer(QTreeView):
    def __init__(self, rootPath=None):
        super(QTreeView, self).__init__()

        if rootPath is None:
            rootPath = QDir.currentPath()

        self.model = QFileSystemModel()
        self.model.setRootPath(rootPath)

        self.setModel(self.model)
        self.setRootIndex(self.model.index(rootPath))

        for i in range(1, self.model.columnCount()):
            self.hideColumn(i)

        # make these functions
        self.setAnimated(False)
        self.setIndentation(10)
        self.setSortingEnabled(True)
        self.sortByColumn(1, Qt.AscendingOrder)

    # TODO - link a click on the directory viewer to open the clicked file
    def onClicked(self, index):
        path = self.sender().model.filePath(index)
        print(path)
