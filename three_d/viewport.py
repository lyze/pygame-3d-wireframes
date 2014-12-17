'''Contains the viewport class'''
from __future__ import division

import itertools
import logging
import math
import numpy as np
import pygame
import time

from three_d.mathutil import deg_to_rad, perspective_division

def timed(f):
  def wrapper(*args):
      now = time.clock()
      result = f(*args)
      logging.log(1, '{}: {}'.format(f.__name__, time.clock() - now))
      return result
  return wrapper


class Viewport(object):
    '''Represents a view of the 3-dimensional scene.
    '''

    def __init__(self, surface, background_color=0x000000, eye=None,
                 look_dir=None, up=None, zoom=1.0, vertical_fov_deg=70,
                 objects=[]):
        self.surface = surface
        self.background_color = background_color
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.eye = eye if eye is not None else np.array([0.0, 0.0, 0.0])
        self.look_dir = look_dir if look_dir is not None \
                        else np.array([0.0, 0.0, 1.0])
        self.up = up if up is not None else np.array([0.0, 1.0, 0.0])
        self.up /= np.linalg.norm(self.up)
        self.zoom = zoom
        self.vertical_fov_deg = vertical_fov_deg
        self.objects = objects
        self.projection_matrix = self.get_projection_matrix()

    def get_projection_matrix(self):
        focal_length = 1.0 / math.tan(deg_to_rad(self.vertical_fov_deg) * 0.5
                                      / self.zoom)
        aspect_ratio = self.width / self.height

        return np.matrix([[focal_length / aspect_ratio, 0.0, 0.0, 0.0],
                          [0.0, focal_length, 0.0, 0.0],
                          [0.0, 0.0, -1.0, -2.0],
                          [0.0, 0.0, -1.0, 0.0]])

    def add_object(self, obj):
        self.objects.append(obj)

    def add_all_objects(self, objs):
        self.objects.extend(objs)

    @timed
    def repaint(self):
        self.surface.fill(self.background_color)
        for obj in self.objects:

            world_starts, world_ends = \
                Viewport.get_world_endpoints(obj.position, obj.edges)

            if len(world_starts) == 0 or len(world_ends) == 0:
                continue

            camera_starts, camera_ends = \
                self.to_camera_coords(world_starts, world_ends)

            if len(camera_starts) == 0 or len(camera_ends) == 0:
                continue

            proj_starts = camera_starts * self.projection_matrix.T
            proj_ends = camera_ends * self.projection_matrix.T

            colors = (edge.color for edge in obj.edges)

            perspective_division(proj_starts)
            perspective_division(proj_ends)

            proj_starts = self.to_view_coords(proj_starts)
            proj_ends = self.to_view_coords(proj_ends)

            for start, end, color in zip(proj_starts, proj_ends, colors):
                start = (start[0, 0], start[0, 1])
                end = (end[0, 0], end[0, 1])
                try:
                    pygame.draw.line(self.surface, color, start, end, 1)
                except TypeError:  # start or end too big
                    continue

    @staticmethod
    def get_world_endpoints(pos, edges):
        '''Returns the edge endpoints in homogeneous world coordinates
        '''
        edge_starts = (coord
                       for edge in edges
                       for coord in itertools.chain(edge.start + pos, (1.0, )))
        edge_ends = (coord
                     for edge in edges
                     for coord in itertools.chain(edge.end + pos, (1.0, )))

        homo_starts = np.fromiter(edge_starts, np.float, count=4 * len(edges))
        homo_ends = np.fromiter(edge_ends, np.float, count=4 * len(edges))

        homo_starts = homo_starts.reshape((len(edges), 4))
        homo_ends = homo_ends.reshape((len(edges), 4))

        return homo_starts, homo_ends

    def to_camera_coords(self, starts, ends):
        zaxis = self.get_look_dir()
        xaxis = self.get_strafe_dir()
        yaxis = self.up
        look_at = np.matrix([
            [xaxis[0], xaxis[1], xaxis[2], -np.dot(xaxis, self.eye)],
            [yaxis[0], yaxis[1], yaxis[2], -np.dot(yaxis, self.eye)],
            [zaxis[0], zaxis[1], zaxis[2], -np.dot(zaxis, self.eye)],
            [0.0,      0.0,      0.0,      1.0]])
        result_starts = []
        result_ends = []
        for start, end in zip(starts, ends):
            start_dotp = np.dot(self.look_dir, start[:3])
            end_dotp = np.dot(self.look_dir, end[:3])
            if start_dotp < 0 and end_dotp < 0:
                continue
            if start_dotp == 0 or end_dotp == 0:
                continue
            result_starts.append((look_at
                                  * np.matrix(start, copy=False).T).getA1())
            result_ends.append((look_at * np.matrix(end, copy=False).T).getA1())
        return result_starts, result_ends

    def to_view_coords(self, proj_mat):
        proj_mat *= self.height / 2
        proj_mat[:, 0] += self.width / 2
        proj_mat[:, 1] += self.height / 2
        return proj_mat

    def rotate_x(self, theta):
        rot_x = np.matrix([[1, 0,               0],
                           [0, math.cos(theta), -math.sin(theta)],
                           [0, math.sin(theta), math.cos(theta)]])

        self.look_dir = (rot_x * np.matrix(self.look_dir, copy=False).T).getA1()
        self.up = (rot_x * np.matrix(self.up, copy=False).T).getA1()

    def rotate_y(self, theta):
        rot_y = np.matrix([[math.cos(theta),  0, math.sin(theta)],
                           [0,                  1, 0],
                           [-math.sin(theta), 0, math.cos(theta)]])

        self.look_dir = (rot_y * np.matrix(self.look_dir, copy=False).T).getA1()

    def translate(self, vect):
        self.eye += vect

    def get_look_dir(self):
        '''Returns the unit vector representing the direction that the camera is
        facing
        '''
        return self.look_dir / np.linalg.norm(self.look_dir)

    def get_strafe_dir(self):
        '''Returns the unit vector representing the direction of a sideways move
        to the right.
        '''
        return np.cross(self.get_look_dir(), self.up)
