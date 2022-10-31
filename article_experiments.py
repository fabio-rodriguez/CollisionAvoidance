import json
from locale import normalize
import numpy as np
import os
import random

from classes import UAV
from utils import euclidian_distance, get_normalized_vector, plot_history, vector_norm
from math import *
from simulations import simulate


TIMESTEP = 0.25
TIMERANGE = 10
SPEED = 1.5
RADIO = 2.5

MAXAMPLITUDE=radians(89.99)


def create_random_exp(expnumber, dronesnumber, boardwidth = 100, boardheight = 100):
    random_experiments = []    
    for _ in range(expnumber):
        drones = []
        for _ in range(dronesnumber):
            # Create initial position 
            while True:
                initial_pos = np.array([random.uniform(0, boardwidth), random.uniform(0, boardheight)])
                # verify at least 10 meters from previous inital positions 
                break_loop = True
                for d in drones:    
                    if euclidian_distance(initial_pos, d.position) < 10:
                        break_loop = False
                
                if break_loop:
                    break
    
            # Create goal position
            while True:
                goal_pos = np.array([random.uniform(0, boardwidth), random.uniform(0, boardheight)])
                # verify initial and goal position are at least 20 meter away
                if euclidian_distance(initial_pos, goal_pos) > 20:
                    break
            
            initial_dir = get_normalized_vector(goal_pos-initial_pos)
            drones.append(UAV(initial_pos, SPEED, RADIO, initial_dir, goal_pos, max_amp=MAXAMPLITUDE))
        
        random_experiments.append(drones)

    return random_experiments


def run_experiments(experiments, direction_number_set, timestep=TIMESTEP, ca_timerange=TIMERANGE):
    
    # cwd = os.getcwd()

    f = open("exp_article/random_results.json", "w")
    f.close()

    f = open("exp_article/random_results.txt", "w")
    f.close()

    results = {}
    for index, drones in enumerate(experiments):
        if index < 68:
            continue
        results = {}
        for k in direction_number_set:
            uavs = [d.copy() for d in drones] 
            print(f"- Experiment {index}")

            measures, _ = simulate(uavs, k, ca_timerange, timestep)

            if not measures:
                measures = {"exp": index, "K": k, "collision": 1}
                print("COLLISION")
                print("Flying uavs", [(uav.position, uav.direction) for uav in uavs])
                print("Directions", [uav.generate_directions(k) for uav in uavs])
                print()
            
            else:
                measures["exp"] = index
                measures["K"] = k
                measures["collision"] = 0

            with open("exp_article/random_results.txt", "a") as f:
                f.write(str(measures))
                f.write("\n")

            try: 
                results[index][k] = measures
            except:
                results[index] = {k: measures}

            plot_history(uavs, f'exp_article/pictures/{index}_{k}')
            
        with open("exp_article/random_results.json", "w") as f:
            f.write(json.dumps(results))


def save_random_exps(experiments):
    exps = {}
    for i, drones in enumerate(experiments):
        exps[i] = []
        for uav in drones:
            props = {
                "position_X": uav.position[0],
                "position_Y": uav.position[1],
                "speed": uav.speed, 
                "radio": uav.radio, 
                "direction_X": uav.direction[0], 
                "direction_Y": uav.direction[1], 
                "goal_X": uav.goal_point[0], 
                "goal_Y": uav.goal_point[1],
                "max_amp": uav.max_amp
            }
            exps[i].append(props)

    with open("exp_article/experiments.json", "w") as f:
        f.write(json.dumps(exps))


def get_random_exps(from_exp=0, to_exp=100):
    with open("exp_article/experiments.json", "r") as f:
        exp_dict = json.loads(f.read())

    experiments = []
    for k in exp_dict.keys():
        if int(k) < from_exp or int(k) >= to_exp:
            continue
        
        drones = []
        for d in exp_dict[k]:
            uav = UAV(
                np.array([d["position_X"], d["position_Y"]]),
                d["speed"],
                d["radio"],
                np.array([d["direction_X"], d["direction_Y"]]),
                np.array([d["goal_X"], d["goal_Y"]]),
                d["max_amp"],
            )
            drones.append(uav)
    
        experiments.append(drones)
    
    return experiments


def get_measures():
    
    with open("exp_article/random_results.json", "r") as f:
        measures = json.loads(f.read())

    results = {}
    key_measures = list(measures[0][2].keys())
    for k in measures[0].keys(): # for each value of k
        results[k] = {}
        for index in measures.keys():
            for key in key_measures:
                if index == 0:
                    results[k][key] = [measures[index][k][key]]
                else: 
                    results[k][key].append(measures[index][k][key])

    for k in measures[0].keys():
        print(f"**{k}")
        for key in key_measures:
            measures_list = results[k][key]
            print(f"{key}: mean = {np.mean(measures_list)}, std = {np.std(measures_list)}")
        print()        
    

if __name__=="__main__":

    ## Create new experiments
    # exps = create_random_exp(100, 5, 50, 50)
    # save_random_exps(exps)

    ## Run experiments
    exps = get_random_exps()
    direction_number_set = list(range(2, 21, 2))
    run_experiments(exps, direction_number_set)

    ## Get measures from experiments
    # get_measures()

