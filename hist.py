#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys
filename = sys.argv[1]
intensities = np.loadtxt(filename, dtype='float', delimiter=' ', usecols=(0), unpack=True, skiprows=0)

# the histogram of the data
n, bins, patches = plt.hist(intensities, 100, facecolor='grey', alpha=0.75)

# add a 'best fit' line
#y = mlab.normpdf( bins, mu, sigma)
#l = plt.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('Intensity')
plt.ylabel('Frequency')
#plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
plt.grid(True)

plt.show()
