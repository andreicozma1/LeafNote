from src.Elements.Textbox import TextBox


class Document(TextBox):
    def __init__(self, bottom_bar):
        super(TextBox, self).__init__()
        print("Document - init")

        self.bottom_bar = bottom_bar
        self.setBackgroundColor("white")
        self.setTextColorByString("black")
        self.setPlaceholderText("Start typing here...")
        self.textChanged.connect(self.getWordCount)
        self.textChanged.connect(self.getCharCount)

    def getWordCount(self):
        wordCount = len(self.toPlainText().split())
        if self.toPlainText() == '':
            wordCount = 0
        self.bottom_bar.l1.setText(str(wordCount) + " Words")
        return wordCount

    def getCharCount(self):
        charCount = len(self.toPlainText()) - len(self.toPlainText().split(" ")) + 1
        self.bottom_bar.l2.setText(str(charCount) + " Characters")
        return charCount

