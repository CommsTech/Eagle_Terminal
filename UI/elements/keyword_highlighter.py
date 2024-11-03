import json
import os

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat


class KeywordHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, chief):
        super().__init__(parent)
        self.chief = chief
        self.highlighting_rules = []
        self.load_keywords()

    def load_keywords(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        keywords_file = os.path.join(script_dir, "keywords.json")

        with open(keywords_file, "r") as f:
            keywords_data = json.load(f)

        for category, words in keywords_data.items():
            color = QColor(keywords_data[category]["color"])
            for word in words["words"]:
                pattern = r"\b" + word + r"\b"
                rule = HighlightingRule(pattern, self.create_format(color))
                self.highlighting_rules.append(rule)

    def create_format(self, color):
        text_format = QTextCharFormat()
        text_format.setForeground(color)
        return text_format

    def highlightBlock(self, text):
        for rule in self.highlighting_rules:
            expression = QRegExp(rule.pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)


class HighlightingRule:
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format
