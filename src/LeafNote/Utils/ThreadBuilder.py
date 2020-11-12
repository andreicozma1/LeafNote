from functools import partial

from PyQt5.QtCore import QThread


class ExecuteThread(QThread):
    def __init__(self, target, args: tuple = (), callback=None):
        super().__init__()
        self.target = target
        self.args = args
        self.return_value = None
        if callback:
            self.finished.connect(partial(callback, self.return_value))

    def run(self):
        self.return_value = self.target(*self.args)


