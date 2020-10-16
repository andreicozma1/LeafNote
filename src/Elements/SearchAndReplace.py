from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from Elements.Replace import Replace
from Elements.Search import Search


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
        super(SearchAndReplace, self).__init__()
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

        """
        self.search.setVisible(False)
        self.replace.setVisible(False)
