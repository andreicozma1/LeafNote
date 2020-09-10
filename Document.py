from Textbox import TextBox


class Document(TextBox):
    def __init__(self, minWidth):
        super(TextBox, self).__init__()
        print("Created Document")

        self.setMinimumWidth(minWidth)
        self.setBackgroundColor("white")
        self.setTextColorByString("black")

