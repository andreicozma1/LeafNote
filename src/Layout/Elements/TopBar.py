"""
all properties of the top bar
"""

import html
import logging
import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QStandardItem
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton, QFontComboBox, \
    QSizePolicy, QListView

from Layout.Elements import Document


class TopBar(QWidget):
    """
    class that holds the top bar attributes
    """

    def __init__(self, path_res: str, document: Document):
        """
        sets up the top bar and its features
        :return: returns nothing
        """
        super().__init__()
        logging.debug("Creating Top Bar")
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
        self.dict_color = None
        self.combo_text_align = None
        self.dict_text_align = None
        self.dict_align = None

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
        """
        Create Title Style Drop Down
        """
        # ComboBox for title style
        self.combo_title_style = QComboBox(self)
        view = QListView(self.combo_title_style)
        view.setStyleSheet("QListView::item { height : 18 px }")
        self.combo_title_style.setView(view)
        self.dict_title_style = dict_title_style
        self.combo_title_style.setToolTip('Styles')
        self.combo_title_style.addItems(self.dict_title_style)
        # traverses through combo_title_style items index
        for x in range(view.model().rowCount()):
            # mods by two to get the index with titles else gives "update" titles index
            # changes font to be bold for if and italic for else
            if x % 2 == 0:
                font = QFont()
                font.setWeight(QFont.Bold)
                self.combo_title_style.setItemData(x, font, Qt.FontRole)
            else:
                font = QFont()
                color = QBrush()
                font.setItalic(True)
                color.setColor(QColor("gray"))
                self.combo_title_style.setItemData(x, font, Qt.FontRole)
                self.combo_title_style.setItemData(x, color, Qt.ForegroundRole)
        # adds separators to clean up look of QComboBox
        for x in range(2, 23, 3):
            size = QSize()
            size.setHeight(7)
            separator = QStandardItem()
            separator.setSizeHint(size)
            view.model().insertRow(x, separator)
        self.combo_title_style.setFocusPolicy(Qt.NoFocus)
        self.combo_title_style.setMaxVisibleItems(view.model().rowCount())
        self.combo_title_style.textActivated.connect(self.document.onTitleStyleChanged)
        return self.combo_title_style

    def makeComboFontStyleBox(self) -> QFontComboBox:
        """
        Create Font Style DropDown
        """
        # ComboBox for font sizes
        self.combo_font_style = QFontComboBox(self)
        self.combo_font_style.setToolTip('Change font')
        self.combo_font_style.setFocusPolicy(Qt.NoFocus)
        self.combo_font_style.currentFontChanged.connect(self.document.onFontStyleChanged)
        self.combo_font_style.setCurrentFont(self.document.currentFont())
        return self.combo_font_style

    def makeComboFontSizeBox(self, list_font_size: list) -> QComboBox:
        """
        Create Font Size Dropdown
        """
        # Adds functionality to the ComboBox
        self.combo_font_size = QComboBox(self)
        self.list_font_size = list_font_size
        self.combo_font_size.setToolTip('Change font size')
        self.combo_font_size.addItems(self.list_font_size)
        self.combo_font_size.setFixedWidth(60)
        self.combo_font_size.setFocusPolicy(Qt.NoFocus)
        self.combo_font_size.setCurrentIndex(
            self.list_font_size.index(str(self.document.font().pointSize())))
        self.combo_font_size.currentTextChanged.connect(self.document.onFontSizeChanged)
        return self.combo_font_size

    def makeBtnBold(self) -> QPushButton:
        """
        Create Bold Btn
        """
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
        """
        Create Ital Btn
        """
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
        """
        Create Strike Btn
        """
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
        """
        Create Underline Button
        """
        # Button press to underline text
        self.button_under = QPushButton("U", self)
        self.button_under.setToolTip('Underline your text. "Ctrl+U"')
        self.button_under.setFixedWidth(33)
        self.button_under.setStyleSheet("QPushButton { text-decoration: underline }")
        self.button_under.setCheckable(True)
        self.button_under.setFocusPolicy(Qt.NoFocus)
        self.button_under.clicked.connect(self.document.onFontUnderChanged)
        return self.button_under

    def updateTextColor(self, index):
        """
        Updates styles for font color
        """
        color_list = list(self.dict_color.values())
        style = "QComboBox::drop-down { border: 0px;}" \
                "QComboBox { background-color: " + list(color_list)[index] + ";" + \
                "border: 1px solid gray;" \
                "border-radius: 5px;" \
                "selection-background-color: rgba(0,0,0,0.2)}" \
                "QComboBox QAbstractItemView { min-width:30px; }"
        self.combo_text_color.setStyleSheet(style)

    def makeComboFontColor(self, color_dict: dict) -> QComboBox:
        """
        Create Font Color Dropdown
        """
        # Button to change text color
        self.combo_text_color = QComboBox(self)
        self.dict_color = color_dict
        color_list = self.dict_color.values()
        self.combo_text_color.setFixedWidth(35)
        self.combo_text_color.setFixedHeight(20)
        model = self.combo_text_color.model()
        for i, c in enumerate(color_list):
            item = QtGui.QStandardItem()
            item.setBackground(QtGui.QColor(c))
            model.appendRow(item)
            self.combo_text_color.setItemData(i, c)
        self.combo_text_color.currentIndexChanged.connect(self.document.onTextColorChanged)
        self.combo_text_color.currentIndexChanged.connect(self.updateTextColor)
        self.combo_text_color.setFocusPolicy(Qt.NoFocus)
        self.combo_text_color.setToolTip("Change Text color.")
        self.combo_text_color.setStyleSheet("QComboBox::drop-down { border: 0px;}"
                                            "QComboBox { background-color: black;"
                                            "            border: 1px solid gray;"
                                            "            border-radius: 5px;"
                                            "selection-background-color: rgba(0,0,0,0.2)} "
                                            "QComboBox QAbstractItemView { min-width:30px; }")
        self.combo_text_color.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        return self.combo_text_color

    def makeClearFormatting(self) -> QPushButton:
        """
        Create Clear Formatting Button
        """
        # Button to Clear Formatting
        path_clear_icon = os.path.join(self.path_res, "clear_formatting.ico")
        button_clear = QPushButton(self)
        button_clear.setIcon(QIcon(path_clear_icon))
        button_clear.setToolTip('Clear Formatting. "Ctrl+0"')
        button_clear.setFixedWidth(33)
        button_clear.setFocusPolicy(Qt.NoFocus)
        button_clear.clicked.connect(self.document.clearSelectionFormatting)
        return button_clear

    def makeComboTextAlign(self, dict_align: dict) -> QComboBox:
        """
        Create Text Alignment Dropdown
        """
        # Adds ability to change alignment of text
        self.combo_text_align = QComboBox(self)
        self.dict_align = dict_align
        self.combo_text_align.setToolTip('Change text alignment')
        self.combo_text_align.addItems(self.dict_align)
        self.combo_text_align.setFocusPolicy(Qt.NoFocus)
        self.combo_text_align.currentIndexChanged.connect(self.document.onTextAlignmentChanged)
        self.combo_text_align.setCurrentIndex(0)
        return self.combo_text_align

    def makeBulletList(self) -> QPushButton:
        """
        Create Bullet List Dropdown
        """
        # Adds ability to change alignment of text
        button_bullet_list = QPushButton(html.unescape('&#8226;'), self)
        button_bullet_list.setToolTip('Bulleted List')
        button_bullet_list.setFixedWidth(33)
        button_bullet_list.setFocusPolicy(Qt.NoFocus)
        button_bullet_list.clicked.connect(self.document.bulletList)
        return button_bullet_list

    def makeBtnFormatMode(self, callback) -> QPushButton:
        """
        Create Enable Format Mode Button
        """
        # Mode Switching button to the very right (after stretch)
        button_mode_switch = QPushButton("Formatting Mode", self)

        button_mode_switch.setToolTip("Enable Document Formatting")
        button_mode_switch.setProperty("persistent",
                                       True)  # Used to keep button enabled in setFormattingMode
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
        # noinspection PyCompatibility
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
        # noinspection PyCompatibility
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(True)

        if self.combo_title_style is not None:
            title = self.document.currentCharFormat()
            index = 0
            title_list = list(self.dict_title_style.values())
            # adds separator slots to the list to make the index match the list in topbar
            for x in range(2, 23, 3):
                title_list.insert(x, None)
            if title in title_list:
                index = title_list.index(title)
            self.combo_title_style.setCurrentIndex(index)

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
        # update the text color
        if self.combo_text_color is not None:
            color = self.document.currentCharFormat().foreground().color().name()
            index = 0
            color_list = list(self.dict_color.values())
            if color in color_list:
                index = color_list.index(color)
            self.updateTextColor(index)

        # Update the text alignment
        if self.combo_text_align is not None:
            align = self.document.alignment()
            align_list = list(self.dict_align.values())
            if align in align_list:
                align_index = align_list.index(align)
                self.combo_text_align.setCurrentIndex(align_index)
        # Unblock signals
        # noinspection PyCompatibility
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(False)
