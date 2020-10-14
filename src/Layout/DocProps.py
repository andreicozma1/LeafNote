import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QColor

"""
holds the class with the document properties
"""


class DocProps():
    """
    class has the default document properties
    """

    def __init__(self):
        """
        the default properties for the document
        :return: returns nothing
        """
        logging.info("Setting up Document Properties")

        # Font sizes available in the TopBar
        self.list_FontSize = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
                              "17", "18", "19", "20", "22", "24", "26", "28", "36", "48", "72"]

        # Colors available in the TopBar
        self.color_dict = {
            'black': '#000000',
            'red': '#ff0000',
            'pink': '#ffc0cb',
            'orange': '#ffa500',
            'yellow': '#ffff00',
            'green': '#00ff00',
            'blue': '#0000ff',
            'violet': '#9400D3',
            'brown': '#a52a3a',
            'white': '#ffffff'
        }

        # Alignment options available in the TopBar and MenuBar
        self.dict_align = {
            'Left': Qt.AlignLeft,
            'Right': Qt.AlignRight,
            'Center': Qt.AlignCenter,
            'Justify': Qt.AlignJustify
        }

        normal = QTextCharFormat()

        title = QTextCharFormat()
        title.setFontPointSize(26)

        subtitle = QTextCharFormat()
        subtitle.setFontPointSize(15)
        subtitle.setForeground(QColor('darkgray'))

        heading1 = QTextCharFormat()
        heading1.setFontPointSize(20)

        heading2 = QTextCharFormat()
        heading2.setFontPointSize(16)

        heading3 = QTextCharFormat()
        heading3.setFontPointSize(14)
        heading3.setForeground(QColor('gray'))

        heading4 = QTextCharFormat()
        heading4.setFontPointSize(12)
        heading4.setForeground(QColor('darkgray'))

        self.dict_title_style = {}
        self.dict_title_style["Normal text"] = normal
        self.dict_title_style["Title"] = title
        self.dict_title_style["Subtitle"] = subtitle
        self.dict_title_style["Header 1"] = heading1
        self.dict_title_style["Header 2"] = heading2
        self.dict_title_style["Header 3"] = heading3
        self.dict_title_style["Header 4"] = heading4
