from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim import similarities

from heapq import nlargest

class Tfidf():
    def __init__(self, dataset):
        self.dataset = dataset  # pre-processed data
        self.dict = Dictionary(self.dataset)
        self.corpus = [self.dict.doc2bow(line) for line in dataset]

    def number_of_tokens(self):
        return len(self.dict)

    def get_token_from_id(self, id):
        return self.dict[id]

    def get_id_from_token(self, token):
        pass

    def get_corpus(self):
        return self.corpus

    def get_dataset(self):
        return self.dataset

    def gen_model(self, normalize=False):
        self.model = TfidfModel(self.corpus, normalize=normalize)
        return self.model

    def get_top_tokens(self, vector, n):
        return nlargest(n, vector, key=lambda tuple: tuple[1])
