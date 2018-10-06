from nlp.collocations import Collocations

class TextMining():
    def __init__(self, tokens):
        self.tokens = tokens

    def bag_of_words(self):
        return dict([(token, True) for token in self.tokens])

    def bag_of_bigram_words(self, score_fn):
        coll = Collocations(self.tokens, score_fn)
        return self.bag_of_words(self.tokens + coll)
