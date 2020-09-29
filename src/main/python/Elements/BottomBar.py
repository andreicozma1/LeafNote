import math

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QPushButton


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
        self.button_zoom_out.setAutoRepeat(True)
        self.button_zoom_out.setToolTip("Zoom out")
        self.horizontal_layout.addWidget(self.button_zoom_out)

        self.zoom_slider = QSlider(Qt.Horizontal, self)
        self.zoom_slider.setGeometry(30, 40, 200, 30)
        self.zoom_slider.setFixedWidth(140)
        self.zoom_slider.setMinimum(-50)
        self.zoom_slider.setMaximum(50)
        # Calculate the middle of the scale
        self.slider_start = 0
        # Set the default position to the middle of the slider
        self.zoom_slider.setValue(self.slider_start)
        # The default font size corresponds to the default position (middle)
        self.default_font_size = self.document.font().pointSize()
        self.zoom_slider.valueChanged[int].connect(self.changeValue)
        self.horizontal_layout.addWidget(self.zoom_slider)

        self.button_zoom_in = QPushButton("+", self)
        self.button_zoom_in.setFixedWidth(33)
        self.button_zoom_in.clicked.connect(self.onZoomInClicked)
        self.button_zoom_in.setAutoRepeat(True)
        self.button_zoom_in.setToolTip("Zoom in")
        self.horizontal_layout.addWidget(self.button_zoom_in)

    def updateWordCount(self):
        wordCount = 0
        if self.document.toPlainText() != '':
            wordCount = len(self.document.toPlainText().split())

        self.label_wc.setText(str(wordCount) + " Words")

    def updateCharCount(self):
        charCount = len(self.document.toPlainText()) - len(self.document.toPlainText().split(" ")) + 1
        self.label_cc.setText(str(charCount) + " Characters")

    def onZoomInClicked(self):
        # Setting the value of the slider calls the changeValue function to perform the appropriate calculations
        self.zoom_slider.setValue(self.zoom_slider.value() + 5)
        self.changeValue()

    def onZoomOutClicked(self):
        # Setting the value of the slider calls the changeValue function to perform the appropriate calculations
        self.zoom_slider.setValue(self.zoom_slider.value() - 5)
        self.changeValue()


    def changeValue(self):
        min_rel_font_size = 2
        max_rel_font_size = 150
        default_rel_font_size = self.default_font_size

        # reset zoom to default
        self.document.zoomIn(self.default_font_size - self.document.font().pointSize())
        curr_val = self.zoom_slider.value()
        max_zoom = self.zoom_slider.maximum()

        # if the zoom bar is on the negative side:
        if curr_val < 0:
            delta_zoom = (curr_val / max_zoom) * (default_rel_font_size - min_rel_font_size)

        # if the zoom bar is on the positive side
        else:
            delta_zoom = (curr_val / max_zoom) * (max_rel_font_size - default_rel_font_size)

        self.document.zoomIn(int(delta_zoom))

    def resetZoom(self):
        self.zoom_slider.setValue(self.slider_start)
