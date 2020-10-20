"""
this module holds a class containing a reminder for the user
"""

import logging
from time import time

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLineEdit, QTimeEdit, QDialogButtonBox, QWidget, QVBoxLayout, \
    QLabel, QPlainTextEdit

from Utils.DialogBuilder import DialogBuilder
from Widgets.Calendar import Calendar


class Reminder(QWidget):
    """
    This is the reminder node class. It contains each individually
    traits of a reminder to allow it to be added to the right bar.
    """

    def __init__(self, key, sort, date, reminder_time, title, description):
        # noinspection PyCompatibility
        super().__init__()
        vertical_layout = QVBoxLayout(self)
        show_title = QLabel(title)
        show_date = QLabel(date + "," + reminder_time)
        show_desc = QLabel(description)
        vertical_layout.addWidget(show_title)
        vertical_layout.addWidget(show_date)
        vertical_layout.addWidget(show_desc)
        self.key = key
        self.sort_key = sort
        self.date = date
        self.reminder_time = reminder_time
        self.title = title
        self.description = description


class Reminders:
    """
    This is a class of reminders. It sets up the Reminder
     dialog as well as adds the reminders to the right menu
    """

    def __init__(self, app, settings):
        logging.debug("Creating Reminders")
        self.app = app
        self.settings = settings
        self.rem_list = list()

    def addReminder(self, reminder: Reminder):
        """
        this will add a reminder to the list of reminders
        """
        self.rem_list.append(reminder)

    def removeReminder(self, reminder: Reminder):
        """
        this will remove a reminder from the list of reminders
        """
        # TODO remove reminder from list
        pass

    def showDialog(self, block, show_calendar: bool = True, date: QDate = None):
        """
        this will show the user a dialog of the the reminders
        """
        # Set the default date format
        # noinspection PyCompatibility
        format_date: str = "MM-dd-yyyy"
        title = QLineEdit()
        title.setPlaceholderText("Title")
        # ------------------------------#
        # QPlain text edit allows text on multiple lines
        description = QPlainTextEdit()
        description.setMaximumHeight(120)

        def limitCharCount():
            # Limits the number of characters in description box
            text_content = description.toPlainText()
            length = len(text_content)
            max_length = 150
            if length > max_length:
                logging.info("Description too long!")
                # Get the cursor and position
                cursor = description.textCursor()
                position = cursor.position()
                # Strip the text and set
                new_text = text_content[:max_length]
                description.setPlainText(new_text)
                # Restore cursor position
                cursor.setPosition(position - 1)
                description.setTextCursor(cursor)

        # Assign text limit listener
        description.textChanged.connect(limitCharCount)
        description.setPlaceholderText("Description")

        dialog = DialogBuilder(block, "Add reminder")
        # ------------------------------#
        cal = Calendar()
        cal.setFixedHeight(300)

        # Update dialog title based off selected date
        def updateTitle():

            # noinspection PyCompatibility
            new_date: QDate = cal.selectedDate()
            # noinspection PyCompatibility
            str_date: str = new_date.toString(format_date)
            logging.debug("Update title %s", str_date)
            dialog.setTitleText(str_date)

        cal.selectionChanged.connect(updateTitle)
        # ------------------------------#
        hour_cb = QTimeEdit()
        # ------------------------------#
        dialog.addWidget(title)
        dialog.addWidget(description)

        # Determine whether to use calendar in dialog or not
        if show_calendar is True or date is None:
            dialog.addWidget(cal)
            dialog.setTitleText(cal.selectedDate().toString(format_date))
        else:
            dialog.setTitleText(date.toString(format_date))

        dialog.addWidget(hour_cb)
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        dialog.addButtonBox(button_box)
        # Set size constrains for looks
        dialog.setFixedWidth(cal.sizeHint().width())
        dialog.setFixedHeight(dialog.sizeHint().height())
        if dialog.exec():
            if title.text():
                # Get the date from either the Cal button or the in-dialog calendar
                if date is None:
                    selected_date = cal.selectedDate().toString(format_date)
                else:
                    selected_date = date.toString(format_date)

                milliseconds = int(time() * 1000)
                time_temp = hour_cb.text()
                sort_key_string = selected_date + "-" + self.convert24(time_temp)
                sort_key_string = sort_key_string.replace(" ", "")
                sort_key_string = sort_key_string.replace("-", "")
                sort_key_string = sort_key_string.replace(":", "")
                reminder_node = Reminder(milliseconds, sort_key_string, selected_date,
                                         hour_cb.text(), title.text(),
                                         description.text())
                print("Printing Class")
                print(reminder_node.key, reminder_node.sort_key, reminder_node.date,
                      reminder_node.reminder_time,
                      reminder_node.title, reminder_node.description)
                self.rem_list.append(reminder_node)
                self.app.right_menu.collapsible_reminders.addElement(reminder_node)
        else:
            print("Clicked cancel")

    def convert24(self, str1):
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
