from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QPushButton
from PyQt5.Qt import Qt


class BottomBar(QWidget):
    def __init__(self, document):
        super(BottomBar, self).__init__()
        print("Bottom Bar - init")
        self.document = document

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(self.horizontal_layout)

        self.label_wc = QLabel("0 Words")
        font = self.label_wc.font()
        font.setPointSize(10)
        self.label_wc.setFont(font)
        self.horizontal_layout.addWidget(self.label_wc)

        self.label_cc = QLabel("0 Characters")
        font = self.label_cc.font()
        font.setPointSize(10)
        self.label_cc.setFont(font)
        self.horizontal_layout.addWidget(self.label_cc)

        self.horizontal_layout.addStretch()

        self.document.textChanged.connect(self.updateWordCount)
        self.document.textChanged.connect(self.updateCharCount)

        self.button_zoom_out = QPushButton("-", self)
        self.button_zoom_out.setFixedWidth(33)
        self.button_zoom_out.clicked.connect(self.onZoomOutClicked)
        self.horizontal_layout.addWidget(self.button_zoom_out)

        self.zoom_slider = QSlider(Qt.Horizontal, self)
        self.zoom_slider.setGeometry(30, 40, 200, 30)
        self.zoom_slider.valueChanged[int].connect(self.changeValue)
        self.horizontal_layout.addWidget(self.zoom_slider)

        self.button_zoom_out = QPushButton("+", self)
        self.button_zoom_out.setFixedWidth(33)
        self.button_zoom_out.clicked.connect(self.onZoomInClicked)
        self.horizontal_layout.addWidget(self.button_zoom_out)

    def updateWordCount(self):
        wordCount = 0
        if self.document.toPlainText() != '':
            wordCount = len(self.document.toPlainText().split())

        self.label_wc.setText(str(wordCount) + " Words")

    def updateCharCount(self):
        charCount = len(self.document.toPlainText()) - len(self.document.toPlainText().split(" ")) + 1
        self.label_cc.setText(str(charCount) + " Characters")

    def onZoomInClicked(self):
            self.document.zoomIn(+1)

    def onZoomOutClicked(self):
            self.document.zoomOut(+1)

    def changeValue(self, value):
        temp = value
        if value <= 50:
            self.document.zoomOut[+1]
        else:
            self.document.zoomIn[+1]
