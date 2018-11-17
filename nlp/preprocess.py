from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import sent_tokenize
import re
from unidecode import unidecode
import multiprocessing as mp
from nlp.es_lemmatizer import ESLemmatizer
from utils import has_numbers

class Preprocess():
    def __init__(self, lang):
        self.lang = lang
        self.stopwords = set(stopwords.words(lang))
        self.lemm = ESLemmatizer()
        self.tokenizer = RegexpTokenizer(r'\w+')

    def word_tokenization(self, text):
        return [self.to_lower(token) for token in self.tokenizer.tokenize(text) if len(token) >= 3 and not has_numbers(token)]

    def sent_tokenization(self, text):
        return sent_tokenize(text)

    def to_lower(self, token):
        return token.lower()

    def unidecode(self, token):
        return unidecode(token)

    def del_stopwords(self, tokens):
        return [token for token in tokens if token not in self.stopwords]

    def lemmatization(self, token):
        """ Stemming, but resulting stems are all valid words """
        return self.lemm.get_lemma(token)

    def complete_process(self, text):
        tokens = self.del_stopwords(self.word_tokenization(text))
        return [self.unidecode(self.lemmatization(token)) for token in tokens]

    def basic_process(self, text):
        tokens = self.word_tokenization(text)
        return [self.unidecode(token) for token in tokens]
