from utils import *


## Resolve collision during a timestep
def resolve_collision(uavs, k, timestep):
    directions_list = [uav.generate_directions(k) for uav in uavs]
    return __solve__(uavs, directions_list, timestep)


def __solve__(uavs, directions_list, timestep):
    
    return solve_brute_force_recursive(uavs, directions_list, timestep, 0, [], max_deviation_cost, uavs[0].max_amp)


def max_deviation_cost(uavs, directions):
    return max([deviation(uav, direction) for uav, direction in zip(uavs, drections)])


def deviation(uav, direction):
    return abs(vector_2angles(uav.direction)[0] - vector_2angles(direction)[0])


## TODO take the input and return the list of opt directions and the opt cost. The initial cost must be big enough (the max amp)
def solve_brute_force_recursive(uavs, directions_list, timestep, index, result, cost_function, cost):
    if index == len(uavs):
        return result, cost

    opt = None
    for direction in directions_list[index]:
        ## TODO provoke collision dron to list
        if not provoke_collisions(uavs[:index], result, uavs[index], direction, timestep):
            result.append(direction)
            new_cost = max(cost, deviation(uavs[index], direction))
            optimal_result, optimal_cost = solve_brute_force_recursive(uavs, directions_list, timestep, index+1, result, new_cost)

            if optimal_result != None and optimal_cost < cost:
                cost = optimal_cost
                opt = optimal_result
    
    return opt, cost
    
                
# Verify collisions between drone and list
def provoke_collisions(uavs, directions, uav, direction, timestep):
    for u, d in UAV_list:
        if collide(u, d, uav, direction, timestep):
            return True
    return False

