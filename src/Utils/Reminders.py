import os
from functools import partial
from time import time
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCalendarWidget, QPushButton, QLineEdit, QTimeEdit, QDialogButtonBox, QWidget, QVBoxLayout, \
    QLabel
from Utils.DialogBuilder import DialogBuilder


class Reminder(QWidget):
    """
    This is the reminder node class. It contains each individualy traits of a reminder to allow it to be added to the right bar.
    """
    def __init__(self, key, sort, date, time, title, description):
        super().__init__()
        vertical_layout = QVBoxLayout(self)
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
    """
    This is a class of reminders. It sets up the Reminder dialog as well as adds the reminders to the right menu
    """
    def __init__(self, app, settings):
        self.app = app
        self.settings = settings
        self.rem_list = list()
        self.temp_list = list()
        self.tlist = list()
        self.datelist = list()
        self.trigger = 0
        self.app.settings.beginGroup("Reminders")
        self.dict_key = {}
        self.setReminder()

    def addReminder(self, reminder: Reminder):
        self.rem_list.append(reminder)

    def removeReminder(self, reminder: Reminder):
        #TODO remove reminder from list
        pass

    def showDialog(self):
        #self.setReminder()
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
        self.dialog.addWidget(hour_cb)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.dialog.addButtonBox(self.button_box)
        if self.dialog.exec():
            if title.text():
                self.trigger = 1
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

                #self.rem_list.append(reminder_node)
                self.temp_list.append(reminder_node.sort_key)
                self.temp_list.append(reminder_node.date)
                self.temp_list.append(reminder_node.time)
                self.temp_list.append(reminder_node.title)
                self.temp_list.append(reminder_node.description)
                #self.app.settings.setValue("reminders", self.dict_key)
                self.app.settings.setValue(str(reminder_node.key), self.temp_list)
                #self.app.settings.setValue(str(reminder_node.key), self.dict_key)

                #self.temp_list.clear()
                print(self.app.settings.value("reminders"))
                #print(self.app.settings.fileName())
                self.app.right_menu.collapsible_reminders.addElement(reminder_node)
                #self.app.right_menu.collapsible_reminders.addElement(self.app.settings.setValue(str(reminder_node.key), self.temp_list))
        else:
            print("Clicked cancel")

    def setReminder(self):
        print("setReminder")
        print(self.app.settings.allKeys())
        self.tlist = list(self.app.settings.allKeys())

        for i in range(3):
            self.tlist.pop(len(self.tlist) - 1)
        print(self.tlist)
        for i in self.tlist:
            reminder_dict = self.app.settings.value(i)
            tb_reminder = Reminder(None, reminder_dict[0], reminder_dict[1], reminder_dict[2], reminder_dict[3], reminder_dict[4])
            self.rem_list.append(tb_reminder)
            self.datelist.append(reminder_dict[0])
            #self.app.right_menu.collapsible_reminders.addElement(tb_reminder)
        self.datelist.sort()

        for i in self.datelist:
            for j in self.rem_list:
                rem_temp = Reminder(None, None, "", "", None, None)
                rem_temp = j
                if i == rem_temp.sort_key:
                      self.app.right_menu.collapsible_reminders.addElement(rem_temp)

    #def addReminderInShowDialog(self, reminder: Reminder):

        #print(self.datelist)


            # count = 0
            # for i in self.tlist:
            #     self.app.settings.remove(i)
            #     count += 1
            #     if count is 1:
            #         break
            # print(self.app.settings.allKeys())

           # print(self.app.settings.value())
            #key_list = list(self.dict_key.keys())
            # for i in key_list:
            #     print(self.app.settings.value(i))

    def deleteKeys(self, int, tlist):
        count = 0
        for i in tlist:
            self.app.settings.remove(i)
            count += 1
            if count is int:
                break

    def convert24(self, str1):
        """
        :param str1: This is a time that we are converting from normal time to 24 hour time
        :return:
        """
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

