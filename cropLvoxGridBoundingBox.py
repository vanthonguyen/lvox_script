import sys
import os
import math
import numpy as np
from utils import readLvoxGridHeaderTuple


def isInside(xindex, yindex, zindex):
    global minXInd
    global minYInd
    global minZInd
    global maxXInd
    global maxYInd
    global maxZInd
    global ny

    yInvertInd = ny - yindex - 1
    if (xindex >= minXInd and xindex <= maxXInd and
        yInvertInd >= minYInd and yInvertInd <= maxYInd and
        zindex >= minZInd and zindex <= maxZInd):
        return True
    return False

gridfile = sys.argv[1]
minX = float(sys.argv[2])
maxX = float(sys.argv[3])
minY = float(sys.argv[4])
maxY = float(sys.argv[5])
minZ = float(sys.argv[6])
maxZ = float(sys.argv[7])
outgrid = sys.argv[8]

nx, ny, nz, xmin, ymin, zmin, xsize, ysize, zsize, noda, dt = readLvoxGridHeaderTuple(gridfile)

infile = open(gridfile, 'r')
outfile = open(outgrid, 'w+')

xmax = xmin + xsize*nx 
ymax = ymin + ysize*ny 
zmax = zmin + zsize*nz 

minX = max(minX, xmin)
minY = max(minY, ymin)
minZ = max(minZ, zmin)

maxX = min(maxX, xmax)
maxY = min(maxY, ymax)
maxZ = min(maxZ, zmax)
print (minX, maxX, minY, maxY, minZ, maxZ)

nbcols = (maxX - minX)//xsize
nbrows = (maxY - minY)//ysize
nblv = (maxZ - minZ)//zsize

minXInd = max(0, (minX - xmin)//xsize - 1)
minYInd = max(0, (minY - ymin)//ysize - 1)
minZInd = max(0, (minZ - zmin)//zsize - 1)

maxXInd = minXInd + nbcols - 1
maxYInd = minYInd + nbrows - 1
maxZInd = minZInd + nblv - 1 

outfile.write("ncols\t%d\n" % nbcols)
outfile.write("nrows\t%d\n" % nbrows)
outfile.write("nzlev\t%d\n" % nblv)
outfile.write("xllcorner\t%f\n" % (xmin + minXInd*xsize))
outfile.write("yllcorner\t%f\n" % (ymin + minYInd*ysize))
outfile.write("zllcorner\t%f\n" % (zmin + minZInd*zsize))

#oldNby = nby

for i in range(0, 11):
    line=infile.readline()
    if i > 5:
        outfile.write(line)
    elif i == 1:
        oldNby = int(line.split()[1])


ix = 0
iy = 0
iz = 0
croppedPAD = 0
oriPAD = 0
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
            if pad > 0:
                oriPAD += pad
            if isInside(ix,iy,iz):

                padStr = str(pad)
                if pad.is_integer() :
                    padStr = str(int(pad))
                outfile.write(padStr)
                if pad > 0:
                    croppedPAD +=pad
                if ix - minXInd < nbcols - 1:
                    outfile.write("\t")
                    #print ("write %d %d %d" % (ix, minXInd, nbcols))
                elif ix - minXInd == nbcols - 1:
                    outfile.write("\n")
            ix +=1
        iy += 1
    else:
        if iz - minZInd <= nblv:
            outfile.write(line) 
        iz += 1
        iy = 0

print ("PAD: %f %f" % (croppedPAD, oriPAD))
infile.close()
outfile.close()
