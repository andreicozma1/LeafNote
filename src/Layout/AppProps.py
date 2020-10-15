import logging
import os

from PyQt5.QtCore import QDir

"""
Application properties
"""


class AppProps:
    """
    class that contains the properties of the application
    """

    def __init__(self, script_path):
        """
        sets the default properties of applications
        :return: returns nothing
        """
        logging.info("Set up Application Properties")

        # Defaults
        self.title = 'LeafNote'
        self.domain = 'andreicozma.com'
        self.default_width = 800
        self.default_height = 600
        self.resizable = True

        # Defines the default path the program opens to
        self.default_path = QDir.currentPath()  # Default to current directory
        self.path_res = os.path.join(script_path, "res")
