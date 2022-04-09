import matplotlib.pyplot as plt
import numpy as np

from math import *
from numpy.linalg import norm


# Dist from line between points p1 and p2, to point p3
def distance_from_line_2point(p1, p2, p3):
    # p1 = p1.astype(float)
    # p2 = p2.astype(float)
    # p3 = p3.astype(float)
    den = 10**-10 if norm(p2-p1) == 0 else norm(p2-p1)
    return norm(np.cross(p2-p1, p1-p3)) / den


def collinear(p0, p1, p2, epsilon=1e-8):
    x1, y1 = p1[0] - p0[0], p1[1] - p0[1]
    x2, y2 = p2[0] - p0[0], p2[1] - p0[1]
    return abs(x1 * y2 - x2 * y1) < epsilon


def deviation_angle(p0, p1, p2, epsilon=1e-8):
    cat = distance_from_line_2point(p0, p1, p2)
    hip = euclidian_distance(p1, p2)
    try:
        return abs(asin(cat/hip))
    except:
        print("******* ASIN ERROR *******")
        print(cat, hip)
        print()
        return abs(asin(1))



# Detect if uav1 with direction d1 collides with uav2 with direction d2
def collide(uav1, d1, uav2, d2, timestep):
    ## The first must be the slower
    uav1, d1, uav2, d2 = (uav1, d1, uav2, d2) if uav1.speed < uav2.speed else (uav2, d2, uav1, d1)
    diffvector = d2*uav2.speed - d1*uav1.speed
    ## New position for faster vehicle
    p2 = uav2.position + diffvector*timestep
    cat1 = distance_from_line_2point(uav2.position, p2, uav1.position) 
    
    radialdist = (uav1.radio + uav2.radio)
    if cat1 < radialdist:
        hip = euclidian_distance(uav2.position, uav1.position)        
        col_dist = sqrt(hip**2 - cat1**2)

        resp, point_near_goal = point_mindist_to_goal(uav2, d2) 
        final_point = uav2.position + diffvector*timestep 

        if resp and euclidian_distance(point_near_goal, uav2.position) < col_dist and euclidian_distance(point_near_goal, uav1.position) > radialdist:
            return False   
        if euclidian_distance(final_point, uav2.position) < col_dist and euclidian_distance(final_point, uav1.position) > radialdist:
            return False

        return True
    
    return False


def point_mindist_to_goal(uav, d):
    new_pos = uav.position + uav.speed*d
    
    ## Distance from P3 to line between P1 and P2
    p1, p2, p3 = uav.position, new_pos, uav.goal_point
    dist = distance_from_line_2point(p1, p2, p3)
    if dist < uav.goal_distance:
        hip = euclidian_distance(p1, p3)
        displacement = sqrt(hip**2 - dist**2)
        time = displacement/(uav.speed*sum(d**2))
        return 1, p1+d*uav.speed*time
    else:
        return 0, None        

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


    colors = ["r", "y", "b", "g", "m", "k"]
    for uav, color in zip(uavs, colors):
        X, Y = zip(*uav.history) 
        plt.plot(X, Y, '-'+color)
        plt.plot([X[0]], [Y[0]], "^"+color)
        plt.plot([uav.goal_point[0]], [uav.goal_point[1]], "x"+color)


    plt.savefig(f"{name}.jpg")
    # plt.show()
    plt.close()


def calc_measures(uav):
    
    # La longitud de la trayectoria
    longitude = sum([euclidian_distance(point, uav.history[i+1]) for i, point in enumerate(uav.history) if i<len(uav.history)-1])

    # La desviación que era la real menos la optima
    deviation = longitude - euclidian_distance(uav.initial_position, uav.goal_point)

    # el número de giros tambien
    turns = [abs(deviation_angle(point, uav.history[i+1], uav.history[i+2])) for i, point in enumerate(uav.history) if i<len(uav.history)-2 and not collinear(point, uav.history[i+1], uav.history[i+2])]

    # el maximo giro tambien
    if turns:
        max_turn = max(turns)
    else:
        max_turn = 0

    # Energy measures
    # m1
    flight_time = longitude/uav.speed
    # m2
    # velocity_variation = sum([sqrt(uav.history[i].speed**2 - uav.history[i+1].speed**2) for i, point in enumerate(uav.history) if i<len(uav.history)-1])
    velocity_variation = 0
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
        "turns_sum": sum(turns), 
        "max_turn": max_turn, 
        "m1": flight_time, 
        "m2": velocity_variation,
        "m3": m3,
        "m4": angles_sum
    }


def angle_in_range(alpha, lower, upper):
    return (alpha - lower) % (2*pi) <= (upper - lower) % (2*pi)