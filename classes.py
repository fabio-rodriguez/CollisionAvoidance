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
        ## WITH POINT TO LINE
        # new_pos = self.position + timestep*self.speed*self.direction

        # ## Distance from P3 to line between P1 and P2
        # p1, p2, p3 = new_pos, self.position, self.goal_point
        # cat1 = distance_from_line_2point(p1, p2, p3)
        
        # cat2 = euclidian_distance(p1, p3)
        
        # ## If it pass near goal position
        # if cat1 <= self.goal_distance+self.radio and sqrt(cat1**2+cat2**2) <= self.speed*timestep:
        #     self.is_in_goal = True
        #     self.history.append(self.goal_point)
        # else:
        #     self.position = new_pos
        #     self.history.append(self.position)
        
        goal = Point(self.goal_point[0], self.goal_point[1])
        res = detect_collision_point(self.position, self.direction, goal,self.goal_distance+self.radio)
        try:
            p1, p2 = res 
            p1 = np.array([p1.x, p1.y])
            p2 = np.array([p2.x, p2.y])
            d1, d2 = euclidian_distance(self.position, p1), euclidian_distance(self.position, p2) 
            near = p1 if d1 < d2 else p2
        except:
            near = None if res == None else np.array([res.x, res.y])

        if not (near is None):
            time = time_from_displacement(self.direction, self.speed, euclidian_distance(self.position, near)) 
            if time < timestep:
                self.is_in_goal = True
                self.history.append(self.goal_point)
                return
        
        self.position = self.position +timestep*self.speed*self.direction 
        self.history.append(self.position)

        if euclidian_distance(self.position, self.goal_point) < (self.radio+self.goal_distance):
            self.is_in_goal = True
    


    def generate_directions(self, k, stop_cost = None):
        
        if k%2!=0:
            k-=1
        goal_dir = get_normalized_vector(self.goal_point - self.position)

        d = []
        amp = 2*self.max_amp/k
        currentamp, _ = vector_2angles(self.direction)
        togoal = True
        for i in range(k+1):
            newamp = -self.max_amp + amp*i
            newdir = get_normalized_vector(angles_2vector(currentamp+newamp))
            cost = euclidian_distance(newdir, goal_dir)
            d.append((newdir, cost))
            # d.append((newdir/4, cost+1))
            # d.append((newdir, euclidian_distance(newdir, self.direction)))
            if goal_dir[0] == newdir[0] and goal_dir[1] == newdir[1]:
                togoal = False
        
        # if k%2!=0:
        #     d.append((self.direction, euclidian_distance(self.direction, 0)))
        goalamp, _ = vector_2angles(goal_dir)
        if togoal and angle_in_range(currentamp-self.max_amp, currentamp+self.max_amp, goalamp):
        # if togoal:
            d.append((goal_dir, 0))
        
        # d.append((goal_dir, 0))


        # if stop_cost:
        #     d.append((goal_dir/5, stop_cost))
            # d.append((np.array([0, 0]), stop_cost))

        return d


    def __str__(self) -> str:
        
        string = f''' DRONE PROPERTIES
                postion: {self.position}\n
                speed: {self.speed}                
                radio: {self.radio}                
                direction: {self.direction}                
                goal: {self.goal_point}                
                max_amp: {self.max_amp}                
            '''

        return string 

    def copy(self):
        uav = UAV((self.position[0], self.position[1]), self.speed, self.radio, (self.direction[0], self.direction[1]), self.goal_point)
        return uav

if __name__=="__main__":

    uav1 = UAV((2.10904519, -0.52810635), 1.3333333333333333, 0.5, (-0.99905033, 0.04357113), (-10, 0), max_amp=0.7853981633974483)

    uav2 = UAV((0.61803399, -1.90211303), 1.3333333333333333, 0.5, (-0.30901699, 0.95105652), (-3.09016994, 9.51056516), max_amp=0.7853981633974483)

    print(collide(uav1, uav1.direction, uav2, uav2.direction, 3))

    uav1.fly(1)
    uav2.fly(1)

    print(sum(((uav1.position-uav2.position)**2))**0.5)
