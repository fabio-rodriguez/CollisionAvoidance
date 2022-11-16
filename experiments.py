import json
import numpy as np
import os

from classes import UAV
from utils import euclidian_distance, get_normalized_vector, plot_history
from math import *
from simulations import simulate


K_DIR = 8
TIMESTEP = 2
TIMERANGE = 10
SPEED = 1.5
SPEEDRATE = 20
RADIO = 1

MAXAMPLITUDE=radians(89.99)

def test_experiment():

    u1 = UAV((-20, 0), SPEED, RADIO, (1, 0), (0, 0),max_amp=MAXAMPLITUDE)
    u2 = UAV((20, 0), SPEED, RADIO, (-1, 0), (0, 0),max_amp=MAXAMPLITUDE)
    u3 = UAV((0, 20), SPEED, RADIO, (0, -1), (0, 0),max_amp=MAXAMPLITUDE)
    u4 = UAV((0, -20), SPEED, RADIO, (0, 1), (0, 0),max_amp=MAXAMPLITUDE)

    measures = simulate([u1, u2, u3, u4],K_DIR,TIMERANGE,TIMESTEP)
    print(measures)

    plot_history([u1, u2, u3, u4])


def experiment1(k=K_DIR, speed = SPEED, radio = RADIO, timestep=TIMESTEP, ca_timerange=TIMERANGE):
    ''' 6 drones antipodales'''

    drone_positions = []
    for i in range(6):
        x = 10*cos(i*2*pi/6) 
        y = 10*sin(i*2*pi/6) 
        drone_positions.append((x,y))

    goals = [(-x, -y) for x,y in drone_positions]

    # SPEEDRATE = defining_speedrate(drone_positions, goals)
    # print("speedrate:", SPEEDRATE)

    uavs = []
    for position, goal in zip(drone_positions, goals):
        # For different speeds
        # speed = euclidian_distance(position, goal)/SPEEDRATE

        direction = get_normalized_vector(np.array(goal)-np.array(position))
        uav = UAV(position, speed, radio, direction, goal, goal_distance=0.5, max_amp=MAXAMPLITUDE)
        uavs.append(uav)
    
    # timestep = defining_timestep(uavs)
    # print(timestep)

    measures, mean_time = simulate(uavs, k, ca_timerange, timestep)
    with open("results/experiments1.json", "w") as f:
        f.write(json.dumps(measures))

    plot_history(uavs, name="results/experiments1")

    return mean_time

def experiment2(k=K_DIR, speed = SPEED, radio = RADIO, timestep=TIMESTEP, ca_timerange=TIMERANGE):
    ''' 5 drones down to up'''

    drone_positions = [(-9.5, -8), (-5, -8), (0, -8), (5, -8), (9.5, -8)]    
    goals = [(9.5, 9), (5, 9), (-5.05, 8.9), (-9.5, 9), (0, 9)]

    # SPEEDRATE = defining_speedrate(drone_positions, goals)
    # print("speedrate:", SPEEDRATE)

    uavs = []
    for position, goal in zip(drone_positions, goals):
        # For different speeds
        # speed = euclidian_distance(position, goal)/SPEEDRATE

        direction = get_normalized_vector(np.array(goal)-np.array(position))
        uav = UAV(position, speed, radio, direction, goal, goal_distance=0.5, max_amp=MAXAMPLITUDE)
        uavs.append(uav)
    
    
    # timestep = defining_timestep(uavs)
    # print(timestep)

    measures, mean_time = simulate(uavs, k, ca_timerange, timestep)
    # print(measures)
    with open("results/experiments2.json", "w") as f:
        f.write(json.dumps(measures))

    plot_history(uavs, name="results/experiments2")

    return mean_time

def experiment3(k=K_DIR, speed = SPEED, radio = RADIO, timestep=TIMESTEP, ca_timerange=TIMERANGE):
    '6agentes_esc4'

    drone_positions = [(0, 0), (10, 0), (15, 2), (15, -2), (20, 4), (20, -4)]    
    goals = [(20, 0), (0, 0.05), (0, -4.05), (0.05, 4.05), (-0.05, -8.05), (0, 8.05)]

    # SPEEDRATE = defining_speedrate(drone_positions, goals)
    # print("speedrate:", SPEEDRATE)

    uavs = []
    for position, goal in zip(drone_positions, goals):
        # For different speeds
        # speed = euclidian_distance(position, goal)/SPEEDRATE

        direction = get_normalized_vector(np.array(goal)-np.array(position))
        uav = UAV(position, speed, radio, direction, goal, goal_distance=0.5, max_amp=MAXAMPLITUDE)
        uavs.append(uav)
    
    
    # timestep = defining_timestep(uavs)
    # print(timestep)

    measures, mean_time = simulate(uavs, k, ca_timerange, timestep)
    with open("results/experiments3.json", "w") as f:
        f.write(json.dumps(measures))

    plot_history(uavs, name="results/experiments3")

    return mean_time

def experiment4(k=K_DIR, speed = SPEED, radio = RADIO, timestep=TIMESTEP, ca_timerange=TIMERANGE):
    ''' 5 drones antipodal alternando '''
    
    drone_positions = []    
    goals = []
    
    for i in range(10):
        if i == 0 or i%2 ==0:
            position = ( 10*cos(i*2*pi/10), 10*sin(i*2*pi/10) )
            drone_positions.append(position)
            
            goals.append((-position[0], -position[1]))
    
    # SPEEDRATE = defining_speedrate(drone_positions, goals)
    # print("speedrate:", SPEEDRATE)

    uavs = []
    for position, goal in zip(drone_positions, goals):
        # For different speeds
        # speed = euclidian_distance(position, goal)/SPEEDRATE

        direction = get_normalized_vector(np.array(goal)-np.array(position))
        uav = UAV(position, speed, radio, direction, goal, goal_distance=0.5, max_amp=MAXAMPLITUDE)
        uavs.append(uav)
    
    # timestep = defining_timestep(uavs)
    # print(timestep)

    measures, mean_time = simulate(uavs, k, ca_timerange, timestep)
    # print(measures)
    with open("results/experiments4.json", "w") as f:
        f.write(json.dumps(measures))

    plot_history(uavs, name="results/experiments4")

    return mean_time


def random_experiments(k=K_DIR, speed = SPEED, radio = RADIO, timestep=TIMESTEP, ca_timerange=TIMERANGE, max_amp=MAXAMPLITUDE):
    
    cwd = os.getcwd()

    f = open("results/random_results.json", "w")
    f.close()

    f = open("results/random_results.txt", "w")
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

        drone_positions.pop()
        goal_positions.pop()

        # SPEEDRATE = defining_speedrate(drone_positions, goal_positions)
        # print("speedrate:", SPEEDRATE)
        
        uavs = []
        for position, goal in zip(drone_positions, goal_positions):
            # For different speeds
            # speed = euclidian_distance(position, goal)/SPEEDRATE

            direction = get_normalized_vector(np.array(goal)-np.array(position))
            uav = UAV(position, speed, radio, direction, goal, goal_distance=1, max_amp=max_amp)
            uavs.append(uav)
        
        
        # timestep = defining_timestep(uavs)
        # print(timestep)

        measures, _ = simulate(uavs, k, ca_timerange, timestep)

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


def defining_timestep(uavs):
    
    dists = [euclidian_distance(uav.goal_point, uav.position) for uav in uavs]
    # dists = [euclidian_distance(uav.goal_point, uav.position)/uav.speed for uav in uavs]
    # return min(dists)/max(dists) ***
    # return 2*min(dists)/max(dists) ***
    # return 3*min(dists)/max(dists)
    
    if min(dists) == max(dists):
        return 1
    else:
        if 3*min(dists)/max(dists) < 1:
            return 5*min(dists)/max(dists)
        else:
            return 3*min(dists)/max(dists)/2
        
        # return 3*min(dists)/max(dists)/2 # ***** 
        

def defining_speedrate(position, goals):
    
    dists = [euclidian_distance(p, g) for p, g in zip(position, goals)]
    res = max((max(dists)/min(dists))**2, 20)
    # return min(res, 40)    
    # return 15
    if (max(dists)/min(dists))>3:
        return (max(dists)/min(dists))**2
    else:
        return 2*(max(dists)/min(dists))*10

# ## for exp 2, 3: 
# speedrate = 15
# timestep = 3*min(dists)/max(dists)/2

# speedrate = 15
# timestep = min(dists)/max(dists)/2

if __name__ == "__main__":

    # test_experiment()

    t = experiment1()

    print("****Experimento 1 terminado****")
    print(f"Iteration Time: Max = {max(t)}, Mean = {sum(t)/len(t)}")
    print()

    t = experiment2()

    print("****Experimento 2 terminado****")
    print(f"Iteration Time: Max = {max(t)}, Mean = {sum(t)/len(t)}")
    print()
    
    t = experiment3()

    print("****Experimento 3 terminado****")
    print(f"Iteration Time: Max = {max(t)}, Mean = {sum(t)/len(t)}")
    print()
    
    t = experiment4()

    print("****Experimento 4 terminado****")
    print(f"Iteration Time: Max = {max(t)}, Mean = {sum(t)/len(t)}")
    print()

    random_experiments()
    
    print("****Random experiments terminados****")
    print()
    