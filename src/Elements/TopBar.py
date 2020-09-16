from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton, QFontComboBox


class TopBar(QWidget):
    def __init__(self, document):
        super(TopBar, self).__init__()
        self.document = document
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.horizontal_layout.setSpacing(3)
        self.setLayout(self.horizontal_layout)

        # List for font sizes
        list_FontSize = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
                         "18", "19", "20", "22", "24", "26", "28", "36", "48", "72"]

        # ComboBox for font sizes
        self.combo_font_style = QFontComboBox()
        self.combo_font_style.currentIndexChanged.connect(self.fontChange)
        self.horizontal_layout.addWidget(self.combo_font_style)

        # Adds functionality to the ComboBox
        self.combo_font_size = QComboBox(self)
        self.combo_font_size.addItems(list_FontSize)
        self.combo_font_size.setCurrentIndex(11)
        self.combo_font_size.currentIndexChanged.connect(self.selectionChange)
        self.horizontal_layout.addWidget(self.combo_font_size)

        # Button press to make text bold
        self.button_bold = QPushButton("B", self)
        self.button_bold.setStyleSheet("font:Bold")
        self.button_bold.setCheckable(True)
        self.button_bold.clicked.connect(self.setBold)
        self.horizontal_layout.addWidget(self.button_bold)

        # Button press to make text italic
        self.button_ital = QPushButton("I", self)
        self.button_ital.setStyleSheet("font:Italic")
        self.button_ital.setCheckable(True)
        self.button_ital.clicked.connect(self.setItal)
        self.horizontal_layout.addWidget(self.button_ital)

        # Button press to make text strikethrough
        self.button_strike = QPushButton("S", self)
        self.button_strike.setStyleSheet("text-decoration: line-through")
        self.button_strike.setCheckable(True)
        self.button_strike.clicked.connect(self.setStrike)
        self.horizontal_layout.addWidget(self.button_strike)

        # Button press to underline text
        self.button_under = QPushButton("U", self)
        self.button_under.setStyleSheet("text-decoration: underline")
        self.button_under.setCheckable(True)
        self.button_under.clicked.connect(self.setUnder)
        self.horizontal_layout.addWidget(self.button_under)

        # Temporary widgets
        self.horizontal_layout.addStretch()

    # Sets the font to the new font
    def fontChange(self):
        self.document.setCurrentFont(self.combo_font_style.currentFont())

    # Sets the current sets the font size from the ComboBox
    def selectionChange(self):
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
