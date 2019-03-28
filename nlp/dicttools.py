from gensim import corpora
from six import iteritems
from itertools import islice
import os
from gensim.utils import SaveLoad
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

def create(collection, preproc):
    collection_preproc = (preproc.proc(doc) for doc in collection)
    try:
        return corpora.Dictionary(preproc.collocations_model[doc] for doc in collection_preproc)
    except AttributeError:
        return corpora.Dictionary(collection_preproc)

def word_exists(dict, word):
    return word in dict.itervalues()

def filter_ids_with_freq(dict, freqs):
    ids = [tokenid for tokenid, docfreq in iteritems(dict.dfs) if docfreq in freqs]
    dict.filter_tokens(bad_ids=ids)

def get_id_from_token(dict, token):
    try:
        return dict.token2id[token]
    except Exception as e:
        print(e)

def get_token_from_id(dict, id):
    try:
        return dict.id2token[id]
    except Exception as e:
        print(e)

def get_freq(dict, id):
    return dict.dfs[id]

def get_n_freq_tokens(dict, n, most=True):
    container = ((key, val) for key, val in sorted(iteritems(dict.dfs), key=lambda pair: pair[1], reverse=most))
    return list(islice(container, n))

def print_n_freq_tokens(dict, n, most=True):
    return list(map(lambda pair: (dict[pair[0]], pair), get_n_freq_tokens(dict, n, most=most)))

def filter_bad_tokens(dict, least_freq, most_freq):
    least_ids = list(map(lambda pair: pair[0], get_n_freq_tokens(dict, least_freq, most=False)))
    most_ids = list(map(lambda pair: pair[0], get_n_freq_tokens(dict, most_freq)))
    dict.filter_tokens(bad_ids=least_ids + most_ids)

def add_token(dict, token, preproc):
    """
    Extends vocabulary with given token

    Notes: token is preprocessed on-the-fy
    """
    token = list(pre.proc(token))
    dict.add_documents([token])

def add_documents(dict, preprocessed_collection):
    """
    Update dictionary from a collection of documents

    Notes: input collection must be an iterator (iterable of iterable)
    of preprocessed documents
    """
    return dict.add_documents(preprocessed_collection)

def get_num_of_features(dict):
    return len(dict.dfs)

def stats(dict, freq=20):
    print(dict)
    print('\n')
    print('Number of documents processed:', dict.num_docs)
    print('\n')
    print('Number of processed words:', dict.num_pos)
    print('\n')
    print('Most', freq, 'frequent tokens:', print_n_freq_tokens(dict, freq))
    print('\n')
    print('Least', freq, 'frequent tokens:', print_n_freq_tokens(dict, freq, most=False))

def save(dict, name):
    dict.save(os.getenv('DICTS_PATH') + '/' + name + '.dict')

def load(name):
    try:
        return SaveLoad.load(os.getenv('DICTS_PATH') + '/' + name + '.dict')
    except Exception as e:
        print(e)

def plot_freq_dist(dict, firsts=100, cumulative=False):
    dist = FreqDist(dict.dfs)
    dist.plot(firsts, cumulative=cumulative)
    plt.show()
