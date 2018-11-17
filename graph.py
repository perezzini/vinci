import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

class DiGraph():
    def __init__(self):
        self.graph = nx.DiGraph()

    def get_number_of_nodes(self):
        return self.graph.number_of_nodes()

    def get_number_of_edges(self):
        return self.graph.number_of_edges()

    def get_nodes(self):
        return list(self.graph.nodes)

    def get_edges(self):
        return list(self.graph.edges)

    def add_edge(self, n1, n2):
        return self.graph.add_edge(n1, n2)

    def add_edges_from(self, list):
        return self.graph.add_edges_from(list)

    def clear(self):
        return self.graph.clear()

    def edges(self):
        return self.graph.edges

    def nodes(self):
        return self.graph.nodes

    def get_node_attr(self, key):
        return nx.get_node_attributes(self.graph, key)

    def dfs_tree(self, node):
        return nx.edges(nx.dfs_tree(self.graph, node))

    # TODO: improve graph drawing
    def draw(self, node_labels, with_labels=True, font_wieght='bold'):
        pos = graphviz_layout(self.graph, prog='dot')
        return nx.draw(self.graph, pos=pos, labels=node_labels, with_labels=True, font_wieght='bold')
