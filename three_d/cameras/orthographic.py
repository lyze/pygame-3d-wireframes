"""Contains an implementation of a viewport that uses an orthogrpahic
projection.
"""
from __future__ import division

import numpy as np

from three_d.cameras.viewport import Viewport

class OrthographicViewport(Viewport):
    """A view displaying an orthographic projection of the scene.
    """
    def __init__(self, surface, **kwargs):
        super(OrthographicViewport, self).__init__(surface, **kwargs)

    def update_projection_matrix(self):
        w = self.width
        h = self.height
        f = self.far
        n = self.near
        p = f - n
        dx = self.center_offset[0]
        dy = self.center_offset[1]
        r = w / 2 - dx
        l = -w / 2 - dx
        t = h / 2 - dy
        b = -h / 2 - dy
        self._projection_matrix = np.matrix([
            [2.0 / w, 0,     0,          -(r + l) / w],
            [0,       2 / h, 0,          -(t + b) / h],
            [0,       0,     1 / (f - n), n / (n - f)],
            [0,       0,     0,           1]])

    def to_view_coords(self, projected_points):
        view = np.empty((projected_points.shape[0], 2))
        view[:, 0] = self.width * projected_points[:, 0].getA1()
        view[:, 0] += self.center_offset[0] + self.width / 2
        view[:, 1] = self.height * projected_points[:, 1].getA1()
        view[:, 1] += self.center_offset[1] + self.height / 2
        return view
