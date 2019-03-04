from gensim import similarities
from nlp.dicttools import get_num_of_features
import os
from heapq import nlargest
from gensim import matutils

def create_index(model, corpus, dict):
    """
    Builds an index for a given set of documents for the
    purpouse of computing cosine similarities
    """
    return similarities.SparseMatrixSimilarity(model[corpus], num_features=get_num_of_features(dict))

def save_index(index, name):
    index.save(os.getenv('SIMS_PATH') + '/' + name + '.index')

def query_index(q, index):
    """
    Given a query (doc) and an index of documents (cosine-sim-ready),
    computes the cosine similarity between the query and every single
    doc in the index
    """
    return index[q]

def get_largest_doc_ids(sims, n):
    """
    Given a computed query-docs similarity,
    retrieves the n largest similar documents (ids)
    """
    return nlargest(n, range(len(sims)), sims.take)

def cos_sim(vec1, vec2):
    """
    Computes cosine similarity between two document vectors (represented
    in any VSM)
    """
    return matutils.cossim(vec1, vec2)
