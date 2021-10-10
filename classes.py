
from functions import get_normalized_vector, vector2angles, angles2vector
from math import sqrt, pi, sin, cos, atan2
from utils import *


class UAV:

    def __init__(self, position, speed, radio, direction, goal_point, goal_distance=1):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.radio = radio
        self.direction = np.array((get_normalized_vector(direction))
        self.goal_point = np.array(goal_point)
        self.is_in_goal = False

    def fly(self, timestep):
        new_pos = self.position + timestep*speed*self.direction

        ## Distance from P3 to line between P1 and P2
        p1, p2, p3 = new_pos, self.position, self.goal_point
        d = distance_from_line_2point(p1, p2, p3)
        if d <= goal_distance:
            self.is_in_goal = True
        
        self.position = new_pos


    def generate_directions(self, k, max_amp=randians(30)):

        d = []
        amp = 2*max_amp/k
        currentamp, _ = vector_2angles(self.direction)
        for i in range(k+1):
            newamp = -max_amp + amp*i
            if newamp>0 and k%2==0:
                d.append(self.direction)

            d.append(angles_2vector(currentamp+newamp))
        
        return d
         

    # def position_after_t(self, time):

    #     px, py, pz = self.position
    #     vx, vy, vz = self.direction
    #     return (px + self.velocity*time*vx, py + self.velocity*time*vy, pz + self.velocity*time*vz)


    # # los rangos se dan en radianes para los planos phi -> XY, theta -> eje Z
    # def generate_directions2D(self, span_theta_range, k):
    #     theta, _, _ = vector2angles(self.direction)

    #     directions = []
    #     for i in range(k+1):
    #         if i:
    #             if not k%2 and i == int((k+1)/2)+1:
    #                 directions.append(self.direction)
    #             theta_i = (theta - span_theta_range/2 + i*span_theta_range/(k+1)) % (2 * pi)
    #             directions.append((cos(theta_i), sin(theta_i), 0))

    #     directions.sort(key = lambda x: atan2(x[1],x[0])%(2*pi))
    #     return directions

    # def get_optimal_direction(self):
    #     X1, Y1, Z1 = self.goal_point
    #     X2, Y2, Z2 = self.position
    #     return get_normalized_vector((X1-X2, Y1-Y2, Z1-Z2))
    
    # def generate_directions3D(self, span_phi_range, span_theta_range, k):
    #     phi, theta, _ = vector2angles(self.direction)

    #     directions = []
    #     k = int(sqrt(k))
    #     for i in range(k):
    #         for j in range(k):
    #             phi_i = (phi - span_phi_range + 2 * i * span_phi_range / k + span_phi_range / k) % (2 * pi)
    #             theta_j = (theta - span_theta_range + 2 * j * span_theta_range / k + span_theta_range / k) % (2 * pi)
    #             directions.append(angles2vector(phi_i, theta_j))

    #             v1 = self.get_optimal_direction()
    #             v2 = angles2vector(phi_i, theta_j)
    #     return directions + [self.get_optimal_direction()]



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

