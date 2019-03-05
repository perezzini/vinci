from gensim import similarities
import os
from heapq import nlargest
from gensim import matutils
from nlp.corpustools import get_num_features

def create_index(model, corpus):
    """
    Builds an index for a given set of documents for the
    purpouse of computing cosine similarities

    Note: Use this if input corpus contains sparse vectors (such as TF-IDF documents)
    and fits into RAM
    """
    return similarities.SparseMatrixSimilarity(model[corpus], num_features=get_num_features(corpus))

def save_index(index, name):
    index.save(os.getenv('SIMS_PATH') + '/' + name + '.index')

def query_index(q, index):
    """
    Given a query (doc) and an index of documents (cosine-sim-ready),
    computes the cosine similarity between the query and every single
    doc in the index (searches documents similar to query in index)
    """
    return index[q]

def get_most_sim_doc_ids(q, n, index):
    """
    Returns the N most similar documents to a query in a given collection
    of documents (indexed docs), using a given transformation model.
    If N > len(index), returns the every doc in index (in decreasing order)
    """
    sims = query_index(q, index)
    return nlargest(n, range(len(sims)), sims.take)

def cos_sim(vec1, vec2):
    """
    Computes cosine similarity between two document vectors (represented
    in any VSM)
    """
    return matutils.cossim(vec1, vec2)
