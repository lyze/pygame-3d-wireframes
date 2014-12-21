'''Contains basic shapes to draw.
'''
import numpy as np

from three_d.primitives import Edge

from game_object import GameObject

class Cube(GameObject):

    def __init__(self, position, color=0xFFFFFF, side=17, **kwargs):
        s = side / 2.0
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
        super(Cube, self).__init__(position, edges=cube, **kwargs)
        self.side = side
