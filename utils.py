import matplotlib.pyplot as plt
import numpy as np

from math import *
from numpy.linalg import norm


# Dist from line between points p1 and p2, to point p3
def distance_from_line_2point(p1, p2, p3):
    den = 10**-10 if norm(p2-p1) == 0 else norm(p2-p1)
    return norm(np.cross(p2-p1, p1-p3)) / den


def collinear(p0, p1, p2, epsilon=1e-12):
    x1, y1 = p1[0] - p0[0], p1[1] - p0[1]
    x2, y2 = p2[0] - p0[0], p2[1] - p0[1]
    return abs(x1 * y2 - x2 * y1) < epsilon


# Detect if uav1 with direction d1 collides with uav2 with direction d2
def collide(uav1, d1, uav2, d2, timestep):
    ## The first must be the slower
    uav1, d1, uav2, d2 = (uav1, d1, uav2, d2) if uav1.speed < uav2.speed else (uav2, d2, uav1, d1)
    diffvector = d2*uav2.speed - d1*uav1.speed
    p2 = uav2.position + diffvector
    cat1 = distance_from_line_2point(uav2.position, p2, uav1.position) 
    
    if cat1 < (uav1.radio + uav2.radio):
        hip = euclidian_distance(uav1.position, uav2.position)
        cat2 = sqrt(hip**2 - cat1**2)
        return cat2 < vector_norm(diffvector)*timestep
    
    return False


# Detect if two uavs in the list collide 
def list_collide(uavs, directions, timestep):
    for i in range(len(uavs)-1):
        for j in range(i+1, len(uavs)):  
            if collide(uavs[i], directions[i], uavs[j], directions[j], timestep):
                return True


def vector_2angles(vector):
    vx, vy = vector
    # phi, r
    return atan2(vy, vx) % (2 * pi), sqrt(vx**2 + vy**2)


def angles_2vector(phi, theta = pi/2, r = 1):
    return np.array([r*sin(theta)*cos(phi), r*sin(theta)*sin(phi)])


def euclidian_distance(vector1, vector2):
    return sqrt(sum([(x-y)**2 for x,y in zip(vector1, vector2)]))


def get_normalized_vector(vector):
    vx, vy = vector
    n = vector_norm(vector)
    return np.array([vx/n, vy/n])


def vector_norm(vector):
    return sqrt(vector[0]**2 + vector[1]**2)


def plot_history(uavs, name="default"):

    for uav in uavs:
        X, Y = zip(*uav.history) 
        plt.plot(X, Y, '.-')
    
    # plt.show()
    plt.savefig(f"{name}.jpg")


def calc_measures(uav):
    # La longitud de la trayectoria
    longitude = sum([euclidian_distance(point, uav.history[i+1]) for i, point in enumerate(uav.history) if i<len(uav.history)-1])

    # La desviación que era la real menos la optima
    deviation = longitude - euclidian_distance(uav.initial_position, uav.goal_point)

    # el número de giros tambien
    number_of_turns = sum([1 for i, point in enumerate(uav.history) if i<len(uav.history)-2 and collinear(point, uav.history[i+1], uav.history[i+2])])

    return {"longitude": longitude, "deviation": deviation, "number_of_turns": number_of_turns}