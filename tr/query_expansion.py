from rdf import SKOS
import os
from rdflib import URIRef
from nlp.preprocess import Preprocess

class Thesaurus():
    def __init__(self, os_path):
        self.skos = SKOS(os_path)
        self.concept_root_uri = 'http://vocabularios.saij.gob.ar/saij/?tema='
        self.pre = Preprocess()

    def get_terms_from_concept(self, concept, relation):
        def flat(list_of_lists):
            return [item for sublist in list_of_lists for item in sublist]

        uri_concept = URIRef(self.concept_root_uri + concept)
        concept_tree = self.skos.get_dfs_tree(relation, uri_concept)
        concept_terms = self.skos.get_terms_from_tree(concept_tree)
        concept_terms = flat([list(self.pre.word_tokenization(concept_term)) for concept_term in concept_terms])
        return list(set(concept_term for concept_term in concept_terms if not self.pre.is_stopword(concept_term)))
