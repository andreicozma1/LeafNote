from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QTextEdit


# Class to hold and customize a QPlainTextEdit Widget
class TextBox(QTextEdit):
    def __init__(self, textDefault=None):
        super(QTextEdit, self).__init__()

        print("TextBox - created")
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

    def getWordCount(self):
        wordCount = len(self.toPlainText().split(" "))
        print(wordCount)




