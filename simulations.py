from utils import *
from solver import resolve_collision 


def simulate(uavs, k, ca_timerange, timestep, max_iterations=10000):

    flying_uavs = uavs[:]
    count = 0
    no_solution = False
    while flying_uavs and count<max_iterations:
        
        directions = [uav.direction for uav in uavs]
        if list_collide(flying_uavs, directions, ca_timerange):
            new_directions, dev_cost, total_cost = resolve_collision(flying_uavs, k, ca_timerange)
            if not new_directions:
                no_solution = True
                break
            for uav, direction in zip(flying_uavs, new_directions):
                uav.direction = direction
    
        aux = []
        for uav in flying_uavs:
            uav.fly(timestep)
            if not uav.is_in_goal:
                uav.direction = get_normalized_vector(uav.goal_point - uav.position)
                aux.append(uav)


        flying_uavs = aux
        count+=1

    if no_solution:
        return None

    return flying_uavs

