from PyQt5.QtWidgets import QFileDialog
from pathlib import Path


def save_document(path):
    print(path)

"""
def showDialog(output, parent):
    home_dir = str(Path.home())
    fname = QFileDialog.getOpenFileName(parent, 'Open file', home_dir)
    if fname[0]:
        f = open(fname[0], 'r')

        with f:
            data = f.read()
            output.setText(data)
"""