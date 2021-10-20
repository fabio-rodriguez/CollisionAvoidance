from math import *
from utils import *


class UAV:

    def __init__(self, position, speed, radio, direction, goal_point, goal_distance=1, max_amp=radians(30)):
        self.position = np.array(position)
        self.initial_position = np.array(position)
        self.speed = speed
        self.radio = radio
        self.direction = np.array(get_normalized_vector(direction))
        self.goal_point = np.array(goal_point)
        self.is_in_goal = False
        self.max_amp = max_amp
        self.history = [self.position]
        ## Minimum distance to reach the goal
        self.goal_distance = goal_distance

    def fly(self, timestep):
        new_pos = self.position + timestep*self.speed*self.direction

        ## Distance from P3 to line between P1 and P2
        p1, p2, p3 = new_pos, self.position, self.goal_point
        cat1 = distance_from_line_2point(p1, p2, p3)
        cat2 = euclidian_distance(p1, p3)

        self.position = new_pos
        self.history.append(self.position)

        if cat1 <= self.goal_distance and sqrt(cat1**2+cat2**2) <= self.speed*timestep:
            self.is_in_goal = True
            self.history.append(self.goal_point)



    def generate_directions(self, k):

        d = []
        amp = 2*self.max_amp/k
        currentamp, _ = vector_2angles(self.direction)
        aux = True
        for i in range(k+1):
            newamp = -self.max_amp + amp*i
            if aux and newamp>0 and k%2==0:
                aux = False
                d.append((self.direction, 0))

            d.append((get_normalized_vector(angles_2vector(currentamp+newamp)), abs(amp*(i-int(k/2)))))
        
        return d


if __name__ == "__main__":

    from math import atan2, degrees

    uav = UAV((1,1,0), 1, 1, (1,0,0), (20,0,0))


