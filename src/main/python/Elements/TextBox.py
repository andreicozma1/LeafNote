import logging

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QTextEdit

"""
all properties and set of of text box
"""


class TextBox(QTextEdit):
    """
    Class to hold and customize a QPlainTextEdit Widget
    """

    def __init__(self, default_text: str = None):
        """
        creates the text box
        :param default_text: text that will be in the text box after creation
        :return: returns nothing
        """
        super(TextBox, self).__init__()
        logging.info(default_text)
        self.textColor = "black"

        if default_text is None:
            default_text = "You can type here."

        self.setText(default_text)
        self.setAutoFillBackground(True)

    def setBackgroundColor(self, color: str):
        """
        Set the background color of the QPlainTextEdit Widget
        :param color: color the background will be set to
        :return: returns nothing
        """
        logging.info(color)
        palette = self.palette()
        # Set color for window focused
        palette.setColor(QPalette.Active, QPalette.Base, QColor(color))
        # Set color for window out of focus
        palette.setColor(QPalette.Inactive, QPalette.Base, QColor(color))

        self.setPalette(palette)
        # self.setBackgroundVisible(False)

    def setTextColorByString(self, color: str):
        """
        sets the text box to designated color
        :param color: color the text box will be set to
        :return: return nothing
        """
        logging.info(color)
        palette = self.palette()
        palette.setColor(QPalette.Text, QColor(color))
        self.setPalette(palette)

    def updateTextBox(self, text: str = None):
        """
        adds text to the text box
        :param text: text to be added
        :return: returns nothing
        """
        logging.info(text)

        if text is not None:
            self.setText(text)
