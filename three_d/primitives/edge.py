'''Contains the Edge class'''

import copy

from three_d.primitives.entity_3d import Entity3D

class Edge(Entity3D):
    '''Represents an edge that connects two nodes.
    '''

    def __init__(self, start, end, color=0xFFFFFF):
        self.start = start
        self.end = end
        self.color = color

    def __add__(self, vect):
        new_edge = copy.deepcopy(self)
        new_edge += vect
        return new_edge

    def __iadd__(self, vect):
        self.start += vect
        self.end += vect
        return self

    def __sub__(self, vect):
        new_edge = copy.deepcopy(self)
        new_edge -= vect
        return new_edge

    def __isub__(self, vect):
        self.start -= vect
        self.end -= vect
        return self

    def __mul__(self, v):
        new_edge = copy.deepcopy(self)
        new_edge *= v
        return new_edge

    def __imul__(self, v):
        self.start *= v
        self.end *= v
        return self

    def __repr__(self):
        return 'Edge(start={!r}, end={!r}, color=0x{:06X})' \
            .format(self.start, self.end, self.color)
