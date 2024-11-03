import re
from collections import Counter
from typing import List


class KeywordExtractor:
    def __init__(self):
        self.stop_words = set(
            [
                "the",
                "a",
                "an",
                "and",
                "or",
                "but",
                "in",
                "on",
                "at",
                "to",
                "for",
                "of",
                "with",
                "by",
            ]
        )

    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        # Tokenize the text
        words = re.findall(r"\b\w+\b", text.lower())

        # Remove stop words
        words = [word for word in words if word not in self.stop_words]

        # Count word frequencies
        word_freq = Counter(words)

        # Get the top N most common words
        keywords = [word for word, _ in word_freq.most_common(top_n)]

        return keywords
