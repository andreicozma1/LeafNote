"""
This module holds a class defining a tab that is held in an open tabs bar
"""
import logging
import random

from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QToolButton

from Widgets.ColorWidget import Color


class Tab(Color):
    """
    sets up the file as a tab
    """

    def __init__(self, tab_bar, path: str):
        """
        creates a tab for specific file
        :param tab_bar: bar where the tabs will be stored
        :param path: path to file being displayed
        :return: returns nothing
        """
        color = "#" + str(format(random.randint(0, 16777215), 'x'))
        super().__init__(color)
        logging.debug("Creating Tab")

        self.tab_bar = tab_bar
        self.path = path
        self.f_name = QFileInfo(self.path).fileName()
        # grab substring of just the file name w/o path for asthetic

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
        self.btn_close.setStyleSheet(
            "background-color: transparent; text-align: center; font-size: 14px")
        self.btn_close.released.connect(self.closeTab)
        self.horizontal_layout.addWidget(self.btn_close)

        self.setLayout(self.horizontal_layout)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        opens file of the path that the tab is holding
        :QMouseEvent: registers the mouse click
        :return: returns nothing
        """
        logging.info(self.path)
        self.tab_bar.openTab(self)
        super().mouseReleaseEvent(event)

    def closeTab(self):
        """
        close out tab when called
        :return: returns nothing
        """
        logging.info(self.path)
        self.tab_bar.closeTab(self.path)
