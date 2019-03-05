from nlp.preprocess import Preprocess
from gensim import matutils
from nlp.dicttools import get_num_of_features

def to_bow(plain_text_doc, dict, preprocess=None, model=None):
    """
    Convert plain-text doc into Gensim BoW format (list of (token_id, token_count))
    using, maybe, some transformation model
    """
    pre = Preprocess()
    if model:
        return model[dict.doc2bow(pre.process(plain_text_doc, proc=preprocess))]
    else:
        return dict.doc2bow(pre.process(plain_text_doc, proc=preprocess))

def to_vec(bow, dict, sparse=True):
    """
    Converts BoW doc into a Scipy sparse or a Numpy dense vector
    """
    bow = [bow]  # place BoW doc in a "singleton" corpus
    if sparse:
        return matutils.corpus2csc(bow, num_terms=get_num_of_features(dict))
    else:
        return matutils.corpus2dense(bow, num_terms=get_num_of_features(dict))

def get_top_terms(bow, dict, n):
    """
    Get top-weighted terms from a doc (in a certain weight representation)
    """
    return list(map(lambda pair: ((dict[pair[0]], pair[0]), pair[1]), sorted(bow, key=lambda pair: pair[1], reverse=True)[:n]))

def transform(plain_text_doc, dict, model, preprocess=None):
    bow = to_bow(plain_text_doc, dict, preprocess=preprocess)
    bow_trans = model[bow]
    return to_vec(bow_trans, dict)
