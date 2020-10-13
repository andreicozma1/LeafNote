from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton


class Calculator(QWidget):

    def __init__(self):
        super(Calculator, self).__init__()
        self.calculator()
        self.show()

    def calculator(self):
        self.equ = 0
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
                if text[len(text) - 2] == "-":
                    self.screen.setText(text[:len(text) - 2])
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
                    if x == len(text) - 1:
                        return
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