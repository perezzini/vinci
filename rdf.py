from rdflib import Graph, Literal
from rdflib.namespace import SKOS as SKS
from rdflib.plugins.sparql import prepareQuery

from graph import DiGraph

class RDF():
    def __init__(self, file_path):
        self.graph = Graph()
        self.graph.load(file_path)

    def graph_len(self):
        return len(self.graph)

    def literal_to_text(self, lit):
        return lit.toPython()

    def query(self, q):
        return self.graph.query(q)

    def get_preferred_label(self, uri):
        return self.graph.preferredLabel(uri)

    def triples(self, subject, predicate, object):
        return self.graph.triples((subject, predicate, object))

class SKOS(RDF):
    def __init__(self, vocab_file):
        self.vocab = RDF(vocab_file)
        self.terms = self.get_terms()
        self.properties = ['prefLabel', 'narrower', 'broader', 'related']

    def get_terms_with_uris(self):
        q = prepareQuery('SELECT ?concept ?term WHERE { ?concept skos:prefLabel ?term .}', initNs = { 'skos': SKS })
        l = list()
        for row in self.vocab.query(q):
            l.append(row)
        return l

    def get_terms(self):
        l = self.get_terms_with_uris()
        l = list(map(lambda pair: self.vocab.literal_to_text(pair[1]), l))
        return [term.lower() for term in l]

    def get_num_of_terms(self):
        return len(self.terms)

    def term_exists(self, term):
        term = term.lower()
        if term in self.terms:
            return True
        else:
            return False

    # Not working well. Must use SPARQL, but it fails too...
    # q = prepareQuery('SELECT ?concept WHERE { ?concept skos:prefLabel ?term .}', initNs = {'skos': SKOS })
    # FIXME: find some solution to retrieve concepts given prefLabels
    def get_uri_from_term(self, term):
        if self.term_exists(term):
            term = term.lower()
            l = list(filter(lambda pair: self.literal_to_text(pair[1]) == term, self.get_terms_with_uris()))
            return list(map(lambda pair: pair[0], l))[0]
        else:
            raise Exception(term + ' does not exist in opened vocabulary')

    def get_term_from_uri(self, uri):
        label = self.vocab.get_preferred_label(uri)[0][1]
        return self.literal_to_text(label).lower()

    def get_dfs_tree(self, property, node):
        if property not in self.properties:
            raise Exception(property + ' is not a SKOS property')
        di_graph = DiGraph()

        for s, p, o in self.vocab.triples(None, SKS[property], None):
            di_graph.add_edge(s, o)

        tree_edges = di_graph.dfs_tree(node)

        di_graph.clear()
        di_graph.add_edges_from(list(tree_edges))

        # label nodes with literals
        for n1, n2 in di_graph.edges():
            di_graph.nodes()[n1]['label'] = self.get_term_from_uri(n1)
            di_graph.nodes()[n2]['label'] = self.get_term_from_uri(n2)

        return di_graph

    def get_terms_from_tree(self, tree):
        nodes = list(tree.nodes())
        return list(map(lambda uri: self.get_term_from_uri(uri), nodes))
