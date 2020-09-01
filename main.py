import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QMainWindow,QVBoxLayout
from PyQt5.QtGui import QIcon
import matplotlib


class App(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # Initialize properties. TODO - make application properties their own class separately
        self.title = '0x432d2d'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        # Vertical main layout. TODO - The middle section of VBox should be a horizontal 3 section box

        self.setCentralWidget(self.initUI())
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)

        textbox = QPlainTextEdit(self)
        textbox.resize(self.width,self.height)

        self.layout = QVBoxLayout()
        self.layout.addWidget(textbox)

        widget = QWidget()
        widget.setLayout(self.layout)
        return widget




# Starting point of the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
