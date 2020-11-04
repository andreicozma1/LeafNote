"""
This module holds a customizable dialog prompt
"""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QLabel, QDialogButtonBox, QProgressBar


class DialogBuilder(QDialog):
    """
    This class is a customizable QDialog that can be used throughout the project
    """

    def __init__(self, blocked_widget=None, text_window: str = None, text_title: str = None,
                 text_msg: str = None):
        """
        Initializes the dialog builder.
        """
        super().__init__(blocked_widget)
        logging.debug("Init DialogBuilder")

        if text_window is None:
            text_window = "Dialog"

        self.setWindowTitle(text_window)
        self.layout_vertical = QVBoxLayout(self)
        self.label_title = QLabel(text_title)
        if text_title is None:
            self.label_title.setHidden(True)
        self.label_message = QLabel(text_msg)
        if text_msg is None:
            self.label_message.setHidden(True)

        self.installEventFilter(self)
        self.setup()

    def setup(self):
        """
        this sets up the initial layout of the dialog builder
        :return: Returns nothing
        """
        logging.info("")

        font = self.label_title.font()
        font.setPointSize(18)
        font.setBold(True)
        self.label_title.setFont(font)

        self.setWindowModality(Qt.WindowModal)

        self.layout_vertical.addWidget(self.label_title)
        self.layout_vertical.addWidget(self.label_message)

    def setTitleText(self, text: str):
        """
        this sets the QDialog title
        :return: Returns nothing
        """
        logging.info(text)
        self.label_title.setText(text)
        self.label_title.setHidden(False)

    def setMsgText(self, text: str):
        """
        this sets the QDialog message
        :return: Returns nothing
        """
        logging.info(text)
        self.label_message.setText(text)
        self.label_message.setHidden(False)

    def addWidget(self, widget: QWidget):
        """
        this adds a widget to the QDialog
        :return: Returns nothing
        """
        logging.info("")
        self.layout_vertical.addWidget(widget)

    def deleteWidget(self, widget: QWidget):
        """
        Deletes a widget from the layout
        :param widget: Widget to delete
        """
        logging.info("Deleted")
        self.layout_vertical.removeWidget(widget)

    def addButtonBox(self, button_box: QDialogButtonBox):
        """
        this adds a button box to the QDialog
        :return: Returns nothing
        """
        logging.info("")
        self.layout_vertical.addWidget(button_box)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def addProgressBar(self, min_max_range: tuple = (0, 0), initial_value: int = 0,
                       text_format: str = None, orientation=None, text_direction=None):
        """
        this adds a progress bar to the QDialog
        :return: Returns nothing
        """
        logging.info("min=%s;max=%s;initial_value=%s", str(min_max_range[0]),
                     str(min_max_range[1]), str(initial_value))

        # create the progress_bar and set its properties
        progress_bar = QProgressBar()

        # closes the dialog if the progress bar is full
        def checkFinished(value):
            if value >= progress_bar.maximum():
                logging.info("Progress bar filled - Closing dialog")
                self.close()

        progress_bar.valueChanged.connect(checkFinished)
        progress_bar.setRange(min_max_range[0], min_max_range[1])
        progress_bar.setValue(initial_value)
        if text_format is not None:
            progress_bar.setFormat(text_format)
        if orientation is not None:
            progress_bar.setOrientation(orientation)
        if text_direction is not None:
            progress_bar.setTextDirection(text_direction)

        # add the progress_bar to the dialog box and return the created object
        self.layout_vertical.addWidget(progress_bar)
        return progress_bar
