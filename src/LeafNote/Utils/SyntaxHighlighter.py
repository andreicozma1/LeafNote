"""
This is the libraries used in this module
"""
import logging

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor


class SyntaxHighlighter(QSyntaxHighlighter):
    """
    SyntaxHighlighter is an instance of QSyntaxHighlighter that allows us the modify the document
    """

    def __init__(self, document):
        super().__init__(document)
        self.document = document
        self.highlighting_rules = []
        self.err_format = QTextCharFormat()

        self.setupRules()

    def setupRules(self):
        """
        Sets up the formatting
        :return: returns nothing
        """
        url_format = QTextCharFormat()
        url_format.setFontUnderline(True)
        url_format.setForeground(QColor("blue"))

        pattern = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[" \
                  r"\w@?^=%&/~+#-])?"
        self.highlighting_rules.append((QRegExp(pattern), url_format))

        self.err_format.setUnderlineColor(Qt.red)
        self.err_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

    def highlightBlock(self, text):
        """
        Runs automatically when the current text block is changed
        :param text: current word in the file
        :return: returns nothing
        """
        for rule in self.highlighting_rules:
            expression = rule[0]
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule[1])
                index = expression.indexIn(text, index + length)

        self.document.onTextChanged()
        # Loop through each misspelled word
        for word in self.document.misspelled_words:
            expression = QRegExp("\\b" + word + "\\b")
            index = expression.indexIn(text)

            # Keep looking for misspelled word in block
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, self.err_format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)





