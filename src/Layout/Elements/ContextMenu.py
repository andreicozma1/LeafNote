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
from Utils.Reminders import Reminder, Reminders
from Widgets.CollapsibleWidget import CollapsibleWidget


class ContextMenu(QScrollArea):
    """
    Scrollable are Right-Menu that shows
    file metadata information, summary, reminders, etc.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, app, document):
        super().__init__()
        logging.debug("Creating Context Menu")
        self.app = app
        self.document = document
        self.format_time = "MM-dd-yyyy HH:mm:ss"


        # self.setupDetails(vertical_layout)
        # vertical_layout.addStretch()

        # Main widget of QScroll area is an expandable QWidget with
        self.main_widget = QWidget()
        # The expandable QWidget has a Vertical Layout
        self.vertical_layout = QVBoxLayout(self.main_widget)

        # Init File Details
        self.col_metadata_main = CollapsibleWidget("File Details:")
        self.col_metadata_contents = ["Name", "Path", "Size", "Owner",
                                      "Viewed", "Modified"]
        # Init Summary Components
        self.col_summary_main = CollapsibleWidget("Summary:")
        self.col_summary_enable = QPushButton("Enable Summarizer")
        self.col_summary_body = self.makePropLabel("Summary")
        # Init Reminders Components
        self.col_reminders_main = CollapsibleWidget("Reminders:")
        self.col_reminders_add_reminder = QPushButton("Add Reminder")
        self.setupComponents()
        self.setupDetails()
        # Initial setup of labels, when no file is open
        self.updateDetails(None)

    def setupComponents(self):
        """
        Initializes the main layout of the Scroll area.
        """
        # Set up sizing
        logging.debug("Setting up layout components")
        self.vertical_layout.setContentsMargins(10, 0, 10, 0)
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

        #self.col_reminders_add_reminder.clicked.connect(self.col_reminders_main.app.right_menu.showDialog) #Saying no instance of app, fix in another issue
        #self.col_reminders_main.addElement(self.col_reminders_add_reminder)

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
