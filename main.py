import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit
from PyQt5.QtGui import QIcon
import matplotlib


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Window Title'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)

        self.textbox = QPlainTextEdit(self)
        self.textbox.resize(self.width,self.height)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
