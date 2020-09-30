from PyQt5.QtGui import QFont

from Elements.TextBox import TextBox


class Document(TextBox):
    def __init__(self):
        super(Document, self).__init__("")
        print("Document - init")

        self.setBackgroundColor("white")
        self.setTextColorByString("black")
        self.setPlaceholderText("Start typing here...")

    # Sets the font to italic
    def onFontItalChanged(self, state):
        print('TopBar - onFontItalChanged -', state)
        self.setFontItalic(state)

    # Sets the font to bold
    def onFontBoldChanged(self, state):
        print('TopBar - onFontBoldChanged -', QFont.Bold if state else QFont.Normal)
        self.setFontWeight(QFont.Bold if state else QFont.Normal)

    # Sets the font to underlined
    def onFontUnderChanged(self, state):
        print('TopBar - onFontUnderChanged -', state)
        self.setFontUnderline(state)

    # Sets the font to strike
    def onFontStrikeChanged(self, state):
        print('TopBar - onFontUnderChanged -', state)
        fontFormat = self.currentCharFormat()
        fontFormat.setFontStrikeOut(state)
        self.setCurrentCharFormat(fontFormat)

    def resetFormatting(self):
        self.onFontUnderChanged(False)
        self.onFontItalChanged(False)
        self.onFontBoldChanged(False)
        self.onFontStrikeChanged(False)

