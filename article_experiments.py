import json
from locale import normalize
import numpy as np
import os
import random
import matplotlib.pyplot as plt

from classes import UAV
from utils import euclidian_distance, get_normalized_vector, plot_history, vector_norm
from math import *
from simulations import simulate


TIMESTEP = 0.25
TIMERANGE = 10
SPEED = 1.5
RADIO = 1

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

    # f = open("exp_article/random_results.json", "w")
    # f.close()

    f = open("exp_article/random_results.txt", "w")
    f.close()

    with open("exp_article/random_results.json", "r") as  f:
        s = f.read()
        if s:
            results = json.loads(s)
        else:
            results = {}

    for index, drones in enumerate(experiments):
        
        for k in direction_number_set:
            if not k in results:
                results[k] = {
                    'longitude': [], 
                    'deviation': [], 
                    'turns': [], 
                    'max_turn': [], 
                    'm1: tiempo de vuelo': [], 
                    'm2': [], 
                    'm3: cant de giros': [], 
                    'm4: suma de angulos': [], 
                    'angles_rate': [],
                    'waypoints': [],
                    'total_time': [],
                    'min_cost': [],
                    "colls_solv_time": [],
                    "collision": 0
                }

            uavs = [d.copy() for d in drones] 
            print(f"- Experiment {index} -> k={k}")

            measures, colls_solv_time = simulate(uavs, k, ca_timerange, timestep)

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

            for key in measures.keys():
                if key in ["exp", "K"]:
                    continue
                elif key=="collision":
                    results[k][key] += measures[key]         
                elif key in [0,1,2,3,4]:
                    for key2 in measures[key]: 
                        results[k][key2].append(measures[key][key2])
                else:
                    results[k][key].append(measures[key])
            
            results[k]["colls_solv_time"] += [n for n in colls_solv_time if n > 0]

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

    for k in measures.keys(): # for each value of k
        print("**",k)
        for key in measures[k]:  
            if key in ['waypoints', 'total_time', 'turns']:
                continue
            if key == "collision":
                print(f"No Solution Cases number: {measures[k][key]}")
            else:
                print(key, np.mean(measures[k][key]), np.std(measures[k][key]))
                if key == "colls_solv_time":
                    print("Number of collisions found", len(measures[k][key]))
            
        print()
        

def get_measures():
    
    with open("exp_article/random_results.json", "r") as f:
        measures = json.loads(f.read())

    Ys = {}
    for k in measures.keys(): # for each value of k
        print("**",k)
        for key in measures[k]:  

            if key in ['waypoints', 'total_time', 'turns']:
                continue

            if not key in ["longitude", "m2", "min_cost", "m4: suma de angulos", "collision", "angles_rate"] \
                and not key in Ys:
                Ys[key] = []

            if key == "collision":
                try:
                    Ys[key].append(measures[k][key])
                except:
                    pass
                
                print(f"No Solution Cases number: {measures[k][key]}")
            else:
                _mean = np.mean(measures[k][key])
                try:
                    Ys[key].append(_mean)
                except:
                    pass
                
                print(key, np.mean(_mean), np.std(measures[k][key]))
                if key == "colls_solv_time":
                    print("Number of collisions found", len(measures[k][key]))
            
        print()

    labels = {
        "deviation": "DEV", 
        "m1: tiempo de vuelo": "TCT", 
        "colls_solv_time": "CST", 
        "max_turn": "MTA", 
        "m3: cant de giros": "NOT",
    } 
    Xs = list(measures.keys())
    for key in Ys.keys():
        ymax = max(Ys[key])
        y = np.array(Ys[key])/ymax

        plt.plot(Xs, list(y), label=labels[key])

    # plt.legend()
    # box = plt.get_position()
    # plt.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
    #       ncol=3, fancybox=True, shadow=True)

    plt.xlabel("Values of k")
    plt.ylabel("Normalized Measures")
    # plt.title("Study on k")
    plt.savefig("test.png",bbox_inches='tight')
    plt.show()

    


if __name__=="__main__":

    ## Create new experiments
    # exps = create_random_exp(50, 4, 28, 28)
    # save_random_exps(exps)

    ## Run experiments
    exps = get_random_exps()
    direction_number_set = [20] #list(range(2, 21, 2))
    run_experiments(exps, direction_number_set)

    ## Get measures from experiments
    get_measures()

