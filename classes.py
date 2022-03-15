from math import *
from utils import *


class UAV:

    def __init__(self, position, speed, radio, direction, goal_point, goal_distance=1, max_amp=radians(45)):
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
        
        # goal_dir = get_normalized_vector(self.goal_point - self.position)

        # d = []
        # amp = 2*self.max_amp/k
        # currentamp, _ = vector_2angles(self.direction)

        # for i in range(k+1):
        #     newamp = -self.max_amp + amp*i
        #     dir = get_normalized_vector(angles_2vector(currentamp+newamp))
        #     d.append((dir, euclidian_distance(dir, goal_dir)))
        
        # d.append((self.direction, euclidian_distance(self.direction, goal_dir)))
        
        goal_dir = get_normalized_vector(self.goal_point - self.position)

        d = []
        amp = 2*self.max_amp/k
        currentamp, _ = vector_2angles(self.direction)
        for i in range(k+1):
            newamp = -self.max_amp + amp*i
            newdir = get_normalized_vector(angles_2vector(currentamp+newamp))
            d.append((newdir, euclidian_distance(newdir, goal_dir)))
        
        if k%2!=0:
            d.append((self.direction, euclidian_distance(self.direction, goal_dir)))
        
        return d


if __name__ == "__main__":

    from math import atan2, degrees

    #  [(array([0.94341668, 0.33160966]), 0.04702048877028444), 
    # (array([0.72697622, 0.68666264]), 0.36971546811559025), 
    # (array([0.38483497, 0.9229854 ]), 0.7702930849531653), 
    # (array([-0.02384775,  0.9997156 ]), 1.1372051977019704), 
    # (array([-0.42840697,  0.9035859 ]), 1.454415986395225), 
    # (array([-0.75889073,  0.65121798]), 1.7080618174207913)]
    uav = UAV((-4.26866144, 11.6145004),1,0.5,(-0.71826272, -0.695772),(-8,8),max_amp=radians(60))

    print(uav)
    print(uav.generate_directions(5))


