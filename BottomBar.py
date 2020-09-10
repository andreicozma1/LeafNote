from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from ColorWidget import Color


class BottomBar(QWidget):
    def __init__(self, *args, **kwargs):
        super(BottomBar, self).__init__(*args, **kwargs)
        self.horz = QHBoxLayout()
        self.setLayout(self.horz)
        self.horz.addWidget(Color("red"))
        self.horz.addWidget(Color("blue"))
        self.horz.addWidget(Color("green"))
        self.horz.addWidget(Color("yellow"))