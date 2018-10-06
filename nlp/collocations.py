from nltk.collocations import BigramCollocationFinder

from nlp.normalization import Normalization

class Collocations():
    def __init__(self, tokens, score_fn):
        self.tokens = tokens
        self.score_fn = score_fn

    def collocations(self, total_num):
        bigram_finder = BigramCollocationFinder.from_words(self.tokens)
        bigrams = bigram_finder.nbest(self.score_fn, total_num)
        return bigrams
