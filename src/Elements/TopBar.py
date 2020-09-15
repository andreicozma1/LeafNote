from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget,QHBoxLayout, QLabel, QFontDialog, QComboBox
from src.Elements.ColorWidget import Color


class TopBar(QWidget):
    def __init__(self, *args, **kwargs):
        super(TopBar, self).__init__(*args, **kwargs)
        self.horz = QHBoxLayout()
        self.horz.setContentsMargins(0, 0 , 0 , 0)
        self.setLayout(self.horz)
        self.horz.addWidget(Color("green"))

        company = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22",]

        self.combo = QComboBox(self)
        self.horz.addWidget(self.combo)
        self.combo.setGeometry(50,50,400,35)
        self.combo.addItems(company)
        self.combo.setCurrentIndex(11)

        self.horz.addWidget(Color("red"))
        self.horz.addWidget(Color("orange"))
        self.horz.addWidget(Color("yellow"))
        self.horz.addWidget(Color("green"))

        """self.l1 = QLabel("Word Count: 0")
        font = self.l1.font()
        font.setPointSize(8)
        self.l1.setFont(font)
       # self.horz.addWidget(self.l1)

        self.l2 = QLabel("Character Count: 0")
        font = self.l2.font()
        font.setPointSize(8)
        self.l2.setFont(font)
       # self.horz.addWidget(self.l2)

        #self.horz.addWidget(Color("red"))
       # self.horz.addWidget(Color("blue"))"""
