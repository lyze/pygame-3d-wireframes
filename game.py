'''Contains the controller.
'''

import numpy as np

from shapes import Cube

class Game(object):
    '''Manipulates the world (and its interactable objects) and the view.
    '''

    def __init__(self, view):
        self.view = view
        view.add_object(Cube(np.array([0, 0, 0]), width=10, color=0xFF0000))
        # view.add_object(Cube(np.array([100, 500, 10]), width=50, color=0xFFFFFF))


    def tick(self):
        self.view.repaint()
