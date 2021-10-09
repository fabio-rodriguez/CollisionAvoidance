from functions import *

### Helping Methods

# Metodo que detecta la colision entre dos UAVs
# Cada UAV tiene: position, direction, radio, velocity
def is_collision(UAV1, UAV2, region):
    UAV1, UAV2 = (UAV1, UAV2) if UAV1.velocity < UAV2.velocity else (UAV2, UAV1)
    distance, vector = colliding_directions(UAV1, UAV1.direction, UAV2, UAV2.direction)
    if distance == None: return False

    # el tiempo se calcula mediante el desplazamiento y la velocidad del vector desplazado
    _, s = point_rect_space_projection(UAV1.position, UAV2.position, UAV2.direction)
    time = s / vector_norm(vector)
    point = UAV2.position_after_t(time)
    if distance <= (UAV1.radio + UAV2.radio) and time > 0 and region.contains(point):
        return True
    return False

# Metodo que detecta la colision entre dos UAVs
# Es lo mismo que el anterior solo que los UAVs no estan siguiendo las direcciones que se comparan
def verify_collision(region, UAV1, d1, UAV2, d2):
    UAV1, d1, UAV2, d2 = (UAV1, d1, UAV2, d2) if UAV1.velocity < UAV2.velocity else (UAV2, d2, UAV1, d1)
    distance, vector = colliding_directions(UAV1, d1, UAV2, d2)
    if distance == None: return False

    # el tiempo se calcula mediante el desplazamiento y la velocidad del vector desplazado
    _, s = point_rect_space_projection(UAV1.position, UAV2.position, UAV2.direction)
    time = s/ vector_norm(vector)
    point = UAV2.position_after_t(time)
    if distance <= (UAV1.radio + UAV2.radio) and time > 0 and region.contains(point):
        return True
    return False

# Dados los drones UAV1, UAV2 siguiendo las direcciones d1, d2 saber si colisionan y la direccion trasladada para UAV2
def colliding_directions(UAV1, d1, UAV2, d2):
    # dejar en UAV1 el de menor velocidad que se fijara

    vector = (d2[0]*UAV2.velocity - d1[0]*UAV1.velocity, d2[1]*UAV2.velocity - d1[1]*UAV1.velocity, d2[2]*UAV2.velocity - d1[2]*UAV1.velocity)
    return rect_point_space_distance(UAV2.position, vector, UAV1.position), vector

# Funcion de costo 1- Distancia entre el vector actual y el nuevo
# Los vectores deben estar normalizados para que funcione correctamente
def direction_vs_direction_cost(UAV, new_direction):
    X1, Y1, Z1 = UAV.direction
    X2, Y2, Z2 = new_direction
    return sqrt((X1-X2)**2 + (Y1-Y2)**2 + (Z1-Z2)**2)

# Funcion de costo 2- Distancia entre el objetivo del UAV y el nuevo vector
# Los vectores deben estar normalizados para que funcione correctamente
def direction_vs_goal_cost(UAV, new_direction):
    X1, Y1, Z1 = UAV.get_optimal_direction()
    X2, Y2, Z2 = new_direction
    return sqrt((X1-X2)**2 + (Y1-Y2)**2 + (Z1-Z2)**2)


### Collision Avoidance Algorithms

# Algoritmo fuerza bruta para resolver casos 2D y 3D

def solve_brute_force_case(region, UAVs, directions_list):
    return solve_brute_force_recursive(region, UAVs, directions_list, 0, [])

def solve_brute_force_recursive(region, UAVs, directions_list, index, result):
    if index == len(UAVs):
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


# Algoritmos fuerza bruta optimizado para casos 2D y 3D
# La funcion de costo debe recibir dos vectores e indicar el costo de cambiar de direccion del primero al segundo

# Minimizar la desviacion maxima, *cost_function recibe un UAV y un vector e indica costo de tomar la direccion para el UAV
# Dos ideas para el calculo del costo son, 1- Diferencia entre vector actual del UAV y nuevo vector, 2- Distancia entre el "objetivo del UAV y el nuevo vector"
# La segunda medida debe ser mejor
def bf_minimize_max_deviation(region, UAVs, directions_list, cost_function):

    def criteria(uavs):
        return max([cost_function(uav.direction, d) for uav, d in uavs])

    result_list = optimize_brute_force(region, UAVs, directions_list, 0, [])
    return select_optimum(result_list, criteria)


# Minimizar la suma de las desviaciones
def bf_minimize_deviation_sum(region, UAVs, directions_list, cost_function):

    def criteria(uavs):
        return sum([cost_function(uav.direction, d) for uav, d in uavs])

    result_list = optimize_brute_force(region, UAVs, directions_list, 0, [], [])
    return select_optimum(result_list, criteria)


# Debe escoger todas las soluciones factibles posibles y devolver una lista de soluciones factubles posibles
def optimize_brute_force(region, UAVs, directions_list, index, result, result_list):

    if index == len(UAVs):
        result_list.append(result)
        return result_list

    for k in directions_list[index]:
        if not provoke_collisions(region, UAVs[index], k, result):
            result_list = optimize_brute_force(region, UAVs, directions_list, index+1, result + (UAVs[index], k), result_list)

    return result_list


# Seleccionar optimo entre una lista de resultados
def select_optimum(result_list, cost):
    costs = list(map(cost, result_list[:]))
    index = costs.index(min(costs))
    return result_list[index]


# Algoritmo eficiente para el caso 2D
# Las listas de direcciones son angulos
def solve_2D_base_case_N2(region, UAV1, list1, UAV2, list2):

    # identificar el mas lento como UAV1
    UAV1, list1, UAV2, list2 = (UAV1, list1, UAV2, list2) if UAV1.velocity < UAV2.velocity else (UAV2, list2, UAV1, list1)

    p1x, p1y, _ = UAV1.position
    p2x, p2y, _ = UAV2.position

    # encontrar los extremos del mas rapido log k
    opposite = get_normalized_vector((p2x - p1x, p2y - p1y, 0))
    index = binary_insert_index(list2, opposite, compare_2Dvectors_by_angle)
    faster_extreme1, faster_extreme2 = list2[(index-1)%len(list2)], list2[index%len(list2)]

    # print("Extremes faster UAV (radianes): ", radians_from_vector(faster_extreme1), radians_from_vector(faster_extreme2))
    # print("Extremes faster UAV (vector): ", faster_extreme1, faster_extreme2)
    # encontrar los extremos del mas lento (4 en total)
    e11, e12 = slower_vehicle_extreme(UAV1, list1, faster_extreme1, UAV2.velocity)
    e21, e22 = slower_vehicle_extreme(UAV1, list1, faster_extreme2, UAV2.velocity)

    #comparar cada extremo del UAV mas rapido con los dos del UAV de menor velocidad
    solution = brute_solution_two_vehicles(region, UAV1, [e11, e12], UAV2, [faster_extreme1])
    if not solution:
        return brute_solution_two_vehicles(region, UAV1, [e21, e22], UAV2, [faster_extreme2])
    else:
        return solution


def slower_vehicle_extreme(UAV, list, vector, velocity):

    # centro del circulo de velocidad desplazado
    vx, vy, _ = vector
    px, py, _ = UAV.position
    cx, cy = px - vx*velocity, py - vy*velocity

    # pendientes de las tangentes de punto exterior a circulo
    m1, m2 = tangents_pending_point2circle((cx, cy, 0), UAV.velocity, UAV.position)
    module = sqrt(velocity ** 2 - UAV.velocity ** 2) # hallar el vector extremo despues de la traslacion
    extrem1, extrem2 = radian_to_vector2D(atan(m1), module), radian_to_vector2D(atan(m2), module)

    # valor original de los extremos sin la transformacion
    extrem1 = (extrem1[0] + velocity*vx)/ UAV.velocity, (extrem1[1] + velocity*vy)/ UAV.velocity
    extrem2 = (extrem2[0] + velocity*vx)/ UAV.velocity, (extrem2[1] + velocity*vy)/ UAV.velocity

    # calcular el mas cercano a cada vector extremo
    index1 = binary_insert_index(list, extrem1, compare_2Dvectors_by_angle)
    index2 = binary_insert_index(list, extrem2, compare_2Dvectors_by_angle)
    slower_extreme1 = list[index1-1] if vectors_distance_by_components(list[index1-1], extrem1) < \
                                        vectors_distance_by_components(list[index1], extrem1) else list[index1]
    slower_extreme2 = list[index2-1] if vectors_distance_by_components(list[index2-1], extrem2) < \
                                        vectors_distance_by_components(list[index2], extrem2) else list[index2]

    return slower_extreme1, slower_extreme2


def brute_solution_two_vehicles(region, UAV1, list1, UAV2, list2):

    for v1 in list1:
        for v2 in list2:
            if not verify_collision(region, UAV1, v1, UAV2, v2):
                return [(UAV1, v1), (UAV2, v2)]

    return False


def solve_2D_base_case_N3(region, UAV1, list1, UAV2, list2, UAV3, list3):
    # ordenar UAV1, UAV2, UAV3 en orden creciente de velocidad
    UAV1, list1, UAV2, list2 = (UAV1, list1, UAV2, list2) if UAV1.velocity < UAV2.velocity else (UAV2, list2, UAV1, list1)
    UAV1, list1, UAV3, list3 = (UAV1, list1, UAV3, list3) if UAV1.velocity < UAV3.velocity else (UAV3, list3, UAV1, list1)
    UAV2, list2, UAV3, list3 = (UAV2, list2, UAV3, list3) if UAV2.velocity < UAV3.velocity else (UAV3, list3, UAV2, list2)

    # encontrar los extremos del mas rapido log k
    p2x, p2y, _ = UAV2.position
    p3x, p3y, _ = UAV3.position
    opposite = get_normalized_vector((p3x - p2x, p3y - p2y, 0))
    index = binary_insert_index(list3, opposite, compare_2Dvectors_by_angle)
    faster_extreme1, faster_extreme2 = list3[(index - 1)%len(list3)], list2[index%len(list3)]
    # Verificar si la lista esta hecha de angulos
    valid_range_v3 = (faster_extreme1, faster_extreme2) if not belongs_to_angle_range((faster_extreme1, faster_extreme2), vector2angles(opposite)[0]) else (faster_extreme2, faster_extreme1)


    for vector in list1:
        # Se debe cacular con el vector que se fija
        I_12 = invalid_angle_range(UAV1, vector, UAV2)
        I_13 = invalid_angle_range(UAV1, vector, UAV3)

        # Sacar los intervalos de angulos validos
        valid_interval_v3 = intersect_ranges(valid_range_v3, I_13)

        # resolver el caso 2D con intervalos validos
        result = solve_N2_with_intervals(region, UAV2, list2, I_12, UAV3, list3, valid_interval_v3)
        if result:
            return result + [(UAV1, vector)]

    return False


# En O(1) detecta el rango de angulos invalidos para un vector del vehiculo mas lento del caso 2D, N=3
# UAV1 estatico tomando su direccion vector como para las direcciones de UAV2
def invalid_angle_range(UAV1, vector, UAV2):

    vx, vy, _ = vector
    px, py, _ = UAV2.position
    tpx, tpy = px - UAV1.velocity*vx, py - UAV1.velocity*vy

    # Pendientes de las rectas tangentees a UAV1 (extremos de UAV2)
    m1, m2 = tangents_pending_point2circle(UAV1.position, UAV1.velocity, UAV2.position)
    point11, point12 = rect_circle_intersections(m1, UAV2.position, (tpx, tpy, 0), UAV2.velocity)
    point21, point22 = rect_circle_intersections(m2, UAV2.position, (tpx, tpy, 0), UAV2.velocity)

    # Hallar los puntos en la circunferencia trasladada que correspondan a los extremos desde el punto inicial
    p1x, p1y = point11 if is_2Dpoint_inside_interval(UAV1.position, UAV2.position, point11) else point12
    p2x, p2y = point21 if is_2Dpoint_inside_interval(UAV1.position, UAV2.position, point21) else point22

    # Hallar los angulos de los vectores entre los puntos en la circunferencia trasladada y su centro
    angle1, _ = vector2angles((p1x - tpx, p1y - tpy, 0))
    angle2, _ = vector2angles((p2x - tpx, p2y - tpy, 0))

    a1, _ = vector2angles((p1x - px, p1y - py, 0))
    a2, _ = vector2angles((p1x - px, p1y - py, 0))
    middle_angle, _ = vector2angles((UAV1.position[0] - px, UAV1.position[1] - py, 0))

    return (angle1, angle2) if belongs_to_angle_range((a1, a2), middle_angle) else (angle2, angle1)


# Resuelve el problema para 2 drones donde UAV1 tiene menor velocidad que UAV2 y tiene un intervalo no valido.
# Los extremos del intervalo valido para UAV2 son los extremos reales dentro del intervalo valido
# Para hallar la solucion se debe encontrar los extremos en la lista del mas rapido y hallar una solucion valida para el mas lento
def solve_N2_with_intervals(region, UAV1, list1, invalid_interval, UAV2, list2, valid_interval):

    # Obtener los extremos validos en la lista del vehiculo mas rapido
    # Verificar si las listas estan en vactores o radianes
    cmp = compare_2Dvectors_by_angle
    index1, index2  = binary_insert_index(list2, valid_interval[0], cmp), binary_insert_index(list2, valid_interval[1], cmp)
    faster_extreme1, faster_extreme2 = list2[index1%len(list2)], list2[(index2-1)%len(list2)]

    # Obtener los extremos validos en la lista del vehiculo mas lento
    v11, v12 = slower_vehicle_extreme(UAV1, list1, faster_extreme1, UAV2.velocity)
    valid_range_v21 = (v11, v12) if not belongs_to_angle_range((v11, v12), vector2angles(faster_extreme1)[0]) else (v12, v11)
    v21, v22 = slower_vehicle_extreme(UAV1, list1, faster_extreme2, UAV2.velocity)
    valid_range_v22 = (v21, v22) if not belongs_to_angle_range((v21, v22), vector2angles(faster_extreme2)[0]) else (v22, v21)

    v11, v12 = intersect_ranges(valid_range_v21, invalid_interval)
    v21, v22 = intersect_ranges(valid_range_v22, invalid_interval)
    index11, index12 = binary_insert_index(list1, v11, cmp), binary_insert_index(list1, v12, cmp)
    index21, index22 = binary_insert_index(list1, v21, cmp), binary_insert_index(list1, v22, cmp)
    e11, e12 = list1[index11 % len(list1)], list1[(index12 - 1) % len(list1)]
    e21, e22 = list1[index21 % len(list1)], list1[(index22 - 1) % len(list1)]

    solution = brute_solution_two_vehicles(region, UAV1, [e11, e12], UAV2, [faster_extreme1])
    if not solution:
        return brute_solution_two_vehicles(region, UAV1, [e21, e22], UAV2, [faster_extreme2])
    else:
        return solution


def collision_avoidance_hybrid(region, UAVs, directions_list):
    return solve_collision_avoidance_hybrid(region, UAVs, directions_list, 0, [])


def solve_collision_avoidance_hybrid(region, UAVs, directions_list, index, result):
    if index == (len(UAVs)-3):
        return solve_last_3vehicles(region, UAVs, directions_list, result)

    for k in directions_list[index]:
        if not provoke_collisions(region, UAVs[index], k, result):
            return solve_collision_avoidance_hybrid(region, UAVs, directions_list, index+1, result + (UAVs[index], k))

    return False


def solve_last_3vehicles(region, UAVs, directions_list, fixed_vehicles):

    n = len(UAVs)
    valid_velocities = [[], [], []]
    for i in range(n - 3, n):
        for k in directions_list[i]:
            if not provoke_collisions(region, UAVs[i], k, fixed_vehicles):
                valid_velocities[i%3].append(k)

    return solve_2D_base_case_N3(region, UAVs[n-3], directions_list[n-3], UAVs[n-2], directions_list[n-2], UAVs[n-1], directions_list[n-1])


# Algoritmos eficientes de optimizacion

# Expresion lambda muy util para calcular la desviacion de un vector 2D respecto a otro mediante angulos
vector_dif = lambda x, y: abs(vector2angles(x)[0] -  vector2angles(y)[0])

def case_2D_N2_optimized(region, UAV1, list1, UAV2, list2):

    # identificar el mas lento como UAV1
    UAV1, list1, UAV2, list2 = (UAV1, list1, UAV2, list2) if UAV1.velocity < UAV2.velocity else (UAV2, list2, UAV1, list1)

    p1x, p1y, _ = UAV1.position
    p2x, p2y, _ = UAV2.position

    # encontrar los extremos del mas rapido log k
    opposite = get_normalized_vector((p2x - p1x, p2y - p1y, 0))
    index = binary_insert_index(list2, opposite, compare_2Dvectors_by_angle)
    faster_extreme1, faster_extreme2 = list2[(index-1)%len(list2)], list2[index%len(list2)]

    # encontrar los extremos del mas lento (4 en total)
    e11, e12 = slower_vehicle_extreme(UAV1, list1, faster_extreme1, UAV2.velocity)
    e21, e22 = slower_vehicle_extreme(UAV1, list1, faster_extreme2, UAV2.velocity)

    #comparar cada extremo del UAV mas rapido con los dos del UAV de menor velocidad
    sol1 = brute_solution_two_vehicles(region, UAV1, [e11, e12], UAV2, [faster_extreme1])
    sol2 = brute_solution_two_vehicles(region, UAV1, [e21, e22], UAV2, [faster_extreme2])

    if not sol1 and not sol2:
        return False

    # Dadas las dos posibles soluciones buscar el optimo en ambas y luego comparar los dos optimos

    amplitude1 = max([vector_dif(e11, UAV1.direction), vector_dif(e12, UAV1.direction),
                     vector_dif(faster_extreme1, UAV2.direction), vector_dif(faster_extreme2, UAV2.direction)])
    amplitude2 = max([vector_dif(e21, UAV1.direction), vector_dif(e22, UAV1.direction),
                     vector_dif(faster_extreme1, UAV2.direction), vector_dif(faster_extreme2, UAV2.direction)])

    if sol1:
        sol1 = search_optimal_in_range(region, UAV1, (e11, e12), list1, UAV2, (faster_extreme1, faster_extreme2), list2, amplitude1/2, amplitude1/4, sol1)
    else:
        return search_optimal_in_range(region, UAV1, (e21, e22), list1, UAV2, (faster_extreme1, faster_extreme2), list2, amplitude2/2, amplitude2/4, sol2)

    if sol2:
        sol2 = search_optimal_in_range(region, UAV1, (e21, e22), list1, UAV2, (faster_extreme1, faster_extreme2), list2, amplitude2/2, amplitude2/4, sol2)
    else:
        return search_optimal_in_range(region, UAV1, (e11, e12), list1, UAV2, (faster_extreme1, faster_extreme2), list2, amplitude1/2, amplitude1/4, sol1)

    # Siempre va a haber solucion pq si no retornara false antes de ejecutar la optimizacion
    return sol1 if solution_value(sol1) <= solution_value(sol2) else sol2


# Busca el optimo en O(logA*logk) resultando O(logk)
# Hace busqueda binaria entre la direccion prinicipal y la amplitud maxima de giro
def search_optimal_in_range(region, UAV1, extremes1, list1, UAV2, extremes2, list2, amplitude, step, actual_solution):

    if step == 0:
        return actual_solution

    e11, e12 = extremes1
    e21, e22 = extremes2

    # cuando se dice que la direccion original del UAV es la incial no quiere decir que es el angulo 0, el angulo 0 se toma con respecto al eje de coordenadas
    # calcular los angulos intermedios para verificar si existe solucion con menor desviacion que el valor de *amplitude
    ae_11 = max((vector2angles(UAV1.direction)[0] - amplitude)%2*pi, vector2angles(e11)[0])
    ae_12 = min((vector2angles(UAV1.direction)[0] + amplitude)%2*pi, vector2angles(e12)[0])
    ae_21 = max((vector2angles(UAV2.direction)[0] - amplitude)%2*pi, vector2angles(e21)[0])
    ae_22 = min((vector2angles(UAV2.direction)[0] + amplitude)%2*pi, vector2angles(e22)[0])

    # encontrar los vectores con valor en el rango (amplitude, -amplitude)
    new_e11 = list1[binary_insert_index(list1, angles2vector(ae_11, pi/2), compare_2Dvectors_by_angle) % len(list1)]
    new_e12 = list1[binary_insert_index(list1, angles2vector(ae_12, pi/2), compare_2Dvectors_by_angle) - 1]
    new_e21 = list2[binary_insert_index(list2, angles2vector(ae_21, pi/2), compare_2Dvectors_by_angle) % len(list2)]
    new_e22 = list2[binary_insert_index(list2, angles2vector(ae_22, pi/2), compare_2Dvectors_by_angle) - 1]

    solution = optimal_brute_2N_solution(region, UAV1, [new_e11, new_e12], UAV2, [new_e21, new_e22])
    if not solution:
        return search_optimal_in_range(region, UAV1, extremes1, list1, UAV2, extremes2, list2, amplitude + step, step/2, actual_solution)
    else:
        return search_optimal_in_range(region, UAV1, (new_e11, new_e12), list1, UAV2, (new_e21, new_e22), list2, amplitude - step, step/2, solution)


# La solucion optima para el caso con 2 vehiculos
def optimal_brute_2N_solution(region, UAV1, list1, UAV2, list2):

    results = []
    for v1 in list1:
        for v2 in list2:
            if not verify_collision(region, UAV1, v1, UAV2, v2):
                results.append([(UAV1, v1), (UAV2, v2)])

    if results:
        results.sort(key=lambda x: solution_value(x))
        return results[0]

    return False

# Criterio para comparar soluciones
def solution_value(solution):
    return max([vector_dif(uav[0].direction, uav[1]) for uav in solution])

def case_2D_N3_optimized(region, UAV1, list1, UAV2, list2, UAV3, list3):

    # ordenar UAV1, UAV2, UAV3 en orden creciente de velocidad
    UAV1, list1, UAV2, list2 = (UAV1, list1, UAV2, list2) if UAV1.velocity < UAV2.velocity else (UAV2, list2, UAV1, list1)
    UAV1, list1, UAV3, list3 = (UAV1, list1, UAV3, list3) if UAV1.velocity < UAV3.velocity else (UAV3, list3, UAV1, list1)
    UAV2, list2, UAV3, list3 = (UAV2, list2, UAV3, list3) if UAV2.velocity < UAV3.velocity else (UAV3, list3, UAV2, list2)

    # encontrar los extremos del mas rapido log k
    p2x, p2y, _ = UAV2.position
    p3x, p3y, _ = UAV3.position
    opposite = get_normalized_vector((p3x - p2x, p3y - p2y, 0))
    index = binary_insert_index(list3, opposite, compare_2Dvectors_by_angle)
    faster_extreme1, faster_extreme2 = list3[(index - 1) % len(list3)], list2[index % len(list3)]
    # Verificar si la lista esta hecha de angulos
    valid_range_v3 = (faster_extreme1, faster_extreme2) if not belongs_to_angle_range(
        (faster_extreme1, faster_extreme2), vector2angles(opposite)[0]) else (faster_extreme2, faster_extreme1)

    # Ordenar la lista de direcciones de 1 por orden de desviacion
    list1.sort(key = lambda x : vector_dif(x, UAV1.direction))

    # llevar la solucion actual con maximo costo
    # Si hay solucion y el costo no se puede mejorar parar el ciclo
    actual, actual_value = False, pi
    for vector in list1:

        # Si entra aqui hay solucion y no se puede mejorar
        if actual and actual_value < vector_dif(vector, UAV1.direction): break

        # Se debe cacular con el vector que se fija
        I_12 = invalid_angle_range(UAV1, vector, UAV2)
        I_13 = invalid_angle_range(UAV1, vector, UAV3)

        # Sacar los intervalos de angulos validos
        valid_interval_v3 = intersect_ranges(valid_range_v3, I_13)

        # resolver el caso 2D con intervalos validos
        result = optimized_2D_N2_with_intervals(region, UAV2, list2, I_12, UAV3, list3, valid_interval_v3)
        new_value = solution_value(result)
        if not actual or new_value <= actual_value:
            actual, actual_value = result, new_value

    return actual

def case_2D_N2_optimized(region, UAV1, list1, UAV2, list2):

    # identificar el mas lento como UAV1
    UAV1, list1, UAV2, list2 = (UAV1, list1, UAV2, list2) if UAV1.velocity < UAV2.velocity else (UAV2, list2, UAV1, list1)

    p1x, p1y, _ = UAV1.position
    p2x, p2y, _ = UAV2.position

    # encontrar los extremos del mas rapido log k
    opposite = get_normalized_vector((p2x - p1x, p2y - p1y, 0))
    index = binary_insert_index(list2, opposite, compare_2Dvectors_by_angle)
    faster_extreme1, faster_extreme2 = list2[(index-1)%len(list2)], list2[index%len(list2)]

    # encontrar los extremos del mas lento (4 en total)
    e11, e12 = slower_vehicle_extreme(UAV1, list1, faster_extreme1, UAV2.velocity)
    e21, e22 = slower_vehicle_extreme(UAV1, list1, faster_extreme2, UAV2.velocity)

    #comparar cada extremo del UAV mas rapido con los dos del UAV de menor velocidad
    sol1 = brute_solution_two_vehicles(region, UAV1, [e11, e12], UAV2, [faster_extreme1])
    sol2 = brute_solution_two_vehicles(region, UAV1, [e21, e22], UAV2, [faster_extreme2])

    if not sol1 and not sol2:
        return False

    # Dadas las dos posibles soluciones buscar el optimo en ambas y luego comparar los dos optimos

    amplitude1 = max([vector_dif(e11, UAV1.direction), vector_dif(e12, UAV1.direction),
                     vector_dif(faster_extreme1, UAV2.direction), vector_dif(faster_extreme2, UAV2.direction)])
    amplitude2 = max([vector_dif(e21, UAV1.direction), vector_dif(e22, UAV1.direction),
                     vector_dif(faster_extreme1, UAV2.direction), vector_dif(faster_extreme2, UAV2.direction)])

    if sol1:
        sol1 = search_optimal_in_range(region, UAV1, (e11, e12), list1, UAV2, (faster_extreme1, faster_extreme2), list2, amplitude1/2, amplitude1/4, sol1)
    else:
        return search_optimal_in_range(region, UAV1, (e21, e22), list1, UAV2, (faster_extreme1, faster_extreme2), list2, amplitude2/2, amplitude2/4, sol2)

    if sol2:
        sol2 = search_optimal_in_range(region, UAV1, (e21, e22), list1, UAV2, (faster_extreme1, faster_extreme2), list2, amplitude2/2, amplitude2/4, sol2)
    else:
        return search_optimal_in_range(region, UAV1, (e11, e12), list1, UAV2, (faster_extreme1, faster_extreme2), list2, amplitude1/2, amplitude1/4, sol1)

    # Siempre va a haber solucion pq si no retornara false antes de ejecutar la optimizacion
    return sol1 if solution_value(sol1) <= solution_value(sol2) else sol2


def optimized_2D_N2_with_intervals(region, UAV1, list1, invalid_interval, UAV2, list2, valid_interval):

    cmp = compare_2Dvectors_by_angle
    index1, index2 = binary_insert_index(list2, valid_interval[0], cmp), binary_insert_index(list2, valid_interval[1], cmp)
    faster_extreme1, faster_extreme2 = list2[index1 % len(list2)], list2[(index2 - 1) % len(list2)]

    # Obtener los extremos validos en la lista del vehiculo mas lento
    v11, v12 = slower_vehicle_extreme(UAV1, list1, faster_extreme1, UAV2.velocity)
    valid_range_v21 = (v11, v12) if not belongs_to_angle_range((v11, v12), vector2angles(faster_extreme1)[0]) else (v12, v11)
    v21, v22 = slower_vehicle_extreme(UAV1, list1, faster_extreme2, UAV2.velocity)
    valid_range_v22 = (v21, v22) if not belongs_to_angle_range((v21, v22), vector2angles(faster_extreme2)[0]) else (v22, v21)

    e11, e12 = intersect_ranges(valid_range_v21, invalid_interval)
    e21, e22 = intersect_ranges(valid_range_v22, invalid_interval)

    # comparar cada extremo del UAV mas rapido con los dos del UAV de menor velocidad
    sol1 = brute_solution_two_vehicles(region, UAV1, [e11, e12], UAV2, [faster_extreme1])
    sol2 = brute_solution_two_vehicles(region, UAV1, [e21, e22], UAV2, [faster_extreme2])

    if not sol1 and not sol2:
        return False

    # Dadas las dos posibles soluciones buscar el optimo en ambas y luego comparar los dos optimos

    amplitude1 = max([vector_dif(e11, UAV1.direction), vector_dif(e12, UAV1.direction),
                      vector_dif(faster_extreme1, UAV2.direction), vector_dif(faster_extreme2, UAV2.direction)])
    amplitude2 = max([vector_dif(e21, UAV1.direction), vector_dif(e22, UAV1.direction),
                      vector_dif(faster_extreme1, UAV2.direction), vector_dif(faster_extreme2, UAV2.direction)])

    # Revisar si el metodo usado para el problema donde no hay optimizacion funciona para este caso (Creo que si)

    if sol1:
        sol1 = search_optimal_in_range(region, UAV1, (e11, e12), list1, UAV2, (faster_extreme1, faster_extreme2), list2,
                                       amplitude1 / 2, amplitude1 / 4, sol1)
    else:
        return search_optimal_in_range(region, UAV1, (e21, e22), list1, UAV2, (faster_extreme1, faster_extreme2), list2,
                                       amplitude2 / 2, amplitude2 / 4, sol2)

    if sol2:
        sol2 = search_optimal_in_range(region, UAV1, (e21, e22), list1, UAV2, (faster_extreme1, faster_extreme2), list2,
                                       amplitude2 / 2, amplitude2 / 4, sol2)
    else:
        return search_optimal_in_range(region, UAV1, (e11, e12), list1, UAV2, (faster_extreme1, faster_extreme2), list2,
                                       amplitude1 / 2, amplitude1 / 4, sol1)

    # Siempre va a haber solucion pq si no retornara false antes de ejecutar la optimizacion
    return sol1 if solution_value(sol1) <= solution_value(sol2) else sol2

