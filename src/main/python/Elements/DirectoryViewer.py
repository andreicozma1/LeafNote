import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileSystemModel, QTreeView

import logging

"""
displays interactive directory on 
left side of text editor
"""


class DirectoryViewer(QTreeView):
    """
    displays a directory
    """

    def __init__(self, file_manager, path=None):
        """
        creates the directory display
        :param file_manager: instance of FileManager class - manages all file communication
        :param path: default path to file being displayed
        :return: returns nothing
        """
        super(DirectoryViewer, self).__init__()
        logging.info("")
        self.fileManager = file_manager

        if path is None:
            path = self.fileManager.app.app_props.mainPath

        self.model = QFileSystemModel()
        self.updateDirectory(path)

    def updateDirectory(self, path):
        """
        works on the visuals and functionality of as user navigates through the open directory
        :param path: default path to file being displayed
        :return: returns nothing
        """
        logging.info(path)

        self.model.setRootPath(path)

        self.setModel(self.model)
        self.setRootIndex(self.model.index(path))

        for i in range(1, self.model.columnCount()):
            self.hideColumn(i)

        # make these functionsPath.home()
        self.setAnimated(False)
        self.setIndentation(10)
        self.setSortingEnabled(True)
        self.sortByColumn(1, Qt.AscendingOrder)

        self.doubleClicked.connect(self.onDoubleClick)

    def onDoubleClick(self, index):
        """
        functionality of double click on directory
        :param index: location of filePath
        :return: returns nothing
        """
        path = self.sender().model.filePath(index)
        logging.info(path)
        if not self.sender().model.isDir(index):
            self.fileManager.openDocument(path)
