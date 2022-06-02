import json
import numpy as np
import math
import matplotlib.pyplot as plt


def get_measures(dict_list):
    
    
    data={}
    cont = 0

    totalrates =[]
    maxangle = 0
    allturns = []
    for d in dict_list:
        if d == None:
            continue 

        for k, v in d.items():
            if k=="waypoints":
                continue

            if type(v) != type({}): 
                try:
                    data[k].append(float(v))
                except:
                    data[k] = [float(v)]
            else:
                for k1, v1 in v.items():
                    if k1 == "turns":
                        l = v[k1]
                        allturns += l
                        maxangle = maxangle if not l else max(max(l), maxangle)
                        turns = [v for v in l if v>math.radians(10)]
                        totalrates.append(sum(turns)/len(turns) if turns else 0)
                        continue

                    try:
                        data[k1].append(float(v1))
                    except:
                        data[k1] = [float(v1)]

        cont+=1

    show_turn_ranges(allturns)

    print("turns rate:", sum(totalrates)/len(totalrates), np.std(totalrates))
    print("max angle:", maxangle)

    measures = {}
    for k, v in data.items():
        mean = sum(v)/len(v)
        measures[k] = {"mean": mean, "std": np.std(v)}


    print(measures)
    print(cont/len(dict_list))



def get_simple_measures(path):
    with open(path, "r") as f:
        d = json.loads(f.read())

    d_mean = []
    for key in d.keys():
        
        try:
            _ = int(key)
            d_mean.append(d[key])
        except:
            if key=="waypoints":
                print(len(d["waypoints"]["0"]["X"]))
                print(len(d["waypoints"]["1"]["X"]))
                print(len(d["waypoints"]["2"]["X"]))
                print(len(d["waypoints"]["3"]["X"]))
                print(len(d["waypoints"]["4"]["X"]))
            # print(f"{key}: {d[key]}")

    maxangle = 0
    dresult = {}
    allturns = []
    for key in d_mean[0].keys():
        dresult[key] = []
        print(key)
        for d in d_mean:
            if key == "turns":
                allturns += d[key]
                maxangle = maxangle if not d[key] else max(max(d[key]), maxangle)
                turns = [v for v in d[key] if v>math.radians(10)]
                dresult[key].append(0 if not turns else sum(turns)/len(turns))
            else:
                dresult[key].append(d[key])

    show_turn_ranges(allturns)
    print("maxangle:", maxangle)

    for key in dresult:
        try:
            if key == "turns":
                print(f"turns rate: mean {sum(dresult[key])/len(dresult[key])}, std {np.std(dresult[key])}")
                # print(f"max angle: {max(turns)}")
            else:
                print(f"{key}: mean {sum(dresult[key])/len(dresult[key])}, std {np.std(dresult[key])}")
        except:
            print("Error:", key)
            print(dresult[key])
            print()

    return d


def show_turn_ranges(turns):
    ranges = [0,5,10,20,30,60,90,360]
    names = []
    values = []
    for i in range(len(ranges)-1):
        minval = math.radians(ranges[i])
        maxval = math.radians(ranges[i+1])
        names.append(f"[{ranges[i]}, {ranges[i+1]}]")
        values.append(0)
        for t in turns:
            if minval <= t < maxval:
                values[-1]+=1

    plt.bar(names, values) 
    plt.xlabel("Intervalos de Angulos (Grados)")
    plt.ylabel("Cantidad de Angulos")
    plt.show()


    print("plot values")
    print(names)
    print(values)


if __name__ == "__main__":

    # with open("random_results.txt", "r") as f:
    #     s = f.read()
    #     r = [eval(d) for d in s.split("\n")[:-1]]

    # measures = get_measures(r)  

    path = "experiments4.json"
    get_simple_measures(path)
