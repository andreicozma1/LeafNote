from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton, QFontComboBox, QDialogButtonBox

from Utils.DialogBuilder import DialogBuilder
import logging

class TopBar(QWidget):
    def __init__(self, app, document):
        super(TopBar, self).__init__()
        logging.info("")
        self.app = app
        self.document = document

        self.horizontal_layout = QHBoxLayout()

        # color dictionary for changing text color
        self.color_dict = {
            'black': '#000000',
            'red': '#ff0000',
            'pink': '#ffc0cb',
            'orange': '#ffa500',
            'yellow': '#ffff00',
            'green': '#00ff00',
            'blue': '#0000ff',
            'violet': '#9400D3',
            'brown': '#a52a3a',
            'white': '#ffffff'
        }

        # List for font sizes
        self.list_FontSize = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
                              "17", "18", "19", "20", "22", "24", "26", "28", "36", "48", "72"]

        # ComboBox for font sizes
        self.combo_font_style = QFontComboBox(self)
        self.combo_font_style.setToolTip('Change font')
        self.combo_font_style.setFocusPolicy(Qt.NoFocus)
        self.combo_font_style.currentFontChanged.connect(self.onFontStyleChanged)
        self.combo_font_style.setCurrentFont(self.document.currentFont())
        self.horizontal_layout.addWidget(self.combo_font_style)

        # Adds functionality to the ComboBox
        self.combo_font_size = QComboBox(self)
        self.combo_font_size.setToolTip('Change font size')
        self.combo_font_size.addItems(self.list_FontSize)
        self.combo_font_size.setFixedWidth(60)
        self.combo_font_size.setFocusPolicy(Qt.NoFocus)
        self.combo_font_size.currentIndexChanged.connect(self.onFontSizeChanged)
        self.combo_font_size.setCurrentIndex(11)
        self.horizontal_layout.addWidget(self.combo_font_size)

        # Button press to make text bold
        self.button_bold = QPushButton("B", self)
        self.button_bold.setToolTip('Bold your text. "Ctrl+B"')
        self.button_bold.setFixedWidth(33)
        self.button_bold.setStyleSheet("QPushButton { font:Bold }")
        self.button_bold.setCheckable(True)
        self.button_bold.setFocusPolicy(Qt.NoFocus)
        self.button_bold.clicked.connect(self.document.onFontBoldChanged)
        self.horizontal_layout.addWidget(self.button_bold)

        # Button press to make text italic
        self.button_ital = QPushButton("I", self)
        self.button_ital.setToolTip('Italicise your text. "Ctrl+I"')
        self.button_ital.setFixedWidth(33)
        self.button_ital.setStyleSheet("QPushButton { font:Italic }")
        self.button_ital.setCheckable(True)
        self.button_ital.setFocusPolicy(Qt.NoFocus)
        self.button_ital.clicked.connect(self.document.onFontItalChanged)
        self.horizontal_layout.addWidget(self.button_ital)

        # Button press to make text strikethrough
        self.button_strike = QPushButton("S", self)
        self.button_strike.setToolTip('Strikeout your text. "Ctrl+S"')
        self.button_strike.setFixedWidth(33)
        f = self.button_strike.font()
        f.setStrikeOut(True)
        self.button_strike.setFont(f)
        # self.button_strike.adjustSize()
        self.button_strike.setStyleSheet("QPushButton { text-decoration: line-through }")
        self.button_strike.setCheckable(True)
        self.button_strike.setFocusPolicy(Qt.NoFocus)
        self.button_strike.clicked.connect(self.document.onFontStrikeChanged)
        self.horizontal_layout.addWidget(self.button_strike)

        # Button press to underline text
        self.button_under = QPushButton("U", self)
        self.button_under.setToolTip('Underline your text. "Ctrl+U"')
        self.button_under.setFixedWidth(33)
        self.button_under.setStyleSheet("QPushButton { text-decoration: underline }")
        self.button_under.setCheckable(True)
        self.button_under.setFocusPolicy(Qt.NoFocus)
        self.button_under.clicked.connect(self.document.onFontUnderChanged)
        self.horizontal_layout.addWidget(self.button_under)

        # Button to change text color
        self.combo_text_color = QComboBox(self)
        self.combo_text_color.setFixedWidth(33)
        self.combo_text_color.setFixedHeight(20)
        model = self.combo_text_color.model()
        self.color_list = self.color_dict.values()
        for i, c in enumerate(self.color_list):
            item = QtGui.QStandardItem()
            item.setBackground(QtGui.QColor(c))
            model.appendRow(item)
            self.combo_text_color.setItemData(i, c)
        self.combo_text_color.currentIndexChanged.connect(self.setColorChange)
        self.combo_text_color.setFocusPolicy(Qt.NoFocus)
        self.combo_text_color.setToolTip("Change Text color.")
        self.combo_text_color.setStyleSheet(" QComboBox::drop-down { border: 0px;}"
                                      " QComboBox { background-color: black;"
                                      "            border: 1px solid gray; }"
                                      " QComboBox QAbstractItemView { selection-background-color: none; }/")
        self.combo_text_color.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontal_layout.addWidget(self.combo_text_color)

        # Temporary widgets
        self.horizontal_layout.addStretch()

        # Mode Switching button to the very right (after stretch)
        self.button_mode_switch = QPushButton("Formatting Mode", self)
        self.button_mode_switch.setToolTip("Enable Document Formatting")
        self.button_mode_switch.setProperty("persistent", True)  # Used to keep button enabled in onEnableFormatting
        self.button_mode_switch.setCheckable(True)
        self.button_mode_switch.setFocusPolicy(Qt.NoFocus)
        self.button_mode_switch.clicked.connect(self.onEnableFormatting)
        self.horizontal_layout.addWidget(self.button_mode_switch)

        self.setup()

    def setup(self):
        logging.info("setup")

        # TODO - Keep object definitions in constructor and move all method calls in setup
        self.setFormattingEnabled(False)

        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.horizontal_layout.setSpacing(3)

        self.setLayout(self.horizontal_layout)

        self.document.selectionChanged.connect(self.updateFormatOnSelectionChange)

        return self

    # Toggles between Formatting Mode and Plain-Text Mode
    def onEnableFormatting(self, state):
        logging.info(str(state))

        if state is True:
            convert_dialog = DialogBuilder(self.app, "Enable Formatting",
                                           "Would you like to convert this file?",
                                           "This file needs to be converted to use enriched text formatting features\n"
                                           "Selecting 'Yes' will convert the original "
                                           "file to the enriched text file format.")
            buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
            convert_dialog.addButtonBox(buttonBox)
            if convert_dialog.exec():
                logging.info("User converted file to Proprietary Format")
                # TODO - Convert file with FileManager to a .lef format, on success, call the function below
                self.app.file_manager.toLef()
                self.setFormattingEnabled(True)
            else:
                logging.info("User DID NOT convert file to Proprietary Format")
                self.button_mode_switch.setChecked(False)
        else:
            # Don't allow converted file to be converted back to Plain Text
            # TODO - allow option to save different file as plain text, or allow conversion back but discard formatting options

            self.app.file_manager.lefToExt()
            logging.info("Cannot convert back to Plain Text")
            self.button_mode_switch.setChecked(True)

    def setFormattingEnabled(self, state):
        """
        :param state: this is a boolean that sets the states
        """
        logging.info(str(state))
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.setEnabled(state)

    # Sets the font to the new font
    def onFontStyleChanged(self):
        logging.info(self.combo_font_style.currentFont())
        self.document.setCurrentFont(self.combo_font_style.currentFont())

    # Sets the current sets the font size from the ComboBox
    def onFontSizeChanged(self):
        logging.info(self.combo_font_size.currentText())
        self.document.setFontPointSize(int(self.combo_font_size.currentText()))

    def updateFormatOnSelectionChange(self):
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(True)

        self.combo_font_style.setCurrentFont(self.document.currentFont())

        size = int(self.document.fontPointSize())
        if size != 0:
            self.combo_font_size.setCurrentIndex(self.list_FontSize.index(str(size)))

        self.button_ital.setChecked(self.document.fontItalic())
        self.button_under.setChecked(self.document.fontUnderline())
        self.button_bold.setChecked(self.document.fontWeight() == QFont.Bold)
        self.button_strike.setChecked(self.document.currentCharFormat().fontStrikeOut())

        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(False)

    def setColorChange(self, index):
        setcolor = "  QComboBox::drop-down          {   border: 0px;}"
        setcolor += " QComboBox                     {   background-color:" + self.combo_text_color.itemData(index) + ";"
        setcolor += "                                   border: 1px solid gray; }"
        setcolor += " QComboBox QAbstractItemView   {   selection-background-color: none; }"
        self.combo_text_color.setStyleSheet(setcolor)
        self.document.setTextColor(QColor(self.combo_text_color.itemData(index)))
