import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from Layout import Layout
import tkinter


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





# Starting point of the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    #ex.docLayout.textBox.getWordCount()

    sys.exit(app.exec_())
