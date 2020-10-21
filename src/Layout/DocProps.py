"""
holds the class with the document properties
"""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QColor


class DocProps:
    """
    class has the default document properties
    """

    # pylint: disable=too-few-public-methods

    def __init__(self):
        """
        the default properties for the document
        :return: returns nothing
        """
        logging.debug("Setting up Doc Props")

        # Font sizes available in the TopBar
        self.font_size_default = 12
        self.list_font_sizes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
                                "14", "15", "16",
                                "17", "18", "19", "20", "22", "24", "26", "28", "36", "48", "72"]

        # Colors available in the TopBar
        self.dict_colors = {
            'black': '#000000',
            'red': '#ff0000',
            'pink': '#ffc0cb',
            'orange': '#ffa500',
            'yellow': '#ffff00',
            'green': '#00ff00',
            'blue': '#0000ff',
            'violet': '#9400d3',
            'brown': '#a52a3a',
            'white': '#ffffff'
        }

        # Alignment options available in the TopBar and MenuBar
        self.dict_text_aligns = {
            'Left': Qt.AlignLeft,
            'Right': Qt.AlignRight,
            'Center': Qt.AlignCenter,
            'Justify': Qt.AlignJustify
        }

        # code works with makeTitleStyleBox in TopBar.py

        # Default style for normal text
        self.normal = QTextCharFormat()
        # Default style for title
        self.title = QTextCharFormat()
        self.title.setFontPointSize(26)
        # Default style for subtitle
        self.subtitle = QTextCharFormat()
        self.subtitle.setFontPointSize(15)
        self.subtitle.setForeground(QColor('darkgray'))
        # Default style for heading 1
        self.heading1 = QTextCharFormat()
        self.heading1.setFontPointSize(20)
        # Default style for heading 2
        self.heading2 = QTextCharFormat()
        self.heading2.setFontPointSize(16)
        # Default style for heading 3
        self.heading3 = QTextCharFormat()
        self.heading3.setFontPointSize(14)
        self.heading3.setForeground(QColor('gray'))
        # Default style for heading 4
        self.heading4 = QTextCharFormat()
        self.heading4.setFontPointSize(12)
        self.heading4.setForeground(QColor('darkgray'))
        self.text_update_title = "Update "
        self.text_reset_title = "Reset to Default"
        # creates dictionary to set the text format to the selected title style in the QComboBox
        self.dict_title_styles = {
            "Normal Text": self.normal,
            self.text_update_title + "Normal Text": None,
            "Title": self.title,
            self.text_update_title + "Title": None,
            "Subtitle": self.subtitle,
            self.text_update_title + "Subtitle": None,
            "Header 1": self.heading1,
            self.text_update_title + "Header 1": None,
            "Header 2": self.heading2,
            self.text_update_title + "Header 2": None,
            "Header 3": self.heading3,
            self.text_update_title + "Header 3": None,
            "Header 4": self.heading4,
            self.text_update_title + "Header 4": None,
            self.text_reset_title: None,
        }
