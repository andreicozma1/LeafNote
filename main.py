import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QSplitter
from Textbox import PlainTextEdit
from MenuBar import MenuBar

from Layout import Layout



class App(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # Initialize properties. TODO - make application properties their own class separately
        self.title = '0x432d2d'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        
        self.initWindow()

        self.docLayout = Layout(self, minDocWidth=.4, maxMenuWidth=.3, barSize=30)

        self.setCentralWidget(self.docLayout.initLayout())
        self.show()

    # Returns the Central Widget
    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

# Starting point of the program
if __name__ == '__main__':
    main()
