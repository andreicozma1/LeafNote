"""
this module holds a class containing a reminder for the user
"""
import html
from functools import partial

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class Reminder(QWidget):
    """
    This is the reminder node class. It contains each individually
    traits of a reminder to allow it to be added to the right bar.
    """

    def __init__(self, key, date_str, time_str, title_str, desc_str, on_delete):
        # noinspection PyCompatibility
        super().__init__()
        self.key = key
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setSpacing(0)

        widget_title = QWidget()
        horizontal_layout = QHBoxLayout(widget_title)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel(title_str)
        lbl_title.setStyleSheet("font-style: bold;")
        lbl_title.setWordWrap(True)
        horizontal_layout.addWidget(lbl_title)

        btn_exit = QPushButton(html.unescape("&times;"))
        btn_exit.setFixedWidth(33)
        btn_exit.clicked.connect(partial(on_delete, key))
        horizontal_layout.addWidget(btn_exit)

        self.vertical_layout.addWidget(widget_title)

        self.show_date = QLabel(date_str + " at " + time_str)
        lbl_title.setStyleSheet("font-style: italic;")
        self.show_date.setWordWrap(True)
        self.vertical_layout.addWidget(self.show_date)

        self.show_desc = QLabel(desc_str)
        self.show_desc.setWordWrap(True)
        self.vertical_layout.addWidget(self.show_desc)
