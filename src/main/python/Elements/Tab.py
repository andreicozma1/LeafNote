import random
from PyQt5.QtCore import QDir
from os import path

from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QToolButton

from Elements.ColorWidget import Color

class Tab(Color):
    def __init__(self, tabBar, path: str):
        # Generate random color for the tab TODO: Change up to preference
        color = "#" + str(format(random.randint(0, 16777215), 'x'))
        super(Tab, self).__init__(color)
        print('Tab - init')
        self.tabBar = tabBar
        self.path = path
        self.f_name = QFileInfo(self.path).fileName()  # grab substring of just the file name w/o path for asthetic

        # create horizontal layout for the tab
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(10, 0, 0, 0)
        self.horizontal_layout.setSpacing(2)

        # add the file name to the tab
        self.label = QLabel(self.f_name)
        self.horizontal_layout.addWidget(self.label)

        self.horizontal_layout.addStretch()
        self.btn_close = QToolButton()
        self.btn_close.setText("x")
        self.btn_close.setToolTip("Close tab")
        self.btn_close.setContentsMargins(0, 0, 0, 0)
        self.btn_close.setStyleSheet("background-color: transparent; text-align: center; font-size: 14px")
        self.btn_close.released.connect(self.closeTab)
        self.horizontal_layout.addWidget(self.btn_close)

        self.setLayout(self.horizontal_layout)

    def closeTab(self):
        print("Tab - closeTab -", self.path)
        self.tabBar.closeTab(self)
