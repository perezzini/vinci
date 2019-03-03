from nlp.preprocess import Preprocess
from gensim import matutils

class Doc():
    def __init__(self, dict, doc, preprocess=None):
        self.dict = dict
        self.doc = doc
        self.preprocess = preprocess

    def to_bow(self):
        pre = Preprocess()
        return self.dict.doc2bow(pre.process(self.doc, proc=self.preprocess))

    def to_vec(self):
        bow = self.to_bow()
        bow = [bow]  # place doc vec into the most minimal corpus ("matrix")
        return matutils.corpus2csc(bow)
