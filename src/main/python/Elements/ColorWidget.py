from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget

"""
hold class Color
"""


class Color(QWidget):
    """
    used as place holder for layout of the text editor
    """
    def __init__(self, color: str):
        """
        set color of new widget created
        :param color: the color widget will be set to
        :return: returns nothing
        """
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)
