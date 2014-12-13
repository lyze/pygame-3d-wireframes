'''Contains the Edge class'''

class Edge(object):
    '''Represents an edge that connects two nodes.
    '''

    def __init__(self, start, end, color):
        self.start = start
        self.end = end
        self.color = color
