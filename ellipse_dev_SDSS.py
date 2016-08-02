"""
Finds the objects in SDSS with a 90% chance or higher of being a DEV galaxy and creates a histogram for these objects' ellipticities. 
Also looks at error in b/a ellipticity and takes out any extremely large uncertainties, as those are probably not consistent values.
"""

import sys
image1 = str(sys.argv[1]) # SDSS csv file

"""
Importing the SDSS csv file into a readable python array
"""
import csv
import itertools
import pandas
df = pandas.read_csv(image1, sep = ',', header=None)

deVAB_r = df.values[:,0]
deVAB_z = df.values[:,1]
lnDeV_r = df.values[:,2]
lnDeV_z = df.values[:,3]
deVABErr_r = df.values[:,4]
deVABErr_z = df.values[:,5]

import numpy as np

dAB_r = np.array([float(x) for x in deVAB_r if x != 'deVAB_r'])
dAB_z = np.array([float(x) for x in deVAB_z if x != 'deVAB_z'])

ln_DeV_r = np.array([float(x) for x in lnDeV_r if x != 'lnLDeV_r'])
ln_DeV_z = np.array([float(x) for x in lnDeV_z if x != 'lnLDeV_z'])

dABErr_r = np.array([float(x) for x in deVABErr_r if x != 'deVABErr_r'])
dABErr_z = np.array([float(x) for x in deVABErr_z if x != 'deVABErr_z'])

from operator import truediv
def ellipticity(x):
    e = truediv((1-x),(1+x))
    return e

from math import exp

DeVLike_r = [exp(x) for x in ln_DeV_r]
DeVLike_z = [exp(x) for x in ln_DeV_z]


deV_r = [x for (x, y, z) in zip(dAB_r, DeVLike_r, dABErr_r) if y > 0.9 and (z < 22 and z > 0)]
deV_z = [x for (x, y, z) in zip(dAB_z, DeVLike_z, dABErr_z) if y > 0.9 and (z < 22 and z > 0)]


dev_r = np.array([ellipticity(x) for x in deV_r])
dev_z = np.array([ellipticity(x) for x in deV_z])


import matplotlib.pyplot as plt

plt.hist(dev_r, bins=100, label='SDSS r', color='b', alpha=0.5,)
plt.hist(dev_z, bins=100, label='SDSS z', color='r',alpha=0.4,histtype='stepfilled')
plt.legend()
plt.xlabel('Ellipticity')
plt.title('SDSS Ellipticity (DEV)')
plt.show()
