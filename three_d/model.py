"""Contains the Model class"""

from three_d.primitives import Entity3D

class Model(Entity3D):
    """Represents a wireframe mesh in its own coordinate system.

    Parameters
    ----------
    edges : iterable of edges, optional
    scale : float, optional

    Attributes
    ----------
    edges : iterable of edges
    scale : float
    """
    def __init__(self, scale=1.0, edges=[]):
        self.edges = edges
        self.scale = scale

    def add_edges(self, new_edges):
        self.edges.extend(new_edges)

    def __repr__(self):
        return 'Model(scale={!r}, edges={!r})'.format(self.scale, self.edges)
