"""
this module holds the calculator widget
"""
import logging
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton


class CalculatorWidget(QWidget):
    """
    this is a customized calculator qwidget
    """

    def __init__(self):
        """
        this initializes the calculator widget
        """
        super().__init__()
        self.equ = False
        self.screen = None
        self.initUI()

    def initUI(self):
        """
        this creates the layout of the calculator
        """
        grid = QGridLayout()
        self.setLayout(grid)
        self.screen = QLabel()
        space = QLabel()
        self.screen.setWordWrap(True)
        self.screen.setAlignment(QtCore.Qt.AlignRight)

        self.screen.setStyleSheet("QLabel"
                                  "{"
                                  "text-align: center;"
                                  "font-size: 15pt;"
                                  "border : 1px solid black;"
                                  "background : white;"
                                  "}")
        self.screen.setFixedHeight(30)

        grid.addWidget(self.screen, 0, 0, 5, 4)
        grid.addWidget(space, 4, 4)

        # creates button on calculator
        def makeButton(name: str, r, c, signal, shortcut: str):
            btn = QPushButton(name)
            grid.addWidget(btn, r, c)
            btn.clicked.connect(signal)
            btn.setShortcut(shortcut)

        makeButton("C", 5, 0, self.action_clear, "c")
        makeButton("/", 5, 1, partial(self.action_operator, '/'), "/")
        makeButton("*", 5, 2, partial(self.action_operator, '*'), "*")
        makeButton("del", 5, 3, self.action_del, "backspace")
        makeButton("7", 6, 0, partial(self.actionNum, 7), "7")
        makeButton("8", 6, 1, partial(self.actionNum, 8), "8")
        makeButton("9", 6, 2, partial(self.actionNum, 9), "9")
        makeButton("4", 7, 0, partial(self.actionNum, 4), "4")
        makeButton("5", 7, 1, partial(self.actionNum, 5), "5")
        makeButton("6", 7, 2, partial(self.actionNum, 6), "6")
        makeButton("1", 8, 0, partial(self.actionNum, 1), "1")
        makeButton("2", 8, 1, partial(self.actionNum, 2), "2")
        makeButton("3", 8, 2, partial(self.actionNum, 3), "3")
        makeButton("+/-", 9, 0, self.action_neg, "CTRL + -")
        makeButton("0", 9, 1, partial(self.actionNum, 0), "0")
        makeButton(".", 9, 2, self.action_decimal, ".")
        makeButton("-", 6, 3, partial(self.action_operator, '-'), "-")
        makeButton("+", 7, 3, partial(self.action_operator, '+'), "+")

        equals = QPushButton("=")
        equals.setFixedWidth(80)
        equals.setFixedHeight(52)
        grid.addWidget(equals, 8, 3, 2, 1)
        equals.clicked.connect(self.action_equal)
        equals.setShortcut("enter")

    def action_equal(self):
        """
        this determines the answer to the given equation
        """
        equation = self.screen.text()

        # solves the equation in the calculator screen
        try:
            ans = eval(equation)
            self.screen.setText(str(ans))
            self.equ = True

        # throws error "Wrong Input" if there is an issue with solving the equation
        except SyntaxError as e:
            logging.exception(e)
            self.screen.setText("Wrong Input")

    def action_operator(self, operator):
        """
        this will insert a given operator into the equation
        """
        # appending label text
        text = self.screen.text()
        # resets the screen if "Wrong Input" was the last thing on the screen
        if text == "Wrong Input":
            text = ""

        # checks for an existing operator and replaces or adds operator to equation
        if text != "":
            if text[len(text) - 1] == ' ':
                self.screen.setText(text[:len(text) - 3])
                text = self.screen.text()
            self.screen.setText(f'{text} {operator} ')
        self.equ = False

    def action_decimal(self):
        """
        this will insert a decimal into the equation
        """
        # if last item on screen was a solution to an equation then it clears screen
        if self.equ:
            self.screen.setText("")

        # appending label text
        text = self.screen.text()

        # checks that "Wrong Input" is not on the screen
        if text != "Wrong Input":

            # if screen is not blank make sure there is no
            # decimal already otherwise add a 0 then the decimal
            if text != "":

                # checks for preexisting decimal or operation (+, -, etc.)
                for x in reversed(text):
                    if x == '.':
                        return
                    if x == ' ':
                        break
                temp = text[len(text) - 1]
                if not temp.isnumeric():
                    text += "0"
            else:
                text += "0"
            self.screen.setText(f'{text}.')
        self.equ = False

    def actionNum(self, num):
        """
        this will insert the given number into the equation
        """
        # if last item on screen was a solution to an equation then it clears screen
        if self.equ:
            self.screen.setText("")

        # adds number to screen
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        if text == "0":
            text = ""
        self.screen.setText(text + str(num))
        self.equ = False

    def action_clear(self):
        """
        this will clear the equation
        """
        # clearing the screen
        self.screen.setText("")

    def action_del(self):
        """
        this will delete the last entered number in the equation
        """
        # clearing a single digit
        text = self.screen.text()

        # resets the screen if "Wrong Input" was the last thing on the screen
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()

        # checks what last input was, if operation delete spaces as well,
        # if decimal following 0 delete 0 as well, if number delete last number
        if text != "":
            if text[len(text) - 1] == ' ':
                self.screen.setText(text[:len(text) - 3])
            elif text[len(text) - 2] == "-":
                self.screen.setText(text[:len(text) - 2])
            else:
                self.screen.setText(text[:-1])
        self.equ = False

    def action_neg(self):
        """
        this will negate the current number
        """
        text = self.screen.text()

        # resets the screen if "Wrong Input" was the last thing on the screen
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()

        # checks for negative if there is none add one else remove it
        # checks for operation to see if its a new number
        if text != "":
            for x in reversed(range(len(text))):
                if text[x] == " ":
                    if x == len(text) - 1:
                        return
                    x += 1
                    text = f'{text[:x]}-{text[x:]}'
                    self.screen.setText(text)
                    return
                if text[x] == '-':
                    text = text[:x] + text[(x + 1):]
                    self.screen.setText(text)
                    return
                if text == "0":
                    return
            text = f'-{text}'
            self.screen.setText(text)
