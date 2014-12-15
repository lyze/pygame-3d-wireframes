'''Contains basic shapes to draw.
'''
import numpy as np

from three_d.primitives.edge import Edge

from game_object import GameObject

class Cube(GameObject):

    def __init__(self, position, color=0xFFFFFF, width=17):
        s = width / 2.0
        cube = [Edge(np.array([-s, -s, -s]), np.array([-s, -s, s]), color=color),
                Edge(np.array([-s, -s, -s]), np.array([-s, s, -s]), color=color),
                Edge(np.array([-s, -s, -s]), np.array([s, -s, -s]), color=color),
                Edge(np.array([-s, -s, s]), np.array([-s, s, s]), color=color),
                Edge(np.array([-s, -s, s]), np.array([s, -s, s]), color=color),
                Edge(np.array([-s, s, -s]), np.array([-s, s, s]), color=color),
                Edge(np.array([-s, s, -s]), np.array([s, s, -s]), color=color),
                Edge(np.array([s, -s, -s]), np.array([s, s, -s]), color=color),
                Edge(np.array([s, -s, -s]), np.array([s, -s, s]), color=color),
                Edge(np.array([-s, s, s]), np.array([s, s, s]), color=color),
                Edge(np.array([s, -s, s]), np.array([s, s, s]), color=color),
                Edge(np.array([s, s, -s]), np.array([s, s, s]), color=color)]
        super(Cube, self).__init__(position, edges=cube)
        self.width = width
