from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from Elements.ColorWidget import Color


class Tab(QWidget):
    def __init__(self, path: str):
        super(Tab, self).__init__()
        print('Tab - init')
        self.path = path
        self.f_name = ''  # grab substring of just the file name w/o path for asthetic

        # create horizontal layout for the tab
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.horizontal_layout.setSpacing(3)

        # set the widget properties
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QColor('red'))
        self.setPalette(palette)
        self.setFixedWidth(33)

        # add the file name to the tab
        self.tab_name = QLabel(self.f_name)
        self.horizontal_layout.addWidget(self.tab_name)

        # add the X icon to the tab
        # self.x = Color('red')
        # self.horizontal_layout.addWidget(self.x)


class OpenTabsBar(QWidget):
    def __init__(self, app):
        super(OpenTabsBar, self).__init__()
        self.app = app
        self.setFixedHeight(self.app.layout_props.bar_tabs_height)

        # crate the hbox layout
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.horizontal_layout.setSpacing(3)
        self.setLayout(self.horizontal_layout)

        # set the background
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('grey'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # (TESTING PURPOSE ONLY DELETE THIS CHUNK OF CODE AFTER DONE) Button press to make text strikethrough
        # self.button_strike = QPushButton("S", self)
        # self.button_strike.setToolTip('Strikeout your text. "Ctrl+S"')
        # self.button_strike.setShortcut('ctrl+s')
        # self.button_strike.setFixedWidth(33)
        # self.horizontal_layout.addWidget(self.button_strike)

        tmp_tab = Tab("tmp.txt")
        tmp_tab = Color('red')
        self.horizontal_layout.addWidget(tmp_tab)

        self.horizontal_layout.addStretch()

    # this will create a new tab and add it to the horizontal layout
    def addTab(self, path: str):
        print('OpenTabsBar - added tab -', path)

    def deleteTab(self, tab: Tab):
        self.app.file_manager.closeDocument(tab.path)


def grabFileName(path: QFileInfo):
    return path.fileName()
