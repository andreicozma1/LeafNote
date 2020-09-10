from PyQt5.QtGui import QPalette, QColor

from Textbox import TextBox


class Document(TextBox):
    def __init__(self, minWidth, textDefault=None):
        super(TextBox, self).__init__()
        print("Created Document")

        self.setMinimumWidth(minWidth)
        self.setBackgroundColor("white")
        self.setTextColorByString("black")

        if textDefault is None:
            textDefault = "You can type here."
        print("TextBox - text: ", textDefault)

        self.setPlainText(textDefault)
        self.setAutoFillBackground(True)

    # Set the background color of the QPlainTextEdit Widget
    def setBackgroundColor(self, color):
        palette = self.palette()
        # Set color for window focused
        palette.setColor(QPalette.Active, QPalette.Base, QColor(color))
        # Set color for window out of focus
        palette.setColor(QPalette.Inactive, QPalette.Base, QColor(color))

        self.setPalette(palette)
        # self.setBackgroundVisible(False)

    def setTextColorByString(self, color):
        self.setTextColor(QColor(color))

