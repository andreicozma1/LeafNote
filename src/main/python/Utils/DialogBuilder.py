from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QLabel, QDialogButtonBox


class DialogBuilder(QDialog):
    def __init__(self, blocks, winTitle: str = None, titleText: str = None, msgText: str = None):
        super(DialogBuilder, self).__init__(blocks)

        if winTitle is None:
            winTitle = "Dialog"

        self.setWindowTitle(winTitle)

        self.vertical_layout = QVBoxLayout(self)
        self.title = QLabel(titleText)
        font = self.title.font()
        font.setPointSize(18)
        font.setBold(True)
        self.title.setFont(font)
        self.message = QLabel(msgText)
        self.vertical_layout.addWidget(self.title)
        self.vertical_layout.addWidget(self.message)

    def setTitleText(self, text: str):
        self.title.setText(text)

    def setMsgText(self, text: str):
        self.message.setText(text)

    def addWidget(self, widget: QWidget):
        self.vertical_layout.addWidget(widget)

    def addButtonBox(self, buttonBox: QDialogButtonBox):
        self.vertical_layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
