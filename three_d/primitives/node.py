'''Contains the Node class'''

import numpy as np

class Node(object):
    '''Represents an infinitesimal point that delimits the endpoints of an edge.
    '''

    def __init__(self, x, y, z):
        self.coordinates = np.array([x, y, z])
