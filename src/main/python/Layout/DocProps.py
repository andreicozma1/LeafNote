import logging

from PyQt5.QtCore import Qt

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
