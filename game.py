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
        # view.add_object(Cube(np.array([0, 0, -200]), width=50, color=0xFFFFFF))
        view.add_object(Cube(np.array([0, 10, 200]), width=50, color=0x0000FF))
        view.add_object(Cube(np.array([10, 0, 25]), width=50, color=0x00FF00))



    def tick(self):
        self.view.repaint()
