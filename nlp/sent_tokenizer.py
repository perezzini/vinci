from nltk import sent_tokenize

class SentTokenizer():
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        sent_tokenize(self.text)
