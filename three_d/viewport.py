'''Contains the viewport class'''
from __future__ import division

import math
import numpy as np
import pygame

from three_d.mathutil import deg_to_rad, normalize_projection_coords
from three_d.primitives.node import Node



class Viewport(object):
    '''Represents a view of the 3-dimensional scene.
    '''

    def __init__(self, surface, background_color=0x000000, camera=Node(0, 0, 0),
                 zoom=1, vertical_fov_deg=70, objects=[]):
        self.surface = surface
        self.background_color = background_color
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.camera = camera
        self.zoom = zoom
        self.vertical_fov_deg = vertical_fov_deg
        self.objects = objects
        self.projection_matrix = self.get_projection_matrix()
        print self.projection_matrix

    def get_projection_matrix(self):
        focal_length = 1.0 / math.tan(deg_to_rad(self.vertical_fov_deg) * 0.5
                                      / self.zoom)
        aspect_ratio = self.width / self.height

        return np.matrix([[focal_length / aspect_ratio, 0, 0, 0],
                          [0, focal_length, 0, 0],
                          [0, 0, -1, -2],
                          [0, 0, -1, 0]])

    def add_object(self, obj):
        self.objects.append(obj)

    def repaint(self):
        self.surface.fill(self.background_color)
        for obj in self.objects:
            homo_ends = []
            homo_starts = []
            colors = []
            for edge in obj.edges:
                homo_starts.append(np.append(edge.start + obj.position, 1.0))
                homo_ends.append(np.append(edge.end + obj.position, 1.0))
                colors.append(edge.color)
            proj_starts = np.matrix(homo_starts) * self.projection_matrix.T
            proj_ends = np.matrix(homo_ends) * self.projection_matrix.T
            normalize_projection_coords(proj_starts)
            normalize_projection_coords(proj_ends)

            self.to_view_coords(proj_starts)
            self.to_view_coords(proj_ends)
            print proj_starts
            for start, end, color in zip(proj_starts, proj_ends, colors):
                start = (start[0, 0], start[0, 1])
                end = (end[0, 0], end[0, 1])
                pygame.draw.line(self.surface, color, start, end, 1)

    def to_view_coords(self, proj_mat):
        proj_mat *= self.height / 2
        proj_mat[:, 1] += self.height / 2
        proj_mat[:, 0] += self.width / 2
