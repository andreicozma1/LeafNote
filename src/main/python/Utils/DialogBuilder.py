from PyQt5.QtWidgets import QDialog, QVBoxLayout,QWidget


class DialogBuilder(QDialog):
    def __init__(self, title):
        super(DialogBuilder, self).__init__()

        if title is None:
            title = "Dialog"

        self.setWindowTitle(title)

        self.vertical_layout = QVBoxLayout(self)

        self.exec()

    def addWidget(self, widget:QWidget):
        self.vertical_layout.addWidget(widget)
