"""Contains utility functions.
"""
from __future__ import division

import math
import numpy as np

def deg_to_rad(deg):
    return math.pi / 180 * deg

def rad_to_deg(rad):
    return 180 / math.pi * rad

def perspective_division(matrix):
    """
    Performs in-place perspective division on homogeneous coordinates.

    Parameters
    ----------
    matrix : iterable of 4-vectors
        the list of vectors on which to operate

    Returns
    -------
    None
    """
    for vec in matrix:
        vec[0, 0] /= vec[0, 3]
        vec[0, 1] /= vec[0, 3]
        vec[0, 2] = 1
        vec[0, 3] = 1


def clip_point(xmin, ymin, xmax, ymax, x, y):
    """Clips the point (i.e., determines if the point is in the clip
    rectangle).

    Parameters
    ----------
    xmin, ymin, xmax, ymax, x, y : float

    Returns
    -------
    bool
        `True`, if the point is inside the clip rectangle; otherwise,
        `False`.
    """
    return xmin <= x <= xmax and ymin <= y <= ymax


def clip_t(denom, num, tE_tL):
    """Computes a new value of `tE` or `tL` for an interior intersection of a
    two-dimensional line segment and an edge. Adapted from James D. Foley, ed.,
    __Computer Graphics: Principles and Practice__ (Reading, Mass. [u.a.]:
    Addison-Wesley, 1998), 122-123.

    Parameters
    ----------
    denom, num : float
    tE_tL : array (size 2) of float

    Returns
    -------
    is_updated : bool

    """
    if denom > 0:
        t = num / denom
        if t > tE_tL[1]:
            return False
        if t > tE_tL[0]:
            tE_tL[0] = t
    elif denom < 0:
        t = num / denom
        if t < tE_tL[0]:
            return False
        tE_tL[1] = t
    elif num > 0:
        return False
    return True


def clip_2d_liang_barsky(xmin, ymin, xmax, ymax, x0, y0, x1, y1):
    """Clips the two-dimensional line segment by the algorithm of Liang and
    Barsky. Adapted from James D. Foley, ed., __Computer Graphics: Principles
    and Practice__ (Reading, Mass. [u.a.]: Addison-wesley, 1998), 122.


    Parameters
    ----------
    xmin, ymin, xmax, ymax, x0, y0, x1, y1 : float

    Returns
    -------
    is_visible : bool
    x0, y0, x1, y1 : float

    """
    dx = x1 - x0
    dy = y1 - y0
    if dx == 0 and dy == 0 and clip_point(xmin, ymin, xmax, ymax, x0, y0):
        return False, x0, y0, x1, y1
    tE_tL = np.array((0.0, 1.2))
    if clip_t(dx, xmin - x0, tE_tL):
        if clip_t(-dx, x0 - xmax, tE_tL):
            if clip_t(dy, ymin - y0, tE_tL):
                if clip_t(-dy, y0 - ymax, tE_tL):
                    # compute PL intersection, if tL has moved
                    tE, tL = tE_tL
                    if tL < 1:
                        x1 = x0 + tL * dx
                        y1 = y0 + tL * dy
                    # compute PE intersection, if tE has moved
                    if tE > 0:
                        x0 += tE * dx
                        y0 += tE * dy
                    return True, x0, y0, x1, y1
    return False, x0, y0, x1, y1


def clip_3d_liang_barsky(zmin, zmax, p0, p1):
    """Clips the three-dimensional line segment in the canonial view volume by
    the algorithm of Liang and Barsky. Adapted from James D. Foley, ed.,
    __Computer Graphics: Principles and Practice__ (Reading, Mass. [u.a.]:
    Addison-Wesley, 1998), 274 as well as
    http://www.eecs.berkeley.edu/Pubs/TechRpts/1992/CSD-92-688.pdf.

    Parameters
    ----------
    zmin, zmax : float
    p0, p1 : array (size 3) of float
        the endpoints to be clipped (in-place operation)

    Returns
    -------
    is_visible : bool
    """
    x0, y0, z0 = p0
    x1, y1, z1 = p1
    # test for a trivial reject
    if (x0 > z0 and x1 > z1) or (y0 > z0 and y1 > z1) or \
       (x0 < -z0 and x1 < -z1) or (y0 < -z0 and y1 < -z1) or \
       (z0 < zmin) and (z1 < zmin) or (z0 > zmax and z1 > zmax):
        return False

    tmin_tmax = np.array((0.0, 1.0))
    dx = x1 - x0
    dz = z1 - z0
    if clip_t(-dx - dz, x0 + z0, tmin_tmax): # right side
        if clip_t(dx - dz, -x0 + z0, tmin_tmax): # left side
            # if we got this far, part of the line is in -z <= x <= z
            dy = y1 - y0
            if clip_t(dy - dz, -y0 + z0, tmin_tmax): # bottom
                if clip_t(-dy - dz, y0 + z0, tmin_tmax): # top
                    # line is in -z <= x <= z, -z <= y <= z
                    if clip_t(-dz, z0 - zmin, tmin_tmax): # front
                        if clip_t(dz, zmax - z0, tmin_tmax): # back
                            # part of the line is visible in -z <= x <= z,
                            # -z <= y <= z, -1 <= z <= zmin
                            tmin, tmax = tmin_tmax
                            if tmax < 1:
                                p1[0] = x0 + tmax * dx
                                p1[1] = y0 + tmax * dy
                                p1[2] = z0 + tmax * dz
                            if tmin > 0:
                                p0[0] += tmin * dx
                                p0[1] += tmin * dy
                                p0[2] += tmin * dz
                            return True
    return False


def clip_4d_liang_barsky(zmin, zmax, p0, p1):
    """Clips the line segment in homogeneous coordinates in the canonial view
    volume by the algorithm of Liang and Barsky. Adapted from
    http://www.eecs.berkeley.edu/Pubs/TechRpts/1992/CSD-92-688.pdf.

    Parameters
    ----------
    zmin, zmax : float
    p0, p1 : array (size 4) of float
        the endpoints to be clipped (in-place operation)

    Returns
    -------
    is_visible : bool
    """
    x0, y0, z0, w0 = p0
    x1, y1, z1, w1 = p1
    print p0, p1
    # test for a trivial reject
    if (x0 > z0 and x1 > z1) or (y0 > z0 and y1 > z1) or \
       (x0 < -z0 and x1 < -z1) or (y0 < -z0 and y1 < -z1) or \
       (z0 < zmin) and (z1 < zmin) or (z0 > zmax and z1 > zmax):
        return False
    tmin_tmax = np.array((0.0, 1.0))
    dx = x1 - x0
    dw = w1 - w0
    if clip_t(-dx - dw, x0 + w0, tmin_tmax): # left
        if clip_t(dx - dw, w0 - x0, tmin_tmax): # right
            dy = y1 - y0
            if clip_t(-dy - dw, y0 + w0, tmin_tmax): # bottom
                if clip_t(dy - dw, w0 - y0, tmin_tmax): # top
                    dz = z1 - z0
                    if clip_t(-dz, z0, tmin_tmax): # front
                        if clip_t(dz - dw, w0 - z0, tmin_tmax): # back
                            tmin, tmax = tmin_tmax
                            if tmax < 1:
                                p1[0] = x0 + tmax * dx
                                p1[1] = y0 + tmax * dy
                                p1[2] = z0 + tmax * dz
                                p1[3] = w0 + tmax * dw
                            if tmin > 0:
                                p0[0] += tmin * dx
                                p0[1] += tmin * dy
                                p0[2] += tmin * dz
                                p0[3] += tmin * dw
                            return True
    return False
