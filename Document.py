from PyQt5.QtGui import QPalette, QColor

from Textbox import TextBox


class Document(TextBox):
    def __init__(self, minWidth, textDefault=None):
        super(TextBox, self).__init__()
        print("Created Document")

        self.setMinimumWidth(minWidth)
        self.setBackgroundColor("white")
        self.setTextColorByString("black")
