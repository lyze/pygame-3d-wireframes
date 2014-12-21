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
        super(PerspectiveViewport, self).__init__(surface, **kwargs)
        if vertical_fov_rad is not None:
            self._vertical_fov_rad = vertical_fov_rad
        else:
            assert vertical_fov_deg is not None
            self.vertical_fov_rad = deg_to_rad(vertical_fov_deg)

    def update_projection_matrix(self):
        focal_length = 1.0 / math.tan(self.vertical_fov_rad * 0.5 / self.zoom)
        aspect_ratio = self.width / self.height
        self._projection_matrix = np.matrix([
            [focal_length / aspect_ratio, 0.0, 0.0, 0.0],
            [0.0, focal_length, 0.0, 0.0],
            [0.0, 0.0, -1.0, -2.0],
            [0.0, 0.0, -1.0, 0.0]])


    # def to_view_coords(self, proj_mat):
        # TODO to_view_coords

    @property
    def vertical_fov_rad(self):
        """The vertical field-of-view in radians.
        """
        return self._vertical_fov_rad
