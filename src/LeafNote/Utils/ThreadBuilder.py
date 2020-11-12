from functools import partial

from PyQt5.QtCore import QThread


class ExecuteThread(QThread):
    def __init__(self, target, args: tuple = (), callback=None):
        super().__init__()
        self.target = target
        self.args = args
        self.callback = callback
        self.return_value = None

    def run(self):
        self.return_value = self.target(*self.args)
        if self.callback:
            self.finished.connect(partial(self.callback, self.return_value))



