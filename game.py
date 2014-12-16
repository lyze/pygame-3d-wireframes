'''Contains the controller.
'''

import math
import numpy as np

from shapes import Cube



class Game(object):
    '''Manipulates the world (and its interactable objects) and the view.
    '''

    def __init__(self, view):
        self.view = view
        self.is_drag = False

    def tick(self):
        self.view.repaint()

    def update_mouse_rel(self, x, y):
        if not self.is_drag:
            return

        theta_x = -y * 0.005
        theta_y = -x * 0.005

        rot_x = np.matrix([[1, 0,                  0],
                           [0, math.cos(theta_x), -math.sin(theta_x)],
                           [0, math.sin(theta_x), math.cos(theta_x)]])

        rot_y = np.matrix([[math.cos(theta_y),  0, math.sin(theta_y)],
                           [0,                  1, 0],
                           [-math.sin(theta_y), 0, math.cos(theta_y)]])

        self.view.look_dir = (rot_x * rot_y *
                              np.matrix(self.view.look_dir).T).getA1()

    def start_drag(self):
        self.is_drag = True

    def end_drag(self):
        self.is_drag = False
