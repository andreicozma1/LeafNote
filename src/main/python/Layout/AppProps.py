import logging

from PyQt5.QtCore import QDir


class AppProps():
    def __init__(self):
        logging.info("Set up Application Properties")

        # Defaults
        self.title = 'LeafNote'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600

        # Defines the default path the program opens to
        self.mainPath = QDir.currentPath()  # Default to current directory

        self.min_width = .3  # Proportion of screen width
        self.resizable = True
