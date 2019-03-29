from gensim import matutils
from nlp.dicttools import get_num_of_features

def to_bow(plain_text_doc, dict, preproc, model=None, collocations=True):
    """
    Convert plain-text doc into Gensim BoW format (list of (token_id, token_count))
    using, maybe, some transformation model
    """
    if model:
        try:
            return model[dict.doc2bow(preproc.apply_collocations_model(preproc.proc(plain_text_doc)))]
        except AttributeError:
            return model[dict.doc2bow(preproc.proc(plain_text_doc))]
    else:
        try:
            return dict.doc2bow(preproc.apply_collocations_model(preproc.proc(plain_text_doc)))
        except AttributeError:
            return dict.doc2bow(preproc.proc(plain_text_doc))

def is_bow(vec):
    """
    Checks if a vector is in the sparse Gensim BoW format
    """
    return matutils.isbow(vec)

def to_dense_vec(bow, dict):
    """
    Converts a document in Gensim BoW format into a dense numpy array
    """
    return matutils.sparse2full(bow, get_num_of_features(dict))

def from_dense_vec(vec):
    """
    Converts a vector into Gensim BoW format
    """
    return matutils.any2sparse(vec)

def get_top_terms(vec, dict, n):
    """
    Returns the top N elements of the greatest magnitude (abs) of
    a doc vector (in Gensim BoW or dense numpy array)
    """
    if not(is_bow(vec)):
        top = matutils.full2sparse_clipped(vec, n)
        return list(map(lambda pair: ((dict[pair[0]], pair[0]), pair[1]), top))
    else:
        return list(map(lambda pair: ((dict[pair[0]], pair[0]), pair[1]), sorted(vec, key=lambda pair: pair[1], reverse=True)[:n]))
