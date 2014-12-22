"""Contains the interface for a game object model in our game world.
"""
from three_d.primitives import Wireframe

class Model(Wireframe):
    """Represents a wireframe model in the game world.

    Parameters
    ----------
    position : numpy array (of size 3)
    scale : float, optional

    Attributes
    ----------
    position : numpy array
    scale : float
    """
    def __init__(self, position, scale=1.0, **kwargs):
        super(Model, self).__init__(**kwargs)
        self.position = position
        self.scale = scale
