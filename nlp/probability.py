from nltk.probability import FreqDist
from nlp.normalization import Normalization

class Probability():
    def __init__(self, tokens):
        self.tokens = tokens

    def freq_dist(self):
        return FreqDist(self.tokens)
