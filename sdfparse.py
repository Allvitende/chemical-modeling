import time
import numpy as np
from periodictable import elements
from scipy.spatial import distance

filename = 'train.sdf'
startstr = "  -OEChem"
start_time = time.time()

with open(filename, 'r') as f:
    data = f.readlines()

def get_batch():
    train_data_dists = []
    train_data_connects = []
    for idx, line in enumerate(data) :
        if startstr in line :
            temp = data[idx + 2].split()
            atmcount = temp[0]
            if int(atmcount) > 28:
                continue
            n = len(atmcount)

            # Scenario if atom count is greater than 999
            if n > 3 :
                numxyz = int(atmcount[0:n/2])
                numc = int(atmcount[n/2:n])
            else :
                numxyz = int(temp[0])
                numc = int(temp[1])

            xyz = [[0.0 for i in range(3)] for j in range (numxyz)]
            connect = [[0 for i in range(3)] for j in range(numc)]
            atmnum = np.zeros(shape=(28,1))
            connection_table = np.zeros(shape=(28,28))
            distance_table = np.zeros(shape=(28,29))

            for i in range(numxyz) :
                temp = data[idx + 3 + i].split()
                for el in elements :
                    if temp[3] == el.symbol :
                        atmnum[i] = float(el.number)
                for j in range(3) :
                    xyz[i][j] = float(temp[j])

            for a in range(numxyz):
                distance_table[a][0] = float(atmnum[a])
            
            for l in range(numxyz):
                for i in range(numxyz):
                    if i > 0: 
                        if i - l == 1:
                            continue
                    if ((distance_table[l][i + 1] > 0.0) or (distance_table[i][l + 1] > 0.0)):
                        continue
                    else:
                        ed = distance.euclidean(xyz[l], xyz[i])
                        distance_table[l][i + 1] = ed
                        distance_table[i][l + 1] = ed
            train_data_dists.append([distance_table.flatten()])

            for i in range(numc) :
                temp = data[idx + 3 + i + numxyz].split()
                if len(temp) == 2 :
                    atmcount = temp[0]
                    n = len(atmcount)
                    connect[i][0] = int(atmcount[0:n/2])
                    connect[i][1] = int(atmcount[n/2:n])
                    connect[i][2] = int(temp[1])
                else :
                    connect[i][0] = int(temp[0])
                    connect[i][1] = int(temp[1])
                    connect[i][2] = int(temp[2])

            # Record connection information in the connection table of all Atoms in molecule
            for i in range(numc):
                connection_table[connect[i][0] - 1][connect[i][1] - 1] = 1.0
                connection_table[connect[i][1] - 1][connect[i][0] - 1] = 1.0
            train_data_connects.append([connection_table.flatten()])

    return train_data_dists, train_data_connects
print("--- %s seconds ---" % (time.time() - start_time))

