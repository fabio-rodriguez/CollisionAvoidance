# Collision-Avoidance
Algorithms for collision avoidance of UAVs in space


A ver, lo voy a redactar en plan compadre, ya despues tu lo pones bonito:

Basicamente para hacer un experimentos solo tienes que crear los drones (cada uno con su goal), meterlos en una lista y llamar a la funcion 'simulate' que recibe los siguientes parametros:

simulate(uavs, k, ca_timerange, timestep, max_iterations)

Lo de arriba lo puedes ver en experiments.py

La definiciond e la funcion simulate esta en simulations.py y hace lo siguiente:

uavs: la lista de drones
k: el numerod e amniobras a generar en caso de collision
ca_timerange: rango de deteccion de collision (es el rango grande de tiempo donde se detectan las colisiones)
timestep: paso temporal del algoritmo, es el tiempo que vuelan los drones antes de plantearse otra vez si hay colision en el rango 'ca_timerange'
max_iterations: cantiad de iteracion maximas de la simulacion, en plan, si el algoritmo no ha terminado despues de 'max_iterations'  pasos de tiempo se detiene

Ahora, para crear un dron con su goal tienes que crear un objeto de la clase UAV definida en classes.py:

se crea asi: 
uav = UAV(parametros...) (esto lo puedes ver en experiments.py)

Los parametros estan en classes.py y son:

UAV(position, speed, radio, direction, goal_point, goal_distance, max_amp)

position: posicion inicial del UAV, es un vector de posicion (x,y)
speed: velocidad del uav (utilizamos 1.5)
radio: radio del uav
direction: direccion inicial del uav
goal_point: punto objetivo, es un vector de posicion (x,y)
goal_distance: distancia minima para que se considere que ha llegado al goal (en plan si estas a un metro del goal ya llegaste)
max_amp: Maxima amplitud para generar los angulos, por ejemplo, si es 45, entonces en caso de colision el dron generar las k direccion entre los 45 grados a la izquierda y los 45 grados a la derecha del objetivo (es en radianes)
