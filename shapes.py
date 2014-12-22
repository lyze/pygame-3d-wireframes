'''Contains basic shapes to draw.
'''
import numpy as np

from three_d.primitives import Edge

from three_d.model import Model

class Cube(Model):

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
