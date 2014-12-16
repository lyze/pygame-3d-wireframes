'''Contains the viewport class'''
from __future__ import division

import math
import numpy as np
import pygame
import sys

from three_d.mathutil import deg_to_rad, perspective_division
from three_d.primitives.node import Node


class Viewport(object):
    '''Represents a view of the 3-dimensional scene.
    '''

    def __init__(self, surface, background_color=0x000000, eye=None,
                 at=None, up=None, zoom=1, vertical_fov_deg=70, objects=[]):
        self.surface = surface
        self.background_color = background_color
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.eye = np.array([0., 0., 0.]) #eye if eye is not None else np.array([0.0, 00.0, 0.0])
        self.look_dir = np.array([0.0, 0.0, 1.0]) # at if at is not None else np.array([0.0, 0.0, 1.0])
        self.up = up if up is not None else np.array([0.0, 1.0, 0.0])
        self.zoom = zoom
        self.vertical_fov_deg = vertical_fov_deg
        self.objects = objects
        self.projection_matrix = self.get_projection_matrix()

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
            homo_starts, homo_ends = \
                Viewport.get_homogeneous_endpoints(obj.position, obj.edges)

            if len(homo_starts) == 0 or len(homo_ends) == 0:
                continue

            homo_starts, homo_ends = \
                self.to_camera_coords(homo_starts, homo_ends)

            if len(homo_starts) == 0 or len(homo_ends) == 0:
                continue

            proj_starts = homo_starts * self.projection_matrix.T
            proj_ends = homo_ends * self.projection_matrix.T

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
                except TypeError: # start or end too big
                    continue

    @staticmethod
    def get_homogeneous_endpoints(position, edges):
        homo_ends = []
        homo_starts = []
        for edge in edges:
            homo_starts.append(np.append(edge.start + position, 1.0))
            homo_ends.append(np.append(edge.end + position, 1.0))
        return homo_ends, homo_starts

    def to_camera_coords(self, starts, ends):
        zaxis = self.look_dir
        zaxis /= np.linalg.norm(zaxis)
        xaxis = np.array(np.cross(self.up, zaxis))
        xaxis /= np.linalg.norm(xaxis)
        yaxis = np.cross(zaxis, xaxis)
        look_at = np.matrix([
            [xaxis[0], yaxis[0], zaxis[0], 0.0],
            [xaxis[1], yaxis[1], zaxis[1], 0.0],
            [xaxis[2], yaxis[2], zaxis[2], 0.0],
            [-np.dot(xaxis, self.eye), -np.dot(yaxis, self.eye),
             -np.dot(zaxis, self.eye), 1.0]])
        print look_at
        result_starts = []
        result_ends = []
        for start, end in zip(starts, ends):
            # transformed_start = (start * look_at.T).getA()
            # transformed_end = (end * look_at.T).getA()
            # exclude edges that are behind the camera
            # start_dotp = np.dot(self.look_dir, transformed_start[0, :3])
            # end_dotp = np.dot(self.look_dir, transformed_end[0, :3])
            start_dotp = np.dot(self.look_dir, start[:3])
            end_dotp = np.dot(self.look_dir, end[:3])
            if start_dotp < 0 and end_dotp < 0:
                continue
            if start_dotp == 0 or end_dotp == 0:
                continue
            result_starts.append((start * look_at.T).getA())
            result_ends.append((end * look_at.T).getA())
        return result_starts, result_ends

    def to_view_coords(self, proj_mat):
        proj_mat *= self.height / 2
        proj_mat[:, 0] += self.width / 2
        proj_mat[:, 1] += self.height / 2
        # proj_mat[:, 0] = np.clip(proj_mat[:, 0], 0, self.width)
        # proj_mat[:, 1] = np.clip(proj_mat[:, 1], 0, self.height)
        return proj_mat
