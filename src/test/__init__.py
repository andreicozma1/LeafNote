"""
Initializes application for tests
"""
from PyQt5.QtWidgets import QApplication

from LeafNote import App

ctx = QApplication.instance()
if ctx is None:
    ctx = QApplication([])
app = App(ctx)
