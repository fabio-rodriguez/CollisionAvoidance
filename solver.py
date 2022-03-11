import random

from utils import *


## Resolve collision during a timestep
def resolve_collision(uavs, k, timestep):
    directions_list = [uav.generate_directions(k) for uav in uavs]
    return __solve__(uavs, directions_list, timestep)


def __solve__(uavs, directions_list, timestep):
    # return solve_brute_force_recursive(uavs, directions_list, timestep, 0, [], None, None)
    return solve_brute_force_recursive2(uavs, directions_list, timestep, 0, [])


def solve_brute_force_recursive(uavs, directions_list, timestep, index, result, dev_cost, total_cost):

    if index == len(uavs):
        return result, dev_cost, sum([c for _, c in result])

    opt = None
    for direction, c in directions_list[index]:
        ## TODO provoke collision dron to list
        if not provoke_collisions(uavs[:index], result, uavs[index], direction, timestep):
            result.append((direction, c))
            new_dev_cost = max(dev_cost, c) if dev_cost else c
            optimal_result, optimal_dev_cost, optimal_total_cost = solve_brute_force_recursive(uavs, directions_list, timestep, index+1, result, new_dev_cost, total_cost)

            if optimal_result != None and \
                (dev_cost == None or optimal_dev_cost <= dev_cost) and \
                (total_cost == None or optimal_total_cost <= total_cost):
                    opt = optimal_result[:]
                    dev_cost = optimal_dev_cost
                    total_cost = optimal_total_cost

            result.pop()
    
    return opt, dev_cost, total_cost
    
                
# Verify collisions between drone and list
def provoke_collisions(uavs, directions, uav, direction, timestep):
    for u, dir in zip(uavs, directions):
        d, _ = dir
        if collide(u, d, uav, direction, timestep):
            return True
    return False


def solve_brute_force_recursive2(uavs, directions_list, timestep, index, result):

    if index == len(uavs):
        return result, 0

    opt = None
    opt_cost = None
    for direction, c in directions_list[index]:
        ## TODO provoke collision dron to list
        if not provoke_collisions(uavs[:index], result, uavs[index], direction, timestep):
            result.append((direction, c))
            optimal_result, cost = solve_brute_force_recursive2(uavs, directions_list, timestep, index+1, result)
            result.pop()

            if optimal_result == None:
                continue

            new_cost = cost + c
            if opt_cost == None or new_cost < opt_cost or \
                (new_cost == opt_cost and random.uniform(0, 1) < 0.5):
                    opt = optimal_result[:]
                    opt_cost = new_cost
    
    return opt, opt_cost
