"""
this module holds a class containing a reminder for the user
"""
import html
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class Reminder(QWidget):
    """
    This is the reminder node class. It contains each individually
    traits of a reminder to allow it to be added to the right bar.
    """

    def __init__(self, key, date_str, time_str, title_str, desc_str, on_delete):
        super().__init__()
        vertical_layout = QVBoxLayout(self)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.setSpacing(0)

        widget_title = QWidget()
        horizontal_layout = QHBoxLayout(widget_title)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel(html.unescape("&#8226;") + " " + title_str)
        lbl_title.setStyleSheet("font-weight: bold;")
        lbl_title.setWordWrap(True)
        lbl_title.setTextInteractionFlags(Qt.TextSelectableByMouse)
        horizontal_layout.addWidget(lbl_title)

        btn_exit = QPushButton(html.unescape("&times;"))
        btn_exit.setFixedWidth(33)
        btn_exit.clicked.connect(partial(on_delete, key))
        horizontal_layout.addWidget(btn_exit)

        vertical_layout.addWidget(widget_title)

        show_date = QLabel(f'{date_str} at {time_str}')
        show_date.setStyleSheet("font-style: italic; margin-left: 5px;")
        show_date.setWordWrap(True)
        show_date.setTextInteractionFlags(Qt.TextSelectableByMouse)
        vertical_layout.addWidget(show_date)

        show_desc = QLabel(desc_str)
        show_desc.setStyleSheet("margin-left: 5px;")
        show_desc.setWordWrap(True)
        show_desc.setTextInteractionFlags(Qt.TextSelectableByMouse)
        vertical_layout.addWidget(show_desc)
