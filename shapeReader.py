'''
 reads in text file with edge coordinates and optional color field
 returns a list of lists of edges with coordinates and color
'''

class ShapeReader(object):

    def __init__(self, shape_file):
        self.shape_file = shape_file

    def process_file(self):
        with open(self.shape_file, 'r') as f:
            edges = []
            for line in f:
                line = line.strip()
                edge = line.split(',')
                egdes.append(edge)
            return edges