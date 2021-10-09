from functions import *
from classes import *
from algorithms import *


def test1():
    pass


def test2():
    pass

    
def test2():
    pass

    
def test2():
    pass
    


if __name__ == "__main__":

    # crear region
    init_point = (0,0,0)
    width, long, height = 1000, 1000, 1000
    region = Region(init_point, width, long, height)
    #print(region.contains((1000,50,2900)))

    # crear UAVs y detectar colision
    p1, v1, r1, d1, goal1 = (200,0,0), 5, 20, (1,0,0), (500,0,0)
    uav1 = UAV(p1, v1, r1, d1, goal1)
    p2, v2, r2, d2, goal2 = (400,0,0), 10, 20, (-1,0,0), (0,0,0)
    uav2 = UAV(p2, v2, r2, d2, goal2)
    #print(is_collision(uav1, uav2, region))

    # 3D example
    radio = 1.5
    k = 16
    time_interval = 20
    
    # Square-space said size
    distance = 100
    a = sqrt((distance**2)/2)
    uav1 =UAV((0,a,a), 1.5, radio, (1,-1,-1), (a/2,0,0))
    uav2 =UAV((a/2,a,a), 1.5, radio, (-1,-1,-1), (0,0,0))
    uav3 =UAV((0,0,a), 1.5, radio, (1,1,-1), (a/2,a,0))
    uav4 =UAV((a/2,0,a), 1.5, radio, (-1,1,-1), (0,a,0))
    
    UAVs = [uav1, uav2, uav3, uav4]
    
    # The same that 2D case
    print(detect_collisions_on_time_interval(UAVs, time_interval))
