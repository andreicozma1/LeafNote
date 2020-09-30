from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton, QFontComboBox, QDialogButtonBox
from PyQt5.QtGui import QFont
from Utils.DialogBuilder import DialogBuilder


class TopBar(QWidget):
    def __init__(self, app):
        super(TopBar, self).__init__()
        print('TopBar - init')
        self.app = app
        self.document = app.document

        self.horizontal_layout = QHBoxLayout()

        # List for font sizes
        self.list_FontSize = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
                              "17", "18", "19", "20", "22", "24", "26", "28", "36", "48", "72"]

        # ComboBox for font sizes
        self.combo_font_style = QFontComboBox(self)
        self.combo_font_style.setToolTip('Change font')
        self.combo_font_style.setFocusPolicy(Qt.NoFocus)
        self.combo_font_style.setCurrentFont(self.document.currentFont())
        self.combo_font_style.currentFontChanged.connect(self.onFontStyleChanged)
        self.horizontal_layout.addWidget(self.combo_font_style)

        # Adds functionality to the ComboBox
        self.combo_font_size = QComboBox(self)
        self.combo_font_size.setToolTip('Change font size')
        self.combo_font_size.addItems(self.list_FontSize)
        self.combo_font_size.setCurrentIndex(11)
        self.combo_font_size.setFixedWidth(60)
        self.combo_font_size.setFocusPolicy(Qt.NoFocus)
        self.combo_font_size.currentIndexChanged.connect(self.onFontSizeChanged)
        self.combo_font_size.setCurrentIndex(11)
        self.horizontal_layout.addWidget(self.combo_font_size)

        # Button press to make text bold
        self.button_bold = QPushButton("B", self)
        self.button_bold.setToolTip('Bold your text. "Ctrl+B"')
        self.button_bold.setShortcut('ctrl+b')
        self.button_bold.setFixedWidth(33)
        self.button_bold.setStyleSheet("font:Bold")
        self.button_bold.setCheckable(True)
        self.button_bold.setFocusPolicy(Qt.NoFocus)
        self.button_bold.clicked.connect(self.onFontBoldChanged)
        self.horizontal_layout.addWidget(self.button_bold)

        # Button press to make text italic
        self.button_ital = QPushButton("I", self)
        self.button_ital.setToolTip('Italicise your text. "Ctrl+I"')
        self.button_ital.setShortcut('ctrl+i')
        self.button_ital.setFixedWidth(33)
        self.button_ital.setStyleSheet("font:Italic")
        self.button_ital.setCheckable(True)
        self.button_ital.setFocusPolicy(Qt.NoFocus)
        self.button_ital.clicked.connect(self.onFontItalChanged)
        self.horizontal_layout.addWidget(self.button_ital)

        # Button press to make text strikethrough
        self.button_strike = QPushButton("S", self)
        self.button_strike.setToolTip('Strikeout your text. "Ctrl+S"')
        self.button_strike.setShortcut('alt+shift+5')
        self.button_strike.setFixedWidth(33)
        self.button_strike.setStyleSheet("text-decoration: line-through")
        self.button_strike.setCheckable(True)
        self.button_strike.setFocusPolicy(Qt.NoFocus)
        self.button_strike.clicked.connect(self.onFontStrikeChanged)
        self.horizontal_layout.addWidget(self.button_strike)

        # Button press to underline text
        self.button_under = QPushButton("U", self)
        self.button_under.setToolTip('Underline your text. "Ctrl+U"')
        self.button_under.setShortcut('ctrl+u')
        self.button_under.setFixedWidth(33)
        self.button_under.setStyleSheet("text-decoration: underline")
        self.button_under.setCheckable(True)
        self.button_under.setFocusPolicy(Qt.NoFocus)
        self.button_under.clicked.connect(self.onFontUnderChanged)
        self.horizontal_layout.addWidget(self.button_under)

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
        print('TopBar - setup')

        # TODO - Keep object definitions in constructor and move all method calls in setup
        self.setFormattingEnabled(False)

        self.horizontal_layout.setContentsMargins(10, 0, 10, 0)
        self.horizontal_layout.setSpacing(3)

        self.setLayout(self.horizontal_layout)

        self.document.selectionChanged.connect(self.updateFormatOnSelectionChange)

        return self

    # Toggles between Formatting Mode and Plain-Text Mode
    def onEnableFormatting(self, state):
        print("TopBar - onEnableFormatting -", state)

        if state is True:
            convert_dialog = DialogBuilder(self.document.layout, "Enable Formatting",
                                           "Would you like to convert this file?",
                                           "This file needs to be converted to use enriched text formatting features\n"
                                           "Selecting 'Yes' will convert the original "
                                           "file to the enriched text file format.")
            buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
            convert_dialog.addButtonBox(buttonBox)
            if convert_dialog.exec():
                print("TopBar - onEnableFormatting - User converted file to Proprietary Format")
                # TODO - Convert file with FileManager to a .lef format, on success, call the function below
                self.setFormattingEnabled(True)
            else:
                print("TopBar - onEnableFormatting - User DID NOT convert file to Proprietary Format")
                self.button_mode_switch.setChecked(False)
        else:
            # Don't allow converted file to be converted back to Plain Text
            # TODO - allow option to save different file as plain text, or allow conversion back but discard formatting options
            print("TopBar - onEnableFormatting - Cannot convert back to Plain Text")
            self.button_mode_switch.setChecked(True)

    def setFormattingEnabled(self, state):
        print('TopBar - setFormattingEnabled -', state)
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.setEnabled(state)

    # Sets the font to the new font
    def onFontStyleChanged(self):
        print('TopBar - onFontStyleChanged -', self.combo_font_style.currentFont())
        self.document.setCurrentFont(self.combo_font_style.currentFont())

    # Sets the current sets the font size from the ComboBox
    def onFontSizeChanged(self):
        print('TopBar - onFontSizeChanged -', int(self.combo_font_size.currentText()))
        self.document.setFontPointSize(int(self.combo_font_size.currentText()))

    # Sets the font to italic
    def onFontItalChanged(self):
        print('TopBar - onFontItalChanged -', self.button_ital.isChecked())
        self.document.setFontItalic(self.button_ital.isChecked())

    # Sets the font to bold
    def onFontBoldChanged(self):
        print('TopBar - onFontBoldChanged -', QFont.Bold if self.button_bold.isChecked() else QFont.Normal)
        self.document.setFontWeight(QFont.Bold if self.button_bold.isChecked() else QFont.Normal)

    # Sets the font to underlined
    def onFontUnderChanged(self):
        print('TopBar - onFontUnderChanged -', self.button_under.isChecked())
        self.document.setFontUnderline(self.button_under.isChecked())

    # Sets the font to strike
    def onFontStrikeChanged(self):
        print('TopBar - onFontUnderChanged -', self.button_strike.isChecked())
        fontFormat = self.document.currentCharFormat()
        fontFormat.setFontStrikeOut(self.button_strike.isChecked())
        self.document.setCurrentCharFormat(fontFormat)

    def updateFormatOnSelectionChange(self):
        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(True)

        self.combo_font_style.setCurrentFont(self.document.currentFont())
        self.combo_font_size.setCurrentText(str(int(self.document.fontPointSize())))

        self.button_ital.setChecked(self.document.fontItalic())
        self.button_under.setChecked(self.document.fontUnderline())
        self.button_bold.setChecked(self.document.fontWeight() == QFont.Bold)
        self.button_strike.setChecked(self.document.currentCharFormat().fontStrikeOut())

        a: QWidget
        for a in self.children():
            if not a.property("persistent"):
                a.blockSignals(False)
