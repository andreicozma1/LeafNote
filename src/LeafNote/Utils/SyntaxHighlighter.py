"""
This is the libraries used in this module
"""
import logging

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from spellchecker import SpellChecker


class SyntaxHighlighter(QSyntaxHighlighter):
    """
    SyntaxHighlighter is an instance of QSyntaxHighlighter that allows us the modify the docuemnt
    """

    def __init__(self, document):
        super().__init__(document)
        self.document = document
        self.highlighting_rules = []
        self.err_format = QTextCharFormat()

        self.spell_checker = SpellChecker()
        # Set of misspelled words
        self.misspelled_words = set()

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

        if self.document.spellcheck_enabled:
            all_words = text.split()
            # If there is at least one word and the last character typed is space
            if len(all_words) >= 1 and text[len(text) - 1] == " ":
                # Gets the last word from list
                last_word = all_words[len(all_words) - 1]
                # Check if the given word is correct
                correct = self.spell_checker[last_word]
                if not correct:
                    self.misspelled_words.add(last_word)
                    logging.debug("Misspelled word: %s - total: %d",
                                  last_word, len(self.misspelled_words))

            if self.misspelled_words:
                # Loop through each misspelled word
                for word in self.misspelled_words:
                    expression = QRegExp("\\b" + word + "\\b")
                    index = expression.indexIn(text)

                    # Keep looking for misspelled word in block
                    while index >= 0:
                        length = expression.matchedLength()
                        self.setFormat(index, length, self.err_format)
                        index = expression.indexIn(text, index + length)

        elif self.misspelled_words:
            logging.debug("Spellcheck is disabled - clearing mispelled word dictionary")
            logging.debug(self.misspelled_words)
            self.misspelled_words.clear()

        self.setCurrentBlockState(0)

    def addAllMisspelledWords(self):
        """
        Re-checks the entire document and adds all misspelled words
        """
        logging.debug("Re-checking entire document to re-construct mispelled words dictionary")
        all_words = self.document.toPlainText().split()
        self.misspelled_words = self.spell_checker.unknown(all_words)
        logging.debug(self.misspelled_words)
