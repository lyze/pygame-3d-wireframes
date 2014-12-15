'''Contains the interface for a game object model in our game world.
'''

from three_d.model import Model

class GameObject(Model):

    def __init__(self, position, edges=[]):
        super(GameObject, self).__init__(edges)
        self.position = position
