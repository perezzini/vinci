import pandas as pd
from unidecode import unidecode
import settings

class ESLemmatizer():
    def __init__(self):
        self.dict = pd.read_csv(settings.ES_LEMMAS_PATH, delim_whitespace=True)
        self.dict = self.dict.set_index('key')['value'].to_dict()

    def word_exists(self, word):
        return word in self.dict

    def get_lemma(self, word):
        if self.word_exists(word):
            return self.dict[word]
        else:
            return word
