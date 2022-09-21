import random
import time

from utils import *


## Resolve collision during a timerange
def resolve_collision(uavs, k, timerange):
    directions_list = [uav.generate_directions(k) for uav in uavs]
    # # For having 0,0 velocity
    # directions_list = [uav.generate_directions(k,stop_cost=1000) for uav in uavs]

    response = __solve__(uavs, directions_list, timerange)
    if response[0] == None:
        name = "".join(str(time.time()).split("."))
        with open(f"collision_{name}.txt", "w+") as f:
            count = 1
            for u, d in zip(uavs,directions_list):
                f.write(f"Drone: {count}")
                f.write(str(u))
                f.write("\n")
                f.write(str(d))
                f.write("\n")
                f.write("\n")
                count+=1
                
    return response


def __solve__(uavs, directions_list, timerange):
    # return solve_brute_force_recursive(uavs, directions_list, timerange, 0, [], None, None)
    return solve_brute_force_recursive(uavs, directions_list, timerange, 0, [])
    
                
# Verify collisions between drone and list
def provoke_collisions(uavs, directions, uav, direction, timerange):
    for u, dir in zip(uavs, directions):
        d, _ = dir
        if collide(u, d, uav, direction, timerange):
            return True

    return False


def solve_brute_force_recursive(uavs, directions_list, timerange, index, result):

    if index == len(uavs):
        return result, 0

    opt = None
    opt_cost = None
    for direction, c in directions_list[index]:
        if not provoke_collisions(uavs[:index], result, uavs[index], direction, timerange):
            result.append((direction, c))
            optimal_result, cost = solve_brute_force_recursive(uavs, directions_list, timerange, index+1, result)

            if optimal_result == None:
                result.pop()
                continue

            # new_cost = cost + c
            new_cost = max(cost, c)
            # if opt_cost == None or new_cost < opt_cost  or \
            #     (new_cost == opt_cost and random.uniform(0, 1) < 0.5):
            if opt_cost == None or new_cost < opt_cost:
                    opt = optimal_result[:]
                    opt_cost = new_cost
            
            result.pop()
    
    return opt, opt_cost
