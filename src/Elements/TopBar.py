import logging
import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton, QFontComboBox, QSizePolicy

from Elements import Document

"""
all properties of the top bar
"""


class TopBar(QWidget):
    """
    class that holds the top bar attributes
    """

    def __init__(self, path_res: str, document: Document):
        """
        sets up the top bar and its features
        :return: returns nothing
        """
        super(TopBar, self).__init__()
        logging.info("")
        self.path_res = path_res
        self.document = document

        self.combo_title_style = None
        self.dict_title_style = None
        self.combo_font_style = None
        self.combo_font_size = None
        self.list_font_size = None
        self.button_bold = None
        self.button_ital = None
        self.button_strike = None
        self.button_under = None
        self.combo_text_color = None
        self.dict_text_color = None
        self.combo_text_align = None
        self.dict_text_align = None

    def makeMainLayout(self):
        """
        You can get the layout generated with self.layout()
        :return: the main layout of the top bar
        """
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(10, 0, 10, 0)
        horizontal_layout.setSpacing(3)
        self.setLayout(horizontal_layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        return horizontal_layout

    def makeTitleStyleBox(self, dict_title_style: list) -> QComboBox:
        # ComboBox for title style
        self.combo_title_style = QComboBox(self)
        self.dict_title_style = dict_title_style
        self.combo_title_style.setToolTip('Styles')
        self.combo_title_style.addItems(self.dict_title_style)
        self.combo_title_style.setFocusPolicy(Qt.NoFocus)
        self.combo_title_style.textActivated.connect(self.document.onTitleStyleChanged)
        return self.combo_title_style

    def makeComboFontStyleBox(self) -> QFontComboBox:
        # ComboBox for font sizes
        self.combo_font_style = QFontComboBox(self)
        self.combo_font_style.setToolTip('Change font')
        self.combo_font_style.setFocusPolicy(Qt.NoFocus)
        self.combo_font_style.currentFontChanged.connect(self.document.onFontStyleChanged)
        self.combo_font_style.setCurrentFont(self.document.currentFont())
        return self.combo_font_style

    def makeComboFontSizeBox(self, list_font_size: list) -> QComboBox:
        # Adds functionality to the ComboBox
        self.combo_font_size = QComboBox(self)
        self.list_font_size = list_font_size
        self.combo_font_size.setToolTip('Change font size')
        self.combo_font_size.addItems(self.list_font_size)
        self.combo_font_size.setFixedWidth(60)
        self.combo_font_size.setFocusPolicy(Qt.NoFocus)
        self.combo_font_size.setCurrentIndex(self.list_font_size.index(str(self.document.font().pointSize())))
        self.combo_font_size.currentTextChanged.connect(self.document.onFontSizeChanged)
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
        return self.button_under

    def makeComboFontColor(self, color_dict: dict) -> QComboBox:
        # Button to change text color
        self.combo_text_color = QComboBox(self)
        self.dict_color = color_dict
        color_list = self.dict_color.values()

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

        return self.combo_text_color

    def makeClearFormatting(self) -> QPushButton:
        # Button to Clear Formatting
        path_clear_icon = os.path.join(self.path_res, "clear_formatting.ico")
        self.button_clear = QPushButton(self)
        self.button_clear.setIcon(QIcon(path_clear_icon))
        self.button_clear.setToolTip('Clear Formatting. "Ctrl+0"')
        self.button_clear.setFixedWidth(33)
        self.button_clear.setFocusPolicy(Qt.NoFocus)
        self.button_clear.clicked.connect(self.document.clearSelectionFormatting)
        return self.button_clear

    def makeComboTextAlign(self, dict_align: dict) -> QComboBox:
        # Adds ability to change alignment of text
        self.combo_text_align = QComboBox(self)
        self.dict_align = dict_align
        self.combo_text_align.setToolTip('Change text alignment')
        self.combo_text_align.addItems(self.dict_align)
        self.combo_text_align.setFocusPolicy(Qt.NoFocus)
        self.combo_text_align.currentIndexChanged.connect(self.document.onTextAlignmentChanged)
        self.combo_text_align.setCurrentIndex(0)
        return self.combo_text_align

    def makeBtnFormatMode(self, callback) -> QPushButton:
        # Mode Switching button to the very right (after stretch)
        button_mode_switch = QPushButton("Formatting Mode", self)

        button_mode_switch.setToolTip("Enable Document Formatting")
        button_mode_switch.setProperty("persistent", True)  # Used to keep button enabled in setFormattingMode
        button_mode_switch.setCheckable(True)
        button_mode_switch.setFocusPolicy(Qt.NoFocus)
        button_mode_switch.clicked.connect(callback)
        return button_mode_switch

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
        # Block signals
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(True)

        # TODO: check if self.list_title is not none then set qcombobox to current cursor selection

        # Update the font style displayed
        if self.combo_font_style is not None:
            self.combo_font_style.setCurrentFont(self.document.currentFont())
        # Update the font size displayed
        if self.combo_font_size is not None:
            size = int(self.document.currentCharFormat().fontPointSize())
            if size != 0:
                size_index = self.list_font_size.index(str(size))
                self.combo_font_size.setCurrentIndex(size_index)
        # Update extra formatting options
        if self.button_ital is not None:
            self.button_ital.setChecked(self.document.fontItalic())
        if self.button_under is not None:
            self.button_under.setChecked(self.document.fontUnderline())
        if self.button_bold is not None:
            self.button_bold.setChecked(self.document.fontWeight() == QFont.Bold)
        if self.button_strike is not None:
            self.button_strike.setChecked(self.document.currentCharFormat().fontStrikeOut())
        # Update the text alignment
        if self.combo_text_align is not None:
            align = self.document.alignment()
            align_list = list(self.dict_align.values())
            if align in align_list:
                align_index = align_list.index(align)
                self.combo_text_align.setCurrentIndex(align_index)
        # Unblock signals
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(False)
