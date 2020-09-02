from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QPlainTextEdit


# Class to hold and customize a QPlainTextEdit Widget
class PlainTextEdit(QPlainTextEdit):
    def __init__(self, plain_text=None):
        super(QPlainTextEdit, self).__init__()
        if plain_text is None:
            plain_text = "You can type here."
        self.setPlainText(plain_text)
        self.setAutoFillBackground(True)

    # Set the background color of the QPlainTextEdit Widget
    def setBackgroundColor(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Active, QPalette.Base, QColor(color))
        self.setPalette(palette)
        self.setBackgroundVisible(False)

