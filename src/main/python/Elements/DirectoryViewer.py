from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileSystemModel, QTreeView
import logging

# Class to display a directory
class DirectoryViewer(QTreeView):
    def __init__(self, fileManager, path=None):
        super(DirectoryViewer, self).__init__()
        logging.info("")
        self.fileManager = fileManager

        if path is None:
            path = self.fileManager.app.app_props.mainPath

        self.model = QFileSystemModel()
        self.updateDirectory(path)

    def updateDirectory(self, path):
        logging.info(path)

        self.model.setRootPath(path)

        self.setModel(self.model)
        self.setRootIndex(self.model.index(path))

        for i in range(1, self.model.columnCount()):
            self.hideColumn(i)

        # make these functionsPath.home(
        self.setAnimated(False)
        self.setIndentation(10)
        self.setSortingEnabled(True)
        self.sortByColumn(1, Qt.AscendingOrder)

        self.doubleClicked.connect(self.onDoubleClick)

    def onDoubleClick(self, index):
        path = self.sender().model.filePath(index)
        logging.info(path)
        if not self.sender().model.isDir(index):
            self.fileManager.openDocument(path)
