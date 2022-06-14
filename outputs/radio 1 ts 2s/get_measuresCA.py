import json
import numpy as np


def get_measures(dict_list):
    
    
    data={}
    cont = 0

    totalrates =[]
    maxangle = 0
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
                        maxangle = maxangle if not l else max(max(l), maxangle)
                        totalrates.append(sum(l)/len(l) if l else 0)
                        continue

                    try:
                        data[k1].append(float(v1))
                    except:
                        data[k1] = [float(v1)]

        cont+=1
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
            print(f"{key}: {d[key]}")

    maxangle = 0
    dresult = {}
    for key in d_mean[0].keys():
        dresult[key] = []
        for d in d_mean:
            if key == "turns":
                maxangle = maxangle if not d[key] else max(max(d[key]), maxangle)
                dresult[key].append(0 if not d[key] else sum(d[key])/len(d[key]))
            else:
                dresult[key].append(d[key])

    print("maxangle:", maxangle)

    for key in dresult:
        try:
            if key == "turns":
                turns = dresult[key]
                print(f"turns rate: mean {sum(turns)/len(turns)}, std {np.std(turns)}")
                # print(f"max angle: {max(turns)}")
            else:
                print(f"{key}: mean {sum(dresult[key])/len(dresult[key])}, std {np.std(dresult[key])}")
        except:
            print("Error:", key)
            print(dresult[key])
            print()

    return d




if __name__ == "__main__":

    with open("random_results.txt", "r") as f:
        s = f.read()
        r = [eval(d) for d in s.split("\n")[:-1]]

    measures = get_measures(r)  

    # path = "experiments4.json"
    # get_simple_measures(path)