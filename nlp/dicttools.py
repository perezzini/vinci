from gensim import corpora
from nlp.preprocess import Preprocess
from six import iteritems
from itertools import islice
import os
from gensim.utils import SaveLoad

def create(collection, proc=None):
    pre = Preprocess()
    return corpora.Dictionary(pre.process(text, proc=proc) for text in collection)

def filter_ids_with_freq(dict, freqs):
    ids = [tokenid for tokenid, docfreq in iteritems(dict.dfs) if docfreq in freqs]
    dict.filter_tokens(bad_ids=ids)

def get_id_from_token(dict, token):
    try:
        return dict.token2id[token]
    except Exception as e:
        print(e)
        print('Token not found in dictionary')

def get_token_from_id(dict, id):
    try:
        return dict.id2token[id]
    except Exception as e:
        print(e)
        print('ID not found in dictionary')

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

def extend(dict, collection, proc=None):
    pre = Preprocess()
    dict.add_documents(pre.process(text, proc=proc) for text in collection)

def get_num_of_features(dict):
    return len(dict.dfs)

def stats(dict, freq=20):
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
        print('Dictionary not found')
