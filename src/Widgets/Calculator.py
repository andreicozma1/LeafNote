"""
this module holds the calculator widgetr
"""
import logging
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton


class Calculator(QWidget):
    """
    this is a customized calculator qwidget
    """

    def __init__(self):
        """
        this initializes the calculator widget
        """
        super().__init__()
        self.equ = 0
        self.screen = None
        self.calculator()
        self.show()

    def calculator(self):
        """
        this creates the layout of the calculator
        """
        grid = QGridLayout()
        self.setLayout(grid)
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

        def makeButton(name: str, r, c, re, rc, signal, shortcut: str):
            btn = QPushButton(name)
            grid.addWidget(btn, r, c, re, rc)
            btn.clicked.connect(signal)
            btn.setShortcut(shortcut)

        makeButton("C", 5, 0, 1, 1, self.action_clear, "c")
        makeButton("/", 5, 1, 1, 1, partial(self.action_operator, '/'), "/")
        makeButton("*", 5, 2, 1, 1, partial(self.action_operator, '*'), "*")
        makeButton("del", 5, 3, 1, 1, self.action_del, "backspace")
        makeButton("7", 6, 0, 1, 1, partial(self.actionNum, 7), "7")
        makeButton("8", 6, 1, 1, 1, partial(self.actionNum, 8), "8")
        makeButton("9", 6, 2, 1, 1, partial(self.actionNum, 9), "9")
        makeButton("4", 7, 0, 1, 1, partial(self.actionNum, 4), "4")
        makeButton("5", 7, 1, 1, 1, partial(self.actionNum, 5), "5")
        makeButton("6", 7, 2, 1, 1, partial(self.actionNum, 6), "6")
        makeButton("1", 8, 0, 1, 1, partial(self.actionNum, 1), "1")
        makeButton("2", 8, 1, 1, 1, partial(self.actionNum, 2), "2")
        makeButton("3", 8, 2, 1, 1, partial(self.actionNum, 3), "3")
        makeButton("+/-", 9, 0, 1, 1, self.action_neg, "CTRL + -")
        makeButton("0", 9, 1, 1, 1, partial(self.actionNum, 0), "0")
        makeButton(".", 9, 2, 1, 1, self.action_decimal, ".")
        makeButton("-", 6, 3, 1, 1, partial(self.action_operator, '-'), "-")
        makeButton("+", 7, 3, 1, 1, partial(self.action_operator, '+'), "+")

        # clear = QPushButton("C")
        # grid.addWidget(clear, 5, 0)
        # divide = QPushButton("/")
        # grid.addWidget(divide, 5, 1)
        # mult = QPushButton("*")
        # grid.addWidget(mult, 5, 2)
        # delete = QPushButton("del")
        # grid.addWidget(delete, 5, 3)
        # seven = QPushButton("7")
        # grid.addWidget(seven, 6, 0)
        # eight = QPushButton("8")
        # grid.addWidget(eight, 6, 1)
        # nine = QPushButton("9")
        # grid.addWidget(nine, 6, 2)
        # four = QPushButton("4")
        # grid.addWidget(four, 7, 0)
        # five = QPushButton("5")
        # grid.addWidget(five, 7, 1)
        # six = QPushButton("6")
        # grid.addWidget(six, 7, 2)
        # one = QPushButton("1")
        # grid.addWidget(one, 8, 0)
        # two = QPushButton("2")
        # grid.addWidget(two, 8, 1)
        # three = QPushButton("3")
        # grid.addWidget(three, 8, 2)
        # neg = QPushButton("+/-")
        # grid.addWidget(neg, 9, 0)
        # zero = QPushButton("0")
        # grid.addWidget(zero, 9, 1)
        # dec = QPushButton(".")
        # grid.addWidget(dec, 9, 2)
        # minus = QPushButton("-")
        # grid.addWidget(minus, 6, 3, 1, 1)
        # plus = QPushButton("+")
        # grid.addWidget(plus, 7, 3, 1, 1)
        equals = QPushButton("=")
        equals.setFixedWidth(80)
        equals.setFixedHeight(52)
        grid.addWidget(equals, 8, 3, 2, 1)

        equals.clicked.connect(self.action_equal)
        equals.setShortcut("enter")
        # zero.clicked.connect(partial(self.actionNum, 0))
        # zero.setShortcut("0")
        # one.clicked.connect(partial(self.actionNum, 1))
        # one.setShortcut("1")
        # two.clicked.connect(partial(self.actionNum, 2))
        # two.setShortcut("2")
        # three.clicked.connect(partial(self.actionNum, 3))
        # three.setShortcut("3")
        # four.clicked.connect(partial(self.actionNum, 4))
        # four.setShortcut("4")
        # five.clicked.connect(partial(self.actionNum, 5))
        # five.setShortcut("5")
        # six.clicked.connect(partial(self.actionNum, 6))
        # six.setShortcut("6")
        # seven.clicked.connect(partial(self.actionNum, 7))
        # seven.setShortcut("7")
        # eight.clicked.connect(partial(self.actionNum, 8))
        # eight.setShortcut("8")
        # nine.clicked.connect(partial(self.actionNum, 9))
        # nine.setShortcut("9")
        # divide.clicked.connect(partial(self.action_operator, '/'))
        # divide.setShortcut("/")
        # mult.clicked.connect(partial(self.action_operator, '*'))
        # mult.setShortcut("*")
        # plus.clicked.connect(partial(self.action_operator, '+'))
        # plus.setShortcut("+")
        # minus.clicked.connect(partial(self.action_operator, '-'))
        # minus.setShortcut("-")
        # dec.clicked.connect(self.action_decimal)
        # dec.setShortcut(".")
        # clear.clicked.connect(self.action_clear)
        # clear.setShortcut("c")
        # delete.clicked.connect(self.action_del)
        # delete.setShortcut("backspace")
        # neg.clicked.connect(self.action_neg)

    def action_equal(self):
        """
        this determines the answer to the given equation
        """
        equation = self.screen.text()

        try:
            ans = eval(equation)
            self.screen.setText(str(ans))
            self.equ = 1

        except SyntaxError as e:
            logging.exception(e)
            self.screen.setText("Wrong Input")

    def action_operator(self, operator):
        """
        this will insert a given operator into the equation
        """
        # appending label text
        text = self.screen.text()
        if text == "Wrong Input":
            text = ""
        if text != "":
            if text[len(text) - 1] == ' ':
                self.screen.setText(text[:len(text) - 3])
                text = self.screen.text()
            self.screen.setText(text + " " + operator + " ")
        self.equ = 0

    def action_decimal(self):
        """
        this will insert a decimal into the equation
        """
        # appending label text
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text != "Wrong Input":
            if text != "":
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
            self.screen.setText(text + ".")
        self.equ = 0

    def actionNum(self, num):
        """
        this will insert the given number into the equation
        """
        if self.equ == 1:
            self.screen.setText("")
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        self.screen.setText(text + str(num))
        self.equ = 0

    def action_clear(self):
        """
        this will clear the equation
        """
        # clearing the label text
        self.screen.setText("")

    def action_del(self):
        """
        this will delete the last entered number in the equation
        """
        # clearing a single digit
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        if text != "":
            if text[len(text) - 1] == ' ':
                self.screen.setText(text[:len(text) - 3])
            else:
                if text[len(text) - 2] == "-":
                    self.screen.setText(text[:len(text) - 2])
                else:
                    self.screen.setText(text[:len(text) - 1])
        self.equ = 0

    def action_neg(self):
        """
        this will negate the current number
        """
        text = self.screen.text()
        if text == "Wrong Input":
            self.screen.setText("")
            text = self.screen.text()
        if text != "":
            for x in reversed(range(len(text))):
                if text[x] == " ":
                    if x == len(text) - 1:
                        return
                    x += 1
                    text = text[:x] + '-' + text[x:]
                    self.screen.setText(text)
                    return
                if text[x] == '-':
                    text = text[:x] + text[(x + 1):]
                    self.screen.setText(text)
                    return
            text = '-' + text
            self.screen.setText(text)
