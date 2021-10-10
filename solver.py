

## Resolve collision during a timestep
def resolve_collision(uavs, k, timestep):
    directions_list = [uav.generate_directions(k) for uav in uavs]
    return __solve__(uavs, directions_list, timestep)


def __solve__(uavs, directions_list, timestep):
    
    return solve_brute_force_recursive(uavs, directions_list, timestep, 0, [])


## TODO Revisar
def solve_brute_force_recursive(uavs, directions_list, timestep, index, result):
    if index == len(uavs):
        return result

    for k in directions_list[index]:
        if not provoke_collisions(region, UAVs[index], k, result):
            return solve_brute_force_recursive(region, UAVs, directions_list, index+1, result + (UAVs[index], k))

    return False

# Verificar si existe colision entre un dron y una lista
def provoke_collisions(region, UAV, direction, UAV_list):
    for uav, d in UAV_list:
        if verify_collision(region, uav, d, UAV, direction):
            return True
    return False

