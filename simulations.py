from utils import *
from solver import resolve_collision 


def simulate(uavs, k, timestep, max_iterations=10000):

    fliying_uavs = uavs[:]
    count = 0
    while fliying_uavs or count<max_iterations:
        
        directions = [uav.direction for uav in uavs]
        if list_collide(fliying_uavs, directions, timestep):
            new_directions = resolve_collision(fliying_uavs, k, timestep)
            for uav, direction in zip(fliying_uavs, new_directions):
                uav.direction = direction
    
        aux = []
        for uav in fliying_uavs:
            uav.fly(timestep)
            if not uav.is_in_goal:
                aux.append(uav)

        fliying_uavs = aux
        count+=1

    return fliying_uavs

