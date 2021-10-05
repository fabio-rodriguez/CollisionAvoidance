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

    # timestep, drone_parameters, drone_positions, goals = experiment1()

    # return simulate(timestep, drone_parameters, drone_positions, goals)

    i = 0
    N = 1000
    while i < N:

        posiciones = []
        for i in range(6):
            x = random.uniform(-25, 25)
            y = random.uniform(-25, 25)
            posiciones.append((x, y))

        goals = []
        for i in range(6):
            x = random.uniform(-25, 25)
            y = random.uniform(-25, 25)
            goals.append((x, y))

        distanciadeseguridad = 3
        auxiliar = False
        for i in range(len(posiciones)):    
            for j in range(i+1, len(posiciones)):
                pos1 = posiciones[i]
                pos2 = posiciones[j]
                if dist(pos1, pos2) < distanciadeseguridad:
                    auxiliar = True
                    break 
        
        for i in range(len(goals)):    
            for j in range(i+1, len(goals)):
                pos1 = goals[i]
                pos2 = goals[j]
                if dist(pos1, pos2) < distanciadeseguridad:
                    auxiliar = True
                    break 

        if auxiliar:
            continue

        ### Imprimir experimento en txt (posiciones y goals)

        ## Haces el experimento

        ### Imprimir resultados en txt (diferentes medidas)

        i+=1

        ## i.TXT
        # pocisiones = [(x1, y1), ... ,(xn, yn)]
        # goals = [(x1, y1), ... ,(xn, yn)]
        # tiempo: MEDIDA DE TIEMPO
        # trayectoria: ...
        # ....















