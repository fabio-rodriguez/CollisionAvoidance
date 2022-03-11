import json
import numpy as np

def get_measures(dict_list):
    
    data={}
    cont = 0
    for d in dict_list:
        if d == None:
            continue 

    # {
    # 0: {'longitude': 15.556349186104026, 'deviation': -1.9539925233402755e-14, 'number_of_turns': 0}, 
    # 1: {'longitude': 38.98189456705836, 'deviation': 0.0717416503709245, 'number_of_turns': 21}, 
    # 2: {'longitude': 46.81879964287882, 'deviation': 3.197442310920451e-13, 'number_of_turns': 0}, 
    # 3: {'longitude': 23.853720883753113, 'deviation': -1.4210854715202004e-14, 'number_of_turns': 0}, 
    # 4: {'longitude': 34.53983207834112, 'deviation': 3.552713678800501e-14, 'number_of_turns': 0}, 
    # 'total_time': 2205.1073389053345, 
    # 'max_turn_angle': 1.5707963267948966, 
    # 'max_total_turn': 0.2617993877991494}

        for k, v in d.items():
            if type(v) != type({}): 
                try:
                    data[k].append(float(v))
                except:
                    data[k] = [float(v)]
            else:
                for k1, v1 in v.items():
                    try:
                        data[k1].append(float(v1))
                    except:
                        data[k1] = [float(v1)]

        cont+=1
    

    measures = {}
    for k, v in data.items():
        mean = sum(v)/len(v)
        measures[k] = {"mean": mean, "std": np.std(v)}
    
    print(measures)
    print(cont/len(dict_list))





#{"0": {"longitude": 100.20973869270162, "deviation": 0.20973869270162027, "number_of_turns": 125, "m1": 100.20973869270162, "m2": 0, "m3": 125, "m4": 1.0754063536830376}, 
# "1": {"longitude": 100.11595039024886, "deviation": 0.11595039024884102, "number_of_turns": 71, "m1": 100.11595039024886, "m2": 0, "m3": 71, "m4": 1.5859728968860989},
# "2": {"longitude": 100.17222271073204, "deviation": 0.17222271073204354, "number_of_turns": 103, "m1": 100.17222271073204, "m2": 0, "m3": 103, "m4": 1.0700913061050932},
# "3": {"longitude": 100.13982254961206, "deviation": 0.13982254961206309, "number_of_turns": 83, "m1": 100.13982254961206, "m2": 0, "m3": 83, "m4": 0.5419030548054129}, 
# "4": {"longitude": 100.28307093799614, "deviation": 0.28307093799615757, "number_of_turns": 168, "m1": 100.28307093799614, "m2": 0, "m3": 168, "m4": 1.0866531018884633}, 
# "5": {"longitude": 100.06138658162382, "deviation": 0.0613865816238075, "number_of_turns": 37, "m1": 100.06138658162382, "m2": 0, "m3": 37, "m4": 0.5318004823246911}, 
# "total_time": 25381.321722745895, "max_turn_angle": 0.7853981633974483, "max_total_turn": 1.308996938995747}
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

    dresult = {}
    for key in d_mean[0].keys():
        dresult[key] = []
        for d in d_mean:
            dresult[key].append(d[key])

    for key in dresult:
        print(f"{key}: mean {sum(dresult[key])/len(dresult[key])}, std {np.std(dresult[key])}")

    return d




if __name__ == "__main__":

    # with open("random_results.txt", "r") as f:
    #     s = f.read()
    #     r = [eval(d) for d in s.split("\n")[:-1]]

    # measures = get_measures(r)  

    path = "experiments4.json"
    get_simple_measures(path)