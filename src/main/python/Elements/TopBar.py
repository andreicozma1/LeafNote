from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGridLayout, QWidget, QHBoxLayout, QComboBox, QPushButton, QFontComboBox, QColorDialog, \
    QFrame, QToolButton
from PyQt5.QtCore import Qt


class TopBar(QWidget):
    def __init__(self, document):
        super(TopBar, self).__init__()
        self.document = document
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.horizontal_layout.setSpacing(3)
        self.setLayout(self.horizontal_layout)

        # color dictionary for changing text color
        self.color_dict = {
            'red': '#ff0000',
            'green': '#00ff00',
            'blue': '#0000ff',
            'yellow': '#ffff00',
            'gold': '#ffd700',
            'pink': '#ffc0cb',
            'bisque': '#ffe4c4',
            'ivory': '#fffff0',
            'black': '#000000',
            'white': '#ffffff',
            'violet': '#ee82ee',
            'silver': '#c0c0c0',
            'forestgreen': '#228b22',
            'brown': '#a52a3a',
            'chocolate': '#d2691e',
            'azure': '#fffff0',
            'orange': '#ffa500'
        }

        # List for font sizes
        list_FontSize = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
                         "18", "19", "20", "22", "24", "26", "28", "36", "48", "72"]

        # ComboBox for font sizes
        self.combo_font_style = QFontComboBox()
        self.combo_font_style.setToolTip('Change font')
        self.combo_font_style.currentIndexChanged.connect(self.fontChange)
        self.combo_font_style.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.combo_font_style)

        # Adds functionality to the ComboBox
        self.combo_font_size = QComboBox(self)
        self.combo_font_size.setToolTip('Change font size')
        self.combo_font_size.addItems(list_FontSize)
        self.combo_font_size.setCurrentIndex(11)
        self.combo_font_size.setFixedWidth(60)
        self.combo_font_size.currentIndexChanged.connect(self.fontSizeChange)
        self.combo_font_size.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.combo_font_size)

        # Button press to make text bold
        self.button_bold = QPushButton("B", self)
        self.button_bold.setToolTip('Bold your text. "Ctrl+B"')
        self.button_bold.setShortcut('ctrl+b')
        self.button_bold.setFixedWidth(33)
        self.button_bold.setStyleSheet("QPushButton { font:Bold }")
        self.button_bold.setCheckable(True)
        self.button_bold.clicked.connect(self.setBold)
        self.button_bold.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.button_bold)

        # Button press to make text italic
        self.button_ital = QPushButton("I", self)
        self.button_ital.setToolTip('Italicise your text. "Ctrl+I"')
        self.button_ital.setShortcut('ctrl+i')
        self.button_ital.setFixedWidth(33)
        self.button_ital.setStyleSheet("QPushButton { font:Italic }")
        self.button_ital.setCheckable(True)
        self.button_ital.clicked.connect(self.setItal)
        self.button_ital.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.button_ital)

        # Button press to make text strikethrough
        self.button_strike = QPushButton("S", self)
        self.button_strike.setToolTip('Strikeout your text. "Ctrl+S"')
        self.button_strike.setShortcut('alt+shift+5')
        self.button_strike.setFixedWidth(33)
        f = self.button_strike.font()
        f.setStrikeOut(True)
        self.button_strike.setFont(f)
        # self.button_strike.adjustSize()
        self.button_strike.setStyleSheet("QPushButton { text-decoration: line-through }")
        self.button_strike.setCheckable(True)
        self.button_strike.clicked.connect(self.setStrike)
        self.button_strike.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.button_strike)

        # Button press to underline text
        self.button_under = QPushButton("U", self)
        self.button_under.setToolTip('Underline your text. "Ctrl+U"')
        self.button_under.setShortcut('ctrl+u')
        self.button_under.setFixedWidth(33)
        # self.button_under.resize(self.button_under.minimumSize())
        self.button_under.setStyleSheet("QPushButton { text-decoration: underline }")
        self.button_under.setCheckable(True)
        self.button_under.clicked.connect(self.setUnder)
        self.button_under.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.button_under)

        # Button to change text color
        self.text_color = QComboBox(self)
        self.text_color.setFixedWidth(33)
        self.text_color.setFixedHeight(20)
        model = self.text_color.model()
        self.color_list = sorted(self.color_dict.values())
        for i, c in enumerate(self.color_list):
            print(c)
            item = QtGui.QStandardItem()
            item.setBackground(QtGui.QColor(c))
            model.appendRow(item)
            self.text_color.setItemData(i, c)
        self.text_color.currentIndexChanged.connect(self.setColorChange)
        self.text_color.setFocusPolicy(Qt.NoFocus)
        self.text_color.setToolTip("Change Text color.")
        self.text_color.setStyleSheet(" QComboBox::drop-down { border: 0px;}"
                                      " QComboBox { background-color: black;"
                                      "            border: 1px solid gray; }"
                                      " QComboBox QAbstractItemView { selection-background-color: none; }/")
        self.text_color.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontal_layout.addWidget(self.text_color)

        # Temporary widgets
        self.horizontal_layout.addStretch()

    # Sets the font to the new font
    def fontChange(self):
        self.document.setCurrentFont(self.combo_font_style.currentFont())

    # Sets the current sets the font size from the ComboBox
    def fontSizeChange(self):
        self.document.setFontPointSize(int(self.combo_font_size.currentText()))

    # Sets the font to italic
    def setItal(self):
        self.document.setFontItalic(self.button_ital.isChecked())

    # Sets the font to bold
    def setBold(self):
        if self.button_bold.isChecked():
            self.document.setFontWeight(75)
        else:
            self.document.setFontWeight(25)

    # Sets the font to underlined
    def setUnder(self):
        self.document.setFontUnderline(self.button_under.isChecked())

    # Sets the font to strike
    def setStrike(self):
        f = self.document.currentCharFormat()
        f.setFontStrikeOut(self.button_strike.isChecked())
        self.document.setCurrentCharFormat(f)

    def setColorChange(self, index):
        print(index)
        print(self.text_color.itemData(index))
        setcolor = "  QComboBox::drop-down          {   border: 0px;}"
        setcolor += " QComboBox                     {   background-color:" + self.text_color.itemData(index) + ";"
        setcolor += "                                   border: 1px solid gray; }"
        setcolor += " QComboBox QAbstractItemView   {   selection-background-color: none; }"
        self.text_color.setStyleSheet(setcolor)
        self.document.setTextColor(QColor(self.text_color.itemData(index)))
