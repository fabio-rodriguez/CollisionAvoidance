import numpy as np
import os

from math import *
from numpy.linalg import norm


def get_measures(path_to_folder, timestep):

    waypoints = []
    for file_name in os.listdir(path_to_folder):
        with open(f"{path_to_folder}/{file_name}", "r") as file: 
            waypoints.append([np.array(list(map(float, l.split()))) for l in file.readlines()])

    dresults = {}
    for wps in waypoints:
        for k, v in calc_measures(wps, timestep).items():
            try:
                dresults[k].append(v)
            except:
                dresults[k] = [v]

    # print(dresults)

    for key in dresults.keys():
        if key != "turns":
            print(f"**{key}** mean: {np.mean(dresults[key])}, std {np.std(dresults[key])}")
        

def calc_measures(waypoints, timestep):
    
    # La longitud de la trayectoria
    longitude = sum([euclidian_distance(point, waypoints[i+1]) for i, point in enumerate(waypoints) if i<len(waypoints)-1])

    # La desviacion que era la real menos la optima
    deviation = longitude - euclidian_distance(waypoints[0], waypoints[-1])

    # el numero de giros tambien
    turns = [abs(deviation_angle(point, waypoints[i+1], waypoints[i+2])) for i, point in enumerate(waypoints) if i<len(waypoints)-2 and not collinear(point, waypoints[i+1], waypoints[i+2])]

    # el maximo giro tambien
    if turns:
        max_turn = max(turns)
    else:
        max_turn = 0

    # Energy measures
    # m1
    flight_time = len(waypoints)*timestep
    # m2
    speeds = [euclidian_distance(point, waypoints[i+1])/timestep for i, point in enumerate(waypoints) if i < len(waypoints)-1]
    diffs = [abs(speeds[i+1]-speed)/timestep for i, speed in enumerate(speeds) if i < len(waypoints)-2]
    acelerationsum= sum(diffs)
    acelerationvariation= acelerationsum/len(waypoints)
    # m3
    m3 = len(turns)
    # m4
    
    # d = lambda p1, p2, p3: asin(distance_from_line_2point(p1, p2, p3)/euclidian_distance(p2,p3))
    # angles_sum = sum([abs(d(point, uav.history[i+1], uav.history[i+2])) for i, point in enumerate(uav.history) if i<len(uav.history)-2 and not collinear(point, uav.history[i+1], uav.history[i+2])])
    angles_sum=sum(turns)
    return {
        "longitude": longitude, 
        "deviation": deviation, 
        "turns": turns, 
        "max_turn": max_turn, 
        "m1: tiempo de vuelo": flight_time, 
        "m2.1: velocity variation": acelerationvariation,
        "m2.2: velocity sum": acelerationsum,
        "m3: cant de giros": m3,
        "m4: suma de angulos": angles_sum,
        "turns rate": 0 if not m3 else angles_sum/m3
    }




def euclidian_distance(vector1, vector2):
    return sqrt(sum([(x-y)**2 for x,y in zip(vector1, vector2)]))


def deviation_angle(p1,p2,p3):
    c1 = distance_from_line_2point(p1,p2,p3)
    h = euclidian_distance(p2,p3)
    try:
        return asin(c1/h) 
    except:
        print("Asin Error (cat, hip):", (c1, h))
        return 0


def collinear(p0, p1, p2, epsilon=1e-8):
    x1, y1 = p1[0] - p0[0], p1[1] - p0[1]
    x2, y2 = p2[0] - p0[0], p2[1] - p0[1]
    return abs(x1 * y2 - x2 * y1) < epsilon


# Dist from line between points p1 and p2, to point p3
def distance_from_line_2point(p1, p2, p3):
    # p1 = p1.astype(float)
    # p2 = p2.astype(float)
    # p3 = p3.astype(float)
    den = 10**-10 if norm(p2-p1) == 0 else norm(p2-p1)
    return norm(np.cross(p2-p1, p1-p3)) / den





if __name__=="__main__":

    path_to_folder = "C:/Users/jmesca/Desktop/CollisionAvoidance/orca/TimeStep0.25/5AA"

    get_measures(path_to_folder, 0.25)