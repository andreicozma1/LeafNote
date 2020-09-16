from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from src.Elements.ColorWidget import Color


class BottomBar(QWidget):
    def __init__(self, *args, **kwargs):
        super(BottomBar, self).__init__(*args, **kwargs)
        self.horz = QHBoxLayout()
        self.horz.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.horz)

        self.l1 = QLabel("0 Words")
        font = self.l1.font()
        font.setPointSize(8)
        self.l1.setFont(font)
        self.l1.adjustSize()
        self.horz.addWidget(self.l1)

        self.l2 = QLabel("0 Characters")
        font = self.l2.font()
        font.setPointSize(8)
        self.l2.setFont(font)
        self.l2.adjustSize()
        self.horz.addWidget(self.l2)

        self.horz.addWidget(Color("transparent"))
        self.horz.addWidget(Color("transparent"))
        self.horz.addWidget(Color("transparent"))
