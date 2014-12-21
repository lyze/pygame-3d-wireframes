"""Contains the base class for all three-dimensional viewports."""
from __future__ import division

import logging
import math
import numpy as np
import pygame
import time

from abc import ABCMeta, abstractmethod
from three_d.mathutil import perspective_division, clip_4d_liang_barsky
from itertools import chain, izip

def timed(f):
  def wrapper(*args):
      now = time.clock()
      result = f(*args)
      logging.log(1, '{}: {}'.format(f.__name__, time.clock() - now))
      return result
  return wrapper


class Viewport(object):
    """Represents a view of the 3-dimensional scene using a left-handed
    coordinate system.

    Parameters
    ----------
    surface : pygame surface
    background_color : int, optional
    eye : numpy array, optional
        Defaults to (0, 0, 0).
    center_offset : tuple of float, optional
        The offset (xy-plane translation) to apply to the center of the view.
        Default is no offset, which is (0, 0).
    look_dir : numpy array, optional
        Defaults to (0, 0, 1).
    up : numpy array, optional
        Defaults to (0, 1, 0).
    zoom : float, optional
    objects : iterable of things to draw, optional

    Attributes
    ----------
    surface
    width
    height
    background_color : int
    eye : 3-D numpy array
    center_offset : tuple of float
    near : float
    far : float
    look_dir
    up_dir
    strafe_dir
    zoom : float
    projection_matrix
    objects : iterable of things to draw
    """
    __metaclass__ = ABCMeta

    def __init__(self, surface, background_color=0x000000, eye=None,
                 center_offset=(0, 0), near=0, far=float('inf'), look_dir=None,
                 up_dir=None, zoom=1.0, objects=None):
        self._surface = surface
        self.background_color = background_color
        self.eye = eye if eye is not None else np.array([0.0, 0.0, 0.0])
        self.center_offset = center_offset
        self.near = near
        self.far = far
        self._look_dir = look_dir or np.array([0.0, 0.0, 1.0])
        self._look_dir /= np.linalg.norm(self._look_dir)
        self._up_dir = up_dir or np.array([0.0, 1.0, 0.0])
        self._up_dir /= np.linalg.norm(self._up_dir)
        self._strafe_dir = np.cross(self.look_dir, self.up_dir)
        self.zoom = zoom
        self.objects = objects or []
        self._projection_matrix = None
        self.update_projection_matrix()

    @abstractmethod
    def update_projection_matrix(self):
        """Updates the projection matrix (`self._projection_matrix`) of this viewport.
        Should be called when the view parameters are changed.
        """
        pass

    def add_object(self, obj):
        self.objects.append(obj)

    def add_all_objects(self, objs):
        self.objects.extend(objs)

    @timed
    def repaint(self):
        self.surface.fill(self.background_color)

        world_to_camera = self.get_world_to_camera_matrix()
        transform = self.projection_matrix * world_to_camera

        for obj in self.objects:
            world_starts, world_ends = \
                Viewport.get_world_endpoints(obj.position, obj.edges)

            if len(world_starts) == 0 or len(world_ends) == 0:
                continue

            proj_starts = transform * world_starts.T
            proj_ends = transform * world_ends.T
            proj_starts = proj_starts.T
            proj_ends = proj_ends.T

            # visible = (clip_4d_liang_barsky(self.near, self.far,
            #                                 start.getA1(),
            #                                 end.getA1())
            #            for start, end in izip(proj_starts, proj_ends))
            # visible = np.fromiter(visible, dtype=bool)
            # proj_starts = proj_starts[visible]
            # proj_ends = proj_ends[visible]
            # colors = (edge.color
            #           for i, edge in enumerate(obj.edges) if visible[i])

            colors = (edge.color for edge in obj.edges)

            perspective_division(proj_starts)
            perspective_division(proj_ends)

            view_starts = self.to_view_coords(proj_starts)
            view_ends = self.to_view_coords(proj_ends)

            for start, end, color in izip(view_starts, view_ends, colors):
                pygame.draw.line(self.surface, color, start, end, 1)

    @staticmethod
    def get_world_endpoints(pos, edges):
        """Returns the edge endpoints in homogeneous world coordinates

        Parameters
        ----------
        pos : numpy array
        edges : iterable of Edge

        Returns
        -------
        tuple of iterable of points
            a value in the form `(start_points, end_points)`, where
            `start_points` and `end_points` are in the form of a numpy matrix
        """
        edge_starts = (coord
                       for edge in edges
                       for coord in chain(edge.start + pos, (1.0, )))
        edge_ends = (coord
                     for edge in edges
                     for coord in chain(edge.end + pos, (1.0, )))

        homo_starts = np.fromiter(edge_starts, np.float, count=4 * len(edges))
        homo_ends = np.fromiter(edge_ends, np.float, count=4 * len(edges))

        homo_starts = homo_starts.reshape((len(edges), 4))
        homo_ends = homo_ends.reshape((len(edges), 4))

        return homo_starts, homo_ends


    def get_world_to_camera_matrix(self):
        """Computes the matrix that transforms the world coordinates to camera
        coordinates.
        """
        xaxis = self.strafe_dir
        yaxis = self.up_dir
        zaxis = self.look_dir
        return np.matrix([
            [xaxis[0], xaxis[1], xaxis[2], -np.dot(xaxis, self.eye)],
            [yaxis[0], yaxis[1], yaxis[2], -np.dot(yaxis, self.eye)],
            [zaxis[0], zaxis[1], zaxis[2], -np.dot(zaxis, self.eye)],
            [0.0,      0.0,      0.0,      1.0]])

    @abstractmethod
    def to_view_coords(self, projected_points):
        """Converts the projected points the coordinate system of the view.

        Parameters
        ----------
        projected_points : iterable of array-like
            the numpy matrix with the position vectors in row-major order

        Returns
        -------
        view_points : iterable of array-like (of at least size 2)
            the points, which must be at least two-dimensional, in the
            coordinate system of the view
        """
        pass

    def rotate_x(self, theta):
        rot_x = np.matrix([[1.0, 0.0,             0.0],
                           [0.0, math.cos(theta), -math.sin(theta)],
                           [0.0, math.sin(theta), math.cos(theta)]])

        self._up_dir = (self.up_dir * rot_x.T).getA1()
        self._look_dir = np.cross(self.up_dir, self.strafe_dir)

    def rotate_y(self, theta):
        rot_y = np.matrix([[math.cos(theta),  0.0, math.sin(theta)],
                           [0.0,              1.0, 0.0],
                           [-math.sin(theta), 0.0, math.cos(theta)]])

        self._look_dir = (self.look_dir * rot_y.T).getA1()
        self._strafe_dir = np.cross(self.look_dir, self.up_dir)

    def rotate_z(self, theta):
        rot_z = np.matrix([[math.cos(theta), -math.sin(theta), 0.0],
                           [math.sin(theta), math.cos(theta),  0.0],
                           [0.0,             0.0,              1.0]])
        self._strafe_dir = (self.strafe_dir * rot_z.T).getA1()
        self._up_dir = np.cross(self.strafe_dir, self.look_dir)

    def translate(self, vect):
        self.eye += vect

    @property
    def surface(self):
        """The underlying pygame surface.
        """
        return self._surface

    @property
    def width(self):
        """The width of this viewport.
        """
        return self.surface.get_width()

    @property
    def height(self):
        """The height of this viewport.
        """
        return self.surface.get_height()

    @property
    def up_dir(self):
        """The unit vector representing the direction of "up".
        """
        return self._up_dir

    @property
    def look_dir(self):
        """The unit vector representing the direction the camera is pointing.
        """
        return self._look_dir

    @property
    def strafe_dir(self):
        """The unit vector representing the direction of "strafe" movements.
        """
        return self._strafe_dir

    @property
    def projection_matrix(self):
        """The projection matrix used by the view.
        """
        return self._projection_matrix
