from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget,QHBoxLayout, QLabel
from ColorWidget import Color


class BottomBar(QWidget):
    def __init__(self, *args, **kwargs):
        super(BottomBar, self).__init__(*args, **kwargs)
        self.horz = QHBoxLayout()
        self.setLayout(self.horz)

        self.l1 = QLabel("Word Count: 0")
        font = self.l1.font()
        font.setPointSize(8)
        self.l1.setFont(font)
        self.horz.addWidget(self.l1)

        self.l2 = QLabel("Character Count: 0")
        font = self.l2.font()
        font.setPointSize(8)
        self.l2.setFont(font)
        self.horz.addWidget(self.l2)
        #l1.setText("Word Count: ")
        #l1.setAlignment(Qt.AlignLeft)

        self.horz.addWidget(Color("red"))
        self.horz.addWidget(Color("blue"))
