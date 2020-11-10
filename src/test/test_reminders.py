"""
test Reminders behaviors.
"""
import unittest

from PyQt5.QtWidgets import QApplication, QComboBox, QFontComboBox, QAbstractButton
from LeafNote import Utils
from LeafNote import App
from PyQt5.QtCore import QDate
import time

ctx = QApplication([])
app = App(ctx)


class TestReminders(unittest.TestCase):
    """
    Unit test for all Bottom Bar functionality
    """

    def setUp(self):
        """
        Set up environment
        """
        self.bottom_bar = app.bottom_bar
        self.reminders = app.reminders
        self.document = app.document
        self.doc_props = app.doc_props
        self.layout_props = app.layout_props

    def test24convert(self):
        self.assertEqual(self.reminders.convert24("1:00 PM"), "13:00 ")

    def testAddReminder(self):
        date: QDate = QDate.currentDate()
        title = "Test Reminders"
        description = "Testing addition"
        time_r = "13:00"

        self.assertEqual(self.reminders.addReminder(date, time_r, title, description), True)
        key_est = int(round(time.time() * 1000))

        dictionary = self.reminders.rem_list
        reminders_list = list(dictionary.values())
        reminders_list.sort(key=lambda t: t['sort'])

        for rem in reminders_list:
            self.key = rem['key']
            if key_est - 30 <= self.key <= key_est + 30:
                self.reminders.deleteReminder(self.key)

    def testDeleteReminder(self):
        date: QDate = QDate.currentDate()
        title = "Test Reminders"
        description = "Testing deletion"
        time_r = "13:00"

        self.reminders.addReminder(date, time_r, title, description)
        key_est = int(round(time.time() * 1000))

        dictionary = self.reminders.rem_list
        reminders_list = list(dictionary.values())
        reminders_list.sort(key=lambda t: t['sort'])

        for rem in reminders_list:
            self.key = rem['key']
            if key_est - 30 <= self.key <= key_est + 30:
                self.assertEqual(self.reminders.deleteReminder(self.key), True)