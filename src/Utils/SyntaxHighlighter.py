"""
This is the libraries used in this module
"""
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor


class SyntaxHighlighter(QSyntaxHighlighter):
    """
    SyntaxHighlighter is an instance of QSyntaxHighlighter that allows us the modify the docuemnt
    """
    def __init__(self, document):
        super().__init__(document)
        self.document = document
        self.highlighting_rules = []
        self.misspelled_words = []
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

        self.err_format = QTextCharFormat()
        self.err_format.setUnderlineColor(Qt.red)
        self.err_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

    def highlightBlock(self, text):
        """
        Will highlight current text
        :param text: current word in the file
        :return: returns nothing
        """
        for rule in self.highlighting_rules:
            expression = rule[0]
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule[1])
                index = expression.indexIn(text, index+length)

        if len(self.misspelled_words) > 0:
            for word in self.misspelled_words:
                expression = QRegExp("\\b" + word[1] + "\\b")
                index = expression.indexIn(text)
                count = 0

                while index >= 0:
                    length = expression.matchedLength()
                    self.setFormat(index, length, self.err_format)
                    index = expression.indexIn(text, index + length)
                    count = count + 1

                if count == 0:
                    self.misspelled_words.remove(word)
        self.setCurrentBlockState(0)
