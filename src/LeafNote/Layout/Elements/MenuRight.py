"""
Right Menu Module creates an interactive menu with collapsible widgets
that displays information including but not limited to:
- File metadata such as name, path, size, modification time, etc.
- Document Summary contents.
- Reminders List.
"""
import html
import logging

from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QDialogButtonBox

from LeafNote.Utils import Summarizer, DialogBuilder
from LeafNote.Widgets import CollapsibleWidget, Reminder


class MenuRight(QScrollArea):
    """
    Scrollable are Right-Menu that shows
    file metadata information, summary, reminders, etc.
    """

    def __init__(self, app, layout_props, document):
        super().__init__()
        logging.debug("Creating Context Menu")
        self.app = app
        self.layout_props = layout_props
        self.document = document
        self.format_time = "MM-dd-yyyy HH:mm:ss"

        # Main widget of QScroll area is an expandable QWidget with
        self.main_widget = QWidget()
        # The expandable QWidget has a Vertical Layout
        self.vertical_layout = QVBoxLayout(self.main_widget)

        # Init File Details
        self.col_metadata_main = CollapsibleWidget("File Details:")
        self.col_metadata_main.setStyleSheet(self.getCollapsibleMenuStyle())
        self.col_metadata_contents = self.makePropLabel("Properties")

        # Init Summary Components
        self.col_summary_main = CollapsibleWidget("Summary:")
        self.col_summary_main.setStyleSheet(self.getCollapsibleMenuStyle())
        self.col_summary_enable = QPushButton("Enable Summarizer")
        self.col_summary_body = self.makePropLabel("Summary")

        # Init Reminders Components
        self.col_reminders_main = CollapsibleWidget("Reminders:")
        self.col_reminders_main.setStyleSheet(self.getCollapsibleMenuStyle())
        self.col_reminders_add = QPushButton("Add Reminder")

        self.setupComponents()
        self.setupDetails()
        # Initial setup of labels, when no file is open
        self.updateDetails(None)
        self.updateReminders()

    def setupComponents(self):
        """
        Initializes the main layout of the Scroll area.
        """
        # Set up sizing
        logging.debug("Setting up layout components")
        self.vertical_layout.setContentsMargins(3, 0, 3, 0)
        self.vertical_layout.setSpacing(3)
        # Set up all the collapsible widget contents

        self.vertical_layout.addWidget(self.col_metadata_main)
        self.vertical_layout.addWidget(self.col_summary_main)
        self.vertical_layout.addWidget(self.col_reminders_main)
        self.vertical_layout.addStretch()
        # Set the main widget of the scroll area to
        # The main widget and make it resizable
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

    @staticmethod
    def makePropLabel(name: str):
        """
        Constructor function for a label
        :prop prop: Property name to reference
        """
        label = QLabel(name)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        return label

    def setupDetails(self):
        """
        Adds all the elements in the collapsible widgets
        :return: nothing
        """
        logging.debug("Setting up layout component details")

        # Add all metadata menu properties from list
        self.col_metadata_main.addElement(self.col_metadata_contents)

        def onSummaryAction():
            """
            Click action for summarizer button
            """
            Summarizer.onSummaryAction(self.app, self.document)

        # Add all summarizer components
        self.col_summary_enable.setVisible(self.document.summarizer is None)
        self.col_summary_enable.clicked.connect(onSummaryAction)
        self.col_summary_main.addElement(self.col_summary_enable)
        self.col_summary_main.addElement(self.col_summary_body)
        self.col_summary_main.btn_toggle.pressed.connect(self.updateSummary)

        def onRemindersAction():
            """
            Adds a new reminder on button click
            """
            self.app.reminders.showDialog(self)

        self.col_reminders_add.clicked.connect(onRemindersAction)
        self.col_reminders_main.addElement(self.col_reminders_add)

    def updateDetails(self, path):
        """
        Updates the elements in the right menu based on arguments
        :param path: path of the file
        :return: nothing
        """
        info = QFileInfo(path)

        bullet = html.unescape("&#8226;")

        value: str = bullet + " File not saved!"
        # Get the file info and update all the respective fields
        if info is not None and path is not None:
            value = ""
            i_s = "<i>"
            i_e = "</i>"
            br = "<br>"

            size = info.size()
            units = ['Bytes', 'KB', 'MB', 'GB']
            unit = 0
            while len(str(round(size, 0))) > 3:
                size /= 1000
                unit += 1

            value += bullet + " Name: " + i_s + info.fileName() + i_e + br
            value += bullet + " Path: " + i_s + info.path() + i_e + br
            value += bullet + " Size: " + i_s + str(size) + " " + units[unit] + i_e + br
            value += bullet + " Owner: " + i_s + (str(info.owner())) + i_e + br
            value += bullet + " Viewed: " + i_s + \
                     (info.lastRead().toString(self.format_time)) + i_e + br
            value += bullet + " Modified: " + i_s + \
                     (info.lastModified().toString(self.format_time)) + i_e

        self.col_metadata_contents.setText(value)
        # Update the summary from file
        self.updateSummary()

    def updateSummary(self):
        """
        Updates and expands the right menu summary section
        """
        logging.debug("Updating Summary")
        if self.document.summarizer is not None:
            self.col_summary_body.show()
            self.col_summary_enable.hide()
            text = self.document.summarizer.summarize(self.document.toPlainText())
            self.col_summary_body.setText(text)
        else:
            self.col_summary_body.hide()
            self.col_summary_enable.show()

    def updateReminders(self):
        """
        Updates the right menu reminders based on dictionary
        """
        layout = self.col_reminders_main.content.layout()
        for i in range(1, layout.count()):
            layout.itemAt(i).widget().deleteLater()

        dictionary = self.app.reminders.rem_list
        reminders_list = list(dictionary.values())
        reminders_list.sort(key=lambda t: t['sort'])

        def fail():
            """
            Failure pop-up for reminder
            """
            dialog_rem_error = DialogBuilder(self.app, "Error")
            dialog_rem_error.setTitleText("Failed to remove reminder")
            dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok)
            dialog_rem_error.addButtonBox(dialog_buttons)
            dialog_rem_error.show()

        def deleteReminder(key):
            """
            Delete pop-up for reminder
            """
            if key not in self.app.reminders.rem_list:
                logging.error("%s not in reminders list", key)
                fail()
                return
            title = self.app.reminders.rem_list[key]['title']

            dialog = DialogBuilder(self.app, "Delete Reminder")
            dialog.setTitleText("Remove '" + title + "'?")
            dialog.setMsgText("This will permanently remove it from your reminders list.")
            dialog_but = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
            dialog.addButtonBox(dialog_but)
            if dialog.exec():
                if not self.app.reminders.deleteReminder(key):
                    logging.error("Could not remove reminder key %s", key)
                    fail()
            else:
                logging.info("User chose to not delete the reminder")

        for rem in reminders_list:
            wid = Reminder(rem['key'], rem['date'], rem['time'],
                           rem['title'], rem['text'], deleteReminder)

            self.col_reminders_main.addElement(wid)

    def getCollapsibleMenuStyle(self) -> str:
        """
        Retrieves the CSS Style used for the right menu
        Collapsible Widgets
        """
        prop_header_height = str(self.layout_props.getDefaultItemHeight())
        prop_header_color = str(self.layout_props.getDefaultHeaderColorLight())
        prop_header_color_select = str(self.layout_props.getDefaultHeaderColor())

        return "QToolButton { background-color: " + prop_header_color + ";" + \
               "color: white;" \
               "height: " + prop_header_height + "; " + \
               "border-radius: 3px; }" + \
               "QToolButton:hover, QToolButton:checked:hover { color: white;" \
               "background-color: " + prop_header_color_select + "; }" + \
               "QToolButton:checked {" + \
               "background-color: " + prop_header_color + "; }"
