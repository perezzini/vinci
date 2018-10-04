from nltk.tokenize import RegexpTokenizer
import re

class WordTokenizer():
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(self.text)
