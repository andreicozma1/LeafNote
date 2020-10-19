import logging
import os

from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QFileSystemModel, QTreeView

from Utils.Encryptor import Encryptor

"""
displays interactive directory on 
left side of text editor
"""


class DirectoryViewer(QTreeView):
    """
    displays a directory
    """

    def __init__(self, document, file_manager, path=None):
        """
        creates the directory display
        :param file_manager: instance of FileManager class - manages all file communication
        :param path: default path to file being displayed
        :return: returns nothing
        """
        super(DirectoryViewer, self).__init__()
        logging.debug("Creating Directory Viewer")

        self.document = document
        self.fileManager = file_manager

        if path is None:
            path = QDir.currentPath()

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

        self.fileManager.encryptor = None
        # Check for encryption key in Workspace
        path_key = os.path.join(path, ".leafCryptoKey")
        if os.path.exists(path_key):
            logging.debug("Encryption key found! " + path_key)
            with open(path_key, 'r') as f:
                key = f.read()
                self.fileManager.encryptor = Encryptor(key)
        else:
            logging.debug("Workspace not encrypted")

    def onDoubleClick(self, index):
        """
        functionality of double click on directory
        :param index: location of filePath
        :return: returns nothing
        """
        path = self.sender().model.filePath(index)
        logging.info(path)
        if not self.sender().model.isDir(index):
            self.fileManager.openDocument(self.document, path)
