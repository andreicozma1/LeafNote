from Textbox import TextBox


class Document(TextBox):
    def __init__(self, min_width):
        super(TextBox, self).__init__()
        print("Created Document")

        self.setMinimumWidth(min_width)
        self.setBackgroundColor("white")
        self.setTextColorByString("black")
