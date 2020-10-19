"""
EQUATION EDITOR
"""
import logging
import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QPushButton

from Utils.DialogBuilder import DialogBuilder


class EquationEditor(QWidget):
    """
    This is a widget is an interactive editor for the user to create and insert equations
    using latex
    """
    def __init__(self, document):
        """
        initializes the widgets
        :param document: reference to the the document
        :return: returns nothing
        """
        logging.debug("")
        super().__init__()

        # initialize variables
        self.document = document
        self.url = "https://latex.codecogs.com/gif.latex?\\dpi{200}"
        self.pixmap = None
        self.equation = None
        self.equation_bar = None

        # create the QDialog and fill it in
        self.dialog = DialogBuilder(document)
        self.initUI()
        self.dialog.exec()

    def initUI(self):
        """
        sets up the layout of the widget
        """
        # creates the label to show what the user is working on
        self.equation = QLabel()
        self.dialog.addWidget(self.equation)

        # creates the qlineedit the user types into
        self.equation_bar = QLineEdit()
        self.dialog.addWidget(self.equation_bar)

        # widget to contain buttons
        widget = QWidget()
        hbox = QHBoxLayout(widget)

        # button to quit dialogs
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.dialog.close)
        hbox.addWidget(cancel)

        # button to refresh the equation
        generate = QPushButton("Generate")
        generate.clicked.connect(self.onGenerate)
        hbox.addWidget(generate)

        # button to insert equation into the document
        insert = QPushButton("Insert")
        insert.clicked.connect(self.onInsert)
        hbox.addWidget(insert)

        self.dialog.addWidget(widget)

    def onGenerate(self):
        """
        Generates the image from the users input.
        """
        logging.info("User Generated Equation")
        # TODO - handle user spamming button

        # get the formatted equation from the web api
        req = requests.get(self.url + self.equation_bar.text())

        # convert the image to a pixmap and display it to the user through the qlabel
        img = QImage()
        img.loadFromData(req.content)
        self.pixmap = QPixmap(img)
        self.equation.setPixmap(self.pixmap)

    def onInsert(self):
        """
        When the user selects to insert the image.
        """
        # generate the image if it has not been yet
        self.onGenerate()

        # if the pixmap is not none insert it to the document
        if self.pixmap is not None:
            logging.info("Inserted Equation")
            cursor = self.document.textCursor()

            # scale the pixmap and get its image
            font_size = self.document.currentCharFormat().fontPointSize()
            self.pixmap = self.pixmap.scaledToHeight(font_size + 35, Qt.SmoothTransformation)
            img = self.pixmap.toImage()

            # add the image to the document and close the prompt
            cursor.insertImage(img)
            self.dialog.close()
        else:
            logging.warning("No Pixmap Found")
