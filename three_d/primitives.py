"""Contains primitive three-dimensional types
"""
import copy

from numbers import Number

from abc import ABCMeta, abstractmethod

class Entity3D(object):
    """The interface for a three-dimensional entity that can be manipulated in
    the usual ways. Subclasses must implement __imul__, __iadd__, and __isub__.
    """
    __metaclass__ = ABCMeta

    def translate(self, vect):
        self += vect
        return self

    def scale(self, center, scale):
        assert isinstance(scale, Number)
        self -= center
        self *= scale
        self += center
        return self

    @abstractmethod
    def __imul__(self, v):
        pass

    @abstractmethod
    def __iadd__(self, vect):
        pass

    @abstractmethod
    def __isub__(self, vect):
        pass

    def __mul__(self, v):
        new = copy.deepcopy(self)
        new *= v
        return new

    def __add__(self, v):
        new = copy.deepcopy(self)
        new += v
        return new

    def __sub__(self, v):
        new = copy.deepcopy(self)
        new -= v
        return new


class Edge(Entity3D):
    """Represents an edge that connects two nodes.

    Parameters
    ----------
    start, end : numpy array (of size 3)
    color : int, optional
        Default is `0xFFFFFF`.

    Attributes
    ----------
    start, end : numpy array
    color : int
    """
    def __init__(self, start, end, color=0xFFFFFF):
        self.start = start
        self.end = end
        self.color = color

    def __iadd__(self, vect):
        self.start += vect
        self.end += vect
        return self

    def __isub__(self, vect):
        self.start -= vect
        self.end -= vect
        return self

    def __imul__(self, v):
        self.start *= v
        self.end *= v
        return self

    def __repr__(self):
        return 'Edge(start={!r}, end={!r}, color=0x{:06X})' \
            .format(self.start, self.end, self.color)


class Wireframe(Entity3D):
    """Represents a wireframe mesh in its own coordinate system.

    Parameters
    ----------
    edges : iterable of edges, optional

    Attributes
    ----------
    edges : iterable of edges
    """
    def __init__(self, edges=None):
        self.edges = edges if edges is not None else []

    def __iadd__(self, vect):
        for i in xrange(len(self.edges)):
            self.edges[i] += vect

    def __isub__(self, vect):
        for i in xrange(len(self.edges)):
            self.edges[i] -= vect

    def __imul__(self, v):
        for i in xrange(len(self.edges)):
            self.edges[i] *= vect

    def __repr__(self):
        return 'Wireframe(edges={!r})'.format(self.edges)
