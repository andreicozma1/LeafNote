import logging
import os

from PyQt5.Qt import Qt, QTimer, QIcon
from PyQt5.QtCore import QDateTime, QSettings, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QPushButton, QDialogButtonBox

from Widgets.Calendar import Calendar
from Utils.DialogBuilder import DialogBuilder

class BottomBar(QWidget):
    """
    BottomBar sets up the bottom bar when called in Main.py
    holds functionality and format of the the tools in
    the bottom bar
    """

    def __init__(self, app, document, settings: QSettings, path_res: str):
        """
        Creates the bottom bar
        :param document: the document the bottom bar will be altering
        :return: returns nothing
        """
        super(BottomBar, self).__init__()
        logging.debug("Creating Bottom Bar")
        self.app = app
        self.document = document
        self.settings = settings
        self.path_res = path_res

        # Sets up the layout of the bottom bar
        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.horizontal_layout.setSpacing(3)

        # Set global font size
        font_default = QFont()
        font_default.setPointSize(8)

        # Create Calendar Button
        path_calendar_icon = os.path.join(self.path_res, "calendar.ico")
        self.calendar = QPushButton("", self)
        self.calendar.setIcon(QIcon(path_calendar_icon))
        self.calendar.clicked.connect(self.showCalendar)
        self.horizontal_layout.addWidget(self.calendar)

        # Create date-time label
        self.label_time = QLabel()
        self.label_time.setFont(font_default)
        self.horizontal_layout.addWidget(self.label_time)
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)
        self.updateTime()

        self.horizontal_layout.addStretch()

        # Create Word Counter
        self.label_wc = QLabel("0 Words")
        self.label_wc.setFont(font_default)
        self.horizontal_layout.addWidget(self.label_wc)

        # Create Character Counter
        self.label_cc = QLabel("0 Characters")
        self.label_cc.setFont(font_default)
        self.horizontal_layout.addWidget(self.label_cc)

        self.horizontal_layout.addStretch()

        # functionality of word and character count
        self.document.textChanged.connect(self.updateWordCount)
        self.document.textChanged.connect(self.updateCharCount)

        # Zoom reset button
        self.button_zoom_reset = QPushButton("100%", self)
        self.button_zoom_reset.setFont(font_default)
        self.button_zoom_reset.setFixedWidth(40)
        self.button_zoom_reset.clicked.connect(self.resetZoom)
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
        logging.info("")
        self.zoom_slider.setValue(self.zoom_slider.value() + 5)
        self.changeValue()

    def onZoomOutClicked(self):
        """
        Setting the value of the slider calls the changeValue function to perform the appropriate calculations
        :return: returns nothing
        """
        logging.info("")
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
        logging.info("")
        self.zoom_slider.setValue(self.slider_start)

    def updateTime(self):
        """
        Updates current time displayed on current_time label
        :return: returns current time
        """
        datetime = QDateTime.currentDateTime()
        self.label_time.setText(datetime.toString(Qt.TextDate))

    def showCalendar(self):
        """
        Shows a calendar with current date
        :return: CalendarWidget()
        """
        logging.debug("Showing calendar")
        calendar = Calendar()

        setting_hint = "hints/showCalendarReminderHint"
        should_show_hint = not self.settings.contains(setting_hint) or self.settings.value(setting_hint) is True
        logging.info(setting_hint + ": " + str(should_show_hint))
        if should_show_hint:
            hint = DialogBuilder(calendar, "Setting Reminders", "Hint: Select a date to create a Reminder!")
            hint.addButtonBox(QDialogButtonBox(QDialogButtonBox.Ok))
            hint.show()
            self.settings.setValue(setting_hint, not should_show_hint)

        def onCalendarReminder():
            date: QDate = calendar.selectedDate()
            logging.info(date.toString("MM-dd-yyyy"))
            self.app.reminders.showDialog(calendar, False, date)

        calendar.selectionChanged.connect(onCalendarReminder)

        self.dialog = DialogBuilder()
        self.dialog.addWidget(calendar)
        self.dialog.layout().setContentsMargins(0, 0, 0, 0)
        self.dialog.setFixedHeight(400)
        self.dialog.show()
