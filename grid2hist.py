import sys
import os
import math
import numpy as np
from utils import readLvoxGridHeaderTuple

gridfile = sys.argv[1]
nx, ny, nz, xmin, ymin, zmin, xsize, ysize, zsize, noda, dt = readLvoxGridHeaderTuple(gridfile)

histfile = gridfile.replace('.GRD3DLVOX', '.hist')
if len(sys.argv) > 2:
    histfile = sys.argv[2]

infile = open(gridfile, 'r')
outhistfile = open(histfile, 'w+')

for i in range(0, 11):
    line=infile.readline()
ix = 0
iy = 0
iz = 0
count = 0
padSumByZ = np.zeros(nz)
nbVoxs = np.zeros(nz)
PADs = np.zeros((nx,ny,nz))

while True:
    line = infile.readline()
    if not line : break  # EOF
    
    #empty line, finish a layer
    if line.strip():
        #sum value
        ix = 0
        ns = [float(x) for x in line.split()] 
        for ind in range(0, len(ns)):
            pad = ns[ind]
            #if ix < nbx and iy > oldNby - nby - 1 and iz < nbz:
            PADs[ix,iy,iz] = pad
            ix +=1
        iy += 1
    else:
        iz += 1
        iy = 0


for i in range(0,11):
    outhistfile.write("Dummy text for compatiblity with computree \n")

coeff = 1
for z in range(0, nz): 
    nbVoxNoOccZ = 0
    nbVox = 0
    sumPadZ = 0.0
    for y in range(0, ny):
        for x in range(0, nx):
            p = PADs[x,y,z]
            if p > -7.9999:
                nbVox += 1
            if p > -0.0001:
                nbVoxNoOccZ += 1
            padStr = str(p)
            if p >= 0:
                sumPadZ += p
        
    #print(z, nbInter, sumInter, nbVoxs[z], nbvoxOfPlot)
    coordZ = zmin + z*zsize + zsize/2
    print(nbVoxNoOccZ, nbVox)
    outhistfile.write("%d\t%d\t%f\t%f\t%f\t%f\n"% (z, z, z, z, coordZ, sumPadZ/nbVoxNoOccZ))

infile.close()
outhistfile.close()
