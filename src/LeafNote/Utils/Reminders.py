"""
this module holds a class containing a reminder for the user
"""
import logging
import time

from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import QLineEdit, QTimeEdit, QDialogButtonBox, QPlainTextEdit

from LeafNote.Utils import DialogBuilder
from LeafNote.Widgets.CalendarWidget import CalendarWidget


class Reminders:
    """
    This is a class of reminders. It sets up the Reminder
     dialog as well as adds the reminders to the right menu
    """

    def __init__(self, app, settings):
        logging.info("Creating Reminders")
        self.app = app
        self.settings = settings
        self.rem_list: dict = dict()
        self.restoreReminders()  # Recalls old reminders and sets them

    def showDialog(self, block, show_calendar: bool = True, date: QDate = None):
        """
        this will show the user a dialog of the the reminders
        :param block: Element to block by dialog
        :param show_calendar: Whether to include calendar or not
        :param date: Pre-defined date if calendar is not shown
        """
        logging.info("showDialog: displays reminders dialog")

        # Set the default date format

        format_date_def: str = "yyyy-MM-dd"
        # ------------------------------#
        input_title = QLineEdit()
        input_title.setPlaceholderText("Title")
        # ------------------------------#

        # ------------------------------#
        # QPlain text edit allows text on multiple lines
        input_description = QPlainTextEdit()
        input_description.setMaximumHeight(120)

        def limitCharCount():
            """
            Limits the maximum number of characters allowed in description box
            """
            # Limits the number of characters in input_description box
            text_content = input_description.toPlainText()
            length = len(text_content)
            max_length = 150
            if length > max_length:
                logging.info("Description too long!")
                # Get the cursor and position
                cursor = input_description.textCursor()
                position = cursor.position()
                # Strip the text and set
                new_text = text_content[:max_length]
                input_description.setPlainText(new_text)
                # Restore cursor position
                cursor.setPosition(position - 1)
                input_description.setTextCursor(cursor)

        # Assign text limit listener
        input_description.textChanged.connect(limitCharCount)
        input_description.setPlaceholderText("Description")
        # ------------------------------#

        # ------------------------------#
        input_calendar = CalendarWidget()
        input_time = QTimeEdit()

        def updateTitle():
            """
            Updates title of the dialog box to selected date and time
            """
            new_date: QDate = input_calendar.selectedDate()
            formatted_date = new_date.toString(format_date_def)
            new_time: QTime = input_time.time()
            formatted_time = new_time.toString("h:mm ap")
            new_title = formatted_date + " at " + formatted_time

            logging.debug("Update input_title %s", new_title)
            dialog.setTitleText(new_title)

        input_calendar.setFixedHeight(300)
        input_calendar.selectionChanged.connect(updateTitle)
        input_time.timeChanged.connect(updateTitle)
        # initial update of title with default values

        # ------------------------------#

        dialog = DialogBuilder(block, "Add reminder")

        dialog.addWidget(input_title)
        dialog.addWidget(input_description)

        # Determine whether to use calendar in dialog or not
        if show_calendar is True or date is None:
            dialog.addWidget(input_calendar)
        else:
            input_calendar.setSelectedDate(date)
        dialog.addWidget(input_time)
        updateTitle()

        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        dialog.addButtonBox(button_box)
        # Set size constrains for looks
        dialog.setFixedWidth(input_calendar.sizeHint().width())
        dialog.setFixedHeight(dialog.sizeHint().height())
        if dialog.exec():
            if len(input_title.text()) != 0:

                if date is None:
                    date = input_calendar.selectedDate()

                self.addReminder(date, input_time.text(), input_title.text(),
                                 input_description.toPlainText())

        else:
            logging.info("Clicked cancel")

    def restoreReminders(self):
        """
        Restore saved reminders from persistent settings
        """
        logging.debug("Restoring saved reminders")

        if self.settings.contains("reminders_dict"):
            self.rem_list = self.settings.value("reminders_dict")
            logging.info("Found reminders in Settings! %s keys", len(self.rem_list.keys()))

    def addReminder(self, date: QDate, time_str: str, title_str: str, desc_str: str):
        """
        Adds a reminder to the dictionary, saves it to settings,
        and update the right menu
        :param date: Reminder date
        :param time_str: Time of reminder
        :param title_str: Title of reminder
        :param desc_str: Description of reminder
        """
        logging.info("Adding reminder!")
        # Get the date as a formatted string
        date_format = "yyyy-MM-dd"
        date_txt = date.toString(date_format)

        # Create a sorting key
        milliseconds = int(round(time.time() * 1000))
        sort_key_string = date_txt + "-" + self.convert24(time_str)
        sort_key_string = sort_key_string.replace(" ", "").replace("-", "").replace(":", "")

        reminder = {
            "key": milliseconds,
            "sort": sort_key_string,
            "title": title_str,
            "text": desc_str,
            "date": date_txt,
            "time": time_str
        }
        logging.debug(reminder)
        # Add the reminder to the ReminderS dictionary
        self.rem_list[milliseconds] = reminder
        # Save the updated dictionary to persistent settings and update menu
        self.settings.setValue("reminders_dict", self.rem_list)
        self.app.right_menu.updateReminders()

    def deleteReminder(self, key):
        """
        Deletes a reminder from the dictionary based on key.
        :param key: key to delete
        """
        if self.rem_list.pop(key, None) is not None:
            logging.info("Removing reminder key %s", key)
            self.settings.setValue("reminders_dict", self.rem_list)
            self.app.right_menu.updateReminders()
        else:
            logging.error("Could not remove reminder key %s", key)

    # Converts time to 24 hours time.
    @staticmethod
    def convert24(str1):
        """
        :param str1: This is a time that we are converting from normal time to 24 hour time
        :return: returns a string of the time
        """
        if str1[1] == ":":
            str1 = "0" + str1

        # Checking if last two elements of time
        # is AM and first two elements are 12
        if str1[-2:] == "AM" and str1[:2] == "12":
            return "00" + str1[2:-2]

            # remove the AM
        if str1[-2:] == "AM":
            return str1[:-2]

            # Checking if last two elements of time
        # is PM and first two elements are 12
        if str1[-2:] == "PM" and str1[:2] == "12":
            return str1[:-2]

        # add 12 to hours and remove PM
        return str(int(str1[:2]) + 12) + str1[2:6]
