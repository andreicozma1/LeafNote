import os
from functools import partial
from time import time

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCalendarWidget, QPushButton, QLineEdit, QTimeEdit, QDialogButtonBox, QWidget, QVBoxLayout, \
    QLabel

from Utils.DialogBuilder import DialogBuilder


#parent->setStyleSheet("*:hover {background: red}");

class Reminder(QWidget):
    def __init__(self, key, sort, date, time, title, description):
        super().__init__()
        vertical_layout = QVBoxLayout(self)
        #self.setLayout(vertical_layout)
        show_title = QLabel(title)
        show_date = QLabel(date + "," + time)
        show_desc = QLabel(description)
        vertical_layout.addWidget(show_title)
        vertical_layout.addWidget(show_date)
        vertical_layout.addWidget(show_desc)
        self.key = key
        self.sort_key = sort
        self.date = date
        self.time = time
        self.title = title
        self.description = description


class Reminders():
    def __init__(self, app, settings):
        self.app = app
        self.settings = settings
        self.rem_list = list()
        self.counter = 0

    def addReminder(self, reminder: Reminder):
        self.rem_list.append(reminder)

    def removeReminder(self, reminder: Reminder):
        #TODO remove reminder from list
        pass

    def showDialog(self):
        selected_date = None

        title = QLineEdit()
        title.setPlaceholderText("Title")
        # ------------------------------#
        description = QLineEdit()
        description.setPlaceholderText("Description")
        # ------------------------------#
        cal = QCalendarWidget()
        # ------------------------------#
        hour_cb = QTimeEdit()
        # ------------------------------#
        self.dialog = DialogBuilder(self.app, "Add Reminder")
        self.dialog.addWidget(title)
        self.dialog.addWidget(description)
        self.dialog.addWidget(cal)
        #self.dialog.addWidget(self.button)
        self.dialog.addWidget(hour_cb)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.dialog.addButtonBox(self.button_box)
        if self.dialog.exec():
            if title.text():
                selected_date = cal.selectedDate().toString("yyyy-MM-dd")
                milliseconds = int(time() * 1000)
                time_temp = hour_cb.text()
                sort_key_string = selected_date + "-" + self.convert24(time_temp)
                sort_key_string = sort_key_string.replace(" ", "")
                sort_key_string = sort_key_string.replace("-", "")
                sort_key_string = sort_key_string.replace(":", "")
                reminder_node = Reminder(milliseconds,sort_key_string, selected_date, hour_cb.text(), title.text(), description.text())
                print("Printing Class")
                print(reminder_node.key, reminder_node.sort_key, reminder_node.date,reminder_node.time,reminder_node.title, reminder_node.description)
                self.rem_list.append(reminder_node)
                self.app.right_menu.collapsible_reminders.addElement(self.rem_list[self.counter])
                self.counter+= 1
        else:
            print("Clicked cancel")

    def convert24(self, str1):

        if(str1[1] == ":"):
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

