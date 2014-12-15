'''Contains the Model class'''

from three_d.primitives.entity_3d import Entity3D

class Model(Entity3D):
    '''Represents a wireframe mesh in its own coordinate system'''

    def __init__(self, edges=[]):
        self.edges = edges

    def add_edges(self, new_edges):
        self.edges.extend(new_edges)

    def __repr__(self):
        return 'Model(edges={!r})'.format(self.edges)
