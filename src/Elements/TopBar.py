from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QFontDialog, QComboBox, QPushButton, QVBoxLayout, \
    QFontComboBox

from src.Elements.ColorWidget import Color


class TopBar(QWidget):
    def __init__(self, document):
        super(TopBar, self).__init__()
        self.doc = document
        self.horz = QHBoxLayout()
        self.horz.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.horz)

        #List for font sizes
        list_FontSize = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
                         "18", "19", "20", "22", "24", "26", "28", "36", "48", "72"]

        #ComboBox for font sizes
        self.fontComboBox = QFontComboBox()
        self.fontComboBox.setToolTip('Change font')
        self.horz.addWidget(self.fontComboBox)
        self.fontComboBox.currentIndexChanged.connect(self.fontChange)

        #Adds functionality to the ComboBox
        self.combo = QComboBox(self)
        self.combo.setToolTip('Change font size')
        self.combo.setGeometry(50, 50, 400, 35)
        self.combo.addItems(list_FontSize)
        self.combo.setCurrentIndex(11)
        self.combo.setFixedWidth(40)
        self.combo.currentIndexChanged.connect(self.selectionChange)
        self.horz.addWidget(self.combo)

        #Button press to make text bold
        self.button_bold = QPushButton("B", self)
        self.button_bold.setToolTip('Bold your text. "Ctrl+B"')
        self.button_bold.setShortcut('ctrl+b')
        self.button_bold.setFixedWidth(20)
        self.button_bold.setStyleSheet("font:Bold")
        self.button_bold.setCheckable(True)
        self.button_bold.clicked.connect(self.setBold)
        self.horz.addWidget(self.button_bold)

        #Button press to make text italic
        self.button_ital = QPushButton("I", self)
        self.button_ital.setToolTip('Italicise your text. "Ctrl+I"')
        self.button_ital.setShortcut('ctrl+i')
        self.button_ital.setFixedWidth(20)
        self.button_ital.setStyleSheet("font:Italic")
        self.button_ital.setCheckable(True)
        self.button_ital.clicked.connect(self.setItal)
        self.horz.addWidget(self.button_ital)

        #Button press to make text strikethrough
        self.button_strike = QPushButton("S", self)
        self.button_strike.setToolTip('Strikeout your text. "Ctrl+S"')
        self.button_strike.setShortcut('ctrl+s')
        self.button_strike.setFixedWidth(20)
        f = self.button_strike.font()
        f.setStrikeOut(True)
        self.button_strike.setFont(f)
        self.button_strike.setCheckable(True)
        self.button_strike.clicked.connect(self.setStrike)
        self.horz.addWidget(self.button_strike)

        #Button press to underline text
        self.button_under = QPushButton("U", self)
        self.button_under.setToolTip('Underline your text. "Ctrl+U"')
        self.button_under.setShortcut('ctrl+u')
        self.button_under.setFixedWidth(20)
        self.button_under.setStyleSheet("text-decoration: underline")
        self.button_under.setCheckable(True)
        self.button_under.clicked.connect(self.setUnder)
        self.horz.addWidget(self.button_under)

        #Temporary widgets
        self.horz.addWidget(Color("transparent"))
        self.horz.addWidget(Color("transparent"))
        self.horz.addWidget(Color("transparent"))
        self.horz.addWidget(Color("transparent"))

    #Sets the font to the new font
    def fontChange(self):
        self.doc.setCurrentFont(self.fontComboBox.currentFont())

    #Sets the current sets the font size from the ComboBox
    def selectionChange(self):
        self.doc.setFontPointSize(int(self.combo.currentText()))

    #Sets the font to italic
    def setItal(self):
        self.doc.setFontItalic(self.button_ital.isChecked())

    #Sets the font to bold
    def setBold(self):
        if self.button_bold.isChecked():
            self.doc.setFontWeight(75)
        else:
            self.doc.setFontWeight(25)

    #Sets the font to underlined
    def setUnder(self):
        self.doc.setFontUnderline(self.button_under.isChecked())

    #Sets the font to strike
    def setStrike(self):
        f = self.doc.currentCharFormat()
        f.setFontStrikeOut(self.button_strike.isChecked())
        self.doc.setCurrentCharFormat(f)


