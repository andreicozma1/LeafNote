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

        # color dictionary for changing text color
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

        # List for font sizes
        self.list_FontSize = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
                              "17", "18", "19", "20", "22", "24", "26", "28", "36", "48", "72"]
        self.list_alignments = ["Left", "Right", "Center", " Justify"]
        self.list_alignments_align = [Qt.AlignLeft, Qt.AlignRight, Qt.AlignCenter, Qt.AlignJustify]
