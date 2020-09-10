from Textbox import TextBox


class Document(TextBox):
    def __init__(self, minWidth):
        super(TextBox, self).__init__()
        print("Created Document")

        self.setMinimumWidth(minWidth)
        self.setBackgroundColor("white")
        self.setTextColorByString("black")
        self.setPlaceholderText("Welcome to your new Note Page, begin typing here.")
        self.textChanged.connect(self.getWordCount)
        self.textChanged.connect(self.getCharCount)


