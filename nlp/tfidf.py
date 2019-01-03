from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim import similarities
from gensim.utils import SaveLoad

from nlp.preprocess import Preprocess

from heapq import nlargest

class Tfidf():
    def __init__(self, lang, dict_path, model_path, sim_matrix_path):
        self.text_preproc = Preprocess(lang)
        self.dict = Dictionary.load(dict_path)
        self.model = TfidfModel.load(model_path)
        self.sim_matrix = SaveLoad.load(sim_matrix_path)

    def doc_to_vec(self, doc):
        doc = self.dict.doc2bow(self.text_preproc.complete_process(doc))
        return self.model[doc]

    def get_top_words_from_doc(self, doc, n):
        vec = self.doc_to_vec(doc)
        return nlargest(n, vec, key=lambda tuple: tuple[1])

    def from_dict(self, id):
        return self.dict[id]

    def get_most_similar_doc_id(self, doc):
        vec = self.doc_to_vec(doc)
        sim_vec = self.sim_matrix[self.model[vec]]
        return sim_vec.argmax()  # returns the most similar
