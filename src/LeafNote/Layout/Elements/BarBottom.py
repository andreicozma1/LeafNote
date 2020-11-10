"""
This module holds a class that displays various information to the user about the document
on the bottom of the application.
"""
import html
import logging

from PyQt5.Qt import Qt, QTimer
from PyQt5.QtCore import QDateTime, QSettings, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QDialogButtonBox, \
    QSizePolicy, QToolButton, QToolBar

from LeafNote.Utils import DialogBuilder
from LeafNote.Widgets import CalendarWidget


class BarBottom(QToolBar):
    """
    BottomBar sets up the bottom bar when called in Main.py
    holds functionality and format of the the tools in
    the bottom bar
    """

    def __init__(self, app, document, settings: QSettings):
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

        # self.setStyleSheet("background-color: #ff0000; height: 100%;")

    def initUI(self):
        """
        Create the layout of the widget
        :return: Returns nothing
        """
        # Set layout params
        self.layout().setSpacing(5)

        # Set global font size
        font_default = QFont()
        font_default.setPointSize(10)

        # Create Calendar Button

        calendar = QToolButton()
        calendar.setText(html.unescape("&#128197;"))
        calendar.clicked.connect(self.showCalendar)
        self.addWidget(calendar)

        def createBottomBarLabel(title, font):
            label = QLabel(title)
            label.setFont(font)
            return label

        # Create date-time label
        self.label_time = createBottomBarLabel('', font_default)
        self.addWidget(self.label_time)
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)
        self.updateTime()

        self.addSpacer()

        # Create Word Counter
        self.label_wc = createBottomBarLabel('0 Words', font_default)
        self.addWidget(self.label_wc)

        # Create Character Counter
        self.label_cc = createBottomBarLabel('0 Characters', font_default)
        self.addWidget(self.label_cc)

        self.addSpacer()

        # functionality of word and character count
        self.document.textChanged.connect(self.updateWordCount)
        self.document.textChanged.connect(self.updateCharCount)

        def createZoomPushButton(title, signal, tool_tip):
            btn = QToolButton()
            btn.setText(title)
            btn.setToolTip(tool_tip)
            btn.clicked.connect(signal)
            return btn

        # Zoom reset button
        button_zoom_reset = createZoomPushButton("100%", self.resetZoom,
                                                 'Reset zoom to default 100%')
        button_zoom_reset.setFont(font_default)
        self.addWidget(button_zoom_reset)

        # Zoom Out button
        button_zoom_out = createZoomPushButton(html.unescape("&minus;"), self.onZoomOutClicked,
                                               'Zoom out (Ctrl+-)')
        button_zoom_out.setAutoRepeat(True)
        self.addWidget(button_zoom_out)

        # Zoom Slider
        self.zoom_slider = QSlider(Qt.Horizontal, self)
        self.zoom_slider.setFixedWidth(240)
        self.zoom_slider.setMinimum(-50)
        self.zoom_slider.setMaximum(50)

        # Set the default position to the middle of the slider
        self.zoom_slider.setValue(self.slider_start)

        self.zoom_slider.valueChanged[int].connect(self.changeValue)
        self.addWidget(self.zoom_slider)

        # Zoom in button
        button_zoom_in = createZoomPushButton(html.unescape("&plus;"), self.onZoomInClicked,
                                              'Zoom in (Ctrl+=)')
        button_zoom_in.setAutoRepeat(True)
        self.addWidget(button_zoom_in)

    def addSpacer(self):
        """
        Creates an expanding spacer in the layout
        """
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(spacer)

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
        char_count = len(self.document.toPlainText())
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
        header = self.app.layout_props.getDefaultHeaderColorLight()
        select = self.app.layout_props.getDefaultSelectColor()
        calendar = CalendarWidget(header, select)

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
            Creates a calendar reminder
            """
            date: QDate = calendar.selectedDate()
            logging.info(date.toString("MM-dd-yyyy"))
            self.app.reminders.showDialog(calendar, False, date)

        calendar.selectionChanged.connect(onCalendarReminder)

        dialog = DialogBuilder()
        dialog.addWidget(calendar)
        dialog.layout().setContentsMargins(0, 0, 0, 0)
        dialog.setMinimumWidth(int(dialog.width() / 1.2))
        dialog.setMinimumHeight(int(dialog.height() / 1.2))
        dialog.exec()
