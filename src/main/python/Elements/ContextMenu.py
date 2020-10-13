from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from Elements.CollapsibleWidget import CollapsibleWidget


class ContextMenu(QWidget):
    def __init__(self):
        super(ContextMenu, self).__init__()
        # Create main vertical layout
        vertical_layout = QVBoxLayout(self)
        vertical_layout.setContentsMargins(10, 0, 10, 0)
        vertical_layout.setSpacing(3)

        self.format_time = "MM-dd-yyyy HH:mm:ss"

        self.setupDetails(vertical_layout)
        vertical_layout.addStretch()

    def setupDetails(self, vertical_layout):
        """
        Adds all the elements of right menu in a vertical layout
        :param vertical_layout: layout to add elements to
        :return: nothing
        """

        def createLabel(prop: str):
            label = QLabel()
            label.setWordWrap(True)
            label.setProperty("prop", prop)
            return label

        self.collapsible_metadata = CollapsibleWidget("File Details:")
        self.collapsible_metadata.addElement(createLabel("Name"))
        self.collapsible_metadata.addElement(createLabel("Path"))
        self.collapsible_metadata.addElement(createLabel("Size"))
        self.collapsible_metadata.addElement(createLabel("Owner"))
        self.collapsible_metadata.addElement(createLabel("Viewed"))
        self.collapsible_metadata.addElement(createLabel("Modified"))
        self.collapsible_metadata.addElement(createLabel("Created"))
        vertical_layout.addWidget(self.collapsible_metadata)
        # Initial setup of labels, when no file is open
        self.updateDetails(None)

    def updateDetails(self, path):
        """
        Updates the elements in the right menu based on arguments
        :param document: a new reference to the document
        :param path: path of the file
        :param formattingMode: whether the file is in formatting mode
        :return: nothing
        """
        # TODO - use document ref to display info about the document
        info = QFileInfo(path)
        # Get the file info and update all the respective fields

        # Iterate through all properties and fill in metadata labels
        for i in range(self.collapsible_metadata.layout_content.count()):
            label = self.collapsible_metadata.layout_content.itemAt(i).widget()
            prop = label.property("prop")
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
            elif prop == "Created":
                value = (info.birthTime().toString(self.format_time))
            else:
                value = "?"
            if len(value) == 0:
                value = "?"
            label.setText(label.property("prop") + ": " + value)
