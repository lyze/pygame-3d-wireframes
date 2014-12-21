'''Contains the interface for a game object model in our game world.
'''

from three_d.model import Model

class GameObject(Model):
    """Represents a wireframe model in the game world.

    Parameters
    ----------
    position : numpy array (of size 3)

    Attributes
    ----------
    position : numpy array
    """
    def __init__(self, position, **kwargs):
        super(GameObject, self).__init__(**kwargs)
        self.position = position
