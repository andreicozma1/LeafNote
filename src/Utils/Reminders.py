import logging
from time import time
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCalendarWidget, QPushButton, QLineEdit, QTimeEdit, QDialogButtonBox, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout, QPlainTextEdit

from Utils.DialogBuilder import DialogBuilder
from Widgets.Calendar import Calendar


gloablelist = list()

class Reminder(QWidget):
    """
    This is the reminder node class. It contains each individually
    traits of a reminder to allow it to be added to the right bar.
    """

    def __init__(self, key, sort, date, time, title, description, settings):
        # noinspection PyCompatibility
        super().__init__()
        self.settings_rem = settings
        self.vertical_layout = QVBoxLayout()
        self.vl = QWidget()
        self.horizontal_layout = QHBoxLayout(self)
        self.show_title = QLabel(title)
        self.show_date = QLabel(date)
        self.show_desc = QLabel(description)
        self.show_time = QLabel(time)
        self.vertical_layout.addWidget(self.show_title)
        self.vertical_layout.addWidget(self.show_date)
        self.vertical_layout.addWidget(self.show_time)
        self.vertical_layout.addWidget(self.show_desc)
        self.vl.setLayout(self.vertical_layout)
        self.horizontal_layout.addWidget(self.vl)
        self.key = key
        self.sort_key = sort
        self.date = date
        self.time = time
        self.title = title
        self.description = description
        self.btn = QPushButton("x")
        self.btn.setFlat(True)
        self.btn.clicked.connect(self.deleteReminder)
        self.horizontal_layout.addWidget(self.btn)

    def deleteReminder(self):
        self.show_title.setParent(None)
        self.show_date.setParent(None)
        self.show_time.setParent(None)
        self.show_desc.setParent(None)
        self.vertical_layout.removeWidget(self.show_title)
        self.vertical_layout.removeWidget(self.show_date)
        self.vertical_layout.removeWidget(self.show_time)
        self.vertical_layout.removeWidget(self.show_desc)
        self.horizontal_layout.removeWidget(self.vl)
        self.horizontal_layout.removeWidget(self.btn)
        self.settings_rem.remove(self.key)


class Reminders:
    """
    This is a class of reminders. It sets up the Reminder
     dialog as well as adds the reminders to the right menu
    """

    def __init__(self, app, settings):
        logging.info("Creating Reminders")
        self.app = app
        self.settings = settings
        self.rem_list = list()
        self.temp_list = list()
        self.date_list = list()
        self.settings_key_list = list()
        self.key_list = list()
        self.app.settings.beginGroup("Reminders")
        self.setReminder()

    def showDialog(self, block, show_calendar: bool = True, date: QDate = None):
        logging.info("showDialog: displays reminders dialog")
        """
        """
        # Set the default date format
        # noinspection PyCompatibility
        format_date: str = "yyyy-MM-dd"
        title = QLineEdit()
        title.setPlaceholderText("Title")
        # ------------------------------#
        # QPlain text edit allows text on multiple lines
        description = QPlainTextEdit()
        description.setMaximumHeight(120)

        def limitCharCount():
            """
            """
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
            """
            """
            # noinspection PyCompatibility
            new_date: QDate = cal.selectedDate()
            # noinspection PyCompatibility
            str_date: str = new_date.toString(format_date)
            logging.debug("Update title " + str_date)
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
        self.button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        dialog.addButtonBox(self.button_box)
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
                                         description.toPlainText(), self.settings)
                self.temp_list.append(reminder_node.sort_key)
                self.temp_list.append(reminder_node.date)
                self.temp_list.append(reminder_node.time)
                self.temp_list.append(reminder_node.title)
                self.temp_list.append(reminder_node.description)
                self.app.settings.setValue(str(reminder_node.key), self.temp_list)
                self.temp_list.clear()
                self.setReminderForDialog(reminder_node)
        else:
            print("Clicked cancel")

    def setReminder(self):
        logging.info("setReminder: recalls stored reminders")
        self.settings_key_list = list(self.app.settings.allKeys())

        for i in range(3):
            self.settings_key_list.pop(len(self.settings_key_list) - 1)

        for i in self.settings_key_list:
            reminder_dict = self.app.settings.value(i)
            tb_reminder = Reminder(None, reminder_dict[0], reminder_dict[1], reminder_dict[2], reminder_dict[3], reminder_dict[4], self.settings)
            self.rem_list.append(tb_reminder)
            self.date_list.append(reminder_dict[len(reminder_dict) - 5])
            reminder_dict.clear()

        self.date_list.sort()

        for i in self.date_list:
            for j in self.rem_list:
                rem_temp = j
                if i == rem_temp.sort_key:
                    self.key_list.append(rem_temp.sort_key)
                    self.app.right_menu.collapsible_reminders.addElement(rem_temp)


    def setReminderForDialog(self, reminder: Reminder):
        logging.info("setReminderForDialog: adds reminder to right_menu")
        current_rem = reminder
        self.rem_list.append(current_rem)
        self.date_list.append(current_rem.sort_key)
        self.date_list.sort()
        for i in self.date_list:
            for j in self.rem_list:
                rem_temp = j
                if i == rem_temp.sort_key:
                    self.app.right_menu.collapsible_reminders.addElement(rem_temp)
                    print("This if statement ran")

    def convert24(self, str1):
        """
        :param str1: This is a time that we are converting from normal time to 24 hour time
        :return:
        """
        if str1[1] == ":":
            str1 = "0" + str1

        # Checking if last two elements of time
        # is AM and first two elements are 12
        if str1[-2:] == "AM" and str1[:2] == "12":
            return "00" + str1[2:-2]

            # remove the AM
        elif str1[-2:] == "AM":
            return str1[:-2]

            # Checking if last two elements of time
        # is PM and first two elements are 12
        elif str1[-2:] == "PM" and str1[:2] == "12":
            return str1[:-2]

        else:
            # add 12 to hours and remove PM
            return str(int(str1[:2]) + 12) + str1[2:6]
