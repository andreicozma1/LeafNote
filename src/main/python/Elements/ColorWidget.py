from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget


class Color(QWidget):
    def __init__(self, color: str):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)
