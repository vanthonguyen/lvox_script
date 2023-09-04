import sys
import os
import math
import numpy as np

gridfile = sys.argv[1]
gridfile2 = sys.argv[2]
gridfile3 = sys.argv[3]

infile = open(gridfile, 'r')
infile2 = open(gridfile2, 'r')
outfile = open(gridfile3, 'w')

for i in range(0, 11):
    outfile.write(infile.readline())
    infile2.readline()

count = 0
while True:
    line1 = infile.readline()
    line2 = infile2.readline()
    if not line1 or not line2: break  # EOF

    if not line1.strip():
        #eompty
        outfile.write(line1) 
    else:
        ns1 = [float(x) for x in line1.split()] 
        ns2 = [float(x) for x in line2.split()] 
        if len(ns1) != len(ns2):
            print ("error the number of elements in two grids is not the same!!!")
            break
        for ind in range(0, len(ns1)):
            if ns2[ind] > 0:
                sub = ns1[ind] / ns2[ind]
                outfile.write(str(sub))
            else:
                outfile.write(str(ns2[ind]))
            if ind < len(ns1) - 1:
                outfile.write("\t")
            else:
                outfile.write("\n")

print(count)
infile.close()
infile2.close()
outfile.close()
