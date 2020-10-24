"""
This module holds a class (AppProps) that hold all pertinent information needed for the main
application.
"""

import logging
import os

from PyQt5.QtCore import QDir


class AppProps:
    """
    class that contains the properties of the application
    """

    def __init__(self, script_path):
        """
        sets the default properties of applications
        :return: returns nothing
        """
        logging.debug("Setting up App Props")

        # Defaults
        self.title = 'LeafNote'
        self.domain = 'andreicozma.com'
        self.default_width = 800
        self.default_height = 600
        self.resizable = True

        # Defines the default path the program opens to
        self.default_path = QDir.currentPath()  # Default to current directory
        self.path_res = os.path.join(script_path, "Resources")
