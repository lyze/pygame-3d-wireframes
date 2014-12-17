'''
 reads in text file with edge coordinates and optional color field
 returns a shape as a list of Edges
 text file has the following format on each line:
 start point, end point, color(optional)
 0 0 0, 1 0 0, 0xFFF000
'''
import numpy as np
import re

from three_d.primitives import Edge
from edge_collection import EdgeCollection

class ShapeReader(object):

    def __init__(self, shape_file):
        self.shape_file = shape_file

    @staticmethod
    def parse_color(s):
        result = re.match(r'#([A-Fa-f0-9]{6})', s.strip())
        if result is None:
            return 0xFFFFFF
        return int(result.group(1), 16)

    @staticmethod
    def parse_point(s):
        coords = s.strip().split(' ')
        try:
            return np.array([float(coords[0]), float(coords[1]),
                             float(coords[2])])
        except ValueError:
            return None

    def process_file(self):
        with open(self.shape_file, 'r') as f:
            edges = []
            for line in f:
                parts = line.split(',')
                if len(parts) != 2 and len(parts) != 3:
                    continue
                if len(parts) == 2:
                    color = 0xFFFFFF
                else:
                    color = ShapeReader.parse_color(parts[2])
                start = ShapeReader.parse_point(parts[0])
                if start is None:
                    continue
                end = ShapeReader.parse_point(parts[1])
                if end is None:
                    continue
                edges.append(Edge(start, end, color))

            return EdgeCollection(np.array([0, 0, 0]), edges)
