from utils import *
from solver import resolve_collision 

def simulate(uavs, k, timestep, max_iterations=10000):

    fliying_uavs = uavs[:]
    count = 0
    while fliying_uavs or count<max_iterations:

        aux = False
        for i in range(len(fliying_uavs)):
            for j in range(i, len(fliying_uavs)):  
                if collide(fliying_uavs[i], fliying_uavs[i].direction, fliying_uavs[j], fliying_uavs[j].direction, timestep)
                    aux = True
                    ## TODO resolve collision for all uavs 
                    directions = resolve_collision(fliying_uavs, k, timestep)
                    for uav, direction in zip(fliying_uavs, directions):
                        uav.direction = direction
                    break
            if aux:
                break
                
        aux = []
        for uav in fliying_uavs:
            uav.fly(timestep)
            if not uav.is_in_goal:
                aux.append(uav)

        fliying_uavs = aux
        count+=1

    return fliying_uavs

# ## return groups of drones in collision
# def collision_groups(uavs, t):

#     # This loop give a number for every colliding group
#     N = len(uavs)
#     aux = list(range(N))
#     for i in range(N):
#         for j in range(i+1, N):
#             if collide(uavs[i], uavs[j]):
#                 aux[j] = aux[i]

#     # This loop return in groups all uavs with the same number
#     groups = []
#     aux2 = [False]*N
#     for index, i in enumerate(aux):
#         g = [uavs[index]]
#         if aux2[index] == True:
#             continue
#         aux2[index] = True

#         for j in range(index+1, N):
#             if aux2[j] == True:
#                 continue

#             if aux[j] == i:
#                 g.append(uavs[j])
#                 aux2[j] = True

#         groups.append(g)

#     return groups    
