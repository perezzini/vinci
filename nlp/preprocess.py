from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import sent_tokenize
from nltk.stem.snowball import SpanishStemmer
import re
from unidecode import unidecode
import pandas as pd
import os
from gensim.utils import SaveLoad

class Preprocess():
    stopwords = pd.read_csv(os.getenv('ES_STOPWORDS_PATH'))  # list of stopwords
    stopwords = stopwords.set_index('word')['index'].to_dict()
    voc = pd.read_csv(os.getenv('ES_VOC_PATH'))
    voc = voc.set_index('word')['index'].to_dict()  # spanish vocabulary (type: dict)
    lemmas = pd.read_csv(os.getenv('ES_LEMMAS_PATH'), delim_whitespace=True)
    lemmas = lemmas.set_index('key')['value'].to_dict()  # spanish lemmas (type: dict)
    tokenizer = RegexpTokenizer(r'\w+')
    stemmer = SpanishStemmer(ignore_stopwords=False)
    preprocessors = [
        'basic',
        'stemming',
        'lemmatization'
    ]

    def __init__(self, process='basic', token_min_len=None):
        if process in self.preprocessors:
            self.process = process
        else:
            raise Exception(process + 'not available')
        if token_min_len:
            self.token_min_len = token_min_len
        else:
            self.token_min_len = 4

    def set_collocations_model(self, name):
        self.collocations_model = SaveLoad.load(os.getenv('COLLOCATIONS_PATH') + name)

    def word_exists(self, word):
        return word in self.voc

    def token_has_numbers(self, token):
    	return bool(re.search(r'\d', token))

    def to_lower(self, token):
        return token.lower()

    def word_tokenization(self, text):
        return (self.to_lower(token) for token in self.tokenizer.tokenize(text))

    def sent_tokenization(self, text):
        return sent_tokenize(text)

    def unidecode(self, token):
        return unidecode(token)

    def is_stopword(self, token):
        return token in self.stopwords

    def proc(self, text):
        """
        Preprocess of raw-text into a list of tokens.

        Notes: Currently supports two kinds of preprocessing
            -   Lemmatization: given a word retrieves its lemma, if exists.
                If word lemma does not exists, process checks if it's a real
                word.
            -   Stemming: process uses Snowball algorithm to get to the root of
                a word. The root is not always a valid word in language's
                vocabulary.
            -   Basic: just apply word tokenization.
        """
        def predicate(token):
            return (
                len(token) >= self.token_min_len
                and (not self.is_stopword(token))
                and (not self.token_has_numbers(token))
            )
        if self.process == 'lemmatization':
            lemmas = (self.get_word_lemma(token) for token in self.word_tokenization(text) if predicate(token))
            return [self.unidecode(lemma) for lemma in lemmas]
        else:
            if self.process == 'stemming':
                stems = (self.stemmer.stem(token) for token in self.word_tokenization(text) if predicate(token))
                return [self.unidecode(stem) for stem in stems]
            else:
                if self.process == 'basic':
                    return [self.unidecode(token) for token in self.word_tokenization(text) if predicate(token)]
                else:
                    return [self.unidecode(token) for token in self.word_tokenization(text)]

    def get_word_lemma(self, word):
        """
        Note: if no lemma is found, or the word itself
        is a lemma, the word is returned as it is
        """
        def lemma_exists(word):
            return word in self.lemmas
        if lemma_exists(word):
            return self.lemmas[word]
        else:
            return word

    def apply_collocations_model(self, preproc_doc):
        """
        Apply collocations model to preprocessed document
        """
        return self.collocations_model[preproc_doc]
