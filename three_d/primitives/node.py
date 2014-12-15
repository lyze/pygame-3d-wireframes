'''Contains the Node class'''

import copy
import numpy as np

class Node(object):
    '''Represents an infinitesimal point that delimits the endpoints of an edge.
    '''

    def __init__(self, x, y, z):
        self.coordinates = np.array([x, y, z])

    def __add__(self, vect):
        new_node = copy.deepcopy(self)
        new_node += vect
        return new_node

    def __iadd__(self, vect):
        self.coordinates += vect
        return self

    def __sub__(self, vect):
        new_node = copy.deepcopy(self)
        new_node -= vect
        return new_node

    def __isub__(self, vect):
        self.coordinates -= vect
        return self

    def __mul__(self, v):
        new_node = copy.deepcopy(self)
        new_node *= v
        return new_node

    def __imul__(self, v):
        self.coordinates *= v
        return self

    def __repr__(self):
        return 'Node(coordinates={!r})'.format(self.coordinates)
