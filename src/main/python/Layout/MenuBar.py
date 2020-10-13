import logging

from PyQt5 import QtWidgets, Qt, QtCore
from PyQt5.QtCore import QDir, QRect
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QAction, QMenuBar, QActionGroup, QMenu, QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtWidgets import QFileDialog

import Utils.DocumentSummarizer as DocumentSummarizer
from Elements import Document
from Layout import DocProps

"""
all properties and functionalities of the menu bar
"""


class MenuBar(QMenuBar):
    """
    Class to hold and customize a QPlainTextEdit Widget
    """

    def __init__(self, document: Document, doc_props: DocProps):
        """
        Sets up the System MenuBar
        :return: returns nothing
        """
        super(MenuBar, self).__init__()
        logging.info("")
        self.doc = document
        self.doc_props = doc_props
        self.setNativeMenuBar(False)

        self.doc.selectionChanged.connect(self.updateFormatOnSelectionChange)
        self.doc.currentCharFormatChanged.connect(self.updateFormatOnSelectionChange)

    # =====================================================================================
    def makeFileMenu(self, app, file_manager, bar_open_tabs):
        """
        sets up the file tabs drop menu
        :return: returns nothing
        """
        logging.info("makeFileMenu")

        def onNewBtn():
            logging.info("MenuBar - onNewBtn")
            file_manager.newFile(self.doc)

        def onOpenBtn():
            logging.info("onOpenBtn")
            # this is opens the file dialogue in the project path
            home_dir = str(QDir.currentPath())
            # opens a file dialogue for the user to select a file to open
            file_name = QFileDialog.getOpenFileName(app, 'Open file', home_dir)
            # open the chosen file and show the text in the text editor
            file_manager.openDocument(self.doc, file_name[0])

        def onOpenFolderBtn():
            logging.info("onOpenFolderBtn")
            # opens a file dialogue for the user to select a file to open
            folder_name = QFileDialog.getExistingDirectory(app, 'Open folder', str(QDir.currentPath()))
            # if the user selected a new folder
            if folder_name != "":
                app.left_menu.updateDirectory(folder_name)
            else:
                logging.info("User chose not to open folder")

        # this saves the current file that is shown in the self.doc
        def onSaveBtn():
            logging.info("onSaveBtn")
            if file_manager.saveDocument(self.doc):
                logging.info("Created tab")
                bar_open_tabs.addTab(file_manager.current_document.absoluteFilePath())

        def onSaveAsBtn():
            logging.info("saveAsFile")
            if file_manager.saveAsDocument(self.doc):
                logging.info("Created tab")

        def onExitBtn():
            logging.info("onExitBtn")
            file_manager.closeAll(self.document)
            app.close()

        self.menu_file = self.addMenu('&File')

        # ========= START FILE MENU SECTION =========
        def makeFileAction(name: str, shortcut: str, signal) -> QAction:
            file_action = QAction(name, app)
            file_action.setShortcut(shortcut)
            file_action.triggered.connect(signal)
            return file_action

        new_file_act = QAction("&New...", app)
        new_file_act.setStatusTip('New')
        new_file_act.triggered.connect(onNewBtn)
        self.menu_file.addAction(makeFileAction("New", "", onNewBtn))
        self.menu_file.addAction(makeFileAction("Open", "", onOpenBtn))
        self.menu_file.addAction(makeFileAction("Open Folder", "", onOpenFolderBtn))
        self.menu_file.addSeparator()
        self.menu_file.addAction(makeFileAction("Save...", "", onSaveBtn))
        self.menu_file.addAction(makeFileAction("Save As...", "", onSaveAsBtn))
        self.menu_file.addSeparator()
        self.menu_file.addAction(makeFileAction("Exit", "", onExitBtn))
        # ========= END FILE MENU SECTION =========

        return self.menu_file

    # =====================================================================================
    def makeEditMenu(self, app):
        """
        Create Edit Menu
        :return: the menu created
        """
        logging.info("makeEditMenu")
        self.menu_edit = self.addMenu('&Edit')

        # ========= START EDIT MENU SECTION =========
        def makeEditAction(name: str, shortcut: str, signal) -> QAction:
            edit_action = QAction(name, app)
            edit_action.setShortcut(shortcut)
            edit_action.triggered.connect(signal)
            return edit_action

        # Add actions
        self.menu_edit.addAction(makeEditAction("Undo", "Ctrl+z", self.doc.undo))
        self.menu_edit.addAction(makeEditAction("Redo", "Ctrl+Shift+z", self.doc.redo))
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(makeEditAction("Select All", "Ctrl+a", self.doc.selectAll))
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(makeEditAction("Cut", "Ctrl+x", self.doc.cut))
        self.menu_edit.addAction(makeEditAction("Copy", "Ctrl+c", self.doc.copy))
        self.menu_edit.addAction(makeEditAction("Paste", "Ctrl+v", self.doc.paste))
        # ========= END EDIT MENU SECTION =========
        return self.menu_edit

    # =====================================================================================
    def makeViewMenu(self, app, bottom_bar) -> QMenu:
        """
        Create View Menu
        :return: the menu created
        """
        logging.info("makeViewMenu")
        self.menu_view = self.addMenu('&View')

        # ========= START VIEW MENU SECTION =========
        def makeViewAction(name: str, shortcut: str, signal) -> QAction:
            view_action = QAction(name, app)
            view_action.setShortcut(shortcut)
            view_action.triggered.connect(signal)
            return view_action

        self.menu_view.addAction(makeViewAction("Zoom In", "ctrl+=", bottom_bar.onZoomInClicked))
        self.menu_view.addAction(makeViewAction("Zoom Out", "ctrl+-", bottom_bar.onZoomOutClicked))
        self.menu_view.addAction(makeViewAction("Zoom Reset", "", bottom_bar.resetZoom))
        # ========= END VIEW MENU SECTION =========
        return self.menu_view

    # =====================================================================================
    def makeFormatMenu(self, app) -> QMenu:
        """
        Create Format Menu
        :return: the menu created
        """
        logging.info("formatMenuSetup")
        self.menu_format = self.addMenu('&Format')

        # ========= START FONT STYLES SECTION =========
        def makeStyleAction(name: str, shortcut: str, signal, docref) -> QAction:
            style_action = QAction(name, app)
            style_action.setShortcut(shortcut)
            style_action.setCheckable(True)
            style_action.setProperty("docref", docref)
            style_action.triggered.connect(signal)
            return style_action

        self.group_style = QActionGroup(self.menu_format)
        self.group_style.setExclusive(False)
        act_bold = makeStyleAction("Bold", "Ctrl+B", self.doc.onFontBoldChanged, self.doc.fontBold)
        self.group_style.addAction(act_bold)
        act_ital = makeStyleAction("Italicize", "Ctrl+I", self.doc.onFontItalChanged, self.doc.fontItalic)
        self.group_style.addAction(act_ital)
        act_strk = makeStyleAction("Strikeout", "Ctrl+Shift+5", self.doc.onFontStrikeChanged, self.doc.fontStrike)
        self.group_style.addAction(act_strk)
        act_undr = makeStyleAction("Underline", "Ctrl+U", self.doc.onFontUnderChanged, self.doc.fontUnderline)
        self.group_style.addAction(act_undr)
        # Add all actions in group to Style Menu
        self.menu_format.addActions(self.group_style.actions())
        # ========= END FONT STYLES SECTION =========

        # ========= START EXTRA SECTION =========
        self.menu_format.addSeparator()

        clear_format = QAction("Clear Format", app)
        clear_format.setShortcut("Ctrl+0")
        clear_format.triggered.connect(self.doc.resetFormatting)
        self.menu_format.addAction(clear_format)

        act_color_picker = QAction("Color Picker", app)
        act_color_picker.triggered.connect(self.doc.openColorDialog)
        self.menu_format.addAction(act_color_picker)

        # ========= END EXTRA SECTION =========

        # ========= START ALIGNMENT SECTION =========
        def makeAlignAction(name: str, shortcut: str, default: bool = False) -> QAction:
            align_action = QAction(name, app)
            align_action.setShortcut(shortcut)
            align_action.setCheckable(True)
            align_action.setChecked(default)
            return align_action

        def onTextAlignmentChanged(state):
            self.doc.onTextAlignmentChanged(list(self.doc_props.dict_align.keys()).index(state.text()))

        self.menu_format.addSeparator()
        # Action Group for Alignments options (Exclusive picks)
        self.group_align = QActionGroup(self.menu_format)
        self.group_align.triggered.connect(onTextAlignmentChanged)

        def getName(index: int):
            return list(self.doc_props.dict_align.keys())[index]

        # Add alignment options to the group
        self.group_align.addAction(makeAlignAction(getName(0), 'Ctrl+Shift+L', True))
        self.group_align.addAction(makeAlignAction(getName(1), 'Ctrl+Shift+R'))
        self.group_align.addAction(makeAlignAction(getName(2), 'Ctrl+Shift+E'))
        self.group_align.addAction(makeAlignAction(getName(3), 'Ctrl+Shift+J'))
        # Add all actions in group to Format Menu
        self.menu_format.addActions(self.group_align.actions())
        # ========= END ALIGNMENT SECTION =========
        return self.menu_format

    # =====================================================================================
    def makeToolsMenu(self, app, document) -> QMenu:
        """
        Create View Menu
        :return: the menu created
        """
        logging.info("makeViewMenu")
        self.menu_tools = self.addMenu('&Tools')

        # ========= START TOOLS MENU SECTION =========

        def onSummaryAction():
            DocumentSummarizer.onSummaryAction(app, document)

        def makeToolsAction(name: str, shortcut: str, signal) -> QAction:
            tools_action = QAction(name, app)
            tools_action.setShortcut(shortcut)
            tools_action.triggered.connect(signal)
            return tools_action

        self.menu_tools.addAction(makeToolsAction("Generate Summary", "", onSummaryAction))
        self.c = QAction("Calculator", app)
        self.c.triggered.connect(self.calculator)
        self.menu_tools.addAction(self.c)

        # ========= END TOOLS MENU SECTION =========

        return self.menu_tools

    # =====================================================================================

    def calculator(self):
        self.equ = 0
        self.calc = QWidget()
        grid = QGridLayout()
        self.calc.setLayout(grid)
        self.screen = QLabel()
        space = QLabel()
        self.screen.setWordWrap(True)
        self.screen.setAlignment(QtCore.Qt.AlignRight)
        # self.screen.setAlignment(QtCore.Qt.AlignVCenter)
        self.screen.setStyleSheet("QLabel"
                                 "{"
                                 "text-align: center;"
                                 "font-size: 15pt;"
                                 "border : 1px solid black;"
                                 "background : white;"
                                 "}")
        self.screen.setFixedHeight(30)
        # output.setGeometry()
        grid.addWidget(self.screen, 0, 0, 5, 4)
        grid.addWidget(space, 4, 4)
        clear = QPushButton("C")
        grid.addWidget(clear, 5, 0)
        divide = QPushButton("/")
        grid.addWidget(divide, 5, 1)
        mult = QPushButton("*")
        grid.addWidget(mult, 5, 2)
        delete = QPushButton("del")
        grid.addWidget(delete, 5, 3)
        seven = QPushButton("7")
        grid.addWidget(seven, 6, 0)
        eight = QPushButton("8")
        grid.addWidget(eight, 6, 1)
        nine = QPushButton("9")
        grid.addWidget(nine, 6, 2)
        four = QPushButton("4")
        grid.addWidget(four, 7, 0)
        five = QPushButton("5")
        grid.addWidget(five, 7, 1)
        six = QPushButton("6")
        grid.addWidget(six, 7, 2)
        one = QPushButton("1")
        grid.addWidget(one, 8, 0)
        two = QPushButton("2")
        grid.addWidget(two, 8, 1)
        three = QPushButton("3")
        grid.addWidget(three, 8, 2)
        neg = QPushButton("+/-")
        grid.addWidget(neg, 9, 0)
        zero = QPushButton("0")
        grid.addWidget(zero, 9, 1)
        dec = QPushButton(".")
        grid.addWidget(dec, 9, 2)
        minus = QPushButton("-")
        grid.addWidget(minus, 6, 3, 1, 1)
        plus = QPushButton("+")
        grid.addWidget(plus, 7, 3, 1, 1)
        equals = QPushButton("=")
        equals.setFixedWidth(80)
        equals.setFixedHeight(52)
        grid.addWidget(equals, 8, 3, 2, 1)
        self.calc.show()

        minus.clicked.connect(self.action_minus)
        minus.setShortcut("-")
        equals.clicked.connect(self.action_equal)
        equals.setShortcut("enter")
        zero.clicked.connect(self.action0)
        zero.setShortcut("0")
        one.clicked.connect(self.action1)
        one.setShortcut("1")
        two.clicked.connect(self.action2)
        two.setShortcut("2")
        three.clicked.connect(self.action3)
        three.setShortcut("3")
        four.clicked.connect(self.action4)
        four.setShortcut("4")
        five.clicked.connect(self.action5)
        five.setShortcut("5")
        six.clicked.connect(self.action6)
        six.setShortcut("6")
        seven.clicked.connect(self.action7)
        seven.setShortcut("7")
        eight.clicked.connect(self.action8)
        eight.setShortcut("8")
        nine.clicked.connect(self.action9)
        nine.setShortcut("9")
        divide.clicked.connect(self.action_div)
        divide.setShortcut("/")
        mult.clicked.connect(self.action_mul)
        mult.setShortcut("*")
        plus.clicked.connect(self.action_plus)
        plus.setShortcut("+")
        dec.clicked.connect(self.action_point)
        dec.setShortcut(".")
        clear.clicked.connect(self.action_clear)
        clear.setShortcut("c")
        delete.clicked.connect(self.action_del)
        delete.setShortcut("backspace")
        neg.clicked.connect(self.action_neg)

    def action_plus(self):
        text = self.screen.text()
        self.screen.setText(text + " + ")

    def action_equal(self):
        equation = self.screen.text()

        try:
            ans = eval(equation)
            self.screen.setText(str(ans))
            self.equ = 1

        except:
            self.screen.setText("Wrong Input")

    def action_plus(self):
        # appending label text
        text = self.screen.text()
        if text == "Wrong Input":
            text = ""
        if text != "":
            if text[len(text) - 1] == ' ':
                self.screen.setText(text[:len(text) - 3])
                text = self.screen.text()
            self.screen.setText(text + " + ")
        self.equ = 0

    def action_minus(self):
        # appending label text
        text = self.screen.text()
        if text == "Wrong Input":
            text = ""
        if text != "":
            if text[len(text) - 1] == ' ':
                self.screen.setText(text[:len(text) - 3])
                text = self.screen.text()
            self.screen.setText(text + " - ")
        self.equ = 0

    def action_div(self):
        # appending label text
        text = self.screen.text()
        if text == "Wrong Input":
            text = ""
        if text != "":
            if text[len(text) - 1] == ' ':
                print("in")
                self.screen.setText(text[:len(text) - 3])
                text = self.screen.text()
            self.screen.setText(text + " / ")
        self.equ = 0

    def action_mul(self):
        # appending label text
        text = self.screen.text()
        if text == "Wrong Input":
            text = ""
        if text != "":
            if text[len(text) - 1] == ' ':
                self.screen.setText(text[:len(text) - 3])
                text = self.screen.text()
            self.screen.setText(text + " * ")
        self.equ = 0

    def action_point(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text != "Wrong Input":
            if text != "":
                for x in reversed(text):
                    if x == '.':
                        return
                    else:
                        if x == ' ':
                            break
                temp = text[len(text) - 1]
                if temp.isnumeric() == False:
                    text += "0"
            else:
                text += "0"
            self.screen.setText(text + ".")
        self.equ = 0

    def action0(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + "0")
        self.equ = 0

    def action1(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + "1")
        self.equ = 0

    def action2(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + "2")
        self.equ = 0

    def action3(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + "3")
        self.equ = 0

    def action4(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + "4")
        self.equ = 0

    def action5(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + "5")
        self.equ = 0

    def action6(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + "6")
        self.equ = 0

    def action7(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + "7")
        self.equ = 0

    def action8(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + "8")
        self.equ = 0

    def action9(self):
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + "9")
        self.equ = 0

    def action_clear(self):
        # clearing the label text
        self.screen.setText("")

    def action_del(self):
        # clearing a single digit
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        if text != "":
            if text[len(text) - 1] == ' ':
                self.screen.setText(text[:len(text) - 3])
            else:
                self.screen.setText(text[:len(text) - 1])
        self.equ = 0

    def action_neg(self):
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        if text != "":
            for x in reversed(range(len(text))):
                if text[x] == " ":
                    x += 1
                    text = text[:x] + '-' + text[x:]
                    self.screen.setText(text)
                    return
                else:
                    if text[x] == '-':
                        text = text[:x] + text[(x + 1):]
                        self.screen.setText(text)
                        return
            text = '-' + text
            self.screen.setText(text)


    def setFormattingButtonsEnabled(self, state):
        """
        Sets all formatting options to Enabled or Disabled
        :param state: boolean that sets the states
        :return: returns nothing
        """
        # Toggle the state of all buttons in the menu
        logging.info(str(state))
        a: QAction
        for a in self.menu_format.actions():
            if not a.property("persistent"):
                a.setEnabled(state)

    def updateFormatOnSelectionChange(self):
        """
        Selected text format reflected in the MenuBar
        :return: returns nothing
        """
        # Block signals
        a: QAction
        for a in self.menu_format.actions():
            if not a.property("persistent"):
                a.blockSignals(True)
        # Update Style options
        for action in self.group_style.actions():
            get = action.property("docref")
            action.setChecked(get())
        # Update Align options
        alignment = self.doc.alignment()
        for action in self.group_align.actions():
            action.setChecked(False)
            index = list(self.doc_props.dict_align.values()).index(alignment)
            if action.text() == list(self.doc_props.dict_align.keys())[index]:
                action.setChecked(True)
        # Unblock signals
        a: QAction
        for a in self.menu_format.actions():
            if not a.property("persistent"):
                a.blockSignals(False)
