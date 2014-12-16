'''Contains a collection of edges representing an object
'''

from game_object import GameObject

class EdgeCollection(GameObject):

    def __init__(self, position, edges):
        super(EdgeCollection, self).__init__(position, edges=edges)
