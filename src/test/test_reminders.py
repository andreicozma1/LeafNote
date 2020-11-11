"""
test Reminders behaviors.
"""
import unittest
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
        key = self.reminders.addReminder(date, time_r, title, description)
        self.assertNotEqual(key, None)
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

        # Adds the reminder into the list
        key = self.reminders.addReminder(date, time_r, title, description)
        self.assertEqual(self.reminders.deleteReminder(key, True), key)
