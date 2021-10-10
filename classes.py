from math import sqrt, pi, sin, cos, atan2
from utils import *


class UAV:

    def __init__(self, position, speed, radio, direction, goal_point, goal_distance=1, max_amp=randians(30)):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.radio = radio
        self.direction = np.array((get_normalized_vector(direction))
        self.goal_point = np.array(goal_point)
        self.is_in_goal = False
        self.max_amp = max_amp

    def fly(self, timestep):
        new_pos = self.position + timestep*speed*self.direction

        ## Distance from P3 to line between P1 and P2
        p1, p2, p3 = new_pos, self.position, self.goal_point
        d = distance_from_line_2point(p1, p2, p3)
        if d <= goal_distance:
            self.is_in_goal = True
        
        self.position = new_pos


    def generate_directions(self, k):

        d = []
        amp = 2*self.max_amp/k
        currentamp, _ = vector_2angles(self.direction)
        for i in range(k+1):
            newamp = -self.max_amp + amp*i
            if newamp>0 and k%2==0:
                d.append(self.direction)

            d.append(get_normalized_vector(angles_2vector(currentamp+newamp)))
        
        return d


if __name__ == "__main__":

    from math import atan2, degrees

    uav = UAV((1,1,0), 1, 1, (1,0,0), (20,0,0))


    # angles = [vector2angles(v) for v in uav.generate_directions_by_span_angles(pi/2, pi/2, 25)]
    # angles = [(degrees(a1), degrees(a2)) for a1, a2, _ in angles]
    # print(angles)

    # print(uav.get_optimal_direction())

