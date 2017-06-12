from periodictable import elements
from scipy.spatial import distance

global filename = 'train.sdf'
global startstr = "  -OEChem"

def get_dist(l, xyz, numxyz):
    distlist = []
    for i in range(numxyz):
        # Distance between an atom and itself is zero
        if i == l:
            distlist.extend([0])
        else:
            # Calculate distance between atoms and all the other vectors in the xyz matrix (need to optimize this)
            distlist.extend([distance.euclidean(xyz[l], xyz[i])])
    return distlist

# Read entire file and parse into list of strings
with open(filename, 'r') as f:
    data = f.readlines()
print( '{:d} {:s}'.format(len(data), ' lines read' ) )

# Search for the beginning of each block of Atoms in file and get the index
for idx, line in enumerate(data) :
    if startstr in line :
        # Store line 4 from each block into a list
        temp = data[idx + 2].split()
        # Store atom count
        atmcount = temp[0]
        n = len(atmcount)
        # Scenario if atom count is greater than 999
        if n > 3 :
            numxyz = int(atmcount[0:n/2])
            numc = int(atmcount[n/2:n])
        else :
            numxyz = int(temp[0])
            numc = int(temp[1])
        # print('{:s}{:4d}{:s}{:4d}'.format('number of atoms =', numxyz, ' number of connections =', numc))

        xyz = [[0.0 for i in range(3)] for j in range (numxyz)]
        connect = [[0 for i in range(3)] for j in range(numc)]
        atmnum = [0 for i in range(numxyz)]
        # mergedlist = []
        dists = []
        for i in range(numxyz) :
            temp = data[idx + 3 + i].split()
            # Loop through periodic table to find element number for each symbol and store it
            for el in elements :
                if temp[3] == el.symbol :
                    atmnum[i] = el.number
            for j in range(3) :
                xyz[i][j] = float(temp[j])

        # for i in range(numxyz): print('{:d} {:s} {:12.5f} {:s} {:12.5f} {:s} {:12.5f}' .format( atmnum[i], ', ', xyz[i][0], ', ', xyz[i][1], ', ',xyz[i][2]) )
        # for i in range(numxyz):
        #     mergedlist.append([atmnum[i], xyz[i][0], xyz[i][1], xyz[i][2]])
        # print(mergedlist[0])

        # Build the distance matrix for each atom in the molecule
        for l in range(numxyz):
            dists.append(get_dist(l, xyz, numxyz))
        # print(dists)
        # break

        # for i in range(numc) :
        #     temp = data[idx + 3 + i + numxyz].split()
        #     if len(temp) == 2 :
        #         atmcount = temp[0]
        #         n = len(atmcount)
        #         connect[i][0] = int(atmcount[0:n/2])
        #         connect[i][1] = int(atmcount[n/2:n])
        #         connect[i][2] = int(temp[1])
        #     else :
        #         connect[i][0] = int(temp[0])
        #         connect[i][1] = int(temp[1])
        #         connect[i][2] = int(temp[2])
        # for i in range(numc): print('{:5d} {:s} {:5d} {:s} {:5d}' .format( connect[i][0], ', ', connect[i][1], ', ',connect[i][2]) )
