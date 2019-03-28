from gensim import corpora
import os
from gensim import matutils

def create(collection, dict, preproc):
    """
    Create BoW corpus of documents collection in a streaming-way
    """
    def preprocess_collection(collection):
        try:
            return (preproc.collocations_model[preproc.proc(doc)] for doc in collection)
        except AttributeError:
            return (preproc.proc(doc) for doc in collection)
    return (dict.doc2bow(doc) for doc in preprocess_collection(collection))

def save(corpus, name):
    """
    Serialize corpus in the Matrix Market format
    """
    corpora.MmCorpus.serialize(os.getenv('CORPUSES_PATH') + '/' + name + '.mm', corpus)

def create_and_save(collection, dict, name, preproc):
    corpus = create(collection, dict, preproc)
    save(corpus, name)
    return corpus

def load(name):
    """
    Load a corpus iterator from a Matrix Market file
    """
    return corpora.MmCorpus(os.getenv('CORPUSES_PATH') + '/' + name + '.mm')

def get_num_docs(corpus):
    """
    Argument is in Matrix Market format
    """
    return corpus.num_docs

def get_num_features(corpus):
    """
    Argument is in Matrix Market format
    """
    return corpus.num_terms

def stats(corpus):
    """
    Argument is in Matrix Market format
    """
    print(corpus)

def to_array(corpus, sparse=True):
    """
    Converts corpus into a Scipy sparse matrix or a Numpy dense matrix
    """
    if sparse:
        return matutils.corpus2csc(corpus, num_terms=get_num_features(corpus))
    else:
        return matutils.corpus2dense(corpus, num_terms=get_num_features(corpus))
