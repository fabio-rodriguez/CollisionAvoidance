import json
import numpy as np


if __name__ == "__main__":
    
    with open("6A_CA.json", "r") as f:
        dic = json.loads(f.read())

    measures = {}
    for key in dic.keys():
        try:
            _ = int(key)
            values = dic[key]
            
            for m in values.keys():
                if not m in measures.keys():
                    measures[m] = []
        
                measures[m].append(values[m])
        except:
            pass

    for key in measures.keys():
        l = measures[key]
        # print(key, l)
        if key=="turns":
            rates =[sum(turns)/len(turns) if turns else 0 for turns in l]
            print("turns_rate:", sum(rates)/len(rates), np.std(rates))
        else:
            print(key, sum(l)/len(l), np.std(l))
        print()



