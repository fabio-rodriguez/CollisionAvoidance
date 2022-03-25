import json
import numpy as np
import os

from sklearn.metrics import euclidean_distances

from classes import UAV
from utils import euclidian_distance, get_normalized_vector, plot_history
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


def experiment1(k=6, speed = 1.5, radio = 0.5, timestep=0.25, ca_timerange=10):
    ''' 6 drones antipodales'''

    drone_positions = []
    for i in range(6):
        x = 50*cos(i*2*pi/6) 
        y = 50*sin(i*2*pi/6) 
        drone_positions.append((x,y))

    goals = [(-x, -y) for x,y in drone_positions]

    uavs = []
    for position, goal in zip(drone_positions, goals):
        # For different speeds
        speed = euclidian_distance(position, goal)/100

        direction = get_normalized_vector(np.array(goal)-np.array(position))
        uav = UAV(position, speed, radio, direction, goal, goal_distance=0.5, max_amp=radians(60))
        uavs.append(uav)
    
    measures = simulate(uavs, k, ca_timerange, timestep)
    with open("results/experiments1.json", "w") as f:
        f.write(json.dumps(measures))

    plot_history(uavs, name="results/experiments1")


def experiment2(k=6, speed = 1.5, radio = 0.5, timestep=0.25, ca_timerange=10):
    ''' 5 drones down to up'''

    drone_positions = [(-8, -8), (-4, -8), (0, -8), (4, -8), (8, -8)]    
    goals = [(8, 8), (4, 8), (-4, 8), (-8, 8), (0, 8)]

    uavs = []
    for position, goal in zip(drone_positions, goals):
        direction = get_normalized_vector(np.array(goal)-np.array(position))
        uav = UAV(position, speed, radio, direction, goal, goal_distance=0.5, max_amp=radians(60))
        uavs.append(uav)
    
    measures = simulate(uavs, k, ca_timerange, timestep)
    print(measures)
    with open("results/experiments2.json", "w") as f:
        f.write(json.dumps(measures))

    plot_history(uavs, name="results/experiments2")


def experiment3(k=6, speed = 1.5, radio = 0.5, timestep=0.25, ca_timerange=10):
    '6agentes_esc4'

    drone_positions = [(0, 0), (10, 0), (15, 2), (15, -2), (20, 4), (20, -4)]    
    goals = [(40, 0), (0, 0), (0, -2), (0, 2), (0, -4), (0, 4)]

    uavs = []
    for position, goal in zip(drone_positions, goals):
        direction = get_normalized_vector(np.array(goal)-np.array(position))
        uav = UAV(position, speed, radio, direction, goal, goal_distance=0.5, max_amp=radians(60))
        uavs.append(uav)
    
    measures = simulate(uavs, k, ca_timerange, timestep)
    with open("results/experiments3.json", "w") as f:
        f.write(json.dumps(measures))

    plot_history(uavs, name="results/experiments3")


def experiment4(k=6, speed = 1.5, radio = 0.5, timestep=0.25, ca_timerange=10):
    ''' 5 drones antipodal alternando '''
    
    drone_positions = []    
    goals = []
    
    for i in range(10):
        if i == 0 or i%2 ==0:
            position = ( 10*cos(i*2*pi/10), 10*sin(i*2*pi/10) )
            drone_positions.append(position)
            
            goals.append((-position[0], -position[1]))
    
    uavs = []
    for position, goal in zip(drone_positions, goals):
        direction = get_normalized_vector(np.array(goal)-np.array(position))
        uav = UAV(position, speed, radio, direction, goal, goal_distance=0.5, max_amp=radians(60))
        uavs.append(uav)
    
    measures = simulate(uavs, k, ca_timerange, timestep)
    print(measures)
    with open("results/experiments4.json", "w") as f:
        f.write(json.dumps(measures))

    plot_history(uavs, name="results/experiments4")


def random_experiments(k=6, speed = 1.5, radio = 0.5, timestep=0.25, ca_timerange=10, max_amp=radians(60)):
    
    cwd = os.getcwd()

    f = open("results/random_results.json", "w")
    f.close()

    allfiles = [f for f in os.listdir(f'{cwd}/data') if os.path.isfile(os.path.join(f'{cwd}/data', f)) if f.endswith(".txt")]
    results = {}
    for file in allfiles:
        with open(f'{cwd}/data/{file}', 'r') as f:
            print(f"- Experiment File {file}")
            f.readline()

            drone_positions = []
            for _ in range(6):
                line = f.readline().split()
                x = float(line[0]) 
                y = float(line[1])

                drone_positions.append((x,y))

            f.readline()
            f.readline()
            
            goal_positions = []
            for _ in range(6):
                line = f.readline().split()
                x = float(line[0]) 
                y = float(line[1])

                goal_positions.append((x,y))

        drone_positions.pop(-1)
        goal_positions.pop(-1)

        uavs = []
        for position, goal in zip(drone_positions, goal_positions):
            direction = get_normalized_vector(np.array(goal)-np.array(position))
            uav = UAV(position, speed, radio, direction, goal, goal_distance=1, max_amp=max_amp)
            uavs.append(uav)
        
        measures = simulate(uavs, k, ca_timerange, timestep)

        if not measures:
            print("COLLISION")
            print("Flying uavs", [(uav.position, uav.direction) for uav in uavs])
            print("Directions", [uav.generate_directions(k) for uav in uavs])
            print()

        with open("results/random_results.txt", "a") as f:
            f.write(str(measures))
            f.write("\n")

        results[file] = measures

        plot_history(uavs, f'data/{file[:-4]}')
    
    with open("results/random_results.json", "w") as f:
        f.write(json.dumps(results))

            
if __name__ == "__main__":

    # test_experiment()

    experiment1()

    print("****Experimento 1 terminado****")
    print()

    experiment2()

    print("****Experimento 2 terminado****")
    print()
    
    experiment3()

    print("****Experimento 3 terminado****")
    print()
    
    experiment4()

    print("****Experimento 4 terminado****")
    print()

    random_experiments()
    
    print("****Random experiments terminados****")
    print()
    