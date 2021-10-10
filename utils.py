import numpy as np

from math import *
from numpy.linalg import norm


# Dist from line between points p1 and p2, to point p3
def distance_from_line_2point(p1, p2, p3):
    return norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)


# Detect if uav1 with direction d1 collides with uav2 with direction d2
def collide(uav1, d1, uav2, d2):
    ## The first must be the slower
    uav1, uav2 = (uav1, uav2) if uav1.speed < uav2.speed else (uav2, uav1)    
    diffvector = d2*uav2.speed - d1*uav1*speed
    p2 = uav2.position + diffvector
    return distance_from_line_2point(UAV2.position, p2, UAV1.position) < (uav1.radio + uav2.radio)


def vector_2angles(vector):
    vx, vy = vector
    # phi, r
    return atan2(vy, vx) % (2 * pi), (Vx**2 + Vy**2)**0.5


def angles_2vector(phi, theta = pi/2, r = 1):
    return np.array([r*sin(theta)*cos(phi), r*sin(theta)*sin(phi)])


