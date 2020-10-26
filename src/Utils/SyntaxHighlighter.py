from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextBlockUserData, QTextCharFormat


class EnchantHighlighter(QSyntaxHighlighter):
    err_format = QTextCharFormat()
    err_format.setUnderlineColor(Qt.red)
    err_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

    def __init__(self, app, document):
        self.app = app
        self.document = document







