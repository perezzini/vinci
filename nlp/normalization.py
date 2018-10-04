from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nlp.word_tokenizer import WordTokenizer

class Normalization():
    def __init__(self, text, lang):
        word_tokenizer = WordTokenizer(text)
        self.tokens = word_tokenizer.tokenize()
        self.lang = lang
        self.stopwords_set = set(stopwords.words(lang))

    def to_lower(self):
        self.tokens = [word.lower() for word in self.tokens]

    def delete_stopwords(self):
        self.tokens = [word for word in self.tokens if word not in self.stopwords_set]

    def stemming(self):
        stemmer = SnowballStemmer(self.lang)
        return [stemmer.stem(word) for word in self.text]

    def lemmatization(self):
        """ Stemming, but resulting stems are all valid words """
        pass

    def process(self):
        self.to_lower()
        self.delete_stopwords()
        return self.tokens
