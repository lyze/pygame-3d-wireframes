'''Contains utility math functions
'''

import math

def deg_to_rad(deg):
    return math.pi / 180 * deg

def rad_to_deg(rad):
    return 180 / math.pi * rad

def perspective_division(matrix):
    for vec in matrix:
        vec[0, 0] /= vec[0, 3]
        vec[0, 1] /= vec[0, 3]
        vec[0, 2] = 1
        vec[0, 3] = 1
