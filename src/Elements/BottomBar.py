from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget,QHBoxLayout, QLabel
from src.Elements.ColorWidget import Color


class BottomBar(QWidget):
    def __init__(self, *args, **kwargs):
        super(BottomBar, self).__init__(*args, **kwargs)
        self.horz = QHBoxLayout()
        self.setLayout(self.horz)
        self.horz.setContentsMargins(0, 0, 0, 0)

        self.l1 = QLabel("Word Count: 0")
        font = self.l1.font()
        font.setPointSize(12)
        self.l1.setFont(font)
        self.horz.addWidget(self.l1)
        self.l1.adjustSize()

        self.l2 = QLabel("Character Count: 0")
        font = self.l2.font()
        font.setPointSize(12)
        self.l2.setFont(font)
        self.horz.addWidget(self.l2)
        self.l2.adjustSize()
        #l1.setText("Word Count: ")
        #l1.setAlignment(Qt.AlignLeft)

        self.horz.addWidget(Color("red"))
        self.horz.addWidget(Color("blue"))
