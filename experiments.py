import numpy as np
import os

from classes import UAV
from utils import get_normalized_vector, plot_history
from math import *
from simulations import simulate


def test_experiment():

    u1 = UAV((-10, 0), 1, 1.5, (1, 0), (10, 0))
    u2 = UAV((10, 0), 1, 1.5, (-1, 0), (-10, 0))
    u3 = UAV((0, 10), 1, 1.5, (0, -1), (0, -10))
    u4 = UAV((0, -10), 1, 1.5, (0, 1), (0, 10))

    measures = simulate([u1, u2, u3, u4], 10, 6, 0.5)
    print(measures)

    plot_history([u1, u2, u3, u4])


def experiment1(k=10, speed = 1, radio = 0.1, timestep=0.05, ca_timerange=0.8):
    ''' 6 drones antipodales'''

    drone_positions = []
    for i in range(6):
        x = cos(i*2*pi/6) 
        y = sin(i*2*pi/6) 
        drone_positions.append((x,y))

    goals = [(-x, -y) for x,y in drone_positions]

    uavs = []
    for position, goal in zip(drone_positions, goals):
        direction = get_normalized_vector(np.array(goal)-np.array(position))
        uav = UAV(position, speed, radio, direction, goal, goal_distance=0.01)
        uavs.append(uav)
    
    measures = simulate(uavs, k, ca_timerange, timestep)
    print(measures)

    plot_history(uavs)


def experiment2():
    pass


def experiment3():
    pass

    
def experiment4():
    pass

    
def experiment5():
    pass


def experiment6():
    pass


def random_experiments(k=10, speed = 1, radio = 0.1, timestep=0.05, ca_timerange=0.8):
    
    cwd = os.getcwd()

    path_to_data = f'{cwd}/data'
    allfiles = [f for f in os.listdir(path_to_data) if os.path.isfile(os.path.join(path_to_data, f)) if f.endswith(".txt")]
    
    for file in allfiles[:3]:
        print(file)
        with open(f'{path_to_data}/{file}', 'r') as f:
            f.readline()

            drone_positions = []
            for _ in range(6):
                line = f.readline().split()
                print(line)
                x = float(line[0]) 
                y = float(line[1])

                drone_positions.append((x,y))

            f.readline()
            f.readline()
            
            goal_positions = []
            for _ in range(6):
                line = f.readline().split()
                print(line)
                x = float(line[0]) 
                y = float(line[1])

                goal_positions.append((x,y))

        uavs = []
        print()
        for position, goal in zip(drone_positions, goal_positions):
            print(position, goal)
            direction = get_normalized_vector(np.array(goal)-np.array(position))
            uav = UAV(position, speed, radio, direction, goal, goal_distance=0.01)
            uavs.append(uav)
        
        measures = simulate(uavs, k, ca_timerange, timestep)
        
        plot_history(uavs, file)

            

        

if __name__ == "__main__":

    # test_experiment()

    # experiment1()

    random_experiments()