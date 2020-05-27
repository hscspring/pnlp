import os
from pnlp.piop import read_lines

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


chinese_stopwords_file = os.path.join(root, "stopwords/chinese_stopwords.txt")
english_stopwords_file = os.path.join(root, "stopwords/english_stopwords.txt")


chinese_stopwords = set(read_lines(chinese_stopwords_file))
english_stopwords = set(read_lines(english_stopwords_file))


class StopWords:

    def __init__(self, path: str = ""):
        self._chinese_stopwords = chinese_stopwords
        self._english_stopwords = english_stopwords
        if path:
            self._stopwords = set(read_lines(path))
        else:
            self._stopwords = set()

    @property
    def zh(self):
        return self._chinese_stopwords

    @property
    def zh_len(self):
        return len(self._chinese_stopwords)

    @property
    def en(self):
        return self._english_stopwords

    @property
    def en_len(self):
        return len(self._english_stopwords)

    @property
    def stopwords(self):
        return self._stopwords
