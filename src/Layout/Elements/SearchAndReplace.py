"""
This module holds a widget that holds both the search file widget and replace file widget
"""

import logging

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from Layout.Utils.ReplaceDoc import Replace
from Layout.Utils.SearchDoc import Search


class SearchAndReplace(QWidget):
    """
    Widget hold the search and replace bars
    """

    def __init__(self, path_res, document):
        """
        initialize the widgets values
        :param path_res: the path to the resources
        :param document: the document
        """
        super().__init__()
        logging.debug("Creating Search and Replace")
        self.path_res = path_res
        self.document = document

        self.search = Search(self, self.document, self.path_res)
        self.replace = Replace(self, self.document)

        self.initUi()

    def initUi(self):
        """
        Sets up the layout
        :return: returns nothing
        """
        # create the layout of the widget
        self.vbox = QVBoxLayout(self)

        # set the color of the widget
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#dadada'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # set the
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(1)

        self.vbox.addWidget(self.search)
        self.vbox.addWidget(self.replace)

    def closeSearchAndReplace(self):
        """
        hides both search and replace widgets
        """
        self.search.setVisible(False)
        self.replace.setVisible(False)

    def nextOccurrence(self):
        """
        When enter is clicked replaces the current selection if the replace is isVisible
        If replace is not visible and search is visible move to the next occurrence
        """
        if self.replace.isVisible():
            self.replace.onReplace()
        elif self.search.isVisible():
            self.search.onNextOccurrenceSelect()
