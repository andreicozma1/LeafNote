"""
this module contains a custom implementation of a qthread
"""
from PyQt5.QtCore import QThread


class ExecuteThread(QThread):
    """
    This is a re-usable qthread implementation
    """
    def __init__(self, target, args: tuple = ()):
        super().__init__()
        self.target = target
        self.args = args
        self.return_value = None

    def run(self):
        """
        Called after thread start
        """
        self.return_value = self.target(*self.args)

    def setCallback(self, callback):
        """
        Sets callback for thread
        """
        self.finished.connect(callback)

    def getReturn(self):
        """
        Gets the thread return value
        """
        return self.return_value
