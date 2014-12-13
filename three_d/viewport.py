'''Contains the viewport class'''

import math

from mathutil import deg_to_rad, rad_to_deg
from primitives.node import Node

class Viewport(object):
    '''Represents a view of the 3-dimensional scene.
    '''

    def __init__(self, context, camera=Node(0, 0, 0), zoom=1,
                 vertical_fov_deg=70, objects=[]):
        self.context = context
        self.width = context.get_width()
        self.height = context.get_height()
        self.camera = camera
        self.zoom = zoom
        self.vertical_fov_deg = vertical_fov_deg
        self.objects = objects

        self.update_projection_matrix()

    def update_projection_matrix(self):
        vertical_fov_rad = rad_to_deg(2 * math.atan(
            math.tan(deg_to_rad(self.vertical_fov_deg) * 0.5) / self.zoom))

    def tick(self):
        pass
