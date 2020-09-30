import logging

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QTextEdit


# Class to hold and customize a QPlainTextEdit Widget
class TextBox(QTextEdit):
    def __init__(self, default_text: str = None):
        super(TextBox, self).__init__()
        logging.info(default_text)
        self.textColor = "black"

        if default_text is None:
            default_text = "You can type here."

        self.setText(default_text)
        self.setAutoFillBackground(True)

    # Set the background color of the QPlainTextEdit Widget
    def setBackgroundColor(self, color: str):
        logging.info(color)
        palette = self.palette()
        # Set color for window focused
        palette.setColor(QPalette.Active, QPalette.Base, QColor(color))
        # Set color for window out of focus
        palette.setColor(QPalette.Inactive, QPalette.Base, QColor(color))

        self.setPalette(palette)
        # self.setBackgroundVisible(False)

    def setTextColorByString(self, color: str):
        logging.info(color)
        palette = self.palette()
        palette.setColor(QPalette.Text, QColor(color))
        self.setPalette(palette)

    def updateTextBox(self, text: str = None):
        logging.info(text)

        if text is not None:
            self.setText(text)
