'''Contains the controller.
'''

import math
import numpy as np

from shapes import Cube



class Game(object):
    '''Manipulates the world (and its interactable objects) and the view.
    '''

    def __init__(self, view, objects=[]):
        self.view = view
        self.view.add_all_objects(objects)

        self.is_moving_forward = False
        self.is_moving_backward = False
        self.is_moving_left = False
        self.is_moving_right = False

        self.move_distance = 2
        self.rotation_scale_factor = 0.003


    def tick(self):
        self.view.repaint()
        if self.is_moving_forward:
            self.view.translate_z(self.move_distance)
        if self.is_moving_backward:
            self.view.translate_z(-self.move_distance)
        if self.is_moving_left:
            self.view.translate_x(-self.move_distance)
        if self.is_moving_right:
            self.view.translate_x(self.move_distance)


    def move_camera(self, dx, dy):

        theta_x = dy * self.rotation_scale_factor
        theta_y = dx * self.rotation_scale_factor

        self.view.rotate_x(theta_x)
        self.view.rotate_y(theta_y)

    def begin_move_forward(self):
        self.is_moving_forward = True

    def begin_move_backward(self):
        self.is_moving_backward = True

    def begin_move_left(self):
        self.is_moving_left = True

    def begin_move_right(self):
        self.is_moving_right = True

    def end_move_forward(self):
        self.is_moving_forward = False

    def end_move_backward(self):
        self.is_moving_backward = False

    def end_move_left(self):
        self.is_moving_left = False

    def end_move_right(self):
        self.is_moving_right = False
