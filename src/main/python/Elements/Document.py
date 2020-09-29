from Elements.Textbox import TextBox


class Document(TextBox):
    def __init__(self, layout):
        super(Document, self).__init__("")
        print("Document - init")

        self.layout = layout
        self.setBackgroundColor("white")
        self.setTextColorByString("black")
        self.setPlaceholderText("Start typing here...")
