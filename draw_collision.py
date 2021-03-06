import matplotlib.pyplot as plt
import numpy as np

from utils import euclidian_distance



def draw_circle():

    fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot

    circle1 = plt.Circle((0, 0), 0.5, color='r')
    circle2 = plt.Circle((0.5, 0.5), 0.2, color='blue')
    circle3 = plt.Circle((1, 1), 0.2, color='g', clip_on=False)

    # (or if you have an existing figure)
    # fig = plt.gcf()
    # ax = fig.gca()

    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(circle3)


def draw_circle2(poss,dirs,t, cs):

    fig, ax = plt.subplots()

    for i in range(len(poss)):
        pos = poss[i]
        dir = dirs[i]
        c = cs[i]
        for k in range(t):
            p = pos+dir*k*1.5
            if k==0:
                circle = plt.Circle(p, 0.75, color=c)
            else:
                circle = plt.Circle(p, 0.5, color=c)

            ax.add_patch(circle)

    plt.xlim([-20, 20])
    plt.ylim([-20, 20])
    plt.show()



if __name__ == "__main__":

    #COLLISIONS:
    #(1,1,1,1,1)
    #(2,1,1,1,1)
    #(3,1,1,1,1)
    #(4,1,1,1,1)
    #(5,1,1,1,1)
    #(6,1,1,1,1)

    #(1,2,1,1,1)
    #(1,3,1,1,1)
    #(1,4,1,1,1)
    #(1,5,1,1,1)
    #(1,6,1,1,1)
    


    # Drone: 1 DRONE PROPERTIES
    #                 postion: [-0.55508902 -0.41191666]

    #                 speed: 1.3333333333333333                
    #                 radio: 0.5                
    #                 direction: [-0.99905033  0.04357113]                
    #                 goal: [-10.  -0.]                
    #                 max_amp: 1.2217304763960306                
                
    # [(array([-0.30075186,  0.95370243]), 1.147152872702092), 
    # (array([-0.65389744,  0.7565832 ]), 0.7921595320783132), 
    # (array([-0.90008646,  0.43571134]), 0.40443514466407554), 
    # (array([-0.99905033,  0.04357113]), 1.3877787807814457e-16), 
    # (array([-0.93460175, -0.3556959 ]), 0.4044351446640758), 
    # (array([-0.71728243, -0.69678255]), 0.7921595320783138), 
    # (array([-0.38263881, -0.92389801]), 1.1471528727020925), 
    # (array([-0.99905033,  0.04357113]), 0)]
    pos1 = np.array([-0.55508902, -0.41191666])    
    dir11 = np.array([-0.30075186,  0.95370243])
    dir12 = np.array([-0.65389744,  0.7565832])
    dir13 = np.array([-0.90008646,  0.43571134])
    dir14 = np.array([-0.93460175, -0.3556959])
    dir15 = np.array([-0.71728243, -0.69678255])
    dir16 = np.array([-0.38263881, -0.92389801])
    

    # Drone: 2 DRONE PROPERTIES
    #                 postion: [ 1.74937852 -0.712795  ]

    #                 speed: 1.3333333333333333                
    #                 radio: 0.5                
    #                 direction: [-0.481978   -0.87618332]                
    #                 goal: [-3.09016994 -9.51056516]                
    #                 max_amp: 1.2217304763960306                
                
    # [(array([-0.98818918,  0.15323882]), 1.1471528727020923), 
    # (array([-0.96806602, -0.25069539]), 0.7921595320783135), 
    # (array([-0.78959844, -0.6136239 ]), 0.4044351446640758), 
    # (array([-0.481978  , -0.87618332]), 1.6653345369377348e-16), 
    # (array([-0.09552148, -0.99542737]), 0.40443514466407554), 
    # (array([ 0.30655928, -0.95185157]), 0.7921595320783131), 
    # (array([ 0.65849682, -0.75258351]), 1.1471528727020923), 
    # (array([-0.481978  , -0.87618332]), 0)]
    pos2 = np.array([1.74937852, -0.712795])    
    dir21 = np.array([-0.98818918,  0.15323882])
    dir23 = np.array([-0.481978  , -0.87618332])

    # Drone: 3 DRONE PROPERTIES
    #                 postion: [0.89318384 0.43862528]

    #                 speed: 1.3333333333333333                
    #                 radio: 0.5                
    #                 direction: [ 0.75158658 -0.65963445]                
    #                 goal: [ 8.09016994 -5.87785252]                
    #                 max_amp: 1.2217304763960306                
                
    # [(array([-0.36279587, -0.93186864]), 1.1471528727020928), 
    # (array([ 0.0359693, -0.9993529]), 0.7921595320783136), 
    # (array([ 0.42885105, -0.90337521]), 0.4044351446640761), 
    # (array([ 0.75158658, -0.65963445]), 4.002966042486721e-16), 
    # (array([ 0.95138677, -0.30799874]), 0.40443514466407526), 
    # (array([0.99557072, 0.09401564]), 0.792159532078313), 
    # (array([0.87691138, 0.4806521 ]), 1.147152872702092), 
    # (array([ 0.75158658, -0.65963445]), 0)]
    pos3 = np.array([0.89318384, 0.43862528])    
    dir31 = np.array([-0.36279587, -0.93186864])
    dir33 = np.array([0.75158658, -0.65963445])

    # Drone: 4 DRONE PROPERTIES
    #                 postion: [-0.20259635  1.0834968 ]

    #                 speed: 1.3333333333333333                
    #                 radio: 0.5                
    #                 direction: [0.8657303  0.50051079]                
    #                 goal: [8.09016994 5.87785252]                
    #                 max_amp: 1.2217304763960306                
                
    # [(array([ 0.7664235, -0.6423356]), 1.147152872702092), 
    # (array([ 0.95815853, -0.28623806]), 0.7921595320783135), 
    # (array([0.9931697 , 0.11667881]), 0.40443514466407576), 
    # (array([0.8657303 , 0.50051079]), 0.0), 
    # (array([0.59668531, 0.80247532]), 0.40443514466407593),
    # (array([0.23004182, 0.97318074]), 0.7921595320783138), 
    # (array([-0.1742291 ,  0.98470514]), 1.147152872702092), 
    # (array([0.8657303 , 0.50051079]), 0)]
    pos4 = np.array([-0.20259635,  1.0834968 ])    
    dir41 = np.array([0.7664235, -0.6423356])
    dir43 = np.array([0.8657303 , 0.50051079])
    
    # Drone: 5 DRONE PROPERTIES
    #                 postion: [-0.20601133  0.63403768]

    #                 speed: 1.3333333333333333                
    #                 radio: 0.5                
    #                 direction: [-0.30901699  0.95105652]                
    #                 goal: [-3.09016994  9.51056516]                
    #                 max_amp: 1.2217304763960306                
                
    # [(array([0.78801075, 0.61566148]), 1.1471528727020919), 
    # (array([0.47971311, 0.8774254 ]), 0.7921595320783134), 
    # (array([0.09294986, 0.99567079]), 0.4044351446640756), 
    # (array([-0.30901699,  0.95105652]), 1.5700924586837752e-16), 
    # (array([-0.66043862,  0.75088003]), 0.4044351446640758), 
    # (array([-0.90383377,  0.42788376]), 0.7921595320783138), 
    # (array([-0.99939083,  0.0348995 ]), 1.147152872702092), 
    # (array([-0.30901699,  0.95105652]), 0)]

    pos5 = np.array([-0.20601133,  0.63403768 ])    
    dir51 = np.array([0.78801075, 0.61566148])
    dir53 = np.array([-0.30901699,  0.95105652])

    speed = 1.3333333333333333                
    
    draw_circle2([pos1,pos2,pos3,pos4,pos5], [dir13,dir23,dir33,dir43,dir53], 10, ['r','y','b','g','m'])
    
    plt.show()
