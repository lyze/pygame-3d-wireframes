'''Contains the Model class'''

class Model(object):
    '''Represents a wireframe mesh in its own coordinate system'''

    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges

    def add_nodes(self, new_nodes):
        self.nodes.extend(new_nodes)

    def add_edges(self, new_edges):
        self.edges.extend(new_edges)
