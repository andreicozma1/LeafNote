from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class ContextMenu(QWidget):
    def __init__(self):
        super(ContextMenu, self).__init__()
        # Create main vertical layout
        vertical_layout = QVBoxLayout(self)
        vertical_layout.setContentsMargins(10, 0, 10, 0)
        vertical_layout.setSpacing(3)

        self.format_time = "MM-dd-yyyy HH:mm:ss"

        self.setupElements(vertical_layout)
        vertical_layout.addStretch()

    def setupElements(self, vertical_layout):
        """
        Adds all the elements of right menu in a vertical layout
        :param vertical_layout: layout to add elements to
        :return: nothing
        """

        def createLabel(text):
            label = QLabel(text)
            label.setWordWrap(True)
            # label.setMinimumHeight(label.sizeHint().height())
            return label

        self.lbl_file = createLabel("Unknown")
        f = self.lbl_file.font()
        f.setBold(True)
        f.setPointSize(20)
        self.lbl_file.setFont(f)
        vertical_layout.addWidget(self.lbl_file)
        self.lbl_formatting_mode = createLabel("Formatting: False")
        vertical_layout.addWidget(self.lbl_formatting_mode)
        self.lbl_path = createLabel("Path: ?")
        vertical_layout.addWidget(self.lbl_path)
        self.lbl_size = createLabel("Size: ?")
        vertical_layout.addWidget(self.lbl_size)
        self.lbl_owner = createLabel("Owner: ?")
        vertical_layout.addWidget(self.lbl_owner)
        self.lbl_created = createLabel("Created: ?")
        vertical_layout.addWidget(self.lbl_created)
        self.lbl_modified = createLabel("Modified: ?")
        vertical_layout.addWidget(self.lbl_modified)
        self.lbl_viewed = createLabel("Viewed: ?")
        vertical_layout.addWidget(self.lbl_viewed)

    def updateMenu(self, document, path, formattingMode):
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
        file_name = info.fileName() if path is not None else "Unknown"
        file_path = info.path() if path is not None else "?"
        file_owner = (str(info.owner())) if path is not None else "?"
        file_size = (str(round(info.size() / 1000000.0, 2))) if path is not None else "?"
        file_birthTime = (info.birthTime().toString(self.format_time)) if path is not None else "?"
        file_lastModified = (info.lastModified().toString(self.format_time)) if path is not None else "?"
        file_lastRead = (info.lastRead().toString(self.format_time)) if path is not None else "?"

        self.lbl_file.setText(file_name)
        self.lbl_formatting_mode.setText("Formatting: " + str(formattingMode))
        self.lbl_path.setText("Path: " + file_path)
        self.lbl_owner.setText("Owner: " + file_owner)
        self.lbl_size.setText("Size: " + file_size + " MB")
        self.lbl_created.setText("Created: " + file_birthTime)
        self.lbl_modified.setText("Modified: " + file_lastModified)
        self.lbl_viewed.setText("Read: " + file_lastRead)
