from nlp.preprocess import Preprocess
from gensim import corpora
import os

def create(collection, dict, preprocess=None):
    """
    Create BoW corpus of documents collection in a streaming-way
    """
    def preprocess_collection(collection, proc):
        pre = Preprocess()
        return (pre.process(doc, proc=proc) for doc in collection)
    return (dict.doc2bow(doc) for doc in preprocess_collection(collection, preprocess))

def save(corpus, name):
    """
    Serialize corpus in the Matrix Market format
    """
    corpora.MmCorpus.serialize(os.getenv('MODELS_PATH') + '/' + name + '.mm', corpus)

def create_and_save(collection, dict, name, preprocess=None):
    corpus = create(collection, dict, preprocess=preprocess)
    save(corpus, name)
    return corpus

def load(name):
    """
    Load a corpus iterator from a Matrix Market file
    """
    return corpora.MmCorpus(os.getenv('MODELS_PATH') + '/' + name + '.mm')

def get_num_docs(corpus):
    """
    Argument is in Matrix Market format
    """
    return corpus.num_docs

def get_num_terms(corpus):
    """
    Argument is in Matrix Market format
    """
    return corpus.num_terms

def stats(corpus):
    """
    Argument is in Matrix Market format
    """
    print(corpus)
