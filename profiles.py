import sys
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import dweibull
from matplotlib import rc

plt.style.use('seaborn-whitegrid')


matplotlib.rcParams.update({'font.size': 14})
#matplotlib.rcParams.update({'text.latex.unicode': True})
#rc('font',**{'family':'sans-serif','sans-serif':['Source Sans Pro']})

matplotlib.rcParams['font.family'] = 'sans-serif'

fig = plt.figure()
ax = plt.axes()
filenames = sys.argv

zcs = []
values = []
maxPad = []
minZ = sys.float_info.max
maxZ = -sys.float_info.max;
# 0 is the script name
for i in range(1, len(filenames) - 1):
    #read value
    zc, value = np.loadtxt(filenames[i], dtype='float, float', delimiter='\t', usecols=(4, 5), unpack=True, skiprows=11)
    zcs.append(zc)
    values.append(value)
    maxPad.append(max(value))
    tmpMinZ = min(zc) 
    tmpMaxZ = max(zc)
    if tmpMinZ < minZ:
        minZ = tmpMinZ

    if tmpMaxZ > maxZ:
        maxZ = tmpMaxZ

maxOfMax = max(maxPad)
for i in range(0, len(values)) :
    ratio = maxOfMax / maxPad[i]
    #for j in range(0, len(values[i])) :
    #    values[i][j] = values[i][j] * ratio
    leg=os.path.splitext(os.path.basename(filenames[i + 1]))[0]

    ax.plot(values[i], zcs[i], label= leg.replace("-"," "))
    #weibull

#filename2 = sys.argv[2]
#filename3 = sys.argv[2]

title = filenames[len(filenames) - 1]
xlabel = "PAD"
ylabel = "z (m)"
ax.legend()
ax.set_ylim(minZ, maxZ)
minor_ticks = np.arange(int(minZ), maxZ)
ax.set_yticks(minor_ticks, minor=True)
ax.grid(which='both')
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)


#print "its me"


plt.title(title)
plt.xlabel(xlabel)
plt.ylabel(ylabel);

fig.set_size_inches(6, 9)
base = os.path.splitext(filenames[1])[0]
outfile = base + ".pdf"
fig.savefig(outfile)
#plt.show()
