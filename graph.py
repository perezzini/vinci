import networkx as nx

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

    def dfs_tree(self, node):
        return list(nx.dfs_tree(self.graph, node))
