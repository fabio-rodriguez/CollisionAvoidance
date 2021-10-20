import time

from utils import *
from solver import resolve_collision 


def simulate(uavs, k, ca_timerange, timestep, max_iterations=10000):

    flying_uavs = uavs[:]
    count = 0
    no_solution = False

    t = time.time()
    max_angle = 0
    max_total_turn = 0
    while flying_uavs and count<max_iterations:
        
        directions = [uav.direction for uav in uavs]
        if list_collide(flying_uavs, directions, ca_timerange):
            new_directions, dev_cost, total_cost = resolve_collision(flying_uavs, k, ca_timerange)
            if not new_directions:
                no_solution = True
                break

            max_angle = max_angle if max_angle > dev_cost else dev_cost
            max_total_turn = max_total_turn if max_total_turn > total_cost else total_cost

            for uav, direction in zip(flying_uavs, new_directions):
                uav.direction = direction[0]
    
        aux = []
        for uav in flying_uavs:
            uav.fly(timestep)
            if not uav.is_in_goal:
                uav.direction = get_normalized_vector(uav.goal_point - uav.position)
                aux.append(uav)


        flying_uavs = aux
        count+=1

    tf = time.time() - t

    measures = {i: calc_measures(uav) for i, uav in enumerate(uavs)}
    measures["total_time"] = tf
    measures["max_turn_angle"] = max_angle
    measures["max_total_turn"] = max_total_turn

    if no_solution:
        return None

    return measures


