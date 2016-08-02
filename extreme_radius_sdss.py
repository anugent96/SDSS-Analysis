"""
For objects with a 90% chance or higher of being EXP type, code wil give a new half-light radius (EXP) histogram. For r and z filters.
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

expRad_r = df.values[:,0] # exponential radius, r-filter
expRad_z = df.values[:,1] # exponential radius, z-filter
lnExp_r = df.values[:,2] # ln(likelihood EXP), r-filter
lnExp_z = df.values[:,3] # ln(likelihood EXP), z-filter

import numpy as np
# Strings to floats
eRad_r = np.array([float(x) for x in expRad_r if x != 'expRad_r'])
eRad_z = np.array([float(x) for x in expRad_z if x != 'expRad_z'])

ln_Exp_r = np.array([float(x) for x in lnExp_r if x != 'lnLExp_r'])
ln_Exp_z = np.array([float(x) for x in lnExp_z if x != 'lnLExp_z'])

from math import exp
# converting l(likelihoods) to likelihoods (probability range: 0  > 1)
ExpLike_r = [exp(x) for x in ln_Exp_r]
ExpLike_z = [exp(x) for x in ln_Exp_z]

# Probability that an object has an EXP likelihood of 90% or higher
expR_r = [x for (x, y) in zip(eRad_r, ExpLike_r) if y > 0.9]
expR_z = [x for (x, y) in zip(eRad_z, ExpLike_z) if y > 0.9]

import matplotlib.pyplot as plt
# Hsitgram for these objects
plt.hist(expR_r, bins=np.logspace(0,2,50), label='SDSS r', color='b', alpha=0.5)
plt.hist(expR_z, bins=np.logspace(0,2,50), label='SDSS z', color='r', alpha=0.4, histtype='stepfilled')
plt.yscale('log')
plt.xscale('log')
plt.title('SDSS Half-Light Radius (EXP)')
plt.xlabel('Radius (arcsec)')
plt.legend()
plt.show()
