from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import sent_tokenize
from nltk.stem.snowball import SpanishStemmer
import re
from unidecode import unidecode
import pandas as pd
import os

class Preprocess():
    def __init__(self, process=None):
        self.stopwords = stopwords.words('spanish')  # list of stopwords
        self.voc = pd.read_csv(os.getenv('ES_VOC_PATH'))
        self.voc = self.voc.set_index('word')['index'].to_dict()  # spanish vocabulary (type: dict)
        self.lemmas = pd.read_csv(os.getenv('ES_LEMMAS_PATH'), delim_whitespace=True)
        self.lemmas = self.lemmas.set_index('key')['value'].to_dict()  # spanish lemmas (type: dict)
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.process = process
        self.stemmer = SpanishStemmer(ignore_stopwords=False)

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

    def get_word_lemma(self, word):
        """
        If no lemma is found, or the word itself
        is a lemma, the word is returned as is
        """
        if self.word_exists(word):
            return self.dict[word]
        else:
            return word

    def process(self, text, proc=None):
        def property(token, min_len):
            return (
                not self.is_stopword(token)
                and not self.token_has_numbers(token)
                and len(token) >= min_len
            )
        if proc == 'lemmatization':
            return (self.unidecode(self.get_word_lemma(token)) for token in self.word_tokenization(text) if property(token, 3))
        else:
            return (self.unidecode(token) for token in self.word_tokenization(text) if property(token, 3))
