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

        # Las direcciones actuales que se supone que no tienen colision
        current_dirs = [uav.direction for uav in flying_uavs]

        # Las direcciones nuevas que van al objetivo
        # flying_dirs = []
        # for uav in flying_uavs:
        
        #     # directions_list = uav.generate_directions(k)
        #     # directions_list.sort(key=lambda d: d[1])
        #     # uav.direction = directions_list[0][0]  

        #     # uav.direction = get_normalized_vector(uav.goal_point - uav.position)
        #     flying_dirs.append(uav.direction)


        # if list_collide(flying_uavs, flying_dirs, ca_timerange):
        
        
        # goal_dirs = [get_normalized_vector(uav.goal_point-uav.position) for uav in flying_uavs]
        # if not list_collide(flying_uavs, goal_dirs, ca_timerange):
        #     for u, d in zip(flying_uavs, goal_dirs):
        #         currentamp, _ = vector_2angles(u.direction)
        #         goalamp, _ = vector_2angles(d)
        #         if currentamp-u.max_amp < goalamp < currentamp+u.max_amp:
        #             u.direction = d 


        new_directions, cost = resolve_collision(flying_uavs, k, ca_timerange)

        # for i, uav in enumerate(flying_uavs):
        #     if uav.position[0] < -5 and uav.position[1] > 5 and count < 50:
        #         print(uav)
        #         print(uav.generate_directions(k))
        #         print("new direction:", new_directions[i])
        #         print()  

        
        if not new_directions:
            
            if list_collide(flying_uavs, current_dirs, ca_timerange):
                no_solution = True
                break

            for uav, d in zip(flying_uavs, current_dirs):
                uav.direction = d
   
        else:
            assert len(new_directions) == len(flying_uavs), "Directions and UAVs must have the same len"
            min_cost = min_cost if min_cost < cost else cost
            
            for uav, direction in zip(flying_uavs, new_directions):
                uav.direction = direction[0]
            

        aux = []
        for uav in flying_uavs:
            uav.fly(timestep)
            if not uav.is_in_goal:
                aux.append(uav)
        
        flying_uavs = aux[:]
        for i in range(len(flying_uavs)):
            for j in range(i+1, len(flying_uavs)):
                v = round(sum((flying_uavs[i].position - flying_uavs[j].position)**2)**0.5, 2)
                assert v >= (flying_uavs[i].radio + flying_uavs[j].radio), f"Drones TOO close: {v}" 

        count+=1

    tf = time.time() - t

    measures = {i: calc_measures(uav) for i, uav in enumerate(uavs)}
    measures["waypoints"] = {i: {
        "X": [float(point[0]) for point in uav.history],
        "Y": [float(point[1]) for point in uav.history]
        } for i, uav in enumerate(uavs)}
    measures["total_time"] = tf
    measures["min_cost"] = min_cost

    if no_solution:
        return None

    return measures


