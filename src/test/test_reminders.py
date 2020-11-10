"""
test Reminders behaviors.
"""
import unittest
import time
import test
from PyQt5.QtCore import QDate


class TestReminders(unittest.TestCase):
    """
    Unit test for reminders functionality
    """

    def setUp(self):
        """
        Set up environment
        """
        self.reminders = test.app.reminders

    def test24convert(self):
        """
        Tests if the convert24 can convert the 12 hour time to 24 hour time
        :return:
        """
        self.assertEqual(self.reminders.convert24("1:00 PM"), "13:00 ")

    def testAddReminder(self):
        """
        Tests the addReminder function
        """

        # Creates fake reminder
        date: QDate = QDate.currentDate()
        title = "Test Reminders"
        description = "Testing addition"
        time_r = "13:00"

        # Adds the reminder into the list
        self.assertEqual(self.reminders.addReminder(date, time_r, title, description), True)

        # Creates an estemate key
        key_est = int(round(time.time() * 1000))

        # Grabs all the reminders stored
        dictionary = self.reminders.rem_list
        reminders_list = list(dictionary.values())
        reminders_list.sort(key=lambda t: t['sort'])

        # Deletes the only key created in the last 30 miliseconds
        for rem in reminders_list:
            key = rem['key']
            if key_est - 30 <= key <= key_est + 30:
                self.reminders.deleteReminder(key, True)

    def testDeleteReminder(self):
        """
        Tests the addReminder function
        """

        # Creates fake reminder
        date: QDate = QDate.currentDate()
        title = "Test Reminders"
        description = "Testing deletion"
        time_r = "13:00"
        key = 1

        # Adds the reminder into the list
        self.reminders.addReminder(date, time_r, title, description)

        # Creates an estemate key
        key_est = int(round(time.time() * 1000))

        # Grabs all the reminders stored
        dictionary = self.reminders.rem_list
        reminders_list = list(dictionary.values())
        reminders_list.sort(key=lambda t: t['sort'])

        # Deletes the only key created in the last 30 miliseconds
        for rem in reminders_list:
            key = rem['key']
            if key_est - 30 <= key <= key_est + 30:
                self.assertEqual(self.reminders.deleteReminder(key, True), True)
                key = 1

        # if key is not 1 then the test has failed to delete the reminder
        if key != 1:
            self.assertEqual(key, 1)
