import logging

from PyQt5.Qt import Qt, QTime, QTimer
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QPushButton, QVBoxLayout
from PyQt5.QtCore import QDate, QDateTime


"""
This file alters tools on the Bottom Bar
of the text editor.
    This includes:
        Word count
        Character count
        Zoom feature
"""


class BottomBar(QWidget):
    """
    BottomBar sets up the bottom bar when called in Main.py
    holds functionality and format of the the tools in
    the bottom bar
    """

    def __init__(self, document):
        """
        Creates the bottom bar
        :param document: the document the bottom bar will be altering
        :return: returns nothing
        """
        super(BottomBar, self).__init__()
        logging.info("")
        self.document = document

        # sets up the bottom bar
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(self.horizontal_layout)

        datetime = QDateTime.currentDateTime()
        self.current_time = QPushButton(datetime.toString(Qt.DefaultLocaleShortDate), self)
        self.horizontal_layout.addWidget(self.current_time)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        # sets default settings for word counter
        self.label_wc = QLabel("0 Words")
        font = self.label_wc.font()
        font.setPointSize(10)
        self.label_wc.setFont(font)
        self.horizontal_layout.addWidget(self.label_wc)

        # sets default settings for character counter
        self.label_cc = QLabel("0 Characters")
        font = self.label_cc.font()
        font.setPointSize(10)
        self.label_cc.setFont(font)
        self.horizontal_layout.addWidget(self.label_cc)

        self.horizontal_layout.addStretch()

        # functionality of word and character count
        self.document.textChanged.connect(self.updateWordCount)
        self.document.textChanged.connect(self.updateCharCount)

        # Zoom reset button
        self.button_zoom_reset = QPushButton("100%", self)
        self.button_zoom_reset.setFixedWidth(40)
        self.button_zoom_reset.clicked.connect(self.resetZoom)
        self.button_zoom_reset.setStyleSheet("QPushButton { font-size: 6pt; }")
        self.button_zoom_reset.setToolTip("Resets zoom to default 100%")
        self.horizontal_layout.addWidget(self.button_zoom_reset)

        # Zoom Out button
        self.button_zoom_out = QPushButton("-", self)
        self.button_zoom_out.setFixedWidth(33)
        self.button_zoom_out.clicked.connect(self.onZoomOutClicked)
        self.button_zoom_out.setAutoRepeat(True)
        self.button_zoom_out.setToolTip("Zoom out")
        self.horizontal_layout.addWidget(self.button_zoom_out)

        # Zoom Slider
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

        # Zoom in button
        self.button_zoom_in = QPushButton("+", self)
        self.button_zoom_in.setFixedWidth(33)
        self.button_zoom_in.clicked.connect(self.onZoomInClicked)
        self.button_zoom_in.setAutoRepeat(True)
        self.button_zoom_in.setToolTip("Zoom in")
        self.horizontal_layout.addWidget(self.button_zoom_in)


    def updateWordCount(self):
        """
        Counts number of words and updates number on bottom bar
        :return: returns nothing
        """
        word_count = 0
        if self.document.toPlainText() != '':
            word_count = len(self.document.toPlainText().split())

        self.label_wc.setText(str(word_count) + " Words")

    def updateCharCount(self):
        """
        Counts number of characters and updates number on bottom bar
        :return: returns nothing
        """
        char_count = len(self.document.toPlainText()) - len(self.document.toPlainText().split(" ")) + 1
        self.label_cc.setText(str(char_count) + " Characters")

    def onZoomInClicked(self):
        """
        Setting the value of the slider calls the changeValue function to perform the appropriate calculations
        :return: returns nothing
        """
        self.zoom_slider.setValue(self.zoom_slider.value() + 5)
        self.changeValue()

    def onZoomOutClicked(self):
        """
        Setting the value of the slider calls the changeValue function to perform the appropriate calculations
        :return: returns nothing
        """
        self.zoom_slider.setValue(self.zoom_slider.value() - 5)
        self.changeValue()

    def changeValue(self):
        """
        changes the font size of the document to match the desired zoom preference
        :return: returns nothing
        """
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
        """
        resets the zoom slider when zoom is reset
        :return: returns nothing
        """
        self.zoom_slider.setValue(self.slider_start)

    def showTime(self):
        """
        Updates current time displayed on current_time label
        :return: returns current time
        """
        datetime = QDateTime.currentDateTime()
        self.current_time.setText(datetime.toString(Qt.DefaultLocaleShortDate))