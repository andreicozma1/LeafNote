"""
This module holds a class that displays various information to the user about the document
on the bottom of the application.
"""
import logging
import os

from PyQt5.Qt import Qt, QTimer, QIcon
from PyQt5.QtCore import QDateTime, QSettings, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QPushButton, QDialogButtonBox

from Utils.DialogBuilder import DialogBuilder
from Widgets.Calendar import Calendar


class BottomBar(QWidget):
    """
    BottomBar sets up the bottom bar when called in Main.py
    holds functionality and format of the the tools in
    the bottom bar
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, app, document, settings: QSettings, path_res: str):
        """
        Creates the bottom bar
        :param document: the document the bottom bar will be altering
        :return: returns nothing
        """
        super().__init__()
        logging.debug("Creating Bottom Bar")
        # save each parameter
        self.app = app
        self.document = document
        self.settings = settings
        self.path_res = path_res

        # initialize each globally used widget
        self.label_time = None
        self.label_wc = None
        self.label_cc = None
        self.zoom_slider = None

        # set the defaults for the zoom slider
        self.default_font_size = self.document.font().pointSize()
        self.slider_start = 0

        # set up the layout
        self.initUI()

    def initUI(self):
        """
        Create the layout of the widget
        :return: Returns nothing
        """
        # Sets up the layout of the bottom bar
        horizontal_layout = QHBoxLayout(self)
        horizontal_layout.setContentsMargins(10, 0, 10, 0)
        horizontal_layout.setSpacing(3)

        # Set global font size
        font_default = QFont()
        font_default.setPointSize(8)

        # Create Calendar Button
        path_calendar_icon = os.path.join(self.path_res, "calendar.ico")
        calendar = QPushButton("", self)
        calendar.setIcon(QIcon(path_calendar_icon))
        calendar.clicked.connect(self.showCalendar)
        horizontal_layout.addWidget(calendar)

        def createBottomBarLabel(title, font):
            label = QLabel(title)
            label.setFont(font)
            return label

        # Create date-time label
        self.label_time = createBottomBarLabel('', font_default)
        horizontal_layout.addWidget(self.label_time)
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)
        self.updateTime()

        horizontal_layout.addStretch()

        # Create Word Counter
        self.label_wc = createBottomBarLabel('0 Words', font_default)
        horizontal_layout.addWidget(self.label_wc)

        # Create Character Counter
        self.label_cc = createBottomBarLabel('0 Characters', font_default)
        horizontal_layout.addWidget(self.label_cc)

        horizontal_layout.addStretch()

        # functionality of word and character count
        self.document.textChanged.connect(self.updateWordCount)
        self.document.textChanged.connect(self.updateCharCount)

        def createZoomPushButton(title, width, signal, tool_tip):
            btn = QPushButton(title)
            btn.setFixedWidth(width)
            btn.setToolTip(tool_tip)
            btn.clicked.connect(signal)
            return btn

        # Zoom reset button
        button_zoom_reset = createZoomPushButton('100%', 40, self.resetZoom,
                                                 'Resets zoom to default 100%')
        button_zoom_reset.setFont(font_default)
        horizontal_layout.addWidget(button_zoom_reset)

        # Zoom Out button
        button_zoom_out = createZoomPushButton('-', 33, self.onZoomOutClicked,
                                               'Zoom out')
        button_zoom_out.setAutoRepeat(True)
        horizontal_layout.addWidget(button_zoom_out)

        # Zoom Slider
        self.zoom_slider = QSlider(Qt.Horizontal, self)
        self.zoom_slider.setGeometry(30, 40, 200, 30)
        self.zoom_slider.setFixedWidth(140)
        self.zoom_slider.setMinimum(-50)
        self.zoom_slider.setMaximum(50)

        # Set the default position to the middle of the slider
        self.zoom_slider.setValue(self.slider_start)

        self.zoom_slider.valueChanged[int].connect(self.changeValue)
        horizontal_layout.addWidget(self.zoom_slider)

        # Zoom in button
        button_zoom_in = createZoomPushButton('+', 33, self.onZoomInClicked,
                                              'Zoom in')
        button_zoom_in.setAutoRepeat(True)
        horizontal_layout.addWidget(button_zoom_in)

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
        char_count = len(self.document.toPlainText()) - len(
            self.document.toPlainText().split(" ")) + 1
        self.label_cc.setText(str(char_count) + " Characters")

    def onZoomInClicked(self):
        """
        Setting the value of the slider calls the changeValue
        function to perform the appropriate calculations
        :return: returns nothing
        """
        logging.info("On Zoom In")
        self.zoom_slider.setValue(self.zoom_slider.value() + 5)
        self.changeValue()

    def onZoomOutClicked(self):
        """
        Setting the value of the slider calls the changeValue
         function to perform the appropriate calculations
        :return: returns nothing
        """
        logging.info("On Zoom Out")
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
        logging.info("On Reset Zoom")
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
        should_show_hint = not self.settings.contains(setting_hint) or self.settings.value(
            setting_hint) is True
        logging.info("%s: %s", setting_hint, str(should_show_hint))
        if should_show_hint:
            hint = DialogBuilder(calendar, "Setting Reminders",
                                 "Hint: Select a date to create a Reminder!")
            hint.addButtonBox(QDialogButtonBox(QDialogButtonBox.Ok))
            hint.exec()
            self.settings.setValue(setting_hint, not should_show_hint)

        def onCalendarReminder():
            """
            """
            # noinspection PyCompatibility
            date: QDate = calendar.selectedDate()
            logging.info(date.toString("MM-dd-yyyy"))
            self.app.reminders.showDialog(calendar, False, date)

        calendar.selectionChanged.connect(onCalendarReminder)

        dialog = DialogBuilder()
        dialog.addWidget(calendar)
        dialog.layout().setContentsMargins(0, 0, 0, 0)
        dialog.setFixedHeight(400)
        dialog.exec()
