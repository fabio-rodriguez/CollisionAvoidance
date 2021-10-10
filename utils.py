import numpy as np

from math import *
from numpy.linalg import norm


# Dist from line between points p1 and p2, to point p3
def distance_from_line_2point(p1, p2, p3):
    return norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)


# Detect if uav1 with direction d1 collides with uav2 with direction d2
def collide(uav1, d1, uav2, d2, timestep):
    ## The first must be the slower
    uav1, uav2 = (uav1, uav2) if uav1.speed < uav2.speed else (uav2, uav1)    
    diffvector = d2*uav2.speed - d1*uav1*speed
    p2 = uav2.position + diffvector
    cat1 = distance_from_line_2point(UAV2.position, p2, UAV1.position) 
    
    if cat1 < (uav1.radio + uav2.radio):
        cat2 = euclidian_distance(uav1.position, uav2.position)
        hip = sqrt(cat1**2 + cat2**2)
        return hip < uav2.speed*timestep
    
    return True


# Detect if two uavs in the list collide 
def list_collide(uavs, directions, timestep):
    for i in range(len(uavs)):
        for j in range(i, len(uavs)):  
            if collide(uavs[i], directions[i], uavs[j], directions[j], timestep):
                return True


def vector_2angles(vector):
    vx, vy = vector
    # phi, r
    return atan2(vy, vx) % (2 * pi), sqrt(Vx**2 + Vy**2)


def angles_2vector(phi, theta = pi/2, r = 1):
    return np.array([r*sin(theta)*cos(phi), r*sin(theta)*sin(phi)])


def euclidian_distance(vector1, vector2):
    return sqrt(sum([(x-y)**2 for x,y in zip(vector1, vector2)]))


def get_normalized_vector(vector):
    vx, vy, vz = vector
    n = vector_norm(vector)
    return (vx/n, vy/n, vz/n)


def vector_norm(vector):
    return sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
