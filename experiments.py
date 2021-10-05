from math import *


def experiment1():
    ''' 6 drones antipodales'''

    timestep = 0.25

    ## Max_dist, timeHorizon, timeHorizonObstacles, radio, , maxSpeed 
    drone_parameters = [15, 10, 10, 1.5, 2] 

    drone_positions = []
    for i in range(6):
        x = cos(i*2*pi/6) 
        y = sin(i*2*pi/6) 
        drone_positions.append((x,y))

    goals = [(-x, -y) for x,y in drone_positions)]

    return  timestep, drone_parameters, drone_positions, goals
    

def experiment2():
    pass


def experiment3():
    pass

    
def experiment4():
    pass

    
def experiment5():
    pass


def experiment6():
    pass


def simulate(timestep, drone_parameters, drone_positions, goals):
    pass



if __name__ == "__main__":

    timestep, drone_parameters, drone_positions, goals = experiment1()

    return simulate(timestep, drone_parameters, drone_positions, goals)