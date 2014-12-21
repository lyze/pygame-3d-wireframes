# TODO: PerspectiveViewport: Actually do something with this copypasted

"""Contains an implementation of a viewport that uses a perspective projection.
"""
from __future__ import division

import math
import numpy as np

from three_d.mathutil import deg_to_rad
from three_d.cameras.viewport import Viewport

class PerspectiveViewport(Viewport):
    """Represents a view of the 3-dimensional scene.

    Parameters
    ----------
    center_offset : tuple of float, optional
        The offset (xy-plane translation) to apply to the center of the view.
        Default is no offset.
    vertical_fov_deg, vertical_fov_rad : float, optional
        If both are `vertical_fov_deg` and `vertical_fov_rad` specified, the
        value of `vertical_fov_rad` is used. Default is 70 degrees.

    Attributes
    ----------
    vertical_fov_rad
    center_offset
    near
    far
    """
    def __init__(self, surface, vertical_fov_deg=70, vertical_fov_rad=None,
                 **kwargs):
        if vertical_fov_rad is not None:
            self._vertical_fov_rad = vertical_fov_rad
        else:
            assert vertical_fov_deg is not None
            self._vertical_fov_rad = deg_to_rad(vertical_fov_deg)
        super(PerspectiveViewport, self).__init__(surface, **kwargs)

    def update_projection_matrix(self):
        dx = self.center_offset[0]
        dy = self.center_offset[1]
        f = self.far
        n = self.near
        h = 2 * math.tan(self.vertical_fov_rad / 2)
        w = h * self.width / self.height
        r = w / 2 - dx
        l = -w / 2 - dx
        t = h / 2 - dy
        b = -h / 2 - dy
        if self.far == float('inf'):
            self._projection_matrix = np.matrix([
            [2.0 / w, 0,         -(l + r) / w, 0],
            [0,           2 / h, -(t + b) / h, 0],
            [0,           0,     1,            n],
            [0,           0,     1,            0]])
        else:
            p = f - n
            # focal_length = 1.0 / math.tan(self.vertical_fov_rad * 0.5 / self.zoom)
            # aspect_ratio = self.width / self.height
            self._projection_matrix = np.matrix([
            [2.0 / w, 0,         -(l + r) / w, 0],
            [0,           2 / h, -(t + b) / h, 0],
            [0,           0,     f / p,        -n * f / p],
            [0,           0,     1,            0]])


    def to_view_coords(self, projected_points):
        view = np.empty((projected_points.shape[0], 2))
        view[:, (0, 1)] = (self.height / 2) * projected_points[:, (0, 1)]
        view[:, 0] += self.width / 2 + self.center_offset[0]
        view[:, 1] += self.height / 2 + self.center_offset[1]
        return view

    @property
    def vertical_fov_rad(self):
        """The vertical field-of-view in radians.
        """
        return self._vertical_fov_rad
