import sys
image1 = str(sys.argv[1]) # SDSS csv file

"""
Importing the SDSS csv file into a readable python array
"""
import csv
import itertools
import pandas
df = pandas.read_csv(image1, sep = ',', header=None)

RA = df.values[:,0] #ra
dec = df.values[:,1] #dec
g = df.values[:,2] #g-Magnitude
r = df.values[:,3] #r-Magnitude
z = df.values[:,4] #z-Magnitude
#de Vaucouleurs radius based on filter
rD_g = df.values[:,5]
rD_r = df.values[:,6]
rD_z = df.values[:,7]
#Exponential radius based on filter
rE_g = df.values[:,8]
rE_r = df.values[:,9]
rE_z = df.values[:,10]
#Ellipticity based on filter
deVAB_g = df.values[:,11]
deVAB_r = df.values[:,12]
deVAB_z = df.values[:,13]

expAB_g = df.values[:,14]
expAB_r = df.values[:,15]
expAB_z = df.values[:,16] 


#Strings to floats
ra2 = [float(x) for x in RA if x != 'ra']
dec2 = [float(x) for x in dec if x != 'dec']

g_mag = [float(x) for x in g if x != 'g']
r_mag = [float(x) for x in r if x != 'r']
z_mag = [float(x) for x in z if x != 'z']

rD_g1 = [float(x) for x in rD_g if x != 'deVRad_g']
rD_r1 = [float(x) for x in rD_r if x != 'deVRad_r']
rD_z1 = [float(x) for x in rD_z if x != 'deVRad_z']

rE_g1 = [float(x) for x in rE_g if x != 'expRad_g']
rE_r1 = [float(x) for x in rE_r if x != 'expRad_r']
rE_z1 = [float(x) for x in rE_z if x != 'expRad_z']

dAB_g = [float(x) for x in deVAB_g if x != 'deVAB_g']
dAB_r = [float(x) for x in deVAB_r if x != 'deVAB_r']
dAB_z = [float(x) for x in deVAB_z if x != 'deVAB_z']

eAB_g = [float(x) for x in expAB_g if x != 'expAB_g']
eAB_r = [float(x) for x in expAB_r if x != 'expAB_r']
eAB_z = [float(x) for x in expAB_z if x != 'expAB_z']

# Getting ellipticity value from b/a
from operator import truediv
def ellipticity(x):
    e = truediv((1-x),(1+x))
    return e

dev_e_g = [ellipticity(x) for x in dAB_g if x !=0]
dev_e_r = [ellipticity(x) for x in dAB_r if x !=0]
dev_e_z = [ellipticity(x) for x in dAB_z if x !=0]

exp_e_g = [ellipticity(x) for x in eAB_g if x !=0]
exp_e_r = [ellipticity(x) for x in eAB_r if x !=0]
exp_e_z = [ellipticity(x) for x in eAB_z if x !=0]

i = 0
while i < len(dev_e_r):
    a = dev_e_r[i]
    b = ra2[i]
    c = dec2[i]
    if a > 0.75:
        print(b, c, a)
    i += 1


j = 0
while j < len(dev_e_r):
    x = exp_e_r[j]
    y = ra2[j]
    w = dec2[j]
    if a > 0.75:
        print(y, x, w)
    j += 1
