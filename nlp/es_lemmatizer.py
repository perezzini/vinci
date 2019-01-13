import pandas as pd
from unidecode import unidecode
import settings
import os

class ESLemmatizer():
    def __init__(self):
        self.dict = pd.read_csv(os.getenv('ES_LEMMAS_PATH'), delim_whitespace=True)
        self.dict = self.dict.set_index('key')['value'].to_dict()

    def word_exists(self, word):
        return word in self.dict

    def get_lemma(self, word):
        if self.word_exists(word):
            return self.dict[word]
        else:
            return word
