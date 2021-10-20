from utils import *


## Resolve collision during a timestep
def resolve_collision(uavs, k, timestep):
    directions_list = [uav.generate_directions(k) for uav in uavs]
    return __solve__(uavs, directions_list, timestep)


def __solve__(uavs, directions_list, timestep):
    return solve_brute_force_recursive(uavs, directions_list, timestep, 0, [], deviation, None, None)


def max_deviation_cost(uavs, directions):
    return max([deviation(uav, direction) for uav, direction in zip(uavs, directions)])


def deviation(uav, direction):
    return round(euclidian_distance(uav.direction, direction), 2)


def solve_brute_force_recursive(uavs, directions_list, timestep, index, result, cost_function, dev_cost, total_cost):

    if index == len(uavs):
        return result, dev_cost, sum([deviation(u, d) for u, d in zip(uavs, result)])

    opt = None
    for direction in directions_list[index]:
        ## TODO provoke collision dron to list
        if not provoke_collisions(uavs[:index], result, uavs[index], direction, timestep):
            result.append(direction)
            c = cost_function(uavs[index], direction)
            new_dev_cost = max(dev_cost, c) if dev_cost else c
            optimal_result, optimal_dev_cost, optimal_total_cost = solve_brute_force_recursive(uavs, directions_list, timestep, index+1, result, cost_function, new_dev_cost, total_cost)

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
    for u, d in zip(uavs, directions):
        if collide(u, d, uav, direction, timestep):
            return True
    return False
