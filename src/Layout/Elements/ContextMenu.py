"""
Right Menu Module creates an interactive menu with collapsible widgets
that displays information including but not limited to:
- File metadata such as name, path, size, modification time, etc.
- Document Summary contents.
- Reminders List.
"""
import logging

from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea

from Utils import DocumentSummarizer
from Utils.Reminders import Reminder
from Widgets.CollapsibleWidget import CollapsibleWidget


class ContextMenu(QScrollArea):
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
        self.col_metadata_contents = ["Name", "Path", "Size", "Owner",
                                      "Viewed", "Modified"]
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
    def makePropLabel(prop: str):
        """
        Constructor function for a label
        :prop prop: Property name to reference
        """
        label = QLabel()
        label.setWordWrap(True)
        label.setProperty("prop", prop)
        return label

    def setupDetails(self):
        """
        Adds all the elements in the collapsible widgets
        :return: nothing
        """
        logging.debug("Setting up layout component details")

        # Add all metadata menu properties from list
        for elem in self.col_metadata_contents:
            self.col_metadata_main.addElement(self.makePropLabel(elem))

        def onSummaryAction():
            """
            Click action for summarizer button
            """
            DocumentSummarizer.onSummaryAction(self.app, self.document)

        # Add all summarizer components
        self.col_summary_enable.setVisible(self.document.summarizer is None)
        self.col_summary_enable.clicked.connect(onSummaryAction)
        self.col_summary_main.addElement(self.col_summary_enable)
        self.col_summary_main.addElement(self.col_summary_body)

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
        # Get the file info and update all the respective fields

        # Iterate through all properties and fill in metadata labels
        for i in range(self.col_metadata_main.layout_content.count()):
            label = self.col_metadata_main.layout_content.itemAt(i).widget()
            prop = label.property("prop")
            # noinspection PyCompatibility
            value: str
            if path is None:
                value = "?"
            elif prop == "Name":
                value = info.fileName()
            elif prop == "Path":
                value = info.path()
            elif prop == "Size":
                value = ((str(round(info.size() / 1000000.0, 2))) + "MB")
            elif prop == "Owner":
                value = (str(info.owner()))
            elif prop == "Viewed":
                value = (info.lastRead().toString(self.format_time))
            elif prop == "Modified":
                value = (info.lastModified().toString(self.format_time))
            else:
                value = "?"
            if len(value) == 0:
                value = "?"
            label.setText(label.property("prop") + ": " + value)

        # Update the summary from file
        self.updateSummary()

    def updateSummary(self):
        """
        Updates and expands the right menu summary section
        """
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

        def onDelete(key):
            self.app.reminders.deleteReminder(key)

        for rem in reminders_list:
            wid = Reminder(rem['key'], rem['date'], rem['time'],
                           rem['title'], rem['text'], onDelete)

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
