from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextBlockUserData, QTextCharFormat, QColor


class SyntaxHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)
        self.document = document
        self.highlighting_rules = []

        self.setupRules()


    def setupRules(self):
        url_format = QTextCharFormat()
        url_expression = None

        url_format.setFontUnderline(True)
        url_format.setForeground(QColor("blue"))

        pattern = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[" \
                  r"\w@?^=%&/~+#-])?"
        self.highlighting_rules.append((QRegExp(pattern), url_format))

        # self.err_format = QTextCharFormat()
        # self.err_format.setUnderlineColor(Qt.red)
        # self.err_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

    def highlightBlock(self, text):
        for rule in self.highlighting_rules:
            expression = QRegExp(rule[0])
            index = expression.indexIn(text)
            while index >= 0:
                print("r")
                length = expression.matchedLength()
                self.setFormat(index, length, rule[1])
                index = expression.indexIn(text, index+length)
        self.setCurrentBlockState(0)


