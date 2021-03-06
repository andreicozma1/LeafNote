"""
holds class Color
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget


class ColorWidget(QWidget):
    """
    used as place holder for layout of the text editor
    """

    def __init__(self, color: str):
        """
        set color of new widget created
        :param color: the color widget will be set to
        :return: returns nothing
        """
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)
