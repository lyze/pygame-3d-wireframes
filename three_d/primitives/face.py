'''Contains the Face class'''

class Face(object):
    '''Represents a face that contains at least three edges.
    '''

    def __init__(self, edges, color):
        self.edges = edges
        self.color = color
