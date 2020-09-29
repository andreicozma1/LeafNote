from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QLabel, QDialogButtonBox


class DialogBuilder(QDialog):
    def __init__(self, blocked_widget, text_window: str = None, text_title: str = None, text_msg: str = None):
        super(DialogBuilder, self).__init__(blocked_widget)

        if text_window is None:
            text_window = "Dialog"

        self.setWindowTitle(text_window)
        self.layout_vertical = QVBoxLayout(self)
        self.label_title = QLabel(text_title)
        self.label_message = QLabel(text_msg)

        self.setup()

    def setup(self):
        font = self.label_title.font()
        font.setPointSize(18)
        font.setBold(True)
        self.label_title.setFont(font)

        self.layout_vertical.addWidget(self.label_title)
        self.layout_vertical.addWidget(self.label_message)

    def setTitleText(self, text: str):
        self.label_title.setText(text)

    def setMsgText(self, text: str):
        self.label_message.setText(text)

    def addWidget(self, widget: QWidget):
        self.layout_vertical.addWidget(widget)

    def addButtonBox(self, button_box: QDialogButtonBox):
        self.layout_vertical.addWidget(button_box)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
