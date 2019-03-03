from nlp.preprocess import Preprocess
from gensim import corpora
import os

def create(collection, dict, preprocess=None):
    """
    Create BoW corpus of documents collection in a streaming-way using generators
    """
    def preprocess_collection(collection, proc):
        pre = Preprocess()
        return (pre.process(doc, proc=proc) for doc in collection)
    return (dict.doc2bow(doc) for doc in preprocess_collection(collection, preprocess))

def save(corpus, name):
    corpora.MmCorpus.serialize(dict.save(os.getenv('MODELS_PATH') + '/' + name + '.mm'), corpus)
