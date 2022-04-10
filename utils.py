import matplotlib.pyplot as plt
import numpy as np

from math import *
from numpy.linalg import norm


class Point:

    def __init__(self, x: float = None, y: float = None) -> None:
        self.x = x
        self.y = y
    
    def point_from_array(self, array):
        self.x = array[0]
        self.y = array[1]
    
    def to_array(self):
        return np.array([self.x, self.y])


class Line:

    def __init__(self, p1: Point, p2: Point) -> None:
        if (p2.x-p1.x) != 0:
            self.m = (p2.y-p1.y)/(p2.x-p1.x)
            self.n = p1.y-p1.x*self.m
        else:
            self.m = float('inf')
            self.n = float('inf')
            self.xaxis = p1.x
        
    def f_x(self, x):
        if self.m == float('inf'):  
            return float('inf')
        return self.m*x+self.n
        
    def f_y(self, y):
        if self.m == float('inf'):  
            return self.xaxis
        return (y-self.n)/self.m



class Circle:

    def __init__(self, center: Point, radio: float) -> None:
        self.center = center
        self.a = center.x
        self.b = center.y
        self.radio = radio


def collision_point_circle_line(circle: Circle, line: Line):
    ## Circle: (x-a)**2+(y-b)**2=r**2
    ## Line: y=mx+n

    if line.m == float('inf'):
        try:
            n = sqrt(circle.radio**2 - (line.xaxis-circle.a)**2)
            y1, y2 = n + circle.b, -n + circle.b
            return Point(line.xaxis, y1), Point(line.xaxis, y2)
        except:
            return None  
    else:
        # (x-circle.a)**2+(line.m*x+line.n-circle.b)**2=circle.r**2
        # x**2-2*circle.a*x+circle.a**2+line.m**2*x**2+2*line.m*x*(line.n-circle.b)+(line.n-circle.b)**2=circle.r**2
        # (1+line.m**2)*x**2 + (-2*circle.a+2*line.m*(line.n-circle.b))*x + circle.a**2+(line.n-circle.b)**2-circle.r**2=0
        a = 1+line.m**2
        b = -2*circle.a+2*line.m*(line.n-circle.b)
        c = circle.a**2+(line.n-circle.b)**2-circle.radio**2
        res = discriminant(a, b, c)
        if not res:
            return None

        try:
            x1, x2 = res
            return Point(x1, line.f_x(x1)), Point(x2, line.f_x(x2)) 
        except:
            return Point(res, line.f_x(res))    


def discriminant(a,b,c):
    D = b**2-4*a*c
    if D<0:
        return None
    elif round(D,6) == 0:
        return -b/(2*a)
    else:
        return (-b+sqrt(D))/(2*a), (-b-sqrt(D))/(2*a) 


def detect_collision_point(point, dir, center: Point, radio):
    assert dir[0]!=0 or dir[1]!=0, "Please provided a valir direction"
    
    c = Circle(center, radio)
    p1 = Point(point[0], point[1])
    p2 = Point(point[0]+dir[0], point[1]+dir[1])
    l = Line(p1, p2)

    return collision_point_circle_line(c, l)


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


# Detect if uav1 with direction d1 collides with uav2 with direction d2
def collide(uav1, d1, uav2, d2, timerange):
    ## The first must be the slower
    uav1, d1, uav2, d2 = (uav1, d1, uav2, d2) if uav1.speed < uav2.speed else (uav2, d2, uav1, d1)
    
    # diffvector = d2*uav2.speed - d1*uav1.speed
    # ## New position for faster vehicle
    # p2 = uav2.position + diffvector*timestep
    # cat1 = distance_from_line_2point(uav2.position, p2, uav1.position) 

    # if cat1 < radialdist:
    #     hip = euclidian_distance(uav2.position, uav1.position)        
    #     col_dist = sqrt(hip**2 - cat1**2)

    #     ## If uav collision is after the timestep then there is not collsion until timestep
    #     final_point = uav2.position + diffvector*timestep 
    #     if euclidian_distance(final_point, uav2.position) < col_dist and euclidian_distance(final_point, uav1.position) > radialdist:
    #         return False

    #     ## If uav1 reaches goal before collision cuidado pq se mueveeeeee
    #     # timegoal1 = point_mindist_to_goal(uav1, d1) 
    #     # if timegoal1:
    #     #     pos1 = uav1.position + timegoal1*uav1.speed*d1
    #     #     if euclidian_distance(uav1.position, pos1) < col_dist and euclidian_distance(pos1, uav2.position)
    #     #     return False
        
    #     ## If uav2 reaches goal before collision
    #     ## TODO dist de linea a circlulo
    #     timegoal2 = point_mindist_to_goal(uav2, d2) 
    #     if timegoal2:
    #         pos2 = uav2.position + timegoal2*uav2.speed*d2
    #         if euclidian_distance(uav2.position, pos2) < col_dist and euclidian_distance(pos2, uav1.position) < radialdist:
    #             return False
                    
    #     return True


    radialdist = (uav1.radio + uav2.radio)
    diffvector = d2*uav2.speed - d1*uav1.speed
    assert diffvector[0]!=0 or diffvector[1]!=0,"The direction must be different from (0,0)"     
    
    center = Point()
    center.point_from_array(uav1.position)
    colpoint = detect_collision_point(uav2.position, diffvector, center, radialdist)
    if colpoint is None:
        return False

    try:
        p1, p2 = colpoint[0].to_array(), colpoint[1].to_array()
        colpoint = p1 if euclidian_distance(uav2.position, p1) < euclidian_distance(uav2.position, p2) else p2
    except:
        colpoint = colpoint.to_array()
    
    coltime = time_from_displacement_wout_speed(diffvector, euclidian_distance(uav2.position, colpoint))

    if coltime < timerange:
        
        ## If uav1 reaches goal before collision
        reach1 = reach_goal_before_time(uav1, d1, coltime)
        
        ## If uav2 reaches goal before collision
        reach2 = reach_goal_before_time(uav2, d2, coltime)
        
        if reach1 or reach2:
            return False
        
        return True 

    return False


def reach_goal_before_time(uav, dir, time):

    center = Point()
    center.point_from_array(uav.goal_point)
    touchpoints = detect_collision_point(uav.position, dir, center, uav.radio+uav.goal_distance)    
    if touchpoints is None:
        return False
    
    try:
        p1, p2 = touchpoints[0].to_array(), touchpoints[1].to_array()
        colpoint = p1 if euclidian_distance(uav.position, p1) < euclidian_distance(uav.position, p2) else p2
    except:
        colpoint = touchpoints.to_array()
    
    coltime = time_from_displacement(dir,uav.speed,euclidian_distance(uav.position,colpoint))
    return coltime < time


def point_mindist_to_goal(uav, d):
    new_pos = uav.position + uav.speed*d
    
    ## Distance from P3 to line between P1 and P2
    p1, p2, p3 = uav.position, new_pos, uav.goal_point
    dist = distance_from_line_2point(p1, p2, p3)
    if dist <= uav.goal_distance+uav.radio:
        hip = euclidian_distance(p1, p3)
        displacement = sqrt(hip**2 - dist**2)
        time = displacement/(uav.speed*norm(d))
        return time     

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


def deviation_angle(p1,p2,p3):
    c1 = distance_from_line_2point(p1,p2,p3)
    h = euclidian_distance(p2,p3)
    try:
        return asin(c1/h) 
    except:
        print("Asin Error (cat, hip):", (c1, h))
        return 0

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


def time_from_displacement(dir, speed, displacement):
    return displacement/(speed*norm(dir))

def time_from_displacement_wout_speed(dir_with_speed, displacement):
    return displacement/(norm(dir_with_speed))
