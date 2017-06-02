filename = 'train.sdf'
startstr = "  -OEChem"
with open(filename, 'r') as f:
    data = f.readlines()                                                        # Read entire file and parse into list of strings
print( '{:d} {:s}'.format(len(data), ' lines read' ) )
for idx, line in enumerate(data) :                                              # Search for the beginning of each block of Atoms in file and get the index
    if startstr in line :
        # print idx, line
        # print(data[idx + 2])
        temp = data[idx + 2].split()                                            # Store line 4 from each block into a list
        atmcount = temp[0]                                                      # Store atom count
        n = len(atmcount)
        if n > 3 :                                                              # Scenario if atom count is greater than 999
            numxyz = int(atmcount[0:n/2])
            numc = int(atmcount[n/2:n])
        else :
            numxyz = int(temp[0])
            numc = int(temp[1])
        if numc <= 4 :                                                          # When atom count is less than 4 there are issues..need to check this
            continue
        print('{:s}{:4d}{:s}{:4d}'.format('number of atoms =', numxyz, ' number of connections =', numc))

        xyz = [[0.0 for i in range(3)] for j in range (numxyz)]
        atm = ['z' for i in range(numxyz)]
        connect = [[0 for i in range(3)] for j in range(numc)]

        for i in range(numxyz) :
            temp = data[idx + 3 + i].split()
            atm[i] = temp[3]
            for j in range(3) :
                xyz[i][j] = float(temp[j])
        for i in range(numxyz): print('{:12.5f} {:s} {:12.5f} {:s} {:12.5f}' .format( xyz[i][0], ', ', xyz[i][1], ', ',xyz[i][2]) )
        for i in range(numxyz): print('{:s}' .format( atm[i]))

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
        for i in range(numc): print('{:5d} {:s} {:5d} {:s} {:5d}' .format( connect[i][0], ', ', connect[i][1], ', ',connect[i][2]) )
