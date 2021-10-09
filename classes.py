from functions import get_normalized_vector, vector2angles, angles2vector
from math import sqrt, pi, sin, cos, atan2


class UAV:

    def __init__(self, position, velocity, radio, direction, goal_point):
        self.position = position
        self.velocity = velocity
        self.radio = radio
        self.direction = get_normalized_vector(direction)
        self.goal_point = goal_point

    def position_after_t(self, time):

        px, py, pz = self.position
        vx, vy, vz = self.direction
        return (px + self.velocity*time*vx, py + self.velocity*time*vy, pz + self.velocity*time*vz)

    # los rangos son los valores que limitan el desvio, o sea, el UAV solo podra tomar desde d-range/2 hasta d+range/2
    # k es el paso que en cada rango salta
    def generate_directions_by_vector_ranges(self, Xrange, Yrange, Zrange, k):

        Xstep, Ystep, Zstep = Xrange / k, Yrange / k, Zrange / k
        x, y, z = self.direction
        directions = []
        for i in range(k):
            for j in range(k):
                for k in range(k):
                    d = (x - Xrange/2 + i * Xstep, y - Yrange/2 + j * Ystep, z - Zrange/2 + k * Zstep)
                    if d != (0,0,0):
                        directions.append(get_normalized_vector(d))

        directions.append(self.direction)
        return directions

    # los rangos se dan en radianes para los planos phi -> XY, theta -> eje Z
    def generate_directions_by_span_angles(self, span_phi_range, span_theta_range, k):
        phi ,theta, _ = vector2angles(self.direction)
        n = int(sqrt(k))

        directions = []
        for i in range(n+1):
            for j in range(n+1):
                if i and j:
                    directions.append(angles2vector((phi - span_phi_range/2 + i*span_phi_range/(n+1)) % (2*pi),
                                                    (theta - span_theta_range/2 + j*span_theta_range/(n+1)) % (2*pi)))

        directions.append(self.direction)
        return directions

    # los rangos se dan en radianes para los planos phi -> XY, theta -> eje Z
    def generate_directions2D(self, span_theta_range, k):
        theta, _, _ = vector2angles(self.direction)

        directions = []
        for i in range(k+1):
            if i:
                if not k%2 and i == int((k+1)/2)+1:
                    directions.append(self.direction)
                theta_i = (theta - span_theta_range/2 + i*span_theta_range/(k+1)) % (2 * pi)
                directions.append((cos(theta_i), sin(theta_i), 0))

        directions.sort(key = lambda x: atan2(x[1],x[0])%(2*pi))
        return directions

    def get_optimal_direction(self):
        X1, Y1, Z1 = self.goal_point
        X2, Y2, Z2 = self.position
        return get_normalized_vector((X1-X2, Y1-Y2, Z1-Z2))
    
    def generate_directions3D(self, span_phi_range, span_theta_range, k):
        phi, theta, _ = vector2angles(self.direction)

        directions = []
        k = int(sqrt(k))
        for i in range(k):
            for j in range(k):
                phi_i = (phi - span_phi_range + 2 * i * span_phi_range / k + span_phi_range / k) % (2 * pi)
                theta_j = (theta - span_theta_range + 2 * j * span_theta_range / k + span_theta_range / k) % (2 * pi)
                directions.append(angles2vector(phi_i, theta_j))

                v1 = self.get_optimal_direction()
                v2 = angles2vector(phi_i, theta_j)
        return directions + [self.get_optimal_direction()]



class Region:

    # La region es un cubo en el espacio
    def __init__(self, init_point, width, long, height):
        self.init_point = init_point
        self.width = width # ancho
        self.long = long # largo
        self.height = height #altura

    def contains(self, point):
        px, py, pz = self.init_point
        x, y, z = point
        return (px <= x <= px + self.width) and (py <= y <= py + self.width) and (pz <= z <= pz + self.width)

if __name__ == "__main__":

    from math import atan2, degrees

    uav = UAV((1,1,0), 1, 1, (1,0,0), (20,0,0))


    # angles = [vector2angles(v) for v in uav.generate_directions_by_span_angles(pi/2, pi/2, 25)]
    # angles = [(degrees(a1), degrees(a2)) for a1, a2, _ in angles]
    # print(angles)

    # print(uav.get_optimal_direction())

