'''Contains primitive three-dimensional types
'''
import copy

from numbers import Number


class Entity3D(object):
    '''The interface for a three-dimensional entity that can be manipulated in
    the usual ways. Subclasses must implement __imul__, __iadd__, and __isub__.
    '''

    def translate(self, vect):
        assert len(vect) == 3
        self += vect
        return self

    def scale(self, center, scale):
        assert len(center) == 3
        assert isinstance(scale, Number)
        self -= center
        self *= scale
        self += center
        return self


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
