import logging

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton, QFontComboBox

from Elements.Document import Document
from Layout.DocProps import DocProps

"""
all properties of the top bar
"""


class TopBar(QWidget):
    """
    class that holds the top bar attributes
    """

    def __init__(self):
        """
        sets up the top bar and its features
        :return: returns nothing
        """
        super(TopBar, self).__init__()
        logging.info("")

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.horizontal_layout.setSpacing(3)
        self.setLayout(self.horizontal_layout)

    def addLayoutSpacer(self):
        # Temporary widgets
        self.horizontal_layout.addStretch()

    def makeComboFontStyleBox(self, doc: Document) -> QFontComboBox:
        # ComboBox for font sizes
        self.combo_font_style = QFontComboBox(self)
        self.combo_font_style.setToolTip('Change font')
        self.combo_font_style.setFocusPolicy(Qt.NoFocus)
        self.combo_font_style.currentFontChanged.connect(doc.onFontStyleChanged)
        self.combo_font_style.setCurrentFont(doc.currentFont())
        self.horizontal_layout.addWidget(self.combo_font_style)
        return self.combo_font_style

    def makeComboFontSizeBox(self, doc: Document, list_FontSize) -> QComboBox:
        # Adds functionality to the ComboBox
        self.combo_font_size = QComboBox(self)
        self.combo_font_size.setToolTip('Change font size')
        self.combo_font_size.addItems(list_FontSize)
        self.combo_font_size.setFixedWidth(60)
        self.combo_font_size.setFocusPolicy(Qt.NoFocus)
        self.combo_font_size.currentIndexChanged.connect(doc.onFontSizeChanged)
        self.combo_font_size.setCurrentIndex(11)
        self.horizontal_layout.addWidget(self.combo_font_size)
        return self.combo_font_size

    def makeBtnBold(self, doc: Document) -> QPushButton:
        # Button press to make text bold
        self.button_bold = QPushButton("B", self)
        self.button_bold.setToolTip('Bold your text. "Ctrl+B"')
        self.button_bold.setFixedWidth(33)
        self.button_bold.setStyleSheet("QPushButton { font:Bold }")
        self.button_bold.setCheckable(True)
        self.button_bold.setFocusPolicy(Qt.NoFocus)
        self.button_bold.clicked.connect(doc.onFontBoldChanged)
        self.horizontal_layout.addWidget(self.button_bold)
        return self.button_bold

    def makeBtnItal(self, doc: Document) -> QPushButton:
        # Button press to make text italic
        self.button_ital = QPushButton("I", self)
        self.button_ital.setToolTip('Italicise your text. "Ctrl+I"')
        self.button_ital.setFixedWidth(33)
        self.button_ital.setStyleSheet("QPushButton { font:Italic }")
        self.button_ital.setCheckable(True)
        self.button_ital.setFocusPolicy(Qt.NoFocus)
        self.button_ital.clicked.connect(doc.onFontItalChanged)
        self.horizontal_layout.addWidget(self.button_ital)
        return self.button_ital

    def makeBtnStrike(self, doc: Document) -> QPushButton:
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
        self.button_strike.clicked.connect(doc.onFontStrikeChanged)
        self.horizontal_layout.addWidget(self.button_strike)
        return self.button_strike

    def makeBtnUnder(self, doc: Document) -> QPushButton:
        # Button press to underline text
        self.button_under = QPushButton("U", self)
        self.button_under.setToolTip('Underline your text. "Ctrl+U"')
        self.button_under.setFixedWidth(33)
        self.button_under.setStyleSheet("QPushButton { text-decoration: underline }")
        self.button_under.setCheckable(True)
        self.button_under.setFocusPolicy(Qt.NoFocus)
        self.button_under.clicked.connect(doc.onFontUnderChanged)
        self.horizontal_layout.addWidget(self.button_under)
        return self.button_under

    def makeComboFontColor(self, doc: Document, color_dict) -> QComboBox:
        # Button to change text color
        self.combo_text_color = QComboBox(self)
        color_list = color_dict.values()

        def updateTextColor(index):
            self.combo_text_color.setStyleSheet(" QComboBox::drop-down { border: 0px;}"
                                                " QComboBox { background-color: " + list(color_list)[index] + ";"
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
        self.combo_text_color.currentIndexChanged.connect(doc.onTextColorChanged)
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

    def makeComboTextAlign(self, doc: Document, list_alignments) -> QComboBox:
        # Adds ability to change alignment of text
        self.combo_text_align = QComboBox(self)
        self.combo_text_align.setToolTip('Change text alignment')
        self.combo_text_align.addItems(list_alignments)
        self.combo_text_align.setFixedWidth(100)
        self.combo_text_align.setFocusPolicy(Qt.NoFocus)
        self.combo_text_align.currentIndexChanged.connect(doc.onTextAlignmentChanged)
        self.combo_text_align.setCurrentIndex(0)
        self.horizontal_layout.addWidget(self.combo_text_align)
        return self.combo_text_align

    def makeBtnFormatMode(self, onEnableFormatting) -> QPushButton:
        # Mode Switching button to the very right (after stretch)
        self.button_mode_switch = QPushButton("Formatting Mode", self)
        self.button_mode_switch.setToolTip("Enable Document Formatting")
        self.button_mode_switch.setProperty("persistent", True)  # Used to keep button enabled in setFormattingMode
        self.button_mode_switch.setCheckable(True)
        self.button_mode_switch.setFocusPolicy(Qt.NoFocus)
        self.button_mode_switch.clicked.connect(onEnableFormatting)
        self.horizontal_layout.addWidget(self.button_mode_switch)
        return self.button_mode_switch

    def setFormattingButtonsEnabled(self, state):
        """
        allows formatting once file type is changed from .txt to .lef in top bar
        :param state: this is a boolean that sets the states
        :return: returns nothing
        """
        logging.info(str(state))
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.setEnabled(state)

    def updateFormatOnSelectionChange(self, doc: Document, doc_props: DocProps):
        """
        selected text format will be checked in top bar
        :return: returns nothing
        """
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(True)

        self.combo_font_style.setCurrentFont(doc.currentFont())

        size = int(doc.fontPointSize())
        if size != 0:
            self.combo_font_size.setCurrentIndex(doc_props.list_FontSize.index(str(size)))

        # update the top bar alignment to the current alignment
        align = doc.alignment()
        self.combo_text_align.setCurrentIndex(doc_props.list_alignments_align.index(align))

        self.button_ital.setChecked(doc.fontItalic())
        self.button_under.setChecked(doc.fontUnderline())
        self.button_bold.setChecked(doc.fontWeight() == QFont.Bold)
        self.button_strike.setChecked(doc.currentCharFormat().fontStrikeOut())

        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(False)
