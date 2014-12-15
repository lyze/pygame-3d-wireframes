'''Contains the interface for a three-dimensional entity.
'''

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
