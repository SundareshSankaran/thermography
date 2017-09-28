import numpy as np


def angle(pt1, pt2):
    """
    Computes the angle (in radiants) between a segment specified by the two points and the x-axis.
    :param pt1: First point of the segment.
    :param pt2: Second point of the segment.
    :return: Angle in radiants between the segment and the x-axis. The returned angle is in [0, pi]
    """
    a = np.arctan2(pt2[1] - pt1[1], pt2[0] - pt1[0])
    if a > np.pi:
        a -= np.pi
    elif a < 0:
        a += np.pi
    return a


def min_distance(seg1, seg2):
    """
    Computes the minimal distance between two segments.
    Implementation taken form "https://ch.mathworks.com/matlabcentral/fileexchange/32487-shortest-distance-between-two-line-segments?focused=3821416&tab=function"
    :param seg1: First segment defined as [x1, y1, x2, y2]
    :param seg2: Second segment defined as [x2, y3, x4, y4]
    :return: The minimal distance between the two segments
    """
    p1 = seg1[0:2]
    p2 = seg1[2:4]
    p3 = seg2[0:2]
    p4 = seg2[2:4]

    u = p1 - p2
    v = p3 - p4
    w = p2 - p4

    a = np.dot(u, u)
    b = np.dot(u, v)
    c = np.dot(v, v)
    d = np.dot(u, w)
    e = np.dot(v, w)
    D = a * c - b * b
    sD = D
    tD = D

    eps = 0.0001

    if D < eps:  # the lines are almost parallel
        sN = 0.0  # force using point P0 on segment S1
        sD = 1.0  # to prevent possible division by 0.0 later
        tN = e
        tD = c
    else:  # get the closest points on the infinite lines
        sN = (b * e - c * d)
        tN = (a * e - b * d)
        if sN < 0.0:  # sc < 0 = > the s=0 edge is visible
            sN = 0.0
            tN = e
            tD = c
        elif sN > sD:  # sc > 1 = > the s = 1 edge is visible
            sN = sD
            tN = e + b
            tD = c

    if tN < 0.0:  # tc < 0 = > the t=0 edge is visible
        tN = 0.0
        # recompute sc for this edge
        if -d < 0.0:
            sN = 0.0
        elif -d > a:
            sN = sD
        else:
            sN = -d
            sD = a
    elif tN > tD:  # tc > 1 = > the t = 1 edge is visible
        tN = tD
        # recompute sc for this edge
        if (-d + b) < 0.0:
            sN = 0
        elif (-d + b) > a:
            sN = sD
        else:
            sN = (-d + b)
            sD = a

    # finally do the division to get sc and tc
    if np.abs(sN) < eps:
        sc = 0.0
    else:
        sc = sN / sD

    if np.abs(tN) < eps:
        tc = 0.0
    else:
        tc = tN / tD

    # get the difference of the two closest points
    dP = w + (sc * u) - (tc * v)  # = S1(sc) - S2(tc)
    distance = np.linalg.norm(dP)

    return distance