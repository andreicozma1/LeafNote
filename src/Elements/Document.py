from src.Elements.Textbox import TextBox


class Document(TextBox):
    def __init__(self, bottom_bar):
        super(TextBox, self).__init__()
        print("Document - init")

        self.bottom_bar = bottom_bar
        self.setBackgroundColor("white")
        self.setTextColorByString("black")
        self.setPlaceholderText("Start typing here...")
        self.textChanged.connect(self.updateWordCount)
        self.textChanged.connect(self.updateWordCount)

    def updateWordCount(self):
        wordCount = len(self.toPlainText().split())
        if self.toPlainText() == '':
            wordCount = 0
        self.bottom_bar.label_wc.setText(str(wordCount) + " Words")

    def updateWordCount(self):
        charCount = len(self.toPlainText()) - len(self.toPlainText().split(" ")) + 1
        self.bottom_bar.label_cc.setText(str(charCount) + " Characters")