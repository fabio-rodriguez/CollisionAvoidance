import time

from utils import *
from solver import resolve_collision 


def simulate(uavs, k, ca_timerange, timestep, max_iterations=10**5):

    flying_uavs = uavs[:]
    count = 0
    no_solution = False

    t = time.time()
    min_cost = 10**6
    max_iterations=10**3
    while flying_uavs and count<max_iterations:
        print("iteration", count)

        directions = [uav.direction for uav in flying_uavs]
        if list_collide(flying_uavs, directions, ca_timerange):
            new_directions, cost = resolve_collision(flying_uavs, k, ca_timerange)
            if not new_directions:
                no_solution = True
                break

            min_cost = min_cost if min_cost < cost else cost

            for uav, direction in zip(flying_uavs, new_directions):
                uav.direction = direction[0]
        else:
            directions_list = [uav.generate_directions(k) for uav in flying_uavs]
            for uav, directions in zip(flying_uavs, directions_list):
                directions.sort(key=lambda x: x[1])
                print(f"position: {uav.position}")
                print(f"direction: {uav.direction}")
                print(f"goal: {uav.goal_point}")
                print(f"goal dir: {get_normalized_vector(uav.goal_point - uav.position)}")
                print(f"sorted direction list: {directions}")
                print()
                uav.direction = directions[0][0]


    
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
    measures["min_cost"] = min_cost

    if no_solution:
        return None

    return measures


