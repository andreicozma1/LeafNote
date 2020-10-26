"""
Dictionary class is a QWidget that lets the user type in words into a text field
and returns the definitions list and pronunciation.
"""
import logging

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
    QSizePolicy, QShortcut


class Definition(QWidget):
    """
    Defines a singular definition entry
    """

    def __init__(self, def_type: str, def_text: str, def_example: str):
        super().__init__()
        self.layout = QVBoxLayout(self)
        # Create elements
        self.lbl_type = QLabel("Type: " + def_type)
        self.lbl_definition = QLabel("Definition: " + def_text)
        self.lbl_example = QLabel("Example: " + def_example)
        self.initUI()

    def initUI(self):
        # Make text selectable
        self.lbl_type.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_definition.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_example.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # Make text wrap
        self.lbl_type.setWordWrap(True)
        self.lbl_definition.setWordWrap(True)
        self.lbl_example.setWordWrap(True)
        # Add all elements to layout
        self.layout.addWidget(self.lbl_type)
        self.layout.addWidget(self.lbl_definition)
        self.layout.addWidget(self.lbl_example)


class Dictionary(QWidget):
    """
    Defines the definition of the dictionary lookup widget
    """

    def __init__(self, minimal=False):
        super().__init__()
        # Define class variables
        self.minimal = minimal
        self.lookup_callback = None
        self.close_callback = None
        self.vertical_layout = QVBoxLayout(self)
        # Defines header section with word and pronunciation
        self.lbl_word = QLabel()
        self.lbl_pronunciation = QLabel()
        # Define Definition Section
        self.lbl_definitions = QLabel("Results: ")
        self.widget_definitions = QWidget()
        self.definitions_layout = QVBoxLayout(self.widget_definitions)
        # Define Search Section
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("Type word here...")
        self.btn_cancel = QPushButton("Cancel")
        self.initUI()

    def initUI(self):
        """
        Initializes Dictionary UI
        """
        logging.debug("Initializing Dictionary")
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        # Set up word field
        font_header = QFont()
        if not self.minimal:
            font_header.setPointSize(20)
        font_header.setBold(True)
        self.lbl_word.setFont(font_header)
        self.lbl_word.setHidden(True)
        self.vertical_layout.addWidget(self.lbl_word)
        # Set up pronunciation field
        if not self.minimal:
            font_pron = QFont()
            font_pron.setItalic(True)
            self.lbl_pronunciation.setFont(font_pron)
            self.lbl_pronunciation.setHidden(True)
            self.vertical_layout.addWidget(self.lbl_pronunciation)
        # Set up definitions field
        if not self.minimal:
            # set up subheader size
            font_definition = QFont()
            font_definition.setPointSize(16)
            font_definition.setItalic(True)
            # Set up definitions section
            self.lbl_definitions.setFont(font_definition)
            self.lbl_definitions.setHidden(True)
            self.vertical_layout.addWidget(self.lbl_definitions)
        self.widget_definitions.setHidden(True)
        self.vertical_layout.addWidget(self.widget_definitions)
        # Set up search text and input field
        if not self.minimal:
            # Set up search section
            lbl_input = QLabel("Search:")
            lbl_input.setFont(font_header)
            self.vertical_layout.addWidget(lbl_input)
        self.vertical_layout.addWidget(self.input_search)
        # Focus the input field and attach a return key shortcut
        self.input_search.setFocus()
        shortcut = QShortcut(Qt.Key_Return, self)
        shortcut.activated.connect(self.search)

        # Set up action buttons section
        widget = QWidget()
        layout_buttons = QHBoxLayout(widget)
        btn_search = QPushButton("Search")
        btn_search.clicked.connect(self.search)
        if not self.minimal:
            layout_buttons.addStretch()
        layout_buttons.addWidget(self.btn_cancel)
        layout_buttons.addWidget(btn_search)
        layout_buttons.addStretch()

        self.vertical_layout.addWidget(widget)

    def onCloseClicked(self, callback):
        """
        Callback setter
        :param callback: callback function
        """
        logging.debug("Set close btn callback")
        self.close_callback = callback
        self.btn_cancel.clicked.connect(self.close_callback)

    def onLookupClicked(self, callback):
        """
        Callback setter
        :param callback: callback function
        """
        logging.debug("Set close btn callback")
        self.lookup_callback = callback

    def search(self):
        """
        Searches the current input in the input field
        """
        url = "https://owlbot.info/api/v4/dictionary/"
        input_txt = self.input_search.text()
        header = {"Authorization": "Token c81f74a1d401e6e47e52f5b75da4542b5c6a4887"}
        # Re-hide widget elements
        self.lbl_word.setHidden(True)
        self.lbl_pronunciation.setHidden(True)
        self.lbl_definitions.setHidden(True)
        self.widget_definitions.setHidden(True)
        # Remove previous definitions in def layout
        while self.definitions_layout.count() != 0:
            wid = self.definitions_layout.itemAt(0).widget()
            self.definitions_layout.removeWidget(wid)
            wid.deleteLater()
        # Error check user input
        if input_txt is not None and input_txt != "":
            logging.info("Looking up definition for - %s", input_txt)
            url += input_txt
            # Make a HTTP request
            response = requests.get(url, headers=header)
            # If request valid
            if response.ok:
                # Process response
                dictionary: dict = response.json()
                word = str(dictionary['word'])
                pronunciation = str(dictionary['pronunciation'])
                definitions_list: list = dictionary['definitions']
                # Show all elements
                self.lbl_word.setVisible(True)
                self.lbl_pronunciation.setVisible(True)
                self.lbl_definitions.setVisible(True)
                self.widget_definitions.setVisible(True)
                # Set text for first 2 fields
                self.lbl_word.setText(word)
                self.lbl_pronunciation.setText("Pronunciation: " + pronunciation)
                # Loop through definitions and add to parent widget
                for definition in definitions_list:
                    logging.debug(definition)
                    def_type = str(definition['type'])
                    def_text = str(definition['definition'])
                    def_example = str(definition['example'])
                    widget = Definition(def_type, def_text, def_example)
                    self.definitions_layout.addWidget(widget)
                logging.info("Definitions found!")
            else:
                error_msg = "Error " + str(response.status_code) + ": " + response.reason
                logging.error(error_msg)
                logging.error("Response: %s", response.text)
                self.lbl_word.setVisible(True)
                self.lbl_word.setText(response.reason)
        else:
            logging.warning("Input was invalid")
            self.lbl_word.setVisible(True)
            self.lbl_word.setText("Invalid Input!")

        self.input_search.setText("")
        # Adjust the size of the widget and call the callback function
        self.adjustSize()
        if self.lookup_callback is not None:
            self.lookup_callback()
