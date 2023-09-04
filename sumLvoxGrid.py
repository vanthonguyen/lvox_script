import sys
import os
import math
import numpy as np

gridfile = sys.argv[1]
gridfile2 = sys.argv[2]
outgrid = sys.argv[3]

infile = open(gridfile, 'r')
infile2 = open(gridfile2, 'r')
outfile = open(outgrid, 'w')

for i in range(0, 11):
    outfile.write(infile.readline())
    infile2.readline()

count = 0
while True:
    line1 = infile.readline()
    line2 = infile2.readline()
    if not line1 or not line2: break  # EOF

    if not line1.strip():
        outfile.write(line1) 
    else:
        ns1 = [int(x) for x in line1.split()] 
        ns2 = [int(x) for x in line2.split()] 
        if len(ns1) != len(ns2):
            print ("error the number of elements in two grids is not the same!!!")
            break
        for ind in range(0, len(ns1)):
            if ns1[ind] == -8 or ns2[ind] == -8:
                outfile.write("-8")
            else :
                outfile.write(str(ns1[ind] + ns2[ind]))
            if ind < len(ns1) - 1:
                outfile.write("\t")
            else:
                outfile.write("\n")

infile.close()
infile2.close()
outfile.close()
