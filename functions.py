from math import *


def vectors_distance_by_components(vector1, vector2):
    return sqrt(sum([(x-y)**2 for x,y in zip(vector1, vector2)]))

vect_dist = vectors_distance_by_components

# Dado un vector devuelve el vector normalizado con norma euclideana
def get_normalized_vector(vector):
    vx, vy, vz = vector
    n = vector_norm(vector)
    return (vx/n, vy/n, vz/n)


# Retorna la norma de un vector
def vector_norm(vector):
    return sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)


# Distancia de punto a recta en el espacio
def rect_point_space_distance(rect_point, rect_vector, point):

    p11, p12, p13 = point
    p21, p22, p23 = rect_point

    q1, q2, q3 = p11 - p21, p12 - p22, p13 - p23
    v1, v2, v3 = rect_vector

    # producto vectorial
    p1, p2, p3 = (q2 * v3 - q3 * v2, -(q1 * v3 - q3 * v1), q1 * v2 - q2 * v1)

    s = (v1 ** 2 + v2 ** 2 + v3 ** 2)
    return sqrt((p1 ** 2 + p2 ** 2 + p3 ** 2) * s) / s if s else None

def vector2angles(vector):
    Vx, Vy, Vz = vector
    # phi, theta, r
    return atan2(Vy, Vx) % (2 * pi), acos(Vz) % (2 * pi), (Vx**2 + Vy**2 + Vz**2)**0.5


def angles2vector(phi, theta = pi/2, r = 1):
    return r*sin(theta)*cos(phi), r*sin(theta)*sin(phi), r*cos(theta)


# Verificar si existe colision entre un dron y una lista de drones y direcciones
def provoke_collisions(UAV, direction, UAV_list, detect_collision_method):
    for uav, d in UAV_list:
        if detect_collision_method(uav, d, UAV, direction):
            return True
    return False


# Detecta si los UAVs colisionan siguiendo sus direcciones en un intervalo de tiempo
def is_collision_on_interval(UAV1, d1, UAV2, d2, time_interval):
    UAV1, d1, UAV2, d2 = (UAV1, d1, UAV2, d2) if UAV1.velocity < UAV2.velocity else (UAV2, d2, UAV1, d1)
    distance, vector = colliding_directions(UAV1, d1, UAV2, d2)

    if distance == None or distance > (UAV1.radio + UAV2.radio): return False

    time_collision = sqrt(distance**2 + vect_dist(UAV1.position, UAV2.position)**2)/vector_norm(vector)
    if time_collision > time_interval:
        return False

    return True


# Detecta si hay colisiones en un intervalo de tiempo sin importar la region
def detect_collisions_on_time_interval(UAVs, time_interval):

    for i in range(len(UAVs)):
        for j in range(i+1, len(UAVs)):
            if is_collision_on_interval(UAVs[i], UAVs[i].direction, UAVs[j], UAVs[j].direction, time_interval):
                return True

    return False


# Dados los drones UAV1, UAV2 siguiendo dos direcciones saber si colisionan y la direccion trasladada para UAV2
def colliding_directions(UAV1, d1, UAV2, d2):
    # dejar en UAV1 el de menor velocidad que se fijara

    vector = (d2[0]*UAV2.velocity - d1[0]*UAV1.velocity, d2[1]*UAV2.velocity - d1[1]*UAV1.velocity, d2[2]*UAV2.velocity - d1[2]*UAV1.velocity)
    return rect_point_space_distance(UAV2.position, vector, UAV1.position), vector






# Proyeccion de un punto en una recta en el espacio
# Retorna el punto de proyeccion entre el punto point y la recta de punto incial rect_point y direccion rect_vector
# Retorna tambien la distancia entre rect_point y el punto proyeccion
# el vector debe estar normalizado
def point_rect_space_projection(point, rect_point, rect_vector):

    p11, p12, p13 = rect_point
    p21, p22, p23 = p11 - point[0], p12 - point[1], p13 - point[2]
    v1, v2, v3 = rect_vector

    s = -(p21*v1 + p22*v2 + p23*v3)/ (v1**2 + v2**2 + v3**2)
    return (p11 + v1*s, p12 + v2*s, p13 + v3*s), s


# Devuelve la posicion en que debe estar un elemento dado una lista ordenada
def binary_insert_index(list, value, comparer):
    return binary_insert_recursive(list, 0, len(list), value, comparer)


def binary_insert_recursive(list, index, n, value, comparer):
    if n-index == 1:
        return index if comparer(value, list[index]) <= 0 else (index + 1)%n

    m = int((index + n) / 2)
    return binary_insert_recursive(list, m, n, value, comparer) if comparer(value, list[m]) >= 0 else binary_insert_recursive(list, index, m, value, comparer)



def discriminate(a, b, c):
    D = b**2 - 4*a*c
    print(a, b, c)

    if D < 0:
        print("Discriminante no válido")
        return None

    if D == 0:
        return -b/2*a
    else:
        return (-b + sqrt(D)) / (2*a), (-b - sqrt(D)) / (2*a)


def vector_from_rect(rect):
    a, b, c = rect
    p1, p2 = (0, c/-b), (1, (a + c)/-b)
    return p2[0] - p1[0], p2[1] - p1[1], 0


def radians_from_vector(vector):
    return atan2(vector[1], vector[0]) % (2*pi)

def degrees_from_vector(vector):
    return degrees(radians_from_vector(vector))

def scalar_by_vector(scalar, vector):
    return tuple([scalar*xi for xi in vector])

def vectors_sum(vector1, vector2):
    return tuple(xi+yj for xi, yj in zip(vector1, vector2))


def compare_2Dvectors_by_angle(vector1, vector2):
    x1, y1, _ = vector1
    x2, y2, _ = vector2

    a1, a2 = atan2(y1, x1), atan2(y2, x2)
    return a1 - a2

def vectors_distance_by_components(vector1, vector2):
    return sqrt(sum([(x+y)**2 for x,y in zip(vector1, vector2)]))

def radian_to_vector2D(angle, r = 1):
    return sin(angle), cos(angle)

def intersect_ranges(valid_range, invalid_range):
    a1, a2 = valid_range
    n1, n2 = invalid_range

    if n1%(2*pi) == n2%(2*pi):
        return None

    if belongs_to_angle_range(invalid_range, a1):
        if belongs_to_angle_range(invalid_range, a2):
            return (n2, n1)
        else:
            return (n1 if belongs_to_angle_range(valid_range, n1) else n2 , a2)
    else:
        if belongs_to_angle_range(invalid_range, a2):
            return (a1, n1 if belongs_to_angle_range(valid_range, n1) else n2)
        else:
            return valid_range

# angulos en radianes
def belongs_to_angle_range(range, value):
    value = value % (2*pi)
    r1, r2 = range
    if r1 > r2:
        return r1 <= value <= 2*pi or value <= r2
    else:
        return r1 <= value <= r2

# Pendiente de las tangentes de un punto exterior a un circulo
def tangents_pending_point2circle(circle_center, radio, external_point):

    cx, cy, _ = circle_center
    px, py, _ = external_point

    a = cx ** 2 - radio ** 2 + px ** 2 - 2 * cx * px
    b = 2 * (-cx * cy + cx * py + cy * px - py * px)
    c = - radio ** 2 + cy ** 2 - 2 * cy * py + py ** 2
    return discriminate(a, b, c)

# puntos de interseccion entre una recta y una circunferencia
# https://www.sangakoo.com/es/temas/interseccion-de-una-circunferencia-y-una-recta
def rect_circle_intersections(rect_pending, rect_point, circle_center, circle_radio):

    # circle equation
    ac, bc = circle_center
    Ac, Bc, Cc = -2*ac, -2*bc, ac**2 + bc**2 - circle_radio**2

    # rect equation
    x0, y0, _ = rect_point

    a = 1 + rect_pending**2
    b = 2*y0*rect_pending - 2*(rect_pending**2)*x0 + Ac + Bc*rect_pending
    c = y0**2 - 2*y0*rect_pending*x0 + Bc*rect_pending*x0 + (rect_pending**2)*(x0**2) + Cc

    x1, x2 = discriminate(a, b, c)
    return (x1, y0 + rect_pending*(x1 - x0)), (x2, y0 + rect_pending*(x2 - x0))


def is_2Dpoint_inside_interval(extrem1, extrem2, point):

    e1x, e1y, _ = extrem1
    e2x, e2y, _ = extrem2
    e1x, e2x = min(e1x, e2x), max(e1x, e2x)
    e1y, e2y = min(e1y, e2y), max(e1y, e2y)
    px, py = point

    if e1x <= px <= e2x and e1y <= py <= e2y:
        return True

    return False


if __name__ == "__main__":
    Q = (2, 3, -1)
    P = (2, 4, 1)
    v = (1, 2, 1)

    o = rect_point_space_distance(Q,v,P)






