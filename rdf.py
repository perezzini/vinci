from rdflib import Graph, Literal
from rdflib.namespace import SKOS as SKS

class RDF():
    def __init__(self, file_path):
        self.graph = Graph()
        self.graph.load(file_path)

    def graph_len(self):
        return len(self.graph)

    def get_objects(self, subject, predicate):
        l = list()
        for obj in self.graph.objects(subject, predicate):
            l.append(obj)
        return l

    def object_exists(self, object):
        if object in self.get_objects(self, None, None):
            return True
        else:
            return False

    def get_subject(self, predicate, object):
        if object_exists(self, object):
            return self.graph.subjects(predicate, object)
        else:
            raise Exception('Object does not exist in graph')

class SKOS(RDF):
    def __init__(self, vocab_file):
        self.vocab = RDF(vocab_file)

    def get_literal_terms(self):
        objects = self.vocab.get_objects(None, SKS['prefLabel'])
        return list(map(lambda lit: lit.toPython(), objects))

    def get_num_of_terms(self):
        return len(self.get_literal_terms())
