from Elements.Textbox import TextBox


class Document(TextBox):
    def __init__(self):
        super(TextBox, self).__init__()
        print("Document - init")

        self.setBackgroundColor("white")
        self.setTextColorByString("black")
