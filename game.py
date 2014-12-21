'''Contains the controller.
'''
import numpy as np

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
        # movement
        move_dir = np.zeros(3)
        if self.is_moving_forward:
            move_dir += self.view.look_dir
        if self.is_moving_backward:
            move_dir -= self.view.look_dir
        if self.is_moving_left:
            move_dir -= self.view.strafe_dir
        if self.is_moving_right:
            move_dir += self.view.strafe_dir
        dir_length = np.linalg.norm(move_dir)
        if dir_length \
           and (self.is_moving_forward or self.is_moving_backward
                or self.is_moving_left or self.is_moving_right):
            move_dir /= dir_length
            self.view.translate(self.move_distance * move_dir)
        self.view.repaint()

    def move_camera(self, dx, dy):
        theta_x = -dy * self.rotation_scale_factor
        theta_y = -dx * self.rotation_scale_factor

        if theta_x:
            self.view.rotate_x(theta_x)
        if theta_y:
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
