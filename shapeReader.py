'''
 reads in text file with edge coordinates and optional color field
 returns a shape as a list of Edges
 text file has the following format on each line:
 start point, end point, color(optional)
 0 0 0, 1 0 0, 0xFFF000
'''

from three_d.primitives.edge import Edge
import numpy as np


class ShapeReader(object):

    def __init__(self, shape_file):
        self.shape_file = shape_file

    def process_file(self):
        with open(self.shape_file, 'r') as f:
            shape = []
            for line in f:
                line = line.strip()
                edge = line.split(',')
                #if no color provided defaults it to black
                if len(edge) == 2:
                    edge.append('0xFFFFFF')
                shape.append(Edge(np.array(list(edge[0]))), Edge(np.array(list(edge[1]))),
                             Edge(np.array(list(edge[2]))))
            return shape
            
            
