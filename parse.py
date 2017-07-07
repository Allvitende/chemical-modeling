import numpy as np
from periodictable import elements
from scipy.spatial import distance

filename = 'train.sdf'
startstr = "  -OEChem"

# def get_dist(l, xyz, numxyz):
#     distlist = []
#     for i in range(numxyz):
#         # Distance between an atom and itself is zero
#         if i == l:
#             distlist.extend([0])
#         else:
#             # Calculate distance between atoms and all the other vectors in the xyz matrix (need to optimize this)
#             distlist.append(distance.euclidean(xyz[l], xyz[i]))
#     return distlist

# Read entire file and parse into list of strings
with open(filename, 'r') as f:
    data = f.readlines()
print( '{:d} {:s}'.format(len(data), ' lines read' ) )

# Search for the beginning of each block of Atoms in file and get the index
for idx, line in enumerate(data) :
    if startstr in line :
        # DEBUGGING CODE
        #print(data[idx - 1])

        # Store line 4 from each block into a list
        temp = data[idx + 2].split()
        # Store atom count
        atmcount = temp[0]
        if int(atmcount) > 28:
            print("Skipping this molecule")
            continue
        n = len(atmcount)
        # Scenario if atom count is greater than 999
        if n > 3 :
            numxyz = int(atmcount[0:n/2])
            numc = int(atmcount[n/2:n])
        else :
            numxyz = int(temp[0])
            numc = int(temp[1])
        print('{:s}{:4d}{:s}{:4d}'.format('number of atoms =', numxyz, ' number of connections =', numc))

        xyz = [[0.0 for i in range(3)] for j in range (numxyz)]
        connect = [[0 for i in range(3)] for j in range(numc)]
        atmnum = np.zeros(shape=(28,1))
        connection_table = np.zeros(shape=(28,28))
        distance_table = np.zeros(shape=(28,29))
        # mergedlist = []

        for i in range(numxyz) :
            temp = data[idx + 3 + i].split()
            # Loop through periodic table to find element number for each symbol and store it
            for el in elements :
                if temp[3] == el.symbol :
                    atmnum[i] = float(el.number)
            for j in range(3) :
                xyz[i][j] = float(temp[j])

        # TEST CODE
        # for i in range(numxyz): print('{:d} {:s} {:12.5f} {:s} {:12.5f} {:s} {:12.5f}' .format( atmnum[i], ', ', xyz[i][0], ', ', xyz[i][1], ', ',xyz[i][2]) )
        # for i in range(numxyz):
        #     mergedlist.append([atmnum[i], xyz[i][0], xyz[i][1], xyz[i][2]])
        # print(mergedlist[0])

        for a in range(numxyz):
            distance_table[a][0] = float(atmnum[a])
        # print(distance_table)
        # print(len(distance_table[a]))
        for l in range(numxyz):
            for i in range(numxyz):
                distance_table[l][i + 1] = distance.euclidean(xyz[l], xyz[i])
        # # TEST CODE
        print(distance_table.flatten()) # Prep for TF Model
        print(len(distance_table.flatten())) # Should print 784

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
        # TEST CODE
        # for i in range(numc): print('{:5d} {:s} {:5d} {:s} {:5d}' .format( connect[i][0], ', ', connect[i][1], ', ',connect[i][2]) )

        # Record connection information in the connection table of all Atoms in molecule
        for i in range(numc):
            connection_table[connect[i][0] - 1][connect[i][1] - 1] = 1.0
            connection_table[connect[i][1] - 1][connect[i][0] - 1] = 1.0

        atmnum.shape = (28, 1)
        connection_table_final = np.hstack((atmnum, connection_table))
        # TEST CODE
        print(connection_table_final.flatten())
        #for i in range(28): print('{:s}' .format(connection_table[i]))
        # TEST CODE
