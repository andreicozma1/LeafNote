import logging

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton, QFontComboBox, QDialogButtonBox

from Utils.DialogBuilder import DialogBuilder

"""
all properties of the top bar
"""


class TopBar(QWidget):
    """
    class that holds the top bar attributes
    """

    def __init__(self, document, doc_props):
        """
        sets up the top bar and its features
        :return: returns nothing
        """
        super(TopBar, self).__init__()
        logging.info("")
        self.document = document
        self.doc_props = doc_props

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.horizontal_layout.setSpacing(3)
        self.setLayout(self.horizontal_layout)

        document.selectionChanged.connect(self.updateFormatOnSelectionChange)
        document.currentCharFormatChanged.connect(self.updateFormatOnSelectionChange)

    def addLayoutSpacer(self):
        # Temporary widgets
        self.horizontal_layout.addStretch()

    def makeComboFontStyleBox(self) -> QFontComboBox:
        # ComboBox for font sizes
        self.combo_font_style = QFontComboBox(self)
        self.combo_font_style.setToolTip('Change font')
        self.combo_font_style.setFocusPolicy(Qt.NoFocus)
        self.combo_font_style.currentFontChanged.connect(self.document.onFontStyleChanged)
        self.combo_font_style.setCurrentFont(self.document.currentFont())
        self.horizontal_layout.addWidget(self.combo_font_style)
        return self.combo_font_style

    def makeComboFontSizeBox(self, list_FontSize) -> QComboBox:
        # Adds functionality to the ComboBox
        self.combo_font_size = QComboBox(self)
        self.combo_font_size.setToolTip('Change font size')
        self.combo_font_size.addItems(list_FontSize)
        self.combo_font_size.setFixedWidth(60)
        self.combo_font_size.setFocusPolicy(Qt.NoFocus)
        self.combo_font_size.setCurrentIndex(list_FontSize.index(str(self.document.font().pointSize())))
        self.combo_font_size.currentIndexChanged.connect(self.document.onFontSizeChanged)
        self.horizontal_layout.addWidget(self.combo_font_size)
        return self.combo_font_size

    def makeBtnBold(self) -> QPushButton:
        # Button press to make text bold
        self.button_bold = QPushButton("B", self)
        self.button_bold.setToolTip('Bold your text. "Ctrl+B"')
        self.button_bold.setFixedWidth(33)
        self.button_bold.setStyleSheet("QPushButton { font:Bold }")
        self.button_bold.setCheckable(True)
        self.button_bold.setFocusPolicy(Qt.NoFocus)
        self.button_bold.clicked.connect(self.document.onFontBoldChanged)
        self.horizontal_layout.addWidget(self.button_bold)
        return self.button_bold

    def makeBtnItal(self) -> QPushButton:
        # Button press to make text italic
        self.button_ital = QPushButton("I", self)
        self.button_ital.setToolTip('Italicise your text. "Ctrl+I"')
        self.button_ital.setFixedWidth(33)
        self.button_ital.setStyleSheet("QPushButton { font:Italic }")
        self.button_ital.setCheckable(True)
        self.button_ital.setFocusPolicy(Qt.NoFocus)
        self.button_ital.clicked.connect(self.document.onFontItalChanged)
        self.horizontal_layout.addWidget(self.button_ital)
        return self.button_ital

    def makeBtnStrike(self) -> QPushButton:
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
        return self.button_strike

    def makeBtnUnder(self) -> QPushButton:
        # Button press to underline text
        self.button_under = QPushButton("U", self)
        self.button_under.setToolTip('Underline your text. "Ctrl+U"')
        self.button_under.setFixedWidth(33)
        self.button_under.setStyleSheet("QPushButton { text-decoration: underline }")
        self.button_under.setCheckable(True)
        self.button_under.setFocusPolicy(Qt.NoFocus)
        self.button_under.clicked.connect(self.document.onFontUnderChanged)
        self.horizontal_layout.addWidget(self.button_under)
        return self.button_under

    def makeComboFontColor(self) -> QComboBox:
        # Button to change text color
        self.combo_text_color = QComboBox(self)
        color_list = self.doc_props.color_dict.values()

        def updateTextColor(index):
            self.combo_text_color.setStyleSheet(" QComboBox::drop-down { border: 0px;}"
                                                " QComboBox { background-color: " + list(color_list)[index] + ";" +
                                                "            border: 1px solid gray;"
                                                "            border-radius: 5px;"
                                                "            selection-background-color: rgba(0,0,0,0.2)}"
                                                " QComboBox QAbstractItemView { min-width:30px; }")

        self.combo_text_color.setFixedWidth(35)
        self.combo_text_color.setFixedHeight(20)
        model = self.combo_text_color.model()
        for i, c in enumerate(color_list):
            item = QtGui.QStandardItem()
            item.setBackground(QtGui.QColor(c))
            model.appendRow(item)
            self.combo_text_color.setItemData(i, c)
        self.combo_text_color.currentIndexChanged.connect(self.document.onTextColorChanged)
        self.combo_text_color.currentIndexChanged.connect(updateTextColor)
        self.combo_text_color.setFocusPolicy(Qt.NoFocus)
        self.combo_text_color.setToolTip("Change Text color.")
        self.combo_text_color.setStyleSheet(" QComboBox::drop-down { border: 0px;}"
                                            " QComboBox { background-color: black;"
                                            "            border: 1px solid gray;"
                                            "            border-radius: 5px;"
                                            "            selection-background-color: rgba(0,0,0,0.2)}"
                                            " QComboBox QAbstractItemView { min-width:30px; }")
        self.combo_text_color.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontal_layout.addWidget(self.combo_text_color)

        return self.combo_text_color

    def makeComboTextAlign(self) -> QComboBox:
        # Adds ability to change alignment of text
        self.combo_text_align = QComboBox(self)
        self.combo_text_align.setToolTip('Change text alignment')
        self.combo_text_align.addItems(self.doc_props.dict_align)
        self.combo_text_align.setFocusPolicy(Qt.NoFocus)
        self.combo_text_align.currentIndexChanged.connect(self.document.onTextAlignmentChanged)
        self.combo_text_align.setCurrentIndex(0)
        self.horizontal_layout.addWidget(self.combo_text_align)
        return self.combo_text_align

    def makeBtnFormatMode(self, callback) -> QPushButton:
        # Mode Switching button to the very right (after stretch)
        self.button_mode_switch = QPushButton("Formatting Mode", self)

        self.button_mode_switch.setToolTip("Enable Document Formatting")
        self.button_mode_switch.setProperty("persistent", True)  # Used to keep button enabled in setFormattingMode
        self.button_mode_switch.setCheckable(True)
        self.button_mode_switch.setFocusPolicy(Qt.NoFocus)
        self.button_mode_switch.clicked.connect(callback)
        self.horizontal_layout.addWidget(self.button_mode_switch)
        return self.button_mode_switch

    def setFormattingButtonsEnabled(self, state):
        """
        Sets all formatting options to Enabled or Disabled
        :param state: boolean that sets the states
        :return: returns nothing
        """
        # Toggle the state of all buttons in the menu
        logging.info(str(state))
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.setEnabled(state)

    def updateFormatOnSelectionChange(self):
        """
        Selected text format reflected in the TopBar
        :return: returns nothing
        """
        logging.info("Started updating")
        # Block signals
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(True)
        # Update the font style displayed
        self.combo_font_style.setCurrentFont(self.document.currentFont())
        # Update the font size displayed
        size = int(self.document.fontPointSize())
        if size != 0:
            self.combo_font_size.setCurrentIndex(self.doc_props.list_FontSize.index(str(size)))
        # Update extra formatting options
        self.button_ital.setChecked(self.document.fontItalic())
        self.button_under.setChecked(self.document.fontUnderline())
        self.button_bold.setChecked(self.document.fontWeight() == QFont.Bold)
        self.button_strike.setChecked(self.document.currentCharFormat().fontStrikeOut())
        # Update the text alignment
        align = self.document.alignment()
        self.combo_text_align.setCurrentIndex(list(self.doc_props.dict_align.values()).index(align))
        # Unblock signals
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(False)
        logging.info("Finished updating")

