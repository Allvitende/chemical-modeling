filename = 'train.sdf'
print('{:s}'.format('Reading sdf data', filename))

with open(filename, 'r') as f:
    data = f.readlines()

print( '{:d} {:s}'.format(len(data), ' lines read' ) )
for i in range(4) :
    print('{:s}'.format(data[i]))

temp = data[3].split()
astr = temp[0]
n= len(astr)
if n > 3:
    numxyz= int(astr[0:n/2])
    numc=   int(astr[n/2:n])
else:
    numxyz= int(temp[0])
    numc=   int(temp[1])
print('{:s}{:4d}{:s}{:4d}'.format('number of atoms =', numxyz, ' number of connections =', numc))

xyz=    [[0.0 for i in range(3)] for j in range (numxyz)]
atm=    ['z' for i in range(numxyz)]
connect=    [[0 for i in range(3)] for j in range(numc)]

for i in range(numxyz):
    temp = data[i + 4].split()
    atm[i] = temp[3]
    for j in range(3):
        xyz[i][j]=  float(temp[j])

for i in range(numc):
    temp = data[i + numxyz + 4].split()
    if len(temp) == 2 :
        astr=temp[0]
        n=len(astr)
        connect[i][0]=  int(astr[0:n/2])
        connect[i][1]=  int(astr[n/2:n])
        connect[i][2]=  int(temp[1])
    else:
        connect[i][0]=  int(temp[0])
        connect[i][1]=  int(temp[1])
        connect[i][2]=  int(temp[2])

print('{:s}'.format('finished'))


for i in range(numxyz): print('{:12.5f} {:s} {:12.5f} {:s} {:12.5f}' .format( xyz[i][0], ', ', xyz[i][1], ', ',xyz[i][2]) )
for i in range(numc): print('{:5d} {:s} {:5d} {:s} {:5d}' .format( connect[i][0], ', ', connect[i][1], ', ',connect[i][2]) )

